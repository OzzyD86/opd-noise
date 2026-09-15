import random, os, json
import traceback

N = "North"
E = "East"
S = "South"
W = "West"

import core.deckGenerator
discard = []

t_assoc = {
	N: ((0, -1), S), 
	S: ((0, 1), N), 
	W: ((-1, 0), E),
	E: ((1, 0), W)
}
ed = [(0, 1), (1, 0), (-1, 0), (0, -1)]
cols = ["red", "yellow", "green", "blue"]

def makeDistinctTiles():
	tiles = []
	for a in cols:
		for b in cols:
			for c in cols:
				for d in cols:
					tile = {N: a, E: b, S: c, W: d}
					tiles.append(tile)
	return tiles

cols = core.deckGenerator.colours
tt = core.deckGenerator.tiles

dg = core.deckGenerator.deckGenerator()
dg.addColour("red", (255, 0, 0))
dg.addColour("green", (0, 255, 0))
dg.addColour("yellow", (255, 255, 0))
dg.addColour("blue", (0, 0, 255))

m = makeDistinctTiles()
m.pop(0)
for i in m:
	dg.addTile(**i)

def tileValidationChecker(tiles):
	for i in tiles:
		for k, l in t_assoc.items():
			t = 0
			for j in tiles:
				m = (i[k] == j[l[1]])
				if (m):
					t += 1
			if (t == 0):
				print(i, k, t, "valid", l[1], "tiles")
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

ofdc = []
if (os.path.exists("wang/saves/discards.dat")):
	ofdc = json.load(open("wang/saves/discards.dat", "r"))
	print("Loaded", len(ofdc), "previously discarded tiles")
else:
	print("No discarded tiles")

from PIL import Image, ImageDraw, ImageFont
try:
	f = ImageFont.load_default_imagefont()
except Exception:
	f = ImageFont.load_default()

def buildExpectations():
	print("Building tile expectations...")
	op = {}
	for i in list(wtp.edges):
		tm = canPlaceAt(i)
		if (tm is False or tm is None):
			if i in wtp.edges:
				wtp.edges.remove(i)
		else:
			if (len(tm) in op):
				op[len(tm)].append(i)
			else:
				op[len(tm)] = [i]
	print("Done.")
	return op

def tile(tData, size=10):
	size = size - 1
	polys = {
		N: [(0, 0), (size, 0), (size / 2, size / 2)],
		E: [(size, 0), (size, size), (size / 2, size / 2)],
		S: [(size, size), (0, size), (size / 2, size / 2)],
		W: [(0, size), (0, 0), (size / 2, size / 2)],
	}
	im = Image.new("RGB", (size + 1, size + 1))
	dr = ImageDraw.Draw(im)
	if (tData is not None):
		for i, j in tData.items():
			if (i in polys):
				dr.polygon(polys[i], fill=cols[j], outline=(0))
	else:
		dr.rectangle((0, 0, size, size), fill=(128, 128, 128))
	return im

def pig(tile, location, largest_match=False):
	mat = 0
	for i, k in t_assoc.items():
		check = (location[0] + k[0][0], location[1] + k[0][1])
		ck = ma.get(*check)
		if (ck is not None):
			mat += 1
			if (ck[k[1]] != tile[i]):
				return False
	if (largest_match):
		return mat
	return True

def canPlaceAt(loc=(0, 0)):
	o = []
	if (wtp.ma.get(*loc) is not None):
		return False
	for i in tt:
		if (pig(i, loc)):
			o.append(i)
	return o

def imageTileGrid(loc=(-8, -8), sz=(16, 16)):
	im = Image.new("RGBA", ((20 * sz[0]) + 1, (20 * sz[1]) + 1), (255, 255, 255, 255))
	dr = ImageDraw.Draw(im)
	for i in range(sz[0]):
		for j in range(sz[1]):
			if (ma.get(loc[0] + i, loc[1] + j) is not None):
				k = tile(ma.get(loc[0] + i, loc[1] + j), 21)
				pos = (int(i * (21 - 1)), int(j * (21 - 1)))
				im.paste(k, pos)
	for i, j in buildExpectations().items():
		for k in j:
			pd = dr.textbbox((0, 0), str(i), font=f)
			dr.text((((k[0] - loc[0]) * 20) + 10 - int(pd[2] / 2), (k[1] - loc[1]) * 20 + 10 - int(pd[3] / 2)), str(i), font=f, fill=(0, 0, 0))
	return im

