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
gOver = tkinter.font.Font(family="Chiller", size=30, weight="bold")
otherFont = tkinter.font.Font(family="OCR-A II", size=20)
menuFont = tkinter.font.Font(family="Fixedsys", size=30)
class player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprites = [PhotoImage(file="ship.gif"),
                        PhotoImage(file="ship.gif")]
        self.timer = 0
        self.tPeriod = 0
        self.period = 1
        self.left = False
        self.right = False
        self.hp = 1
        self.autofire = False
        disp.bind("<Left>", self.moveLeft)
        disp.bind("<Right>", self.moveRight)
        disp.bind("<KeyRelease-Left>", self.stopLeft)
        disp.bind("<KeyRelease-Right>", self.stopRight)
        disp.bind("<Up>", self.moveUp)
        disp.bind("<Down>", self.moveDown)
        disp.bind("<KeyRelease-Up>", self.stopUp)
        disp.bind("<KeyRelease-Down>", self.stopDown)
        disp.bind("<KeyRelease-space>", self.spawnBullet)
        disp.bind("<KeyRelease-Shift_L>", self.toggleAutoFire)
        disp.bind("<Up>", self.moveUp)
        disp.bind("<Down>", self.moveDown)
    def draw(self):
        disp.create_image(self.x, self.y,
                          image=self.sprites[self.tPeriod],
                          anchor=NW)
        self.timer += 1
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= len(self.sprites)
        disp.create_text(self.x + 25, self.y - 20, text="HP: " + str(self.hp),
                         fill="white", font=otherFont)
    def update(self):
        global dead
        if self.hp > 0:
            if self.left and self.x >= 0:
                self.x -= 10
            if self.x < 0:
                self.x = 0
            if self.right and self.x + 50 <= disp.winfo_width():
                self.x += 10
            if self.x + 50 > disp.winfo_width():
                self.x = disp.winfo_width() - 50
            self.draw()
            if self.tPeriod == 1 and self.timer == 1 and self.autofire:
                self.spawnBullet(False)
        else:
            dead = True
        for i in aliens:
            if i.x + 50 >= self.x and i.x <= self.x + 50 and i.y + 50 >= self.y \
                and i.y <= self.y + 50:
                self.hp = -1
        for j in enemyProjectiles:
            if j.x + 15 >= self.x and j.x <= self.x + 50 and j.y + 25 >= self.y \
                and j.y <= self.y + 50:
                self.hp -= 1
                j.dead = True
                if self.hp > 0:
                    j.yVel *= -1.25
                    j.y -= 50
                if self.hp > -1:
                    explosions.append(explosion(j.x + 7.5, self.y))
    def moveLeft(self, event):
        self.left = True
    def moveRight(self, event):
        self.right = True
    def moveUp(self, event):
        self.up = True
    def moveDown(self, event):
        self.down = True
    def stopUp(self, event):
        self.up = False
    def stopDown(self, event):
        self.down = False
    def stopLeft(self, event):
        self.left = False
    def stopRight(self, event):
        self.right = False
    def spawnBullet(self, event):
        if self.hp > 0:
            global shots
            shots.append(bullet(self.x + 25, self.y, 0, -20))
            if opAttack:
                shots.append(bullet(self.x + 25, self.y, -3, -20))
                shots.append(bullet(self.x + 25, self.y, 3, -20))
            if otherOPAttack:
                shots.append(bullet(self.x + 25, self.y + 25, 0, -20))
                shots.append(bullet(self.x + 25, self.y - 25, 0, -20))
                shots.append(bullet(self.x + 25, self.y - 50, 0, -20))
                shots.append(bullet(self.x + 25, self.y - 75, 0, -20))
    def toggleAutoFire(self, event):
        self.autofire = not self.autofire
        print(self.autofire)

p = player(150, 550)

# MAKING SURE THAT THE CANVAS ACTUALLY RECEIVES KEYBOARD INPUT!!!!
disp.focus_set()
disp.bind("<Return>", startGame)
disp.bind("<Key>", writeCheatCode)
disp.bind("<Down>", eraseCheatCode)
spawnAliens()
def drawBackground():
    pass
root.mainloop()
