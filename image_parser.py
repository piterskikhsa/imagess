#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from PIL import Image
from iter import find_zero


def save_image(file_image, out_file_name, ext):
    out_file = out_file_name + "." + ext
    if ext=="PNG":
        file_image.save(out_file, ext, optimize=True )
    elif ext=="JPEG":
        out = file_image.convert("RGB")
        out.save(out_file, ext, quality=75)

    print(file_name + u"--------- ОК")


def update_image(file_name, out_file_name):
    try:
        im = Image.open(file_name)

        if ext in (".tif", ".png"):
            out = im.convert("RGBA")
            pix_data = out.load()
            pixels = ((0, 0), (0, im.size[1] - 1), (im.size[0] - 1, im.size[1] - 1), (im.size[0] - 1, 0))
            background_color = tuple(pix_data[pix] for pix in pixels)

            if find_zero(background_color):
                save_image(out, out_file_name, "PNG")
            else:
                save_image(out, out_file_name, "JPEG")
        else:
            save_image(im, out_file_name, "JPEG")

    except Exception as e:
        print(file_name, e)


try:
    directory = sys.argv[1]
except Exception as e:
    raise
else:
    pass
finally:
    pass

os.chdir(directory)
path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

for file_name in os.listdir(os.getcwd()):
    file, ext = os.path.splitext(file_name)
    outfile = directory + "\\images\\" + file
    update_image(file_name, outfile)