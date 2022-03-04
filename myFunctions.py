import random
import time
import json
import glob
from PIL import Image
from pathlib import Path


def shuffle(arr):
    return random.shuffle(arr)


def store_directory(path):
    if path != "":

        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            paths = data['paths']
            print("path to append", path)
            paths.append(path)

            json_file.close()
            
            newpath = {"paths": paths} 
            with open('data.json', 'w') as json_file:
                json.dump(newpath, json_file)

def remove_directory(path_to_remove):
    with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            paths = data['paths']
            print("remove", path_to_remove)
            paths.remove(path_to_remove)

            json_file.close()
            
            newpath = {"paths": paths} 
            with open('data.json', 'w') as json_file:
                json.dump(newpath, json_file)
    #using path get files from directory
def get_files(path, extensions, files_grabbed_list):
    for ext in extensions:
        files_grabbed_list.extend(Path(path).glob(ext))
    return files_grabbed_list



    #preserve aspect ration and resize
    
def resize_aspect_image(img, mywidth, myheight):
    #if myheight < mywidth:

    wpercent = (mywidth/float(img.size[0]))
    hpercent = (myheight/float(img.size[1]))

    wsize  = int((float(img.size[0])*float(hpercent)))
    hsize = int((float(img.size[1])*float(wpercent)))

    if wsize >= hsize:
        img = img.resize((mywidth,hsize), Image.ANTIALIAS)
    else:
        img = img.resize((wsize,myheight), Image.ANTIALIAS)
        #if width exceeds container, resize smaller
    return img



def shorten_path(file_paths, length):
    intermediate = []
    for path in file_paths:
        intermediate.append(Path(*Path(path).parts[-length:]))
    return intermediate