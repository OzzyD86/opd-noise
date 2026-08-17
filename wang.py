import random, os, json
N = "North"
E = "East"
S = "South"
W = "West"

import core.deckGenerator
discard = []

t_assoc = {
	N:((0,-1),S), 
	S:((0,1),N), 
	W:((-1,0),E),
	E:((1,0),W)
}
ed = [(0,1),(1,0),(-1,0),(0,-1)]
cols = ["red", "yellow", "green", "blue"]
def makeDistinctTiles():
	tiles = []
	for a in cols:
		for b in cols:
			for c in cols:
				for d in cols:
					tile = {N:a,E:b,S:c,W:d}
					tiles.append(tile)
	return tiles
cols = core.deckGenerator.colours
tt = core.deckGenerator.tiles

dg = core.deckGenerator.deckGenerator()
dg.addColour("red", (255,0,0))
dg.addColour("green", (0,255,0))
dg.addColour("yellow", (255,255,0))
dg.addColour("blue", (0,0,255))
#dg.addColour("pink", (255,0,255))
#dg.addTile(N = "red", E = "red", S = "red", W = "red")
m = makeDistinctTiles()
m.pop(0)
for i in m:
	dg.addTile(**i)
	#print(i)
#tt = [
#	{N:2, E:2, S:2, W:2},
#	{N:1, E:1, S:2, W:2},
#	{N:2, E:2, S:1, W:1},
#	{N:2, E:2, S:3, W:1},
#	{N:3, E:1, S:2, W:2},
	#{N:3, E:2, S:1, W:1},
#]
#tt, cols = dg.compile()
def tileValidationChecker(tiles):
	for i in tiles:
		for k,l in t_assoc.items():
			t = 0
			for j in tiles:
				m = (i[k] == j[l[1]])
				if (m):
					t+= 1
			
			if (t == 0):
				print(i,k,t,"valid", l[1], "tiles")
				return False
	return True

if not (tileValidationChecker(tt)):
	exit()

def specialTiles(num):
	tiles = []
	for i in range(num):
		tiles.append(random.choice(tt))
	return tiles
	
from core.matrixController import matrixController
#grid = {}

ofdc = []
if (os.path.exists("wang/saves/discards.dat")):
	ofdc = json.load(open("wang/saves/discards.dat", "r"))
	print("Loaded",len(ofdc),"previously discarded tiles")
else:
	print("No discarded tiles")
	
class mc(matrixController):
	def save(self):
		for i, j in self.matrices.items():
			fl = self.getFilenameFor(i)
			print("save", fl, "here")
			dirs = ("/".join(fl.split("/")[:-1]))
			os.makedirs(dirs, exist_ok=True)
			f = open(fl, "w")
			f.write(json.dumps({
				"version" : 1,
				"data" : j.save()
			}))
			f.close()

def orth(loc=(0,0)):
	jj = []
	for qa in ed:
		jj.append((loc[0]+qa[0], loc[1]+qa[1]))
	return jj
	
class wangTilePlacer():
	def __init__(self, stack_size = 0):
		self.ma = mc("wang")
		self.stack = []
		self.edges = [(0,0)]
	
	def place(self, where, what, anc = {}):
		ty = []
		#if (where not in self.edges):
		#	return False
		if (where in self.edges):
			self.edges.remove(where)
		self.stack.append([where, what, anc])
		self.ma.set(*where, what)
		for i in orth(where):
					#pl = gat(i)
					#if ((pl is not None)):
					#	if (len(pl) == 0):
					#		print("This doesn't work")
					#		pla = False
					#		ma.set(*ch_gr, None)
			if ((self.ma.get(*i) is None) and (list(i) not in ty) and (list(i) not in self.edges)):
				ty.append(tuple(i))
		self.edges += ty
		print(self.edges)
		return True
		
	def unplace(self, where):
		self.ma.set(*where, None)
		if (where not in self.edges):
			self.edges.append(where)
		for i in orth(where):
			if (i in self.edges):
				l=0
				for k in orth(i): # not orth(where) as original!
					if (k in self.edges or self.ma.get(*k) is None):
						l+=1
				if (l == 4):
					print("Remove",i)
					self.edges.remove(i)
		return True
		
	def rollback(self):
		#print("Rollback")
		i = self.stack.pop()
		self.unplace(i[0])
		return i

	def rollbackTo(self, thesePoints = []):
		print("=== Start rollback ===")
		#print(thesePoints,"\n")
		rblist = []
		satisfied = False
		while (satisfied is False):
			rbclock = None # rollback clock to tell us where we are
			p = None
			while ((rbclock not in thesePoints)) :# or (p is None or len(p[2]) == 0)):
	#			print("This should run at least once")
				p = self.rollback()
				print(len(p[2]), p[0], thesePoints)
				rbclock = tuple(p[0])
				rblist.append(p)
			print("Complete")
			satisfied = True
			print(p[2])
			if (len(p[2]) == 0):
				print ("Not satisfied")
				satisfied = False
				print(p[0])
				thesePoints = orth(p[0])
				#print(jorth)
		return rblist
	
