import random, os, json
import traceback
N = "North"
E = "East"
S = "South"
W = "West"

from datetime import datetime
print (datetime.now())
start = datetime.now()
def timely(start, now, progress, total):
	elap = (now-start)
	
	return (total - progress)*(elap/progress)
	
print(timely(start, datetime.now(),1,2))
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

from PIL import Image, ImageDraw, ImageFont
try:
	f = ImageFont.load_default_imagefont()
except:
	f = ImageFont.load_default() #_imagefont()

def buildExpectations():
	raise Exception("Not sorted")
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

def pig(grid, tile, location, largest_match = False):
	mat=0
	for i,k in t_assoc.items():
		check = (location[0]+k[0][0],location[1]+k[0][1])
		if (check in grid):
			#print(ck)
			mat+=1
			if (grid[check][k[1]] != tile[i]):
				return False
	if (largest_match):
		return mat
	return True
	
def canPlaceAt(grid, loc = (0,0)):
	o = []
	if (loc in grid):
		return False
	for i in tt:
		if (pig(grid, i, loc)):
			o.append(i)
	return o
	
def imageTileGrid(grid, loc=(-8,-8), sz=(16,16)):
	im = Image.new("RGBA", ((20*sz[0])+1,(20*sz[1])+1), (255,255,255, 255))
	dr = ImageDraw.Draw(im)
	for i in range(sz[0]):
		for j in range(sz[1]):
			if ((loc[0]+i,loc[1]+j) in grid):
				k = tile(grid[(loc[0]+i,loc[1]+j)], 21)
				pos = (int(i* (21-1)), int(j* (21-1)))
				im.paste(k, pos)
				
	for i in wtp.getEdges(grid):
		#print(i)
		p = (len(canPlaceAt(grid, i)))
	#	for k in j:
		pd = dr.textbbox((0,0), str(p),font=f)
			#print(p)
		dr.text((((i[0]-loc[0])*20)+10-int(pd[2]/2),(i[1]-loc[1])*20+10-int(pd[3]/2)), str(p),font=f,fill=(0,0,0))

	return im
	
def showWorkings(grid, workings = {}, Trace = False):
	sc = [None, None, None, None]
	#print(grid)
	be = wtp.getEdges(grid)
	for i in be:
			#print(i)
			j = i
			if (sc[0] is None or j[0] < sc[0]):
				sc[0]= j[0]
			if (sc[2] is None or j[0] > sc[2]):
				sc[2]= j[0]
			if (sc[1] is None or j[1] < sc[1]):
				sc[1]= j[1]
			if (sc[3] is None or j[1] > sc[3]):
				sc[3]= j[1]
			#print(j)

	sz = [sc[2]-sc[0]+1, sc[3]-sc[1]+1]
	im = imageTileGrid(grid, (sc[0], sc[1]), (sz[0], sz[1]))
	return im
	im = Image.new("RGB", ((20*sz[0])+1,(20*sz[1])+1), (255,255,255))
	dr = ImageDraw.Draw(im)
	c = [(255,127,127),(255,255,127), (127, 255, 127)]
	cc = 0
	for i in workings.values():
		for j in i:
			dr.rectangle(((j[0]-sc[0])*20, (j[1]-sc[1])*20, (j[0]-sc[0]+1)*20, (j[1]-sc[1]+1)*20), fill=c[cc%len(c)])
		cc+=1
			
	for i in range(sz[0]):
		for j in range(sz[1]):
			if (ma.get(i+sc[0],j+sc[1]) is not None):
				k = tile(ma.get(i+sc[0],j+sc[1]), 21)
				pos = (int(i* (21-1)), int(j* (21-1)))
				im.paste(k, pos)
	for i,j in be.items():
		for k in j:
				pd = dr.textbbox((0,0), str(i),font=f)
				dr.text((((k[0]-sc[0])*20)+10-int(pd[2]/2),(k[1]-sc[1])*20+10-int(pd[3]/2)), str(i),font=f,fill=(0,0,0))

	if (Trace):
		v = 0
		for i in traceback.extract_stack():
			li = str(i)
			pd = dr.textbbox((0,0), str(li),font=f)
			dr.text((0,v), str(li),font=f,fill=(0,0,0))
			v+= (pd[3]-pd[1])
			#print(i)
		#exit(1)
	#im.save("wang/xWang.png")
	return im

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

from core.keyMatrix import json_dumps_tuple_keys
from core.matrixController import json_loads_tuple_keys

def doesThisWorkHere(grid, loc):
	check = True
	for i in orth(loc):
		if (i in grid and check):
			k = canPlaceAt(grid, i)
			#print(k)
			if (k is not False and len(k) == 0):
				#print("Neighbour cannot be placed")
				#rb = wtp.rollback()
				return False
	return True

