#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from PIL import Image

try:
	directory = sys.argv[1]
except Exception as e:
	raise
else:
	pass
finally:
	pass

def find_zero(tuple):
	for _ in tuple:
		if len(_)>3 and _[3]==0:
			return True
		else:
			continue
	return False

os.chdir(directory)
path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
for file_name in os.listdir(os.getcwd()):
	file, ext = os.path.splitext(file_name)
	format_file = "JPEG"
	outfile = directory + "\\images\\" + file

	try:
		im = Image.open(file_name)
		
		if ext in (".tif", ".png"):
			out = im.convert("RGBA")
			pix_data = im.load()
			pixels = ((0,0),(0, im.size[1]-1),(im.size[0]-1,im.size[1]-1),(im.size[0]-1, 0))
			background_color =	tuple(pix_data[pix] for pix in pixels)
			
			if find_zero(background_color):
				outfile = outfile + ".png"
				im.save(outfile, "PNG")
				print file_name  + u"--------- ОК"
			else:
				out = im.convert("RGB")
				print out.format
				out.save(outfile, format_file, quality=60)
				print file_name  + u"--------- ОК"
		else: 
			out = im
			print out.format
			out.save(outfile, format_file, quality=60)
			print file_name  + u"--------- ОК"
	except Exception as e:
		print file_name, e
		
