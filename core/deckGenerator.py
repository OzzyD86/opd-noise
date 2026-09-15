class deckGenerator():
	def __init__(self):
		self.colours = {}
		self.tiles = []
		
	def addColour(self, name, value):
		self.colours[name] = value
		
	def addTile(self, **edges):
		#print(edges)
		self.tiles.append(edges)
		pass
		
	def compile(self):
		cols = {}
		piccols = {}
		for i,j in self.colours.items():
			cols[i] = len(cols)+1
			piccols[len(cols)] = j
		
		tile_list = []
		for i in self.tiles:
			new_tile = {}
			for j,k in i.items():
				new_tile[j] = cols[k]
			tile_list.append(new_tile)
		return (tile_list, piccols)
		
q = deckGenerator()
q.addColour("white", (255,255,255))
q.addColour("red", (255,0,0))
q.addColour("green", (0,255,0))
q.addColour("blue", (0,0,255))
q.addTile(North="red", East="red", South="red", West="green")
q.addTile(North="blue", East="red", South="blue", West="green")
q.addTile(North="red", East="green", South="green", West="green")
q.addTile(North="white", East="blue", South="red", West="blue")

q.addTile(North="blue", East="blue", South="white", West="blue")
q.addTile(North="white", East="white", South="red", West="white")
q.addTile(North="red", East="green", South="blue", West="white")

q.addTile(North="blue", East="white", South="blue", West="red")
q.addTile(North="blue", East="red", South="white", West="red")
q.addTile(North="green", East="green", South="blue", West="red")
q.addTile(North="red", East="white", South="red", West="green")

tiles, colours = (q.compile())
#print(tiles)
#print(colours)
