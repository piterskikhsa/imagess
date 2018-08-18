import os
import sys

from PIL import Image

from iter import find_zero
from xml_work_helper import update_xml_files, write_to_json_file


def save_image_png(file_image, out_file_name, ext):
    out_file = out_file_name + ext
    if ext in (".png",):
        file_image = file_image.convert('RGBA', palette=Image.WEB)
        file_image.save(out_file, "PNG", optimize=True, quality=100)
    print(out_file_name + "--------- ОК")


def update_image_name_dict(image_name_dict, name, file_directory):
    image_name_dict['count'] += 1
    image_name_dict['data'][name] = [name[:-4] + '.jpg', 0]
    image_name_dict['data'][name].append(file_directory)


def save_image_jpeg(file_image, out_file_name, ext, file_name, name_dict):
    name = file_name.split('\\')[-1]
    file_directory = file_name.split('\\')[-2]
    out_file = out_file_name + '.jpg'
    update_image_name_dict(name_dict, name, file_directory)
    if file_image.mode in ('RGBA', 'P'):
        background_color = (255, 255, 255)
        background_image = Image.new(file_image.mode[:-1], file_image.size, background_color)
        background_image.paste(file_image, file_image.split()[-1])
        file_image = background_image.convert("RGB")

    if file_image.size[0] > 1300:
        base_width = 1300
        wpercent = (base_width/float(file_image.size[0]))
        h_size = int((float(file_image.size[1])*float(wpercent)))
        file_image = file_image.resize((base_width,h_size), Image.ANTIALIAS)    
    
    file_image.save(out_file, "JPEG", optimize=True, quality=60)
    print(out_file_name + "--------- ОК")


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
    pass


def main(path):
    image_name_dict = {'count':0, 'data':{}}

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
            if ext in (".tif", ".png", '.jpg', '.jpeg'):
                try:
                    im = Image.open(file_name)

                    # if change_ext_image(im, ext):
                    #     save_image_png(im, outfile, ext)
                    # else:
                    save_image_jpeg(im, outfile, ext, file_name, image_name_dict)
                except Exception as e:
                    print(file_name, e)

    return image_name_dict


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

    if os.path.exists('data.json'):
        update_xml_files()
    else:
        write_to_json_file(main(path))