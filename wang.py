import random, os, json
import traceback
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

from PIL import Image, ImageDraw, ImageFont
try:
	f = ImageFont.load_default_imagefont()
except:
	f = ImageFont.load_default() #_imagefont()

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
	
def imageTileGrid(loc=(-8,-8), sz=(16,16)):
	im = Image.new("RGBA", ((20*sz[0])+1,(20*sz[1])+1), (255,255,255, 255))
	dr = ImageDraw.Draw(im)
	for i in range(sz[0]):
		for j in range(sz[1]):
			if (ma.get(loc[0]+i,loc[1]+j) is not None):
				k = tile(ma.get(loc[0]+i,loc[1]+j), 21)
				pos = (int(i* (21-1)), int(j* (21-1)))
				im.paste(k, pos)
	for i,j in buildExpectations().items():
		for k in j:
			pd = dr.textbbox((0,0), str(i),font=f)
			#print(p)
			dr.text((((k[0]-loc[0])*20)+10-int(pd[2]/2),(k[1]-loc[1])*20+10-int(pd[3]/2)), str(i),font=f,fill=(0,0,0))
	return im
	
def showWorkings(workings = {}, Trace = True):
	sc = [None, None, None, None]
	for i in buildExpectations().values():
		for j in i:
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
	im = imageTileGrid((sc[0], sc[1]), (sz[0], sz[1]))
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
	for i,j in buildExpectations().items():
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
	
class wangTilePlacer():
	def __init__(self, stack_size = 0):
		self.ma = mc("wang")
		self.stack = []
		self.edges = [(0,0)]
	
		if (os.path.exists("wang/saves/edges.dat")):
			self.edges = json.load(open("wang/saves/edges.dat", "r"))

		if (os.path.exists("wang/saves/stack.dat")):
			self.stack = json.load(open("wang/saves/stack.dat", "r"))

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
				print(thesePoints)
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

def makeTiles(num):
	tiles = []
	for i in range(num):
		tile = {}
		for j in tile_sides:
			tile[j] = random.choice(list(cols.keys()))
		tiles.append(tile)
	return tiles
	
tiles = ofdc + specialTiles(1)
#print("Placing",len(tiles),"tiles.")
prb = True
qwik = False

def doesThisWorkHere(loc):
	check = True
	for i in orth(loc):
		j = i
		if (not wtp.ma.get(*j) and check):
			if (len(canPlaceAt(j)) == 0):
				#print("Neighbour cannot be placed")
				#rb = wtp.rollback()
				check = False
	return check
	
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

	showWorkings({"selected" : [t_loc]}).save("wang/workingsOut-" + str(workings) + ".png")
	workings += 1
		
	ls = canPlaceAt(t_loc)
	random.shuffle(ls)
	rb = None
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

