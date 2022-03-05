#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 10:43:53 2022

@author: danielschliesing
"""

from cgitb import grey
from textwrap import fill
import tkinter as tk
from tkinter import BOTH, CENTER, LEFT, RIGHT, TOP, SINGLE, StringVar, filedialog, Canvas, font
from turtle import bgcolor
from PIL import Image, ImageTk, ImageOps
import json
import glob
from pathlib import Path
from myFunctions import *
import os
import time





window = tk.Tk()
window.geometry("1000x750")
window['background']='#050203'
window.title("Sketch Ref")

current_image_index = 0
files_grabbed = []
fr_image = tk.Frame(window, bg="#050203" )
fr_buttons = tk.Frame(window, bg="#2A2B2E")
fr_ppn = tk.Frame(fr_buttons, bg="#2A2B2E")
wWidth = 800#window.winfo_width
wHeight = 750#window.winfo_height only works on 'command' ie after intitial window loop
timer_time = "0:00:00"
timer_actual = 0 #in minutes
time_chosen = 0
play = False
options_list = ["Class Mode", "1 H", "30 M",
                 "10 M", "5 M", "1 M", "30 S", "10 S"]
directory_list = []
value_inside = StringVar(window)
value_inside.set("Select a Timer")
directory_value = StringVar(window)
selected_time = 0
files_grabbed = []

#store path


def select_folder(files):
    global files_grabbed
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
    
    for x in data['paths']:
        directory_list.append(x)

    path = data['paths'][0]

if path == "":
    print("please pick a folder with reference pictures in it ", path)
else:
    files_grabbed = get_files(path,('*.jpg', '*.png', '*.jpeg'))

#get image
if files_grabbed: #returns true
    image = Image.open(files_grabbed[current_image_index])
else:
    image = Image.open("Answered-Prayers-Modern-Horizons.webp")


image_resized = resize_aspect_image(image, wWidth, wHeight)
test = ImageTk.PhotoImage(image_resized)

imageLabel = tk.Label(fr_image, image=test, bg= "#050203")
imageLabel.image = test
#copy_of_image = image.copy()

#imageLabel.grid(row=0, column=0, padx=20)
imageLabel.config(anchor=CENTER)
imageLabel.pack()


directory_value.set(Path(*Path(path).parts[-2:]))


fr_image.pack(side=LEFT, expand=True)

def update_image(index = 0):
    global current_image_index
    global files_grabbed
    
    if index == 2:
        if current_image_index == len(files_grabbed) - 1:
            current_image_index = 0
        else:
            current_image_index += 1
    elif index == 1:
        if current_image_index <= 0:
            current_image_index = len(files_grabbed) - 1
        else: 
            current_image_index -= 1
    elif index == 0:
        current_image_index = 0

    print("current index: ", current_image_index)

    nimg = Image.open(files_grabbed[current_image_index])
    #copy_of_image = nimg
    newImage = ImageTk.PhotoImage(resize_aspect_image(nimg, wWidth, wHeight))
    imageLabel.configure(image=newImage)
    imageLabel.image = newImage


def change_directory(event):
    global files_grabbed
    global path
    global directory_list
    #set currently selected path in json
    #change path var

    path = str(event)
    fullpath = [string for string in directory_list if path in string]
    fullpath = fullpath[0]
    #get images
    files_grabbed = get_files(fullpath,('*.jpg', '*.png', '*.jpeg'))
    print(files_grabbed)
    #set current img index to 0
    #change images and reconfigure
    update_image()

###Play/pause next and previous
def set_currently_selected_path():
    print('sdf')

def update_btn_text():
    global play
    if(play_pause["text"]==">"):
        play = True
        countdowntimer()
        play_pause.configure(text="||")

        #pause timer
    else:
        play = False
        play_pause.configure(text=">")
        countdowntimer()
        #play timer

def countdowntimer():
    global timer_actual
    global time_chosen
    global play

    if not time_chosen:
        #if unchosen time and pres pause/play do nothing
        return
    elif not timer_actual:
        print("end")
        timer_actual = time_chosen
        play = True
        update_image(True)
        countdowntimer()
    elif timer_actual and play:
        print("seconds", timer_actual)
        timer_text = str(timer_actual) + "s"
        timer_label.configure(text=timer_text)
        timer_actual -= 1

        window.after(1000, countdowntimer)
    elif not play and timer_actual:
        #paused
        return

timer_label = tk.Label(fr_buttons, text=timer_time, font=("Times","20"), bg="#2A2B2E", fg="white")

def option_changed(self):
    x = value_inside.get()
    global timer_actual
    global timer_label
    global time_chosen
    if x == "Class Mode":
        #[0.5,0.5,0.5,0.5,0.5,0.5,0,5,0,5,1,1,1,1,1,5,5,10,30]  
        print("do class mode")
    elif x == "1 H":
        timer_label.configure(text="1:00:00")
        timer_actual = 3600
        time_chosen = timer_actual
    elif x ==  "30 M":
        timer_label.configure(text="30:00")
        timer_actual = 1800
        time_chosen = timer_actual
    elif x ==  "10 M":
        timer_label.configure(text="10:00")
        timer_actual = 600
        time_chosen = timer_actual
    elif x ==  "5 M":
        timer_label.configure(text="05:00")
        timer_actual = 300
        time_chosen = timer_actual
    elif x == "1 M":
        timer_label.configure(text="01:00")
        timer_actual= 60
        time_chosen = timer_actual
    elif x == "30 S":
        timer_label.configure(text="00:30")
        timer_actual = 30
        time_chosen = timer_actual
    elif x == "10 S":
        timer_label.configure(text="00:10")
        timer_actual = 10
        time_chosen = timer_actual
    print("Selected Option: {}".format(value_inside.get()))


def shuffle():
    global files_grabbed 
    random.shuffle(files_grabbed)
    update_image()

############### Menu frame

titleFont = ("Times", "24", "bold italic")
user_directories =  os.path.basename(os.path.normpath(path))

#example        frame window, label text,   button dimensions, command=anonymous function
title = tk.Label(fr_buttons, text="/"+user_directories, font=titleFont, bg="#2A2B2E", fg="white")
timer_picker_menu = tk.OptionMenu(fr_buttons, value_inside, *options_list, command= option_changed)
shuffle_button = tk.Button(fr_ppn, text="~~", command=lambda: shuffle(), bg="#2A2B2E")
play_pause = tk.Button(fr_ppn, text=">", width="2", command= lambda: update_btn_text(), bg="#2A2B2E")
prev = tk.Button(fr_ppn, text="<<", command=lambda: update_image(1), bg="#2A2B2E")
next = tk.Button(fr_ppn, text=">>", command=lambda: update_image(2), bg="#2A2B2E")
browser_button = tk.Button(fr_buttons, text="browse", command=lambda: select_folder(files_grabbed), bg="#2A2B2E")
directory_box = tk.OptionMenu(fr_buttons, directory_value, *shorten_path(directory_list, 2), command=change_directory)

title.pack(side=TOP, fill=BOTH)
timer_label.pack(side=TOP, fill=BOTH)
shuffle_button.pack(side=TOP)
prev.pack(side=LEFT)
next.pack(side=RIGHT)
play_pause.pack(side=RIGHT, fill=BOTH)
fr_ppn.pack(fill=BOTH)
timer_picker_menu.pack(side=TOP, fill=BOTH)
directory_box.pack(side=TOP, fill=BOTH)
browser_button.pack(side=TOP, fill=BOTH)


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

#def resize_image(event):
#    new_width = event.width
#    new_height = event.height
#    image = copy_of_image.resize((new_width, new_height))
#    newImage = ImageTk.PhotoImage(resize_aspect_image(image, new_width, new_height))
#    imageLabel.configure(image=newImage)
#    imageLabel.image = newImage

#imageLabel.bind('<Configure>', resize_image)#resize with window movement