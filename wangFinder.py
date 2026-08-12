from core.keyMatrix import keyMatrix
from time import sleep
import wang
import json, os
import random
from core.matrixController import json_loads_tuple_keys
#print("Here?!")
field_size = 16
p = wang.makeDistinctTiles(1)
#p.remove({penrose.N:1,penrose.E:1,
#	penrose.S:1,penrose.W:1})
'''p = [

	{"North":1,"East":2,"South":3, "West":4},
	{"North":2,"East":3,"South":4, "West":1},
	{"North":3,"East":4,"South":1, "West":2},
	{"North":4,"East":1,"South":2, "West":3},

]'''

unique_p = []
for i in p:
	if not i in unique_p:
		unique_p.append(i)
p = unique_p

input = None
pree = 0
if (False and os.path.exists("stack.dat")):
	input = json.load(open("stack.dat", "r"))
	field_size = input["size"]
	#print(input)
	pree = input["loop"]

def pig(tile, location, largest_match = False):
	mat=0
	i=k=0
	for i,k in wang.t_assoc.items():
		check = ((location[0]+k[0][0]) %ma.size,(location[1]+k[0][1]) % ma.size)
		ck = ma.get(*check)
		if (ck is not None):
			mat+=1
			if (ck[k[1]] != tile[i]):
				return False
	if (largest_match):
		return mat
	return True

class loopTileGenerator():
	def __init__(self, size=16):
		self.ma = keyMatrix()
		self.ma.size = size
		self.stack = []
		pass

	def _popDown(self, cho):
		x = self.uniqueness()["oo"]
		#print(x)
		uni = []
		nonuni = []
		random.shuffle(cho[1])
		for i in cho[1]:
			if (i in x):
				uni.append(i)
			else:
				nonuni.append(i)
		
		cho = (cho[0], list(nonuni) + list(uni))
		st_item = [cho[0],cho[1].pop(0),cho[1]]

		self.ma.set(*st_item[0], st_item[1])
		self.stack.append(st_item)

	def _pushUp(self):
		xm = self.stack.pop()
		self.ma.set(*xm[0], None) 
		tmq = len(xm[2])
		while (tmq == 0):
			xm = self.stack.pop()
			self.ma.set(*xm[0], None)
			tmq = len(xm[2])
			
		xm[1] = xm[2].pop(0)
		
		self.ma.set(*xm[0], xm[1])
		self.stack.append(xm)

	def uniqueness(self):
		oo = []
		noo=[]
		for j in range(self.ma.size):
			for k in range(self.ma.size):
				if ((j,k) in self.ma.keys and self.ma.keys[j,k] not in oo):
					oo.append(ma.keys[j,k])
				elif ((j,k) not in self.ma.keys or self.ma.keys[j,k] is None):
					noo.append((i,j))
		return {"oo": oo, "noo": noo}

	def getStack(self):
		tiv={}
		tp = None
		st = []
		for i in range(self.ma.size):
			for j in range(self.ma.size):
				if (self.ma.get(i,j) is None):
					c=0
					t = []
					for k in p:
						if (pig(k, (i,j), False) is True):
							c += 1
							t.append(k)
							
					tiv[i,j] = c
					if (tp is None or c < tp):
						tp = c
						st = [((i,j),t)]
						#print(tp)
					elif (tp == c):
						st.append([(i,j),t])
					#print(i,j,ma.get(i,j),c)
		return [st, tiv]	
		
	def _go(self, val):
		cct = 0
		si = 0
		for i in range(500000000):
			x, tiv = (self.getStack())
			if (i % 100 == 0):
				print(i + pree, len(self.stack))
				#drwImg(tiv, self.ma.size).save("wang/" +str(i) +".png")
			if (i% 1000 == 0):
				json.dump({ "stack": self.stack, "state" : self.ma.save(), "size": self.ma.size, "loop": i+pree}, open("stack.dat", "w"))
			ap = self.uniqueness()

			#print(len(x), len(ap['noo']), len(p) - len(ap['oo']))
			if (len(x) == 0):
				print("Complete")
				oo = len(ap["oo"])
				if (oo == len(p)):
					print("Happy")
					drwImg(tiv, self.ma.size).save("wang/" +str(i+pree) +".png")
				else:
					if ((oo)> si):
						print(i, si, oo)
						drwImg(tiv, self.ma.size).save("wang/" +str(i+pree) +".png")
						si = oo
					#print("No matchy matchy")
				self._pushUp()
				#break
			elif ((len(p) - len(ap["oo"])) > len(ap["noo"])):
				#print(str(i), "Impossible?")
				if (len(ap["oo"]) > cct):
					drwImg(tiv).save("wang/" +str(i+pree) +".png")
					cct=len(ap["oo"])
				self._pushUp()
				
			else:
				cho = random.choice(x)
				#print(cho)
				if (len(cho[1]) > 0):
					self._popDown(cho)
				else:
					self._pushUp()
				
			if (len(self.ma.keys) == 0):
				break
			#print(ma.keys)
		
ltg = loopTileGenerator(field_size)
ma = ltg.ma
if (input is not None):
	input['state'] = json.dumps(input['state'])
	ma.keys = json_loads_tuple_keys(input["state"])
	ltg.stack = input["stack"]

from PIL import Image, ImageDraw, ImageFont
try:
	f = ImageFont.load_default_imagefont()
except:
	f = ImageFont.load_default() #_imagefont()

def drwImg(tivs, sz = 16):
	im = Image.new("RGB", ((20*sz)+1,(20*sz)+1), (255,255,255))
	dr = ImageDraw.Draw(im)
	for i in range(sz):
		for j in range(sz):
			if (ma.get(i,j) is not None):
				k = wang.tile(ma.get(i,j), 21)
				pos = (int(i* (21-1)), int(j* (21-1)))
				im.paste(k, pos)
			elif ((i,j) in tivs):
				pd = dr.textbbox((0,0), str(tivs[i,j]),font=f)
				#print(p)
				dr.text(((i*20)+10-int(pd[2]/2),j*20+10-int(pd[3]/2)), str(tivs[i,j]),font=f,fill=(0,0,0))
	return im
stack = ltg.stack

# Stack down
si = 0
ltg._go(500000000)
	
im = Image.new("RGB", ((20*16)+1,(20*16)+1), (255,255,255))
for i in range(16):
	for j in range(16):
		if (ma.get(i,j) is not None):
			k = wang.tile(ma.get(i,j), 21)
			pos = (int(i* (21-1)), int(j* (21-1)))
			im.paste(k, pos)
im.save("wang/fWang.png")
