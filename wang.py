import random, os, json
N = "North"
E = "East"
S = "South"
W = "West"

from core.deckGenerator import deckGenerator

discard = []
tile_sides = {N, E, S, W}
t_assoc = {
	N:((0,-1),S), 
	S:((0,1),N), 
	W:((-1,0),E),
	E:((1,0),W)
}
ed = [(0,1),(1,0),(-1,0),(0,-1)]

dg = deckGenerator()
dg.addColour("red", (255,0,0))
dg.addColour("green", (0,255,0))
dg.addColour("yellow", (255,255,0))
dg.addColour("blue", (0,0,255))
#dg.addColour("pink", (255,0,255))
dg.addTile(N = "red", E = "red", S = "red", W = "red")

tt = [
	{N:2, E:2, S:2, W:2},
	{N:1, E:1, S:2, W:2},
	{N:2, E:2, S:1, W:1},
	{N:2, E:2, S:3, W:1},
	{N:3, E:1, S:2, W:2},
	#{N:3, E:2, S:1, W:1},
]

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

class wangTilePlacer():
	def __init__(self, stack_size = 0):
		self.ma = mc("wang", 500)
		self.stack = []
		self.edges = [(0,0)]
	
	def place(self, where, what, anc = {}):
		ty = []
		#if (where not in self.edges):
		#	return False
		if (where in self.edges):
			print("Remove", where, "from edges")
			self.edges.remove(where)
			print("Edges is now", self.edges)
		self.stack.append([where, what, anc])
		self.ma.set(*where, what)
		for j in ed:
			i = tuple([where[0]+j[0], where[1]+j[1]])
					#pl = gat(i)
					#if ((pl is not None)):
					#	if (len(pl) == 0):
					#		print("This doesn't work")
					#		pla = False
					#		ma.set(*ch_gr, None)
			if ((self.ma.get(*i) is None) and (list(i) not in ty) and (list(i) not in self.edges)):
				#print(i, "is not in", ty)
				#print(i, "is not in", self.edges)
				#print("Add", i, "to edges")
				ty.append(tuple(i))
		self.edges += ty
		return True
		
	def unplace(self, where):
		self.ma.set(*where, None)
		if (where not in self.edges):
#			print("Remove", where, "from edges")

			self.edges.append(where)
		for j in ed:
			i =(where[0]+j[0], where[1]+j[1])
			if (i in self.edges):
				l=0
				for sj in ed:
					k =(where[0]+j[0]+sj[0], where[1]+j[1]+sj[1])
					if (k in self.edges or self.ma.get(*k) is None):
						l+=1
				if (l == 4):
#					print("Remove", i, "from edges")
					self.edges.remove(i)
#					print("Edges is now", self.edges)
		return True
		
	def rollback(self):
		#print("Rollback")
		i = self.stack.pop()
		self.unplace(i[0])
		return i
	
	def placeInGrid(self, tile, location, largest_match = False):
		mat=0
		for i,k in t_assoc.items():
			check = (location[0]+k[0][0],location[1]+k[0][1])
			ck = self.ma.get(*check)
			if (ck is not None):
				mat+=1
				if (ck[k[1]] != tile[i]):
					return False
		if (largest_match):
			return mat
		return True
		pass
	
wtp = wangTilePlacer()
ma = wtp.ma

if (os.path.exists("wang/saves/edges.dat")):
		wtp.edges = json.load(open("wang/saves/edges.dat", "r"))

if (os.path.exists("wang/saves/stack.dat")):
		wtp.stack = json.load(open("wang/saves/stack.dat", "r"))

#wtp.place({}, (0,0))
#wtp.unplace((0,0))

_, cols = dg.compile()

def makeTiles(num):
	tiles = []
	for i in range(num):
		tile = {}
		for j in tile_sides:
			tile[j] = random.choice(list(cols.keys()))
		tiles.append(tile)
	return tiles
	
def makeDistinctTiles(num):
	tiles = []
	for i in range(num):
		for a in cols:
			for b in cols:
				for c in cols:
					for d in cols:
						tile = {N:a,E:b,S:c,W:d}
						
						tiles.append(tile)
	return tiles
#print(tiles)

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

tiles = ofdc + makeTiles(256*5)
print("Placing",len(tiles),"tiles.")
prb = True
qwik = False

def placeTile():
	print("Building tile expectations...")
	op = {}
	for i in wtp.edges:
		tm = canPlaceAt(i)
		if (tm is False):
			print("Is there something at",i,"?")
		else:
			if (len(tm) in op):
				op[len(tm)].append(i)
			else:
				op[len(tm)] = [i]
			print(len(tm), "items can be placed at", i)
	print("Done.")
	
	# Choose the item with the smallest options
	p = sorted(list(op.keys()))
	
	# Choose an option
	t_loc = op[p[0]].pop()
	print(t_loc)
	
	# Get a tile
	pl = canPlaceAt(t_loc)
	ttp = random.choice(pl)
	#pl.removr(ttp)
	rem = pl.remove(ttp)
	# Place it
	if (not pig(ttp, t_loc)):
		print("What's happened?")
		exit()
	wtp.place(t_loc, ttp, pl)
	
	for i in ed:
		j =(t_loc[0]+i[0], t_loc[1]+i[1])
		if (not wtp.ma.get(*j)):
			if (len(canPlaceAt(j)) == 0):
				print("Neighbour cannot be placed")
				print(wtp.rollback())
				exit()
				break
	#exit()

def placeTiles(tiles, quick = True):
	placeTile()
	return []
	# New code here
	ti = 0

	discarded = []
	#print("Run")
	while(len(tiles) > 0):
		ch_ti = tiles.pop(random.randrange(len(tiles)))
		if (len(tiles) % 100 == 0):
			print(len(tiles))
		nn=0
		ls = []
		for k in y:
			p = wtp.placeInGrid(ch_ti, k, prb)
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
				
		if (len(ls) > 0):
			ch_gr = random.choice(ls)
			#print(ch_gr)
			wtp.place(ch_gr, ch_ti)
		else:
			print("Discarded")
			discarded.append(ch_ti)
	return discarded

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
		pass
	return im

if (__name__ == "__main__"):
	discard = placeTiles(tiles, qwik)
	print(len(discard),"discarded items.")
	ct = 0
	while(len(discard) > 0 and ct < 5):
		ct+= 1
		discard = placeTiles(discard, False)
		print(len(discard),"discarded items in sequence",ct,".")

	ma.save()
	json.dump(discard, open("wang/saves/discards.dat", "w"))
	json.dump(wtp.edges, open("wang/saves/edges.dat", "w"))
	json.dump(wtp.stack, open("wang/saves/stack.dat", "w"))

#	im = Image.new("RGB", (800,600), (255,255,255))
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
	#m = 4	# Yes good. M = 4, where is this used?

	os.makedirs("wang/saves/ims/", exist_ok=True)

	for i,j in ma.matrices.items():
		im = Image.new("RGB", ((sz-1)*100,(sz-1)*100), (255,255,255))
		for k,l in j.keys.items():
			pos = (int(k[0]* (sz-1)), int(k[1]* (sz-1)))
			im.paste(tile(l,sz), pos)

		im.save("wang/saves/ims/"+str(i[0]) +"." + str(i[1])+".png")

	l = ImageDraw.Draw(im2)
	px = im2.load()
	im = Image.new("RGB", (800,600), (255,255,255))

	for i,j in ma.matrices.items():
		#print(len(j.keys),"items in",i)
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
		
	#	im.paste(tile(j,sz), pos)
	im2.save("wang/reddy.png")
	#im.save("what.png")

