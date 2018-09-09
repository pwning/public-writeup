import tkinter
from PIL import Image, ImageTk, ImageDraw, ImageOps
from sys import argv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from math import pi, sin, cos
import cv2
import numpy as np

def pil_to_cv(im):
	return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

def cv_to_pil(im):
	return Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))

window = tkinter.Tk(className="Color Classifier")

display_size = (720, 405)

# Protip: copy/paste these from output, then you don't need to set them over and over again
points = [
    (593, 185), (598, 293), (600, 397), (601, 505), (600, 609), (605, 719), (605, 817), (607, 922),
    (713, 922), (710, 813), (709, 707), (698, 602), (703, 503), (703, 394), (699, 286), (699, 180),
    (807, 178), (806, 291), (808, 394), (812, 503), (812, 605), (813, 716), (818, 816), (816, 920),
    (919, 918), (917, 813), (919, 707), (917, 607), (917, 500), (917, 389), (914, 290), (916, 178),
    (1021, 173), (1022, 287), (1022, 392), (1025, 496), (1024, 605), (1026, 711), (1025, 816), (1026, 914),
    (1130, 917), (1128, 812), (1129, 703), (1129, 600), (1128, 499), (1124, 394), (1128, 286), (1125, 182),
    (1230, 176), (1229, 287), (1229, 393), (1232, 497), (1233, 600), (1233, 706), (1233, 807), (1233, 916),
    (1336, 913), (1335, 802), (1334, 704), (1334, 595), (1333, 496), (1333, 389), (1332, 285), (1331, 180)
]
led_pos = [(x * display_size[0] / 1920, y * display_size[1] / 1080) for (x, y) in points]

pcnt = 5
params = [(0 for __ in range(pcnt)) for _ in led_pos]
values = [0 for _ in led_pos]
led_size = 14
circle_ang_ranges = [(0, 2*pi)]
circle_divs = 16
select_idx = 0
image = None
img = None
waiting = True
items = []
k = 3
palette_size = 8

data = []
with open("data.csv") as infile:
	for line in infile:
		dat = [float(x) for x in line.split(", ")]
		dat[0] = int(dat[0])
		data.append(dat)

canvas = tkinter.Canvas(window, width=display_size[0], height=display_size[1])
canvas.pack()

def classify(i):
	x, y = led_pos[i]
	r, g, b = 0, 0, 0
	for start, end in circle_ang_ranges:
		for j in range(circle_divs):
			rad = j * (end - start) / (circle_divs - 1) + start
			xx = x + led_size / 2 * cos(rad)
			yy = y + led_size / 2 * sin(rad)
			pr, pg, pb = image.getpixel((xx, yy))
			r += pr
			g += pg
			b += pb

	r /= circle_divs * 255
	g /= circle_divs * 255
	b /= circle_divs * 255

	if min(r, g, b) == max(r, g, b):
		hue = 0 # :(
	elif r == max(r, g, b):
		hue = (g - b) / (max(r, g, b) - min(r, g, b))
	elif g == max(r, g, b):
		hue = 2 + (b - r) / (max(r, g, b) - min(r, g, b))
	else:
		hue = 4 + (r - g) / (max(r, g, b) - min(r, g, b))

	brightness = (r + g + b) / 3 / 256

	hue /= 6
	if hue < 0:
		hue += 1
	hue *= 16

	p = [hue, brightness, r, g, b]
	red, green, blue = r, g, b

	## If you have a classifier you want to test, comment out the following and put it here
	## Default: KNN classifier based on hue ONLY

	# def distfn(p1, p2):
	# 	return min(abs(p1[0] - p2[0]), 16 - abs(p1[0] - p2[0]))

	# dists = [(dat[0], distfn(p, dat[1:])) for dat in data]
	# dists.sort(key=lambda l: l[1])

	# labels = map(lambda dat: dat[0], dists[:k])

	# mp = {}
	# for l in labels:
	# 	if l not in mp:
	# 		mp[l] = 0
	# 	mp[l] += 1

	# answer = -1
	# for j in mp:
	# 	if answer == -1 or mp[j] > mp[answer]:
	# 		answer = j

	## This is the classifier we ended up using, produced by Weka

	if blue <= 0.844118:
		if brightness <= 0.002659:
			if green <= 0.702083:
				answer = 0
			else:
				answer = 3

		else:
			if hue <= 2.435594:
				answer = 1
			else:
				answer = 2


	else:
		if red <= 0.568995:
			if green <= 0.784926:
				answer = 5
			else:
				answer = 4

		else:
			if green <= 0.703431:
				answer = 6
			else:
				answer = 7


	## End of classifier

	params[i] = p
	values[i] = answer

