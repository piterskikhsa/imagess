#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, json, re
from PIL import Image
from iter import find_zero


image_name_dict = {'count':0, 'data':{}}


def save_image_png(file_image, out_file_name, ext):
    out_file = out_file_name + ext
    if ext in (".png",):
        file_image = file_image.convert('RGBA', palette=Image.WEB)
        file_image.save(out_file, "PNG", optimize=True, quality=100)
    print(out_file_name + u"--------- ОК")


def save_image_jpeg(file_image, out_file_name, ext, file_name):
    name = file_name.split('\\')[-1].decode('utf8')
    print(name)
    file_directory = file_name.split('\\')[-2].decode('utf8')
    out_file = out_file_name + '.jpg'
    image_name_dict['count'] += 1
    image_name_dict['data'][name] = [name[:-4] + '.jpg', 0]
    image_name_dict['data'][name].append(file_directory)
    if file_image.mode in ('RGBA', 'P'):
        file_image = file_image.convert("RGB")
    file_image.save(out_file, "JPEG", optimize=True, quality=75)
    print(out_file_name + u"--------- ОК")


def change_ext_image(im, ext):
    if ext in (".tif", ".png"):
        out = im.convert("RGBA")
        pix_data = out.load()
        pixels = ((0, 0), (0, im.size[1] - 1), (im.size[0] - 1, im.size[1] - 1), (im.size[0] - 1, 0))
        background_color = tuple(pix_data[pix] for pix in pixels)

        if find_zero(background_color):
            return True
        else:
            return False
    else:
        return False


def update_image(file_name, out_file_name, ext):
    try:
        im = Image.open(file_name)

        if change_ext_image(im, ext):
            save_image_png(im, out_file_name, ext)
        else:
            save_image_jpeg(im, out_file_name, ext, file_name)
    except Exception as e:
        print(file_name, e)


def main(path):
    for d, dirs, files in os.walk(path):
        for file_name in files:
            file_directory = d.split('images')[-1].strip('\\')
            file, ext = os.path.splitext(file_name)
            base_directory = path + "\\images\\" + str(file_directory)
            if not os.path.exists(base_directory):
                os.makedirs(base_directory)
            outfile = base_directory + "\\" + file
            file_name = os.path.join(d, file_name)
            if file in ("title", "title_thumb"):
                # save_image(file_name, outfile, ext)
                continue
            if ext in (".tif", ".png", '.jpg'):
                update_image(file_name, outfile, ext)


def write_to_json_file(json_file):
    with open('data.json', 'w') as outfile:
        json_file['elements'] = len(json_file['data']) 
        json.dump(json_file, outfile, indent=4)


if __name__ == "__main__":
    try:
        directory = sys.argv[1]
    except Exception as e:
        raise
    else:
        pass
    finally:
        pass

    os.chdir(directory)

    path = os.getcwd()

    # main(path)

    # write_to_json_file(image_name_dict)
    
    if os.path.exists('data.json'):
        with open('data.json', 'r') as file:
            rename_image = json.load(file)

            print(json.dumps(rename_image, sort_keys=True, indent=4))


        for d, dirs, files in os.walk('../articles/'):
            for file_name in files:
                print(d)
                with open(d + '/' + file_name, 'r') as readfile:
                    readfile = readfile.read()
                    for item, value in rename_image['data'].items():
                        if item == 'elements':
                            continue
                        find_string = re.search(item, readfile)
                        if find_string:
                            rename_image['data'][item][1] += 1
                        readfile = re.sub(item.decode('utf8'), value[0].decode('utf8'), readfile)
                        print('+')
                file = open(d + '/' + file_name, 'w')
                file.write(readfile)

        write_to_json_file(rename_image)