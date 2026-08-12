import json

def json_dumps_tuple_keys(mapping, stringify = True):
	string_keys = {json.dumps(k): v for k, v in mapping.items()}
	if (stringify):
		return json.dumps(string_keys)
	else:
		return string_keys

class keyMatrix():
	def __init__(self):
		self.size = 100
		self.keys = {}
		
	def set(self,x,y,value):
		self.keys[x,y] = value
	
	def get(self,x,y):
		if((x,y) in self.keys):
			return self.keys[x,y]
		return None
		
	def save(self):
		return json_dumps_tuple_keys(self.keys, stringify = False)
