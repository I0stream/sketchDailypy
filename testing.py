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


current_image_index = 0
def overflow_protect(nexPrev):
    if current_image_index == 0 and nexPrev == -1:
        current_image_index = len(files_grabbed)
    elif current_image_index == len(files_grabbed) and nexPrev == 1:
        current_image_index = 0
    elif nexPrev == -1:
        current_image_index = current_image_index -1
    else:
        current_image_index = current_image_index + 1
    return current_image_index

window = tk.Tk()
window.geometry("750x500")




###json
#if json folder directory is not empty, grab img from path and display

##load, if empty do x
with open('data.json', 'r') as f:
    data = json.load(f)
    print(data)
    path = data['path']

if path == "":
    print("json path empty")
else:
    print("we have a path in json")




#also make an array with all the files in directory

files_grabbed = []
def select_folder():
    path= filedialog.askdirectory()

     # the tuple of file types
    get_files(path)    
    

def get_files(path):
    types = ('{path}/*.jpg', '{path}/*.png', '{path}/*.webp', '{path}/*.jpeg')
    for files in types:
        files_grabbed.extend(glob.glob(files))
    print(files_grabbed)


###image display

image = Image.open("Answered-Prayers-Modern-Horizons.webp")
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


def update_btn_text():
    if(play_pause["text"]=="play"):
        play_pause.configure(text="pause")
    else:
        play_pause.configure(text="play")
play_pause = tk.Button(window, text="play", command=update_btn_text)
play_pause.pack()


def update_image(index):
    newImage = Image.open(files_grabbed[overflow_protect(index)])


prev = tk.Button(text="prev", width="5",height="1", command=update_image(-1))
prev.pack()

next = tk.Button(text="next", width="5",height="1", command=update_image(1))
next.pack()



browserButton = tk.Button(text="browse", width="5",height="1", command= select_folder)
browserButton.pack()


#####


window.mainloop() 