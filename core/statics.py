N = "North"
E = "East"
S = "South"
W = "West"

t_assoc = {
	N:((0,-1),S), 
	S:((0,1),N), 
	W:((-1,0),E),
	E:((1,0),W)
}
ed = [(0,1),(1,0),(-1,0),(0,-1)]

cols = ["red", "yellow", "green", "blue"]