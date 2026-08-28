import random, os, json
import traceback

from core.statics import *

from datetime import datetime
print (datetime.now())
start = datetime.now()
def timely(start, now, progress, total):
	elap = (now-start)
	
	return (total - progress)*(elap/progress)
	
print(timely(start, datetime.now(),1,2))
import core.deckGenerator
discard = []

from core.gridCommands import *

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
		p = (len(canPlaceAt(grid, i)))

		pd = dr.textbbox((0,0), str(p),font=f)
			#print(p)
		dr.text((((i[0]-loc[0])*20)+10-int(pd[2]/2),(i[1]-loc[1])*20+10-int(pd[3]/2)), str(p),font=f,fill=(0,0,0))

	return im
	
if not (tileValidationChecker(tt)):
	exit()

def specialTiles(num):
	tiles = []
	for i in range(num):
		tiles.append(random.choice(tt))
	return tiles
	
#grid = {}

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

from core.wangTilePlacer import wangTilePlacer

if (os.path.exists("wang/saves/grids.dat")):
	grids_init = [{}]#json.load(open("wang/saves/grids.dat", "r"))
	grids_in =[]
	#for i in grids_init:
	#	grids_in.append(json_loads_tuple_keys(i))
else:
	grids_in =[{}]
	
wtp = wangTilePlacer()
ma = wtp.ma

from core.gridManager import gridManager
	
grids_out = []

gm = gridManager(250)

#print(gm.findAllGrids())
gm.load(0)

if (0 not in list(gm.listGridSizes().keys())):
	print("No")
	gm.grids[0] = [{}]

tileMax = None
x=0
ct = 0
tot=150
g = 0
while (ct < tot and gm.listGridSizes()[g] > 0 ):
	for i in range(gm.listGridSizes()[g]):
		#print(ct,i)
		ign = False
		gr = gm.grids[g].pop()
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

print(list(gm.listGridSizes().keys()))
	
print(gm.listGridSizes())
#def saveAllGrids(grids):
#	c=0
#	if (os.path.exist)
gm.saveAll()
exit()

tiles = specialTiles(1)

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

if (__name__ == "__main__"):

	ma.save()
	json.dump(discard, open("wang/saves/discards.dat", "w"))
	json.dump(wtp.edges, open("wang/saves/edges.dat", "w"))
	json.dump(wtp.stack, open("wang/saves/stack.dat", "w"))
	
	imageTileGrid((-15,-15),(30,30)).save("wang/xWang.png")
