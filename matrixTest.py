from PIL import Image, ImageDraw
import os

offset = (-4, -4)
sz = (8,8)
im = Image.new("RGB", (sz[0]*100,sz[1] * 100), (255,255,255))
lev = 4
for i in range(0, sz[0]):
	for j in range(0, sz[1]):
		f = "saves/ims/"+str(lev)+ "/" + str(offset[0] + i) + "." + str(offset[1] + j) + ".png"
		if (os.path.exists(f)):
			k = Image.open(f)
			im.paste(k, (i * 100, j * 100))
			print("Yes")
		print(i, j)

im.save("o5.png")