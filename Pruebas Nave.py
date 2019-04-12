# Import tkinter library.
from tkinter import *
import random
import tkinter.font
import tkinter.messagebox
#import os
# Create window, window title, and icon.
root = Tk()
root.wm_title("Space Invaders NEO")
root.iconbitmap("SpIn.ico.ico")
# Create menu with "File" submenu and "Quit" Button.
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Quit", command=quit)
menubar.add_cascade(label="File", underline=0, menu=filemenu)
root.config(menu=menubar)
# Create canvas.
disp = Canvas(root, width=800, height=800, bg="black")
disp.grid(row=0, column=0)
opAttack = False
otherOPAttack = False
gOver = tkinter.font.Font(family="Chiller", size=30, weight="bold")
otherFont = tkinter.font.Font(family="OCR-A II", size=20)
menuFont = tkinter.font.Font(family="Fixedsys", size=30)
gameState = 0
cheatCode = ""
root.mainloop()
