import json
from matrixController import json_loads_tuple_keys
import os

def load_matrix(x, y):
	dr = (x // 100, y // 100)
	fn = (x % 100, y % 100)
	#print("Loading saves/" + str(dr[0]) + "." + str(dr[1]) + "/" + str(fn[0]) + "." + str(fn[1]) + ".dat")
	
	if (not os.path.exists("saves/" + str(dr[0]) + "." + str(dr[1]) + "/" + str(fn[0]) + "." + str(fn[1]) + ".dat")):
		return None
		
	d = json.load(open("saves/" + str(dr[0]) + "." + str(dr[1]) + "/" + str(fn[0]) + "." + str(fn[1]) + ".dat", "r"))

	if ("version" in d):
		#print(d['version'])
		#print(d)
		return json_loads_tuple_keys(d['data'], False)
	else:
		return json_loads_tuple_keys(d, False)

zone = ((-500,-50), (50,50))
	
loaded_matrices = {}	

open_mats = ((zone[0][0] // 100, zone[0][1] // 100), ((zone[1][0]-1) // 100, (zone[1][1]-1) // 100))
#print(open_mats)
vert_mat = None

var = 0
ct = 0
nx = []
for i in range(zone[0][1], zone[1][1]): # Top to bottom
	if (vert_mat is None or vert_mat != (i // 100)):
		loaded_matrices = {}
		# Load new tiles here
		vert_mat = i // 100
		for j in range(open_mats[0][0], open_mats[1][0]+1):
			loaded_matrices[j, vert_mat] = load_matrix(j, vert_mat)
			#print("Open matrix", (vert_mat, j))
		#print(vert_mat)
	for j in range(zone[0][0], zone[1][0]): # left to right
		#print(j, i)
		dloc = ((j // 100, vert_mat), (j % 100, i % 100))
		
		if (loaded_matrices[dloc[0]] is not None):
			if (dloc[1] in loaded_matrices[dloc[0]]):
				pix = loaded_matrices[dloc[0]][dloc[1]]
				ct += 1
				var = (var*2) + pix
				if (ct >= 8):
					nx.append(str(hex(var)[2:].zfill(2).upper()))
					var = 0
					ct = 0
			else:
				pass
				#print(dloc[1], "is not in matrix", dloc[0])

print(" ".join(nx))
exit()

