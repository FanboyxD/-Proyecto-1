from tkinter import *
import random
import tkinter.font
import tkinter.messagebox
import json 

root = Tk()
root.wm_title("nave ak7")
root.iconbitmap("SpIn.ico.ico")


disp = Canvas(root, width=800, height=700, bg="black")
disp.grid(row=0, column=0)
shots = []
gameState = 0
dead = False


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
        self.up = False
        self.down = False
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

        
    def draw(self):
        disp.create_image(self.x, self.y,
                          image=self.sprites[self.tPeriod],
                          anchor=NW)
        self.timer += 1
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= len(self.sprites)
        

    def update(self):
        global dead
        if self.hp > 0:
            if self.left and self.x >= 0:
                self.x -= 10
            if self.x < 0:
                self.x = 0
            if self.right and self.x + 50 <= disp.winfo_width():
                self.x += 10
            if self.up and self.y >= 0:
                self.y -= 10
            if self.y < 0:
                self.y = 0
            if self.down and self.y + 75 <= disp.winfo_height():
                self.y += 10
            if self.x + 50 > disp.winfo_width():
                self.x = disp.winfo_width() - 50
            if self.y - 50 > disp.winfo_height():
                self.y = disp.winfo_height() - 50
            self.draw()
            if self.tPeriod == 1 and self.timer == 1 and self.autofire:
                self.spawnBullet(False)


        else:
            dead = True
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
    def toggleAutoFire(self, event):
        self.autofire = True
        print(self.autofire)
p = player(150,675)

def startGame(event):
    global gameState
    gameState = 1
disp.focus_set()
disp.bind("<Return>", startGame)


def drawBackground():
    pass
def draw():
    disp.delete("all")
    if gameState:
        drawBackground()
        p.update()
        
        if dead:
            disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2,
                                 text="GAME OVER", fill="red", font=gOver)
            disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2 + 30,
                             text="ROUNDS SURVIVED: ",
                             fill="yellow", font=otherFont)
    else:
        drawBackground()
        
    root.after(25, draw)
draw()
root.mainloop()