def getAR(grid):
	# ive copied this code I could refactor it
	sc = [None, None, None, None]
	#print(grid)
	be = wtp.getEdges(grid)
	for i in be:
			#print(i)
			j = i
			if (sc[0] is None or j[0] < sc[0]):
				sc[0]= j[0]
			if (sc[2] is None or j[0] > sc[2]):
				sc[2]= j[0]
			if (sc[1] is None or j[1] < sc[1]):
				sc[1]= j[1]
			if (sc[3] is None or j[1] > sc[3]):
				sc[3]= j[1]
			#print(j)
	if (sc[0] is None):
		return 1
	sz = [sc[2]-sc[0]+1, sc[3]-sc[1]+1]
	#print(sz)
	if (sz[1] == 0):
		return 1
	return sz[0]/sz[1]
class wangTilePlacer():
	def __init__(self, stack_size = 0):
		self.ma = mc("wang")
		self.stack = []
		self.edges = [(0,0)]
	
		#if (os.path.exists("wang/saves/edges.dat")):
		#	self.edges = json.load(open("wang/saves/edges.dat", "r"))

		#if (os.path.exists("wang/saves/stack.dat")):
		#	self.stack = json.load(open("wang/saves/stack.dat", "r"))

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
		#print(self.edges)
		return True
		
	def unplace(self, grid, where):
		if (where in grid):
			grid.remove(where)
			return True
		return False
		
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
	
	def getEdges(self, grid):
		j = []
		for i in grid.keys():
			for k in orth(i):
				if (k not in j and k not in grid):
					j.append(k)
			if (i in j):
				j.remove(i)
		return j
			
	def step(self, grid):
		if (len(grid) == 0):
			edge = [(0,0)]
		else:
			edge = self.getEdges(grid)
		
		#print(edge)
		
		d = None
		ls = []
		for i in edge:
			#p = (len(canPlaceAt(gr, i)))
			p = (abs(i[0]) + abs(i[1]))
			if (d is None or (p >= 0 and p < d)):
				d = p
				ls = [i]
			elif (p == d):
				ls.append(i)
		
		d = None
		lls = []
		for i in ls:
			p = (len(canPlaceAt(gr, i)))
			#p = (abs(i[0]) + abs(i[1]))
			if (d is None or (p > 0 and p < d)):
				d = p
				lls = [i]
			elif (p == d):
				lls.append(i)
		#print(d, ls)
		
		r = random.choice(lls)
		#print("r:",r)
		
		d = canPlaceAt(grid, r)

		out = []
		for i in d:
			x = grid.copy()
			x[r] = i
			#print(doesThisWorkHere(grid, r))
			if (doesThisWorkHere(grid, r)):
				#print("Grid works")
				out.append(x)
			else:
				print("Grid dropped")
		
		return out

#p = [1,2,3,3,4,5]
#first = p[:3]
#print(p)
#n=1
#print(p[:n], p[n:])
#exit()

if (os.path.exists("wang/saves/grids.dat")):
	grids_init = [{}]#json.load(open("wang/saves/grids.dat", "r"))
	grids_in =[]
	#for i in grids_init:
	#	grids_in.append(json_loads_tuple_keys(i))
else:
	grids_in =[{}]
	
wtp = wangTilePlacer()
ma = wtp.ma

def splitGrids(grid, split = 10000):
	return grid[:split], grid[split:]
	
class gridManager():
	def __init__(self):
		self.grids = {}
		self.path = "wang/saves/"
		
	def load(self, grid):
		if (grid in self.grids):
			#print("Grid already loaded")
			return False
			
		if (os.path.exists(self.path + "grids-" + str(grid) + ".dat")):
			grid_loader = json.load(open(self.path+"grids-"+str(grid)+".dat", "r"))
			self.grids[grid] = []
			for i in grid_loader:
				self.grids[grid].append(json_loads_tuple_keys(i))
			return True
		else:
			print("No such file")
			return False
			
	def findAllGrids(self):
		c=0
		
		while(os.path.exists("wang/saves/grids-"+str(c)+".dat") or c in self.grids):
			c+= 1
		return c

	def saveAll(self):
		for i,j in self.grids.items():
			out = []
			for k in j:
				out.append(json_dumps_tuple_keys(k, True))
			json.dump(out, open("wang/saves/grids-"+str(i)+".dat", "w"))

	def appendMany(self, these):
		c=0
		while (len(these) > 0):
			if (c in self.grids):
				b = len(self.grids[c])
			else:
				if (self.load(c)):
					b = len(self.grids[c])
				else:
					if (c in self.grids):
						b = len(self.grids[c])
					else:
						print("Grid made")
						self.grids[c] = []
						b = 0
		
			a,these= splitGrids(these, 10000-b)
			self.grids[c] += a
			
	def listGridSizes(self):
		d = {}
		for i in range(self.findAllGrids()):
			
			self.load(i)
			d[i] = len(self.grids[i])
		return d
		
grids_out = []

gm = gridManager()
#gm.grids[0] = [{}]
print(gm.findAllGrids())
gm.load(0)
print(list(gm.listGridSizes().keys()))

if (0 not in list(gm.listGridSizes().keys())):
	print("No")
	gm.grids[0] = [{}]

