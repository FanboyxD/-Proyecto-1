#importar la libreria tkinter
from tkinter import *
import random
import tkinter.font
import tkinter.messagebox

#Crear la ventana, su nombre e icono
root = Tk()
root.wm_title("Space Invaders")
root.iconbitmap("SpIn.ico.ico")



#se crean canvas
disp = Canvas(root, width=800, height=800, bg="black")

disp.grid(row=0, column=0)
root.mainloop()
shots = []
enemyProjectiles = []
aliens = []
explosions = []
opAttack = False
otherOPAttack = False
wavesSurvived = 0
dead = False
hardMode = False
gOver = tkinter.font.Font(family="Chiller", size=30, weight="bold")
otherFont = tkinter.font.Font(family="OCR-A II", size=20)
menuFont = tkinter.font.Font(family="Fixedsys", size=30)
gameState = 0
cheatCode = ""