def showWorkings(workings={}, Trace=True):
	sc = [None, None, None, None]
	be = buildExpectations()
	for i in be.values():
		for j in i:
			if (sc[0] is None or j[0] < sc[0]): sc[0] = j[0]
			if (sc[2] is None or j[0] > sc[2]): sc[2] = j[0]
			if (sc[1] is None or j[1] < sc[1]): sc[1] = j[1]
			if (sc[3] is None or j[1] > sc[3]): sc[3] = j[1]

	if None in sc:
		sc = [-5, -5, 5, 5]

	sz = [sc[2] - sc[0] + 1, sc[3] - sc[1] + 1]
	im = Image.new("RGB", ((20 * sz[0]) + 1, (20 * sz[1]) + 1), (255, 255, 255))
	dr = ImageDraw.Draw(im)
	c = [(255, 127, 127), (255, 255, 127), (127, 255, 127)]
	cc = 0
	for i in workings.values():
		if isinstance(i, list):
			for j in i:
				if isinstance(j, (tuple, list)) and len(j) >= 2:
					dr.rectangle(((j[0] - sc[0]) * 20, (j[1] - sc[1]) * 20, (j[0] - sc[0] + 1) * 20, (j[1] - sc[1] + 1) * 20), fill=c[cc % len(c)])
		cc += 1
			
	for i in range(sz[0]):
		for j in range(sz[1]):
			if (ma.get(i + sc[0], j + sc[1]) is not None):
				k = tile(ma.get(i + sc[0], j + sc[1]), 21)
				pos = (int(i * (21 - 1)), int(j * (21 - 1)))
				im.paste(k, pos)
	for i, j in be.items():
		for k in j:
			pd = dr.textbbox((0, 0), str(i), font=f)
			dr.text((((k[0] - sc[0]) * 20) + 10 - int(pd[2] / 2), (k[1] - sc[1]) * 20 + 10 - int(pd[3] / 2)), str(i), font=f, fill=(0, 0, 0))

	if (Trace):
		v = 0
		for i in traceback.extract_stack():
			li = str(i)
			pd = dr.textbbox((0, 0), str(li), font=f)
			dr.text((0, v), str(li), font=f, fill=(0, 0, 0))
			v += (pd[3] - pd[1])
	return im

class mc(matrixController):
	def save(self):
		for i, j in self.matrices.items():
			fl = self.getFilenameFor(i)
			print("save", fl, "here")
			dirs = ("/".join(fl.split("/")[:-1]))
			if dirs:
				os.makedirs(dirs, exist_ok=True)
			f = open(fl, "w")
			f.write(json.dumps({
				"version": 1,
				"data": j.save()
			}))
			f.close()

def orth(loc=(0, 0)):
	jj = []
	for qa in ed:
		jj.append((loc[0] + qa[0], loc[1] + qa[1]))
	return jj

class wangTilePlacer():
	def __init__(self, stack_size=0):
		self.ma = mc("wang")
		self.stack = []
		self.edges = [(0, 0)]
	
		if (os.path.exists("wang/saves/edges.dat")):
			self.edges = json.load(open("wang/saves/edges.dat", "r"))

		if (os.path.exists("wang/saves/stack.dat")):
			self.stack = json.load(open("wang/saves/stack.dat", "r"))

	def place(self, where, what, anc={}):
		ty = []
		if (where in self.edges):
			self.edges.remove(where)
		self.stack.append([where, what, anc])
		self.ma.set(*where, what)
		for i in orth(where):
			if ((self.ma.get(*i) is None) and (tuple(i) not in ty) and (tuple(i) not in self.edges)):
				ty.append(tuple(i))
		self.edges += ty
		return True
		
	def unplace(self, where):
		self.ma.set(*where, None)
		if (where not in self.edges):
			self.edges.append(where)
		for i in orth(where):
			if (i in self.edges):
				l = 0
				for k in orth(i):
					if (k in self.edges or self.ma.get(*k) is None):
						l += 1
				if (l == 4 and i in self.edges):
					self.edges.remove(i)
		return True
		
	def rollback(self):
		if (len(self.stack) == 0):
			print("Stack empty: Cannot rollback further.")
			return None
		i = self.stack.pop()
		self.unplace(i[0])
		return i

	def rollbackTo(self, thesePoints=[]):
		print("=== Start rollback ===")
		rblist = []
		satisfied = False
		thesePointsTuples = [tuple(p) for p in thesePoints]
		while not satisfied and len(self.stack) > 0:
			rbclock = None
			p = None
			while len(self.stack) > 0 and (rbclock not in thesePointsTuples):
				p = self.rollback()
				if p is None:
					break
				rbclock = tuple(p[0])
				rblist.append(p)
			
			if p is None:
				break

			satisfied = True
			if len(p[2]) == 0:
				satisfied = False
				thesePointsTuples += [tuple(x) for x in orth(p[0])]
		return rblist

wtp = wangTilePlacer()
ma = wtp.ma

tiles = ofdc + specialTiles(1)
prb = True
qwik = False

def doesThisWorkHere(loc):
	check = True
	for i in orth(loc):
		if (wtp.ma.get(*i) is None and check):
			k = canPlaceAt(i)
			if (k is not False and len(k) == 0):
				check = False
	return check

workings = 0

