import os, json
from core.keyMatrix import json_dumps_tuple_keys
from core.matrixController import json_loads_tuple_keys
from core.gridCommands import splitGrids

class gridManager():
	def __init__(self, grid_size =199):
		self.grids = {}
		self.grid_size = grid_size
		self.path = "wang/saves/"
		
	def load(self, grid):
		if (grid in self.grids):
			#print("Grid already loaded")
			return False
		print("Load", self.path + "grids-" + str(grid) + ".dat")
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
		
			#if (len(out) > 0):
			json.dump(out, open("wang/saves/grids-"+str(i)+".dat", "w"))
		#	elif(os.path.exists("wang/saves/grids-"+str(i)+".dat")):
				#os.remove("wang/saves/grids-"+str(i)+".dat")
			#	print("Can delete",i,"as empty")
				
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
		
			a, these = splitGrids(these, self.grid_size-b)
			#print(len(a), len(these))
			self.grids[c] += a
			c+= 1
			
	def listGridSizes(self):
		d = {}
		for i in range(self.findAllGrids()):
			
			self.load(i)
			d[i] = len(self.grids[i])
		return d