wtp = wangTilePlacer()
ma = wtp.ma

if (os.path.exists("wang/saves/edges.dat")):
		wtp.edges = json.load(open("wang/saves/edges.dat", "r"))

if (os.path.exists("wang/saves/stack.dat")):
		wtp.stack = json.load(open("wang/saves/stack.dat", "r"))

#print(wtp.edges)

#_, cols = dg.compile()

def makeTiles(num):
	tiles = []
	for i in range(num):
		tile = {}
		for j in tile_sides:
			tile[j] = random.choice(list(cols.keys()))
		tiles.append(tile)
	return tiles
	
def pig(tile, location, largest_match = False):
	mat=0
	for i,k in t_assoc.items():
		check = (location[0]+k[0][0],location[1]+k[0][1])
		ck = ma.get(*check)
		if (ck is not None):
			#print(ck)
			mat+=1
			if (ck[k[1]] != tile[i]):
				return False
	if (largest_match):
		return mat
	return True

def canPlaceAt(loc = (0,0)):
	o = []
	if (wtp.ma.get(*loc) is not None):
		return False
	for i in tt:
		#p = pig(i, loc)
		#print(p)
		if (pig(i, loc)):
			#print(i)
			o.append(i)
	return o

tiles = ofdc + specialTiles(1)#256*5)
print("Placing",len(tiles),"tiles.")
prb = True
qwik = False

def gat(tile = (0,0)):
	k = tt.copy() # All the tiles
	tht = ma.get(*tile)
	if (tht is not None):
		return None
	
	for i,j in t_assoc.items():
		ntl = []
		#print(i,j)
		l =(tile[0]+j[0][0], tile[1]+j[0][1])
		tst = ma.get(*l)
		#print(tht)
		if (tst is not None):
			for m in k:
				
				if (m[i] == tst[j[1]]):
					ntl.append(m)
			k = ntl.copy()
	return k

def buildExpectations():
	print("Building tile expectations...")
	op = {}
	for i in wtp.edges:
		tm = canPlaceAt(i)
		if (tm is False):
			wtp.edges.remove(i)
			pass
			#print("Is there something at",i,"?")
			#print(wtp.ma.get(*i))
		else:
			if (len(tm) in op):
				op[len(tm)].append(i)
			else:
				op[len(tm)] = [i]
			#print(len(tm), "items can be placed at", i)
	print("Done.")
	return op
	
def down(point = None):
	print("Down Command")
	if (point is None):
		
		op = buildExpectations()
	
		# Choose the item with the smallest options
		#p = list(op.keys())
		#random.shuffle(p)
		p = sorted(list(op.keys()))
	
		# Choose an option
		random.shuffle(op[p[0]])
	
		# Pick a location, any location
		t_loc = op[p[0]].pop()
	else:
		t_loc = point
		
	ls = canPlaceAt(t_loc)
	random.shuffle(ls)
	
	while (len(ls) > 0):
		i = ls.pop(0)
		print("Trying",i)
		if (not pig(i, t_loc)):
			print("What's happened?")
			exit()
		wtp.place(t_loc, i, ls)
		
		check = True
		for i in orth(t_loc):
			j = i
			if (not wtp.ma.get(*j) and check):
				if (len(canPlaceAt(j)) == 0):
					print("Neighbour cannot be placed")
					print(wtp.rollback())
					check = False
		if (check):
			return {"ret":True, "loc":t_loc}
	return {"ret": False, "loc":t_loc}


