from core.matrixController import matrixController
from core.gridCommands import orth, canPlaceAt, doesThisWorkHere
import random

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
			p = (len(canPlaceAt(grid, i)))
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
