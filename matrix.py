x = {}
y = [(0,0)]

import json, os, random
from datetime import datetime

from core.matrixController import matrixController

if (os.path.exists("saves/edges.dat")):
	y = json.load(open("saves/edges.dat", "r"))

ma = matrixController()

ed = [(0,1),(0,-1),(1,0),(-1,0)]
st = datetime.now().timestamp()
for i in range(400000):
	a = random.choice(y)
	#print(a)
	y.remove(a)
	
	p =random.choice((0,1))
	ma.set(a[0], a[1], p)
	
	for j in ed:
		q = (a[0]+j[0], a[1]+j[1])
		if (q not in y and ma.get(q[0],q[1]) is None):
			y.append(q)
	
	if (i % 10000 == 0 and i is not 0):
		t = datetime.now().timestamp()
		print(i, "in", t-st, "seconds (", (t-st)/i, "seconds average )")
		
	if (ma.loads > 1000):
		print("Too many loaded files")
		break
json.dump(y, open("saves/edges.dat", "w"))
#print(json_dumps_tuple_keys(x))
#print(json.dumps(y))
end = datetime.now().timestamp()
print("Complete in", end-st, "seconds.") 
ma.save()
print("Y count:",len(y))
print("Loaded files:", ma.loads)
