#!/usr/bin/env python3
"""
Created on Sat Feb 26 10:43:53 2022

@author: danielschliesing
"""

from textwrap import fill
import tkinter as tk
from tkinter import BOTH, CENTER, LEFT, RIGHT, TOP, SINGLE, StringVar, filedialog
from turtle import bgcolor
from PIL import Image, ImageTk, ImageOps
import json
from pathlib import Path
from myFunctions import *
import os
import io


#{"paths": ["/Users/danielschliesing/Desktop/portraits", "/Users/danielschliesing/Desktop/ref/Current", "/Users/danielschliesing/Desktop/ref/nekked"], "currently_selected": "/Users/danielschliesing/Desktop/ref/Current"}

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
timer_time = "0:00"
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

json_path = 'data.json'
###json
#if json folder directory is not empty, grab img from path and display

##load
#check if json path empty
#check if paths valid
#then load

def startupCheck():
    global path
    if os.path.isfile(json_path) and os.access(json_path, os.R_OK):
        # checks if file exists
        with open(json_path, 'r') as f:
 
            data = json.load(f)
            
            for x in data['paths']:
                directory_list.append(x)
            
            path = data['currently_selected']
    else:
        print ("Either file is missing or is not readable, creating file...")
        with io.open(os.path.join('data.json'), 'w') as db_file:
            newpath = {"paths": [], "currently_selected": ""}          
            db_file.write(json.dumps(newpath))
        path = ""

startupCheck()




if path == "":
    print("please pick a folder with reference pictures in it ", path)
else:
    files_grabbed = get_files(path,('*.jpg', '*.png', '*.jpeg'))

#get image
if files_grabbed: #returns true
    image = Image.open(files_grabbed[current_image_index])
else:
    image = Image.open("no_pics.png")
    if path != "":
        remove_directory(path)
    


image_resized = resize_aspect_image(image, wWidth, wHeight)
test = ImageTk.PhotoImage(image_resized)
imageLabel = tk.Label(fr_image, image=test, bg= "#050203")
imageLabel.image = test
imageLabel.config(anchor=CENTER)
imageLabel.pack()
fr_image.pack(side=LEFT, expand=True)

directory_value.set(Path(*Path(path).parts[-2:]))

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


    if files_grabbed: #returns true
        nimg = Image.open(files_grabbed[current_image_index])
    
    #copy_of_image = nimg
        newImage = ImageTk.PhotoImage(resize_aspect_image(nimg, wWidth, wHeight))
        imageLabel.configure(image=newImage)
        imageLabel.image = newImage
    else:
        nimg = Image.open("no_pics.png")
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
    if files_grabbed: #returns true
        update_image()
        currently_selected_store(fullpath)
    else:
        directory_list.remove(fullpath)
        remove_directory(fullpath)
        update_image()

###Play/pause next and previous


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
    elif not timer_actual:#timer over
        timer_actual = time_chosen
        play = True
        update_image(True)
        countdowntimer()
    elif timer_actual and play:#timer going
        min = timer_actual // 60
        sec = timer_actual % 60
        timer_text = str(min) + ":" + str(sec)
        timer_label.configure(text=timer_text)
        timer_actual -= 1

        window.after(1000, countdowntimer)
    elif not play and timer_actual:#paused
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

titleFont = ("Times", "24", "bold italic")
user_directories =  os.path.basename(os.path.normpath(path))
title = tk.Label(fr_buttons, text="/"+user_directories, font=titleFont, bg="#2A2B2E", fg="white")

#store path, browser button
def select_folder(files):
    global files_grabbed
    path = filedialog.askdirectory()
    store_directory(path)
     # the tuple of file types
    directory_list.append(path)
    files_grabbed = get_files(path,('*.jpg', '*.png', '*.jpeg'))
    update_image()


############### Menu frame


#example        frame window, label text,   button dimensions, command=anonymous function
timer_picker_menu = tk.OptionMenu(fr_buttons, value_inside, *options_list, command= option_changed)
shuffle_button = tk.Button(fr_ppn, width=3, text="~~", command=lambda: shuffle())
play_pause = tk.Button(fr_ppn, width=3, text=">", command= lambda: update_btn_text(), bg="#2A2B2E")
prev = tk.Button(fr_ppn, text="<<", command=lambda: update_image(1), bg="#2A2B2E")
next = tk.Button(fr_ppn, text=">>", command=lambda: update_image(2), bg="#2A2B2E")
browser_button = tk.Button(fr_buttons, text="browse", command=lambda: select_folder(files_grabbed), bg="#2A2B2E")

if directory_list != []:
    directory_box = tk.OptionMenu(fr_buttons, directory_value, *shorten_path(directory_list, 2), command=change_directory)

title.pack(side=TOP, fill=BOTH)
timer_label.pack(side=TOP, fill=BOTH)
shuffle_button.pack(side=TOP)
prev.pack(side=LEFT)
next.pack(side=RIGHT)
play_pause.pack(side=RIGHT, fill=BOTH)
fr_ppn.pack(fill=BOTH)
timer_picker_menu.pack(side=TOP, fill=BOTH)
if directory_list != []:
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