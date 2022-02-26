#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 10:43:53 2022

@author: danielschliesing
"""

#gui tests
import tkinter as tk

window = tk.Tk()

browserButton = tk.Button(text="open browser", width="25",height="5", background="blue", fg="red")
browserButton.pack()


window.mainloop() 