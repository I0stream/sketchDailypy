#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 10:43:53 2022

@author: danielschliesing
"""

from cgitb import grey
from textwrap import fill
import tkinter as tk
from tkinter import BOTH, CENTER, LEFT, RIGHT, TOP, SINGLE, StringVar, filedialog, Canvas
from turtle import bgcolor
from PIL import Image, ImageTk, ImageOps
import json
import glob
from pathlib import Path
from myFunctions import *
import os


current_image_index = 0
files_grabbed = []

window = tk.Tk()
window.geometry("1000x750")
window['background']='#2A2B2E'

#remove title bar completely
#window.overrideredirect(1)
#window.overrideredirect(0)

window.rowconfigure(4, minsize=2, weight=1)
window.columnconfigure(2, minsize=200, weight=1)
window.columnconfigure(1, minsize=200, weight=1)

fr_image = tk.Frame(window, bg="#2A2B2E" )
fr_buttons = tk.Frame(window, bg="grey")
fr_ppn = tk.Frame(fr_buttons, bg="#2A2B2E")

wWidth = 800#window.winfo_width
wHeight = 750#window.winfo_height only works on 'command' ie after intitial window loop

timer_time = StringVar()
timer_time.set("0:00:00")

options_list = ["Class Mode", "1 H", "30 M",
                 "10 M", "5 M", "1 M", "30 S", "Custom"]

directory_list = []
value_inside = StringVar(window)
value_inside.set("Select a Timer")


directory_value = StringVar(window)
directory_value.set("directory")
selected_time = 0

#store path


def select_folder(files):
    path = filedialog.askdirectory()
    print(path)
    store_directory(path)
     # the tuple of file types
    files_grabbed = get_files(path,('*.jpg', '*.png', '*.jpeg'),[])




###json
#if json folder directory is not empty, grab img from path and display

##load, if empty do x
with open('data.json', 'r') as f:
    data = json.load(f)
    
    for x in data['paths']:
        directory_list.append(x)

    path = data['paths'][0]

if path == "":
    print("please pick a folder with reference pictures in it ", path)
else:
    files_grabbed = get_files(path,('*.jpg', '*.png', '*.jpeg'),files_grabbed)

#get image
if files_grabbed: #returns true
    image = Image.open(files_grabbed[current_image_index])
else:
    image = Image.open("Answered-Prayers-Modern-Horizons.webp")


image_resized = resize_aspect_image(image, wWidth, wHeight)
test = ImageTk.PhotoImage(image_resized)

imageLabel = tk.Label(fr_image, image=test, bg= "#2A2B2E")
imageLabel.image = test
#imageLabel.grid(row=0, column=0, padx=20)
imageLabel.config(anchor=CENTER)
imageLabel.pack()

fr_image.pack(side=LEFT, expand=True)

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
    newImage = ImageTk.PhotoImage(resize_aspect_image(nimg, wWidth, wHeight))
    imageLabel.configure(image=newImage)
    imageLabel.image = newImage

def change_directory():
    print("ligma")
    #set currently selected path in json
    #change path var
    #set current img index to 0
    #change images and reconfigure

###Play/pause next and previous

def update_btn_text():
    if(play_pause["text"]==">"):
        play_pause.configure(text="||")
        #pause timer
    else:
        play_pause.configure(text=">")
        #play timer

def countdowntimer(t):
    while t:
        mins, sec = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins,sec)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
        

def print_answers():
    x = value_inside.get()
    if x == "Class Mode":
        return [0.5,0.5,0.5,0.5,0.5,0.5,0,5,0,5,1,1,1,1,1,5,5,10,30]  
    elif x == "1 H":
        return 60
    elif x ==  "30 M":
        return 30
    elif x ==  "10 M":
        return 10
    elif x ==  "5 M": 
        return 5
    elif x == "1 M":
        return 1
    elif x == "30 S": 
        return 0.5
    elif x == "Custom":
        custom()
        return None
    print("Selected Option: {}".format(value_inside.get()))
    return None

def custom():
    print("bring up a menu to enter repeated times")

user_directories = tk.StringVar(value = os.path.basename(os.path.normpath(path)))

############### Menu frame
#example        frame window, label text,   button dimensions, command=anonymous function
timer = tk.Label(fr_buttons, textvariable=timer_time, width="5",height="1")
#remaining = tk.Label(fr_buttons, text="2/20", width="5",height="1")
timer_picker_menu = tk.OptionMenu(fr_buttons, value_inside, *options_list)
play_pause = tk.Button(fr_ppn, text=">", command= lambda: update_btn_text())
prev = tk.Button(fr_ppn, text="<<", command=lambda: update_image(False))
next = tk.Button(fr_ppn, text=">>", command=lambda: update_image(True))
browser_button = tk.Button(fr_buttons, text="browse", width="5",height="1", command=lambda: select_folder(files_grabbed))
directory_box = tk.OptionMenu(fr_buttons, directory_value, *directory_list)

#timer.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
#remaining.grid(row=1, column=1, columnspan=2, padx=5)
#play_pause.grid(row=2, column=1, columnspan=2, padx=5)
#prev.grid(row=3, column=1)
#next.grid(row=3, column=2)
#browserButton.grid(row=4, column=1, columnspan=2, padx=5)

#fr_buttons.grid(row=0,column=1, sticky= "e")

timer.pack(side=TOP)
#remaining.pack(side=TOP)
prev.pack(side=LEFT)
next.pack(side=RIGHT)
play_pause.pack(side=RIGHT)
fr_ppn.pack()
timer_picker_menu.pack(side=TOP)
browser_button.pack(side=TOP)
directory_box.pack(side=TOP)

fr_buttons.pack(side=RIGHT, fill=BOTH)

#####key binds
def leftKey(event):
    update_image(False)

def rightKey(event):
    update_image(True)

def spaceBar(event):
    print("pause space press")

window.bind('<Left>', leftKey)
window.bind('<Right>', rightKey)
window.bind('<space>', spaceBar)


window.mainloop() 