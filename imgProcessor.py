from PIL import Image
import os

class imgProcessor():
	def __init__(self, values = [], level = 1, full = False):
		self.next =[]
		os.makedirs("saves/ims/" + str(level) +"/", exist_ok=True)
		for i in values:
			o = []
			im = Image.new("RGB",(100,100), (255,192 + int(level * 15.75), 192 + int(level * 15.75)))
			px = im.load()
			for j in [(0,0),(0,1),(1,0),(1,1)]:
				jj = ((i[0]*2+j[0],i[1]*2+j[1]))
				
				ff = "saves/ims/" + str(level-1) + "/" + str(jj[0])+"."+str(jj[1])+".png"
				if (os.path.exists(ff)):
					sim = Image.open(ff)
					spx = sim.load()
					for l in range(0,50):
							for m in range(0,50):
								v = 0
								for n in [(l*2,m*2), (l*2+1,m*2), (l*2,m*2+1), (l*2+1,m*2+1)]:
									if (type(spx[n]) is tuple and type(v) is not tuple):
										v = (v + spx[n][0], v + spx[n][1], v + spx[n][2])
									elif (type(spx[n]) is tuple and type(v) is tuple):
										v = (v[0] + spx[n][0], v[1] + spx[n][1], v[2] + spx[n][2])
									else:
										v += spx[n]
								
								if (type(v) is tuple):
									v = (int(v[0] / 4), int(v[1] / 4), int(v[2] / 4))
								else:
									v = (int(v / 4), int(v / 4), int(v / 4))
								px[(j[0]*50)+l,(j[1]*50)+ m] = v

					#print("Yes")
			im.save("saves/ims/"+str(level)+"/"+str(i[0]) +"." + str(i[1])+".png")
			if not ((i[0]//2,i[1]//2) in self.next):
				self.next.append((i[0]//2,i[1]//2))
			#print("Attempt ",o, "for", i)
			#print("Build level",level,",", i)
		pass
		
	def passByMatrices(self, matrices):
		pass