def do():
	global workings, d, rb_mapping_list
	print("Let's do this")
	print("Initial depth down...")

	d = down()
	showWorkings({"selected" : [d['loc']]}).save("wang/workingsOut-" + str(workings) + ".png")
	workings += 1
	print("Result is:", d)
	# This is all good until d['ret'] returns False, which means all objects in this entry have returned unworkable
	
	if (d['ret'] is False):
		rbstack = [] # The rollback stack
		print("We need to rollback from this point")
		rbstack.append(d['rb'])	# rb SHOULD be ONLY not be None if ret is False
		stack = orth(d['loc']) # Prepare for rollback!
		#rb_core_answer = []
		satisfied = False
		rb_mapping_list = []
		while (not satisfied):
			rb_core_answer = wtp.rollbackTo(stack)
			print(rb_core_answer)
			
			for i in rb_core_answer:
				rbstack.append(i)
				rb_mapping_list.append(i[0])
			showWorkings({"selected" : [d['loc']], "rbs": rb_mapping_list}).save("wang/workingsOut-" + str(workings) + ".png")
			workings += 1
			
			grid_changed = False
			while (len(rbstack) > 0):	# Run through all the tiles and add them back
				satisfied = True
				a = rbstack.pop()
				print(a)
				# NOT JUST YET
				showWorkings({"selected" : [d['loc']], "rbs": rb_mapping_list, "focus": [a[0]]}).save("wang/workingsOut-" + str(workings) + ".png")
				workings += 1
				# a[1] is current value, this should be valid but not correct
				if (len(a[2]) > 0):
					print("a[2] is", a[2])
					# This is a list of new values to try. If these pass, then let the whole loop continue
					if (grid_changed):
						tsa = False # Try Something Else
						# Try current answer again, then try re-running canPlaceAt without current answer
						if (pig(a[1], a[0])):
							wtp.place(a[0], a[1], a[2])
							if (doesThisWorkHere(a[0])):
								print("This worked")
								placed = True
								grid_changed = True
								# Let's make a picture!
								showWorkings({"selected" : [d['loc']], "rbs": rb_mapping_list, "focus": [a[0]]}).save("wang/workingsOut-" + str(workings) + ".png")
								workings += 1
							else:
								tsa = True
								wtp.rollback()
						else:
							tsa = True
							
						if (tsa):
							y = canPlaceAt(a[0])
							if (len(y) == 0):
								raise Exception("F05A: What now?") # But I've not written that yet
							else:
								placed = canima(a[0], y)
								
								if (placed is False):
									rbstack.append([a[0], [], []])
									stack += orth(a[0])	# Unsure, but we should break if an item adjacent to any other chosen is selected?
									satisfied = False
									break		
								else:
									grid_changed = True
									
						#raise Exception("F01: Success, carry on") # But I've not written that yet
					else:
						placed = canima(a[0], a[2])
						'''placed = False
						while (len(a[2]) > 0):
							b = a[2].pop(0)	# Take the next tile for this square
							if (pig(b, a[0])):
								wtp.place(a[0], b, a[2])
								if (doesThisWorkHere(a[0])):
									print("This worked")
									grid_changed = True
									# Let's make a picture!
									showWorkings({"selected" : [d['loc']], "rbs": rb_mapping_list, "focus": [a[0]]}).save("wang/workingsOut-" + str(workings) + ".png")
									workings += 1
									break
								else:
									wtp.rollback()'''
						if (placed is False and grid_changed is False):
							rbstack.append([a[0], [], []])
							stack += orth(a[0])	# Unsure, but we should break if an item adjacent to any other chosen is selected?
							satisfied = False
							break # This will break the rb_core_answer loop as desired
						elif (placed is False and grid_changed is True):
							raise Exception("F04: Does this happen? How do I resolve this?") # But I've not written that yet
						else:
							grid_changed = True
				else:
					# This is where the heartache starts: 
					if (grid_changed):
						# If the grid has changed, then we should re-run canPlaceAt, exclude a[1] from this list and cycle?
						y = canPlaceAt(a[0])
						if (len(y) == 0):
							raise Exception("F05: What now?") # But I've not written that yet
						else:
							placed = canima(a[0], y)
							#False
							'''while (len(y) > 0):
								# I've copied this from above
								b = y.pop()

								if (pig(b, a[0])):
									wtp.place(a[0], b, y)
									if (doesThisWorkHere(a[0])):
										print("This worked")
										placed = True
										grid_changed = True
										# Let's make a picture!
										showWorkings({"selected" : [d['loc']], "rbs": rb_mapping_list, "focus": [a[0]]}).save("wang/workingsOut-" + str(workings) + ".png")
										workings += 1
										break
									else:
										wtp.rollback()'''
										
							if (placed is False):
								rbstack.append([a[0], [], []])
								stack += orth(a[0])	# Unsure, but we should break if an item adjacent to any other chosen is selected?
								satisfied = False
								break
							else:
								grid_changed = True
						#	raise Exception("F02: Eh? I'm here and the grid's not changed!") # But I've not written that yet
					else:
						# If the grid has NOT changed, and the length of remaining a is 0 then we should rollback further with THIS tile as the orth
						rbstack.append([a[0], [], []]) # This bit of code again?
						stack += orth(a[0])	# Unsure, but we should break if an item adjacent to any other chosen is selected?
						satisfied = False
						break
						
						raise Exception("F03: Unhandled this part") # But I've not written that yet
				pass

		# Did it get here?
		showWorkings({"selected" : [d['loc']], "rbs": rb_mapping_list, "focus": [a[0]]}).save("wang/workingsOut-" + str(workings) + ".png")
		workings += 1

		#exit(1) # Fuck don't save it here!
		
	print("=" * 8)
	print("Operation complete")

do()

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
