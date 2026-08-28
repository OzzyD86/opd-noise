from PIL import Image, ImageDraw
from core.statics import *
from core.deckGenerator import colours as cols # This replaces core.statics.cols

from core.deckGenerator import tiles as tt

def tile(tData, size = 10):
	size = size-1
	polys = {
		N: [(0,0),(size,0),(size/2,size/2)],
		"East": [(size,0),(size,size),(size/2,size/2)],
		"South": [(size,size),(0,size),(size/2,size/2)],
		"West": [(0,size),(0,0),(size/2,size/2)],
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

def getAspectRatio(grid):
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
	
def orth(loc=(0,0)):
	jj = []
	for qa in ed:
		jj.append((loc[0]+qa[0], loc[1]+qa[1]))
	return jj
	
def canPlaceAt(grid, loc = (0,0)):
	o = []
	if (loc in grid):
		return False
	for i in tt:
		if (pig(grid, i, loc)):
			o.append(i)
	return o
ofdc = []

def splitGrids(grid, split = 10000):
	return grid[:split], grid[split:]
