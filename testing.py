#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 10:43:53 2022

@author: danielschliesing
"""

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import json
import glob
from pathlib import Path


current_image_index = 0
files_grabbed = []

window = tk.Tk()
window.geometry("1000x750")


#store path
def store_directory(path):
    if path != "":
        directory_path = {"path": path}
        with open('data.json', 'w') as json_file:
            json.dump(directory_path, json_file)

def get_files(path, extensions):
    for ext in extensions:
        files_grabbed.extend(Path(path).glob(ext))
    return files_grabbed

def select_folder():
    path = filedialog.askdirectory()
    print(path)
    store_directory(path)
     # the tuple of file types
    files_grabbed = get_files(path,('*.jpg', '*.png', '*.jpeg'))


###json
#if json folder directory is not empty, grab img from path and display

##load, if empty do x
with open('data.json', 'r') as f:
    data = json.load(f)
    path = data['path']

if path == "":
    print("json path empty ", path)
else:
    files_grabbed = get_files(path,('*.jpg', '*.png', '*.jpeg'))


###image display

image = Image.open(files_grabbed[current_image_index])
image2 = ImageOps.contain(image, (512,512))
test = ImageTk.PhotoImage(image2)

imageLabel = tk.Label(image=test)
imageLabel.image = test
imageLabel.pack()

### menu
timer = tk.Label(text="1:20...", width="5",height="1")
timer.pack()

remaining = tk.Label(text="2/20", width="5",height="1")
remaining.pack()


###Play/pause next and previous

def update_btn_text():
    if(play_pause["text"]=="play"):
        play_pause.configure(text="pause")
    else:
        play_pause.configure(text="play")

play_pause = tk.Button(window, text="play", command=lambda: update_btn_text)
play_pause.pack()



def update_image(index):
    global current_image_index
    if index:
        current_image_index += 1
    else:
        current_image_index -= 1

    if current_image_index <= 0 and not index:
        current_image_index = len(files_grabbed)-1


    newImage = ImageTk.PhotoImage(Image.open(files_grabbed[index]))
    imageLabel.configure(image=newImage2)
    imageLabel.image = newImage




prev = tk.Button(text="prev", width="5",height="1", command=lambda: update_image(False))
prev.pack()

next = tk.Button(text="next", width="5",height="1", command=lambda: update_image(True))
next.pack()



#get directory, and then get files in directory







browserButton = tk.Button(text="browse", width="5",height="1", command=lambda: select_folder)
browserButton.pack()





#####


window.mainloop() 