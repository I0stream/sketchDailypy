import random
import time
import json
import glob
from PIL import Image
from pathlib import Path


def shuffle(arr):
    return random.shuffle(arr)


def countdowntimer(t):
    while t:
        mins, sec = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins,sec)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print("end/next photo")

def store_directory(path):
    if path != "":
        directory_path = {"path": path}
        with open('data.json', 'w') as json_file:
            json.dump(directory_path, json_file)

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
    return img