def placeTile():
	op = down()
	
	#if op return is true, item has been placed, otherwise no
	
	if (not op["ret"]):
		rblist = []
		satisfied = False
		jorth = orth(op["loc"])
		supersatisfied = False
		while (supersatisfied is False):
			
			rblist += wtp.rollbackTo(jorth)
			print("=== RIGHT ===")
			print("Tried", op["loc"])
			print("Removed these:")
			for i in rblist:
				print(i)
			#print("rbclock is",rbclock)
			print("===")
		
			#print(wtp.stack)
		
			p = rblist.pop()
			print(p)
			p[1] = p[2].pop() # It should have something, but should check
			wtp.place(p[0], p[1], p[2])
		
			while (len(rblist) > 0):
				p = rblist.pop()
				if (pig(p[1], p[0])):
					wtp.place(p[0], p[1], p[2])
					success = True
				elif (len(p[2]) > 0):
					success = False
					while (len(p[2]) > 0):
						p[1] = p[2].pop()
						if (pig(p[1], p[0])):
							wtp.place(p[0], p[1], p[2])
							success = True
							break
				else:
					success = False
					#raise Exception("F05: Now. What do I do here?")
				supersatisfied = True
				if (success is False):
					x = canPlaceAt(p[0])
					if (len(x) == 0):
						#Ooh! Shove all this in supersatisfied and call it false!
						#raise Exception("F03: Okay this isnt working")
						jorth = orth(p[0])
						print("We need to dig a little further!")
						supersatisfied = False
						break
						#raise Exception("F03: Rerun")
					else:
						dp = down(p[0])
						if (not dp["ret"]):
							supersatisfied = False
							jorth = orth(p[0])
							break
							#raise Exception("F04: This is legitimate panic time")
				
		return
	
	if (not op["ret"]):
				
				#print (rbclock not in jorth, p is None or len(p[2]) > 0)
				
				# Need to rollback another.
				p = wtp.rollback()
				print(len(p[2]))
				#rbclock = tuple(p[0])
				rblist.append(p)
				
				#print(rblist)
				tt = rblist.pop() # wild assumption 
				if (len(tt[2]) > 0):
					tt[1] = tt[2].pop(0)
					if (pig(tt[1], tt[0])):
						wtp.place(tt[0], tt[1], tt[2])
					else:
						raise Exception("F01: This needs handling!")
					
				while (len(rblist) > 0):
					tt = rblist.pop()
					print("tt:",tt[0])
					#tt[1] = tt[2].pop(0)
					if (pig(tt[1], tt[0])): # Replace if can, else ignore
						wtp.place(tt[0], tt[1], tt[2])
					else:
						# Rebuild and hope
						pla = canPlaceAt(tt[0])
						print(pla)
						oo = random.choice(pla)
						pla.remove(oo)
						wtp.place(tt[0], oo, pla)
						#raise Exception("F02: What do I do here?")

	#exit()
	
def placeTiles(tiles, quick = True):
	for i in range(1):
		placeTile()
		
	return []
	# New code here
	ti = 0
	global y
	#y = wtp.edges
	discarded = []
	#print("Run")
	while(len(tiles) > 0):
		
		# Choose which tile has lowest expectation
		ti+= 1
		print("Tile " + str(ti) + "!")
		ch_ti = tiles.pop(random.randrange(len(tiles)))
		if (len(tiles) % 100 == 0):
			print(len(tiles))
		nn=0
		ls = []
		#print("Hello?!", y)
		for k in y:
			p = pig(ch_ti, k, prb)
			if (p is not False):
				if (prb):
					if (p > nn):
						ls = [k]
						nn = p
					elif (p == nn):
						ls.append(k)
				else:
					ls.append(k)
			if (quick and len(ls) > 0):
				break
		#print(len(ls),"candidates")
		if (len(ls) > 0):
			pla = False
			while (not pla):
				ty = []
				ch_gr = random.choice(ls)
				ls.remove(ch_gr)
				wtp.place(ch_gr, ch_ti)
				pla = True
				for j in ed:
					i =(ch_gr[0]+j[0], ch_gr[1]+j[1])
					op = canPlaceAt(i)
					
					if (op is not False):
						print(i,":", len(op))
					pl = gat(i)
					if ((pl is not None)):
						if (len(pl) == 0):
							print("This doesn't work")
							pla = False
							ma.set(*ch_gr, None)
				if (pla):
					#y += ty
					print("Placed",ch_gr)
					#y.remove(ch_gr)
				# If we get here and pla is still false and ls is empty
				if (not pla and len(ls) == 0):
					print("Whoops")
					print("Couldn't place",ch_gr)
					jj=[]
					for qa in ed:
						jj.append((ch_gr[0]+qa[0], ch_gr[1]+qa[1]))
					
					#print(jj)
					for qi in reversed(wtp.stack):
						#print(qi)
						if (qi[0] in jj):
							print("Rollback to", qi[0])
							qx = None
							rbstack = []
							while(qx != qi[0]):
								rb = wtp.stack.pop()
								rbstack.append(rb)
								qx = rb[0]
								print("Rollback", rb[0], "here")
								wtp.unplace(rb[0])
							#print(qi)
							for qj in rbstack:
								print(qj)
							exit(2)
					exit(1)
				# search the stack for a neighbouring tile
				# Remove the stack to that point
				# Rehash entries where relevant
				# Drop out
		else:
			print("Discarded")
			discarded.append(ch_ti)
	return discarded
	
