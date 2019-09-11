import subprocess
from PIL import Image, ImageDraw

d = {}

for i in range(768):
    print("try", i)
    im = Image.new("RGB", (768, 768), color=(255,255,255))
    pixels = im.load()
    pixels[i,0] = (255, 0, 0)
    im.save("whatt.png")
    subprocess.call("neko meow.n whatt.png whattt.png", shell=True)
    im2 = Image.open("whattt.png")
    p2 = im2.load()
    for k in range(768):
        j = 0
        if not (p2[k,j][0] == p2[k,j][1] == p2[k,j][2]):
            print(i, j, k, p2[k,j])
            d[i] = k
            print(d)
            break
print(d)

im = Image.open("flag_enc.png")
pixels = im.load()

im2 = Image.new("RGB", (768, 768), color=(255,255,255))
pixels2 = im2.load()

im3 = Image.open("what3.png") # generate this image by encrypting an all white image
p3 = im3.load()

for i in range(768):
    print(i)
    for j in range(768):
        if i in d:
            pixels2[i, j] = (p3[d[i], j][0] ^ pixels[d[i], j][0] ^ 255, p3[d[i], j][1] ^ pixels[d[i], j][1] ^ 255, p3[d[i], j][2] ^ pixels[d[i], j][2] ^ 255)

im2.save("flag.png")
