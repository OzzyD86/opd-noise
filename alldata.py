import os
import json

from matrixController import json_loads_tuple_keys
#(string):
 #   mapping = json.loads(string)
 #   return {tuple(json.loads(k)): v for k, v in mapping.items()}
# Get all data

points = 0
for core, dirs, files in os.walk("saves"):
	if (core not in ["saves"] and core[:9] not in ["saves\\ims"]):
		for f in files:
			fl = core + "/" + f
			#print("Open " + fl)
			
			ff = open(fl, "r")
			data = ff.read()
			dd = json.loads(data)
			if ("version" in dd):
				final_data = json_loads_tuple_keys(dd['data'], False)
			else:
				final_data = json_loads_tuple_keys(data)
			points += len(final_data)
			#print(len(final_data))
#		print(core, files)
print("Points:", points)