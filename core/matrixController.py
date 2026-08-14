def json_loads_tuple_keys(string, unstringify=True):
	if (unstringify):
		mapping = json.loads(string)
	else:
		mapping = string
	return {tuple(json.loads(k)): v for k, v in mapping.items()}

from PIL import Image
import os
import json
from imgProcessor import imgProcessor
from core.keyMatrix import keyMatrix

class matrixController():
	def __init__(self, dir = ".", stack = False):
		self.stack = []
		self.stack_size = stack
		self.dir = dir
		self.loads = 0
		self.matrices = {}
		
	def getFilenameFor(self, zn):
		i = zn
		d = (i[0] // 100, i[1] // 100)
		f = (i[0] % 100, i[1] % 100)
		return self.dir + "/saves/" + str(d[0])+"."+str(d[1])+"/"+str(f[0])+"."+str(f[1])+".dat"
	
	def writeImages(self, i, j):
		return True

	def save(self):
		subs = []
		for i, j in self.matrices.items():
			#print(i)
			os.makedirs("saves/ims/1/", exist_ok=True)

			# now ... before saving, lets make a picture
			im = Image.new("RGB",(100,100), (255, 192, 192))
			px = im.load()
			for p in j.keys:
				px[p] = (j.keys[p]*255, j.keys[p]*255, j.keys[p]*255)
				
			if not ((i[0]//2, i[1] //2 ) in subs):
				subs.append((i[0]//2, i[1] //2))
			im.save("saves/ims/1/"+str(i[0]) +"." + str(i[1])+".png")
			
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
			#print(i,j)
			
		ip = imgProcessor(subs, level = 2)
		ip2 = imgProcessor(ip.next, level = 3)
		ip3 = imgProcessor(ip2.next, level = 4)
	
	def load(self, m):
		if (os.path.exists(self.getFilenameFor(m))):
			print("loaded", self.getFilenameFor(m))
			f = open(self.getFilenameFor(m), "r")
			o = f.read()
			oo = json.loads(o)
			self.matrices[m] = keyMatrix()
			if ("version" in oo):
				#print("LOADED VERSION", oo['version'])
				self.matrices[m].keys = json_loads_tuple_keys(oo['data'], False)
				setattr(self.matrices[m], "version", 1)
			else:
				self.matrices[m].keys = json_loads_tuple_keys(o)
			
			f.close()
			# load it from file
		else:
			print("New", self.getFilenameFor(m))
			self.matrices[m] = keyMatrix()
		self.loads += 1
		
	def get(self,x,y):
		t = (x % 100, y % 100)
		m = (x // 100, y // 100)
		
		if (m not in self.matrices):
			self.load(m)
			
		return self.matrices[m].get(t[0],t[1])
		
	def set(self,x,y,v):
		t = (x % 100, y % 100)
		m = (x // 100, y // 100)
		
		if (m not in self.matrices):
			self.load(m)
		
		self.matrices[m].set(t[0], t[1], v)
		pass
		