#print(gm.grids)
#print(gm.listGridSizes())
tileMax = None
x=0
ct = 0
tot=100
while (ct < tot and gm.listGridSizes()[0] > 0 ):
	for i in range(gm.listGridSizes()[0]):
		ign = False
		gr = gm.grids[0].pop()
		for i in wtp.getEdges(gr):
			p = (len(canPlaceAt(gr, i)))
			if (p == 0):
				ign = True
				break
		if (ign):
			if (tileMax is None or len(gr) > tileMax):
				tileMax = len(gr) 
				print("Saved fail", tileMax)
				showWorkings(gr, {}).save("wang/saves/failed-" + str(tileMax)+".png")
			pass
		#	print("I'm ignoring this grid as it is impossible")
		else:
			#d = getAR(gr)
			#if (d> 5 or d < 0.2):
				#print("d:",d)
				#print("Grid aspect ratio too stretched")
			#else:
			gm.appendMany(wtp.step(gr))
		x+=1
	ct+=1
	if (ct%10==0):
		print(x, ct, timely(start, datetime.now(), ct, tot))
		#print(ct)

imageTileGrid(gr, (-32, -32), (64, 64)).save("wang/saves/help.png")
	
print(gm.listGridSizes())
#def saveAllGrids(grids):
#	c=0
#	if (os.path.exist)
gm.saveAll()
exit()


#p,q = splitGrids(grids_in)

#json.dump(p, open("wang/saves/grids.dat", "w"))
#json.dump(q, open("wang/saves/grids-next.dat", "w"))

print(len(final),"grids")

print("Done?")

tiles = specialTiles(1)

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

workings = 0

def down(point = None):
	global workings
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

	#showWorkings({"selected" : [t_loc]}).save("wang/workingsOut-" + str(workings) + ".png")
	#workings += 1
	
	ls = canPlaceAt(t_loc)
	print("Can place",len(ls),"tiles at",t_loc)
	random.shuffle(ls)
	rb = None
	while (len(ls) > 0):
		i = ls.pop(0)
		print("Trying",i,"at",t_loc,"with",len(ls),"others.")
		if (not pig(i, t_loc)):
			print("What's happened?")
			exit()
		wtp.place(t_loc, i, ls)
		
		check = True
		for i in orth(t_loc):
			j = i
			if (wtp.ma.get(*j) is None and check):
				if (len(canPlaceAt(j)) == 0):
					print("Neighbour cannot be placed")
					rb = wtp.rollback()
					check = False
		if (check):
			return {"ret":True, "loc":t_loc, "rb" : rb}
	return {"ret": False, "loc":t_loc, "rb": rb}

def placeTile():
	rblist = []
	op = down()
	#if op return is true, item has been placed, otherwise no
	print(op)
	if (not op["ret"]):
		if (op['rb'] is None):
			print(op)
			exit()		
		rblist.append(op['rb'])
		satisfied = False
		jorth = orth(op["loc"])
		supersatisfied = False
		while (supersatisfied is False):
			
			rblist += wtp.rollbackTo(jorth)
			print("RBList is now:", rblist)
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
		
#			print("=== list ===")
#			for i in rblist:
#				print(i)
			while (len(rblist) > 0):
				p = rblist.pop()
				if (pig(p[1], p[0])):
					wtp.place(p[0], p[1], p[2])
					success = True
				elif (len(p[2]) > 0):
					success = False
					while (len(p[2]) > 0):
						p[1] = p[2].pop(0)
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
					else:
						dp = down(p[0])
						if (not dp["ret"]):
							if (dp['rb'] is None):
								print(db)
								exit()

							rblist.append(dp['rb'])
							supersatisfied = False
							jorth = orth(p[0])
							break
							#raise Exception("F04: This is legitimate panic time")
			print("RBList is still:", rblist)
				
		return

def placeTiles(tiles, quick = True):
	for i in range(10):
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
	
# Let's do this once and for all

def canima(loc, ls):
	
	global workings, d, rb_mapping_list
	placed = False
	while (len(ls) > 0):
		# I've copied this from above
		b = ls.pop()

		if (pig(b, loc)):
			wtp.place(loc, b, ls)
			if (doesThisWorkHere(loc)):
				print("This worked")
				placed = True
				grid_changed = True
				# Let's make a picture!
				showWorkings({"selected" : [d['loc']], "rbs": rb_mapping_list, "focus": [loc]}).save("wang/workingsOut-" + str(workings) + ".png")
				workings += 1
				break
			else:
				wtp.rollback()

	return placed

if (__name__ == "__main__" and False):
	discard = placeTiles(tiles, qwik)
	
	#print(len(discard),"discarded items.")
	#ct = 0
	#while(len(discard) > 0 and ct < 5):
	#	ct+= 1
	#	discard = placeTiles(discard, False)
	#	print(len(discard),"discarded items in sequence",ct,".")
	
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
		
	for i in wtp.edges:
		p = (400+(i[0]*1)+0, 300+(i[1]*1)+0)
		px[p] = (255,0,0)
		
	im2.save("wang/reddy.png")

if (__name__ == "__main__"):

	ma.save()
	json.dump(discard, open("wang/saves/discards.dat", "w"))
	json.dump(wtp.edges, open("wang/saves/edges.dat", "w"))
	json.dump(wtp.stack, open("wang/saves/stack.dat", "w"))
	
	imageTileGrid((-15,-15),(30,30)).save("wang/xWang.png")
