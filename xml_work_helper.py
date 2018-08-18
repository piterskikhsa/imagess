import os 
import json 
import re


def write_to_json_file(json_file):
    with open('data.json', 'w') as outfile:
        json_file['elements'] = len(json_file['data']) 
        json.dump(json_file, outfile, indent=4)


def update_xml_files():
    with open('data.json', 'r') as file:
        rename_image = json.load(file)
        if rename_image['elements'] == 0:
            raise ValueError('Error - no elements')

    for d, dirs, files in os.walk('../articles/'):
        for file_name in files:
            with open(d + '/' + file_name, 'r', encoding='utf-8') as readfile:
                readfile = readfile.read()
                for item, value in rename_image['data'].items():
                    if item == 'elements':
                        continue
                    template_string = r'%s\S%s' % (value[-1], item) 
                    replace_string = r'%s\\%s' % (value[-1], value[0])
                    readfile = re.sub(template_string, replace_string, readfile)
                        
            file = open(d + '/' + file_name, 'w', encoding='utf-8')
            file.write(readfile)

    write_to_json_file(rename_image)