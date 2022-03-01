#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 10:43:53 2022

@author: danielschliesing
"""

import tkinter as tk
from tkinter import LEFT, RIGHT, filedialog, Canvas
from PIL import Image, ImageTk, ImageOps
import json
import glob
from pathlib import Path
from myFunctions import *


current_image_index = 0
files_grabbed = []

window = tk.Tk()
window.geometry("1000x750")

#wHeight = window.winfo_height
#wWidth = window.winfo_width

#store path


def select_folder():
    path = filedialog.askdirectory()
    print(path)
    store_directory(path)
     # the tuple of file types
    files_grabbed = get_files(path,('*.jpg', '*.png', '*.jpeg'),files_grabbed)


###json
#if json folder directory is not empty, grab img from path and display

##load, if empty do x
with open('data.json', 'r') as f:
    data = json.load(f)
    path = data['path']

if path == "":
    print("json path empty ", path)
else:
    files_grabbed = get_files(path,('*.jpg', '*.png', '*.jpeg'),files_grabbed)

#get image
if files_grabbed: #returns true
    image = Image.open(files_grabbed[current_image_index])
else:
    image = Image.open("Answered-Prayers-Modern-Horizons.webp")


image_resized = resize_aspect_image(image, 512)
test = ImageTk.PhotoImage(image_resized)

imageLabel = tk.Label(image=test)
imageLabel.image = test
imageLabel.grid(column=0, row=0)

def update_image(index):
    global current_image_index
    if index:
        current_image_index += 1
    else:
        current_image_index -= 1

    if current_image_index <= 0 and not index:
        current_image_index = len(files_grabbed)-1
    elif current_image_index == len(files_grabbed) - 1 and index:
        current_image_index = 0
    
    print("current index: ", current_image_index)

    nimg = Image.open(files_grabbed[current_image_index])
    newImage = ImageTk.PhotoImage(resize_aspect_image(nimg, 512))
    imageLabel.configure(image=newImage)
    imageLabel.image = newImage

###Play/pause next and previous

def update_btn_text():
    if(play_pause["text"]=="play"):
        play_pause.configure(text="pause")
        #pause timer
    else:
        play_pause.configure(text="play")
        #play timer


############### Menu frame

timer = tk.Label(text="1:20...", width="5",height="1")
remaining = tk.Label(text="2/20", width="5",height="1")
play_pause = tk.Button(window, text="play", command= lambda: update_btn_text())
prev = tk.Button(text="prev", width="5",height="1", command=lambda: update_image(False))
next = tk.Button(text="next", width="5",height="1", command=lambda: update_image(True))
browserButton = tk.Button(text="browse", width="5",height="1", command=lambda: select_folder)

timer.grid
remaining.grid
play_pause.grid(column=0,row=1)
prev.grid
next.grid
browserButton.grid




#####


window.mainloop() 