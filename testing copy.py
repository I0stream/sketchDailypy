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

window.rowconfigure(4, minsize=2, weight=1)
window.columnconfigure(2, minsize=800, weight=1)


fr_buttons = tk.Frame(window)
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
    print("uncomment me")
else:
    image = Image.open("Answered-Prayers-Modern-Horizons.webp")


image_resized = resize_aspect_image(image, 512)
test = ImageTk.PhotoImage(image_resized)

imageLabel = tk.Label(window, image=test)
imageLabel.image = test
imageLabel.grid(row=0, column=0, sticky="nsew")

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
    if(play_pause["text"]==">"):
        play_pause.configure(text="||")
        #pause timer
    else:
        play_pause.configure(text=">")
        #play timer


############### Menu frame
#example        frame window, label text,   button dimensions, command=anonymous function
timer = tk.Label(fr_buttons, text="1:20...", width="5",height="1")
remaining = tk.Label(fr_buttons, text="2/20", width="5",height="1")
play_pause = tk.Button(fr_buttons, text=">", command= lambda: update_btn_text())
prev = tk.Button(fr_buttons, text="<<", width="5",height="1", command=lambda: update_image(False))
next = tk.Button(fr_buttons, text=">>", width="5",height="1", command=lambda: update_image(True))
browserButton = tk.Button(fr_buttons, text="browse", width="5",height="1", command=lambda: select_folder)

timer.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
remaining.grid(row=1, column=1, columnspan=2, padx=5)
play_pause.grid(row=2, column=1, columnspan=2, padx=5)
prev.grid(row=3, column=1)
next.grid(row=3, column=2)
browserButton.grid(row=4, column=1, columnspan=2, padx=5)

fr_buttons.grid(row=0,column=1)


#####


window.mainloop() 