def click(event):
	global led_pos
	led_pos.append((event.x, event.y))
	print(led_pos)
	params.append((0, 0))
	values.append(0)
	classify(len(led_pos) - 1)
	update()

def donext():
	## Loads the next image; you'll probably want to replace the path here
	global current_index, img, image, image_tk
	path = os.path.abspath("out/img%06d.jpg"%current_index)
	print("Doing", path)
	image = Image.open(path)
	image = image.resize((720, 405))

	for i in range(len(led_pos)):
		classify(i)

	if img is not None:
		canvas.delete(img)

	image_tk = ImageTk.PhotoImage(image)
	img = canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)
	update()

def left(event):
	global select_idx
	if len(led_pos) > 0:
		select_idx += len(led_pos) - 1
		select_idx %= len(led_pos)
		update()

def right(event):
	global select_idx
	if len(led_pos) > 0:
		select_idx += 1
		select_idx %= len(led_pos)
		update()

def up(event):
	values[select_idx] += 1
	values[select_idx] %= palette_size
	update()

def down(event):
	values[select_idx] += palette_size - 1
	values[select_idx] %= palette_size
	update()

def enter(event):
	global items, waiting
	items += [ canvas.create_text(100, 20, font="Roboto 12 bold", fill="red", text="Waiting...") ]
	with open("data.csv", "a") as datafile:
		for i in range(len(led_pos)):
			datafile.write("%d, %s\n"%(values[i], ", ".join(str(j) for j in params[i])))
			p = [values[i]] + params[i]
			data.append(p)
	donext()

def skip(event):
	global items, waiting
	items += [ canvas.create_text(100, 20, font="Roboto 12 bold", fill="red", text="Waiting...") ]
	donext()

def delete(event):
	global led_pos, all_pts, values, select_idx, params
	if len(led_pos) > 0:
		led_pos = led_pos[:-1]
		values = values[:-1]
		params = params[:-1]
		all_pts = []
		if select_idx >= len(led_pos):
			select_idx = 0
		update()

def update():
	global items

	for item in items:
		canvas.delete(item)

	items = []

	for i in range(len(led_pos)):
		x, y = led_pos[i]
		color = "#0066ff" if i == select_idx else "red"
		items += [
			canvas.create_line(x - 6, y, x - 2, y, fill=color),
			canvas.create_line(x + 2, y, x + 6, y, fill=color),

			canvas.create_line(x, y - 6, x, y - 2, fill=color),
			canvas.create_line(x, y + 2, x, y + 6, fill=color),
			canvas.create_oval(x - led_size / 2, y - led_size / 2, x + led_size / 2, y + led_size / 2, outline=color),

			canvas.create_text(x, y - 14, font="Roboto 12 bold", fill=color, text=str(i + 1)),
			canvas.create_text(x, y + 16, font="Roboto 12 bold", fill=color, text=hex(values[i])[2:])
		]

training_mode = len(argv) < 2 or argv[1] == "train"
current_index = 301

last = [0 for i in range(len(led_pos))]

if training_mode:
	canvas.bind("<Button-1>", click)
	window.bind("<BackSpace>", delete)
	window.bind("<Left>", left)
	window.bind("<Right>", right)
	window.bind("<Up>", up)
	window.bind("<Down>", down)
	window.bind("<Return>", enter)
	window.bind("<`>", enter)
	donext()
	tkinter.mainloop()
else:
	# You may need to replace what's here depending on the problem setup
	# Here we wait for a change and then take a data snapshot two frames later
	# (to give the video brightness a bit of time to stabilize)
	files = os.listdir("out")
	files.sort()
	key = []
	timer = -1
	for file in files[133:]:
		pth = os.path.join("out", file)
		image = Image.open(pth)
		image = image.resize(display_size)
		for i in range(len(led_pos)):
			classify(i)
		match_count = 0

		for i in range(len(led_pos)):
			if last[i] == values[i]:
				match_count += 1

		if match_count < 0.5 * len(led_pos):
			if timer <= 0:
				timer = 2

		timer -= 1

		if timer == 0:
			last = values[:]
			print(values, ",  #", file)
