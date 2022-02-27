#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 10:43:53 2022

@author: danielschliesing
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageOps

window = tk.Tk()

window.geometry("750x500")

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
    if(btn["text"]=="a"):
        btn.configure(text="b")
    else:
        btn.configure(text="a")
btn = tk.Button(window, text="a", command=update_btn_text)
btn.pack()

play = tk.Button(text="play", width="5",height="1")
play.pack()

prev = tk.Button(text="prev", width="5",height="1")
prev.pack()

next = tk.Button(text="next", width="5",height="1")
next.pack()

browserButton = tk.Button(text="browse", width="5",height="1")
browserButton.pack()


#####


window.mainloop() 