def down(point=None):
	print("Down Command")
	if (point is None):
		op = buildExpectations()
		if not op:
			return {"ret": False, "loc": (0,0), "rb": None}
		p = sorted(list(op.keys()))
		random.shuffle(op[p[0]])
		t_loc = op[p[0]].pop()
	else:
		t_loc = point

	ls = canPlaceAt(t_loc)
	if not ls:
		return {"ret": False, "loc": t_loc, "rb": None}

	random.shuffle(ls)
	rb = None
	while (len(ls) > 0):
		i = ls.pop(0)
		if (not pig(i, t_loc)):
			continue
		wtp.place(t_loc, i, list(ls))
		
		check = True
		for neighbor in orth(t_loc):
			if (wtp.ma.get(*neighbor) is None and check):
				placements = canPlaceAt(neighbor)
				if (placements is not False and len(placements) == 0):
					rb = wtp.rollback()
					check = False
		if (check):
			return {"ret": True, "loc": t_loc, "rb": rb}
	return {"ret": False, "loc": t_loc, "rb": rb}

def canima(loc, ls):
	global workings, d, rb_mapping_list
	placed = False
	while (len(ls) > 0):
		b = ls.pop()
		if (pig(b, loc)):
			wtp.place(loc, b, list(ls))
			if (doesThisWorkHere(loc)):
				placed = True
				#showWorkings({"selected": [d['loc']], "rbs": rb_mapping_list, "focus": [loc]}).save(f"wang/workingsOut-{workings}.png")
				#workings += 1
				break
			else:
				wtp.rollback()
	return placed

def do():
	global workings, d, rb_mapping_list
	print("Let's do this")
	print("Initial depth down...")

	d = down()
	showWorkings({"selected": [d['loc']]}).save(f"wang/workingsOut-{workings}.png")
	workings += 1
	print("Result is:", d)
	
	if (d['ret'] is False):
		rbstack = []
		if d['rb'] is not None:
			rbstack.append(d['rb'])
		stack = orth(d['loc'])
		
		satisfied = False
		rb_mapping_list = []
		while (not satisfied and (len(wtp.stack) > 0 or len(rbstack) > 0)):
			rb_core_answer = wtp.rollbackTo(stack)
			for i in rb_core_answer:
				rbstack.append(i)
				rb_mapping_list.append(i[0])
			
			grid_changed = False
			while (len(rbstack) > 0):
				satisfied = True
				a = rbstack.pop()
				
				if (len(a[2]) > 0):
					if (grid_changed):
						tsa = False
						if (pig(a[1], a[0])):
							wtp.place(a[0], a[1], a[2])
							if (doesThisWorkHere(a[0])):
								grid_changed = True
								#showWorkings({"selected": [d['loc']], "rbs": rb_mapping_list, "focus": [a[0]]}).save(f"wang/workingsOut-{workings}.png")
								#workings += 1
							else:
								tsa = True
								wtp.rollback()
						else:
							tsa = True
							
						if (tsa):
							y = canPlaceAt(a[0])
							if not y:
								rbstack.append([a[0], [], []])
								stack += orth(a[0])
								satisfied = False
								break
							else:
								placed = canima(a[0], y)
								if (placed is False):
									rbstack.append([a[0], [], []])
									stack += orth(a[0])
									satisfied = False
									break
								else:
									grid_changed = True
					else:
						placed = False
						while (len(a[2]) > 0):
							a[1] = a[2].pop()
							if (pig(a[1], a[0])):
								wtp.place(a[0], a[1], a[2])
								if (doesThisWorkHere(a[0])):
									placed = True
									grid_changed = True
									break
								else:
									wtp.rollback()
						if (placed is False):
							rbstack.append([a[0], [], []])
							stack += orth(a[0])
							satisfied = False
							break
						else:
							grid_changed = True
				else:
					if (grid_changed):
						y = canPlaceAt(a[0])
						if not y:
							rbstack.append([a[0], [], []])
							stack += orth(a[0])
							satisfied = False
							break
						else:
							placed = canima(a[0], y)
							if (placed is False):
								rbstack.append([a[0], [], []])
								stack += orth(a[0])
								satisfied = False
								break
							else:
								grid_changed = True
					else:
						rbstack.append([a[0], [], []])
						stack += orth(a[0])
						satisfied = False
						break

		showWorkings({"selected": [d['loc']], "rbs": rb_mapping_list}).save(f"wang/workingsOut-{workings}.png")
		workings += 1
		
	print("=" * 8)
	print("Operation complete")
	print(f"Total steps saved: {workings}")

for i in range(1):
	do()

if (__name__ == "__main__"):
	ma.save()
	os.makedirs("wang/saves/", exist_ok=True)
	json.dump(discard, open("wang/saves/discards.dat", "w"))
	json.dump(wtp.edges, open("wang/saves/edges.dat", "w"))
	json.dump(wtp.stack, open("wang/saves/stack.dat", "w"))
	
	imageTileGrid((-15, -15), (30, 30)).save("wang/xWang.png")