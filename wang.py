import random, os, json
N = "North"
E = "East"
S = "South"
W = "West"

discard = []
tile_sides = {N, E, S, W}
t_assoc = {
	N:((0,-1),S), 
	S:((0,1),N), 
	W:((-1,0),E),
	E:((1,0),W)
}
ed = [(0,1),(1,0),(-1,0),(0,-1)]
cols = {
	1: (255,0,0),
	2:(0,255,0),
	3:(255,255,0),
	4:(0,0,255),
	#5:(255,0,255)
}
tt = [
	{N:1, E:1, S:1, W:1},
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

#if not (tileValidationChecker(tt)):
#	exit()

def specialTiles(num):
	tiles = []
	for i in range(num):
		tiles.append(random.choice(tt))
	return tiles
	
from core.matrixController import matrixController
#grid = {}
y = [(0,0)]

if (os.path.exists("wang/saves/edges.dat")):
		y = json.load(open("wang/saves/edges.dat", "r"))

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

ma = mc("wang")

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

tiles = ofdc + makeTiles(256*5)
print("Placing",len(tiles),"tiles.")
prb = True
qwik = False

def placeTiles(tiles, quick = True):
	discarded = []
	#print("Run")
	while(len(tiles) > 0):
		ch_ti = tiles.pop(random.randrange(len(tiles)))
		if (len(tiles) % 100 == 0):
			print(len(tiles))
		nn=0
		ls = []
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
				
		if (len(ls) > 0):
			ch_gr = random.choice(ls)
			y.remove(ch_gr)

			ma.set(*ch_gr, ch_ti)
			for j in ed:
				i =(ch_gr[0]+j[0], ch_gr[1]+j[1])
				#print(ma.get(*i))
				if ((ma.get(*i) is None) and (not i in y)):
					y.append(i)
		else:
			print("Discarded")
			discarded.append(ch_ti)
	return discarded

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
	json.dump(y, open("wang/saves/edges.dat", "w"))

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
	for i, j in tData.items():
		if (i in polys):
			dr.polygon(polys[i], fill = cols[j], outline=(0))
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
#		im = Image.new("RGB", ((sz-1)*100,(sz-1)*100), (255,255,255))
		for k,l in j.keys.items():
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
	for i in y:
		p = (400+(i[0]*1)+0, 300+(i[1]*1)+0)
		px[p] = (255,0,0)
		
	#	im.paste(tile(j,sz), pos)
	im2.save("wang/reddy.png")
	#im.save("what.png")