if (__name__ == "__main__"):
	discard = placeTiles(tiles, qwik)
	
	#print(len(discard),"discarded items.")
	#ct = 0
	#while(len(discard) > 0 and ct < 5):
	#	ct+= 1
	#	discard = placeTiles(discard, False)
	#	print(len(discard),"discarded items in sequence",ct,".")
	
from PIL import Image, ImageDraw

def tile(tData, size = 10):
	size = size-1
	polys = {
		N: [(0,0),(size,0),(size/2,size/2)],
		E: [(size,0),(size,size),(size/2,size/2)],
		S: [(size,size),(0,size),(size/2,size/2)],
		W: [(0,size),(0,0),(size/2,size/2)],
	}
	im = Image.new("RGB", (size+1,size+1))
	dr = ImageDraw.Draw(im)
	if (tData is not None):
		for i, j in tData.items():
			if (i in polys):
				dr.polygon(polys[i], fill = cols[j], outline=(0))
	else:
		dr.rectangle((0,0,size,size), fill=(128,128,128))
		pass
	return im

if (__name__ == "__main__"):
	im = Image.new("RGB", (800,600), (255,255,255))
	im2 = Image.new("RGB", (800,600), (192,128,255))
	rec = ImageDraw.Draw(im2)
	for x in range(-4,4):
		for yy in range(-3,3):
			if ((x+yy) % 2 == 0):
				fll = (192,128,255)
			else:
				fll = (128,192,255)
			rec.rectangle((400+(x*100),300+(yy*100),400+((x+1)*100)-1,300+((yy+1)*100)-1), fill=fll)
	sz = 11
	m = 4
	os.makedirs("wang/saves/ims/", exist_ok=True)

	for i,j in ma.matrices.items():
		im = Image.new("RGBA", ((sz-1)*100,(sz-1)*100), (255,255,255,0))
		for k,l in j.keys.items():
			pos = (int(k[0]* (sz-1)), int(k[1]* (sz-1)))
			im.paste(tile(l,sz), pos)

		im.save("wang/saves/ims/"+str(i[0]) +"." + str(i[1])+".png")

	l = ImageDraw.Draw(im2)
	px = im2.load()
	im = Image.new("RGB", (800,600), (255,255,255))

	for i,j in ma.matrices.items():
		print(len(j.keys),"items in",i)
#	im = Image.new("RGB", ((sz-1)*100,(sz-1)*100), (255,255,255))
		for k,l in j.keys.items():
			if (l is not None):
				p = (400+(i[0]*100)+k[0], 300+(i[1]*100)+k[1])
				c = (0,0,0)
				if (l[N] == 1):
					if (l[E] == 1):
						if (l[W] == 1):
							if (l[S] == 1):
							#print(k)
								c=(255,255,255)
			px[p] = c
		
if (__name__ == "__main__"):
	for i in wtp.edges:
		p = (400+(i[0]*1)+0, 300+(i[1]*1)+0)
		px[p] = (255,0,0)
		
	im2.save("wang/reddy.png")
	ma.save()
	json.dump(discard, open("wang/saves/discards.dat", "w"))
	json.dump(wtp.edges, open("wang/saves/edges.dat", "w"))
	json.dump(wtp.stack, open("wang/saves/stack.dat", "w"))
	
	from PIL import ImageFont
	try:
		f = ImageFont.load_default_imagefont()
	except:
		f = ImageFont.load_default() #_imagefont()

	im = Image.new("RGB", ((20*16)+1,(20*16)+1), (255,255,255))
	dr = ImageDraw.Draw(im)
	for i in range(16):
		for j in range(16):
			if (ma.get(i-8,j-10) is not None):
				k = tile(ma.get(i-8,j-10), 21)
				pos = (int(i* (21-1)), int(j* (21-1)))
				im.paste(k, pos)
	for i,j in buildExpectations().items():
		for k in j:
				pd = dr.textbbox((0,0), str(i),font=f)
				#print(p)
				dr.text((((k[0]+8)*20)+10-int(pd[2]/2),(k[1]+10)*20+10-int(pd[3]/2)), str(i),font=f,fill=(0,0,0))

	im.save("wang/xWang.png")
