#----------------------------------librerias--------------------------------#
from tkinter import *
import random
import tkinter.font
import tkinter.messagebox
import json
import time
import csv
from winsound import*
#import os

#-------------------Ventana------------------------------------------------#
root = Tk()
root.wm_title("Space Invaders NEO")
root.iconbitmap("SpIn.ico.ico")
root.resizable(width=False, height=False)
#-------------------Barra-de-menu------------------------------------------#

def salir():#Funcion que pregunta si el usuario desea salir del juego
    pregunta = tkinter.messagebox.askyesno('Salir','''Si desea salir del juego seleccione: si
Si desea salir al menu seleccione: no''' )
    if pregunta == True:
        root.destroy()
    

def version():#funcion que muestra una ventana emergente con la version del programa
    tkinter.messagebox.showinfo("Space invaders",'''Instituto Tecnologico de Costa Rica
        Space Invaders v0.5''')

    

menubar = Menu(root)#Se crea la barra de menu
root.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)

filemenu.add_command(label="Quit", command=salir)#sub menu de "file"
menubar.add_cascade(label="File", underline=0, menu=filemenu)#menu en la barra de menu
aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label="Acerca de ...", command=version)#sub menu de "about"
menubar.add_cascade(label="About", underline=0, menu=aboutmenu)#menu en la barra


#--------------Canvas-o-Contenedores---------------------------#
disp = Canvas(root, width=800, height=800, bg="black")
disp.grid(row=0, column=0)
w = Label(disp, text = "Nivel 1")
shots = []
enemyProjectiles = []
aliens = []
explosions = []
opAttack = False
otherOPAttack = False
wavesSurvived = 0
Score = 0
dead = False
gOver = tkinter.font.Font(family="Chiller", size=30, weight="bold")
otherFont = tkinter.font.Font(family="OCR-A II", size=14)
menuFont = tkinter.font.Font(family="Fixedsys", size=30)
gameState = 0
cheatCode = ""

#--------------------Clase-balas-----------------------------------#

class bullet():
    def __init__(self, x, y, xVel, yVel):
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.sprites = [PhotoImage(file="laser.gif"),
                        PhotoImage(file="laser.gif")]
        self.playmusic = PlaySound('shoot.wav',SND_FILENAME|SND_ASYNC)
        self.timer = 0
        self.tPeriod = 0
        self.period = 5
        self.dead = False
    def draw(self):
        disp.create_image(self.x, self.y - 25,
                          image=self.sprites[self.tPeriod],
                          anchor=NW)
        self.timer += 1
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= len(self.sprites)
    def checkCollisions(self):
        global Score
        for i in aliens:
            if i.x + 50 >= self.x and i.x <= self.x + 15 and i.y + 50 >= self.y \
               and i.y <= self.y + 25:
                self.dead = True
                i.hp -= 1
                Score += 1
                explosions.append(explosion(self.x + 7.5, self.y))

    def update(self):
        self.draw()
        self.x += self.xVel
        self.y += self.yVel
        # Bouncing off horizontal walls
        if self.x >= disp.winfo_width() or self.x <= 0:
            self.xVel *= -1
        # 
        if self.y + 25 >= disp.winfo_height() or self.y <= 0:
            self.dead = True
        
        self.checkCollisions()
class enemyBullet(bullet):
    def __init__(self, x, y, xVel, yVel, shotDown):
        super().__init__(x, y, xVel, yVel)
        self.shotDown = shotDown
        if not self.shotDown:
            self.sprites = [PhotoImage(file="AlienBullet1.gif"),
                            PhotoImage(file="AlienBullet2.gif"),
                            PhotoImage(file="AlienBullet3.gif")]
    def checkCollisions(self):

        if self.shotDown:
            for i in shots:
                if i.x + 15 >= self.x and i.x <= self.x + 15 and i.y + 25 >= self.y \
                and i.y <= self.y + 25:
                    self.dead = True
                    j.dead = True
                    explosions.append(explosion(self.x + 7.5, self.y + 12.5))
            

class explosion():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprites = [PhotoImage(file="explosionpurple.gif"),
                        PhotoImage(file="explosionpurple.gif"),
                        PhotoImage(file="explosionpurple.gif"),
                        PhotoImage(file="explosionpurple.gif")]
        self.timer = 0
        #os.system("start Explosion.wav")
    def draw(self):
        disp.create_image(self.x, self.y - 25,
                          image=self.sprites[self.timer % len(self.sprites)],
                          anchor=NW)
        self.timer += 1
        # Killing the animation
        if self.timer >= len(self.sprites):
            self.dead = True
class alien():
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
        # One-hit wonder alien, no attack
        if self.t == 1:
            self.sprites = [PhotoImage(file="invader.gif"),
                            PhotoImage(file="enemy1_2.gif")]
            self.period = 15
            self.moveSpeed = 3
            self.hp = 1
        # 3-hit alien, no attack
        if self.t == 2:
            self.sprites = [PhotoImage(file="enemy2_1.gif"),
                            PhotoImage(file="enemy2_2.gif")]
            self.period = 12
            self.moveSpeed = 3
            self.hp = 3

        # One-hit alien, bullet spawner
        if self.t == 3:
            self.sprites = [PhotoImage(file="enemy3_1.gif"),
                            PhotoImage(file="enemy3_2.gif")]
            self.period = 6
            self.moveSpeed = 3
            self.hp = 1
            self.period = 7
            self.moveSpeed = 2
            self.hp = 3
        self.xVel = self.moveSpeed
        self.timer = 0
        self.tPeriod = 0
        self.moveDownTimer = 0
        self.moveNext = True
    def draw(self):
        disp.create_image(self.x, self.y - 25,
                          image=self.sprites[self.tPeriod],
                          anchor=NW)
        self.timer += 1
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= len(self.sprites)
    def update(self):
        self.draw()
        self.x += self.xVel
        if self.x <= 0 or self.x + 50 >= disp.winfo_width():
            # Speed up, move down
            self.xVel *= -1.15
            self.y += 50
        if self.hp <= 0:
            self.dead = True
        if self.t == 3 and self.tPeriod == len(self.sprites) - 1 \
           and self.timer == self.period - 1 \
           and random.random() < 0.3:
            enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 7,
                                                False))
        if self.t == 4 and self.tPeriod == len(self.sprites) - 1 and \
           self.timer == 0:
            if random.random() < 0.3:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 1, 7,
                                                    True))
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, -1, 7,
                                                    True))
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 7,
                                                    True))
            elif random.random() < 0.7:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 7,
                                                    True))
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 25, 0, 7,
                                                    True))
            else:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 7,
                                                    False))
        if self.t == 5 and self.tPeriod == 0 and self.timer == 0 and \
           random.random() < 0.5:
            if random.random() < 0.1:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 1, 7,
                                                    False))
            else:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 1, 7,
                                                    True))
# Make a 8rowx6column grid of aliens.
def spawnAliens():
    global wavesSurvived
    for i in range(0, 400, 50):
        for j in range(0, 300, 50):
            chancy = random.random()
            if wavesSurvived <= 0:
                aliens.append(alien(i, j, 2))
            elif wavesSurvived <= 1:
                aliens.append(alien(i, j, random.randint(1, 3)))
            elif wavesSurvived <=2 :
                if j >= 200:
                    aliens.append(alien(i, j, 4))
    p.hp = 1
    wavesSurvived += 1
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
        disp.bind("<KeyRelease-space>", self.spawnBullet)
        disp.bind("<KeyRelease-Shift_L>", self.toggleAutoFire)
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

def drawShots():
    for i in range(len(shots)):
        try:
            shots[i].update()
            if shots[i].dead:
                del shots[i]
        except:
            pass
def drawAliens():
    for i in range(len(aliens)):
        try:
            aliens[i].update()
            if aliens[i].dead:
                del aliens[i]
        except:
            pass
def drawExplosions():
    for i in range(len(explosions)):
        try:
            explosions[i].draw()
            if explosions[i].dead:
                del explosions[i]
        except:
            pass
def drawEnemyBullets():
    for i in range(len(enemyProjectiles)):
        try:
            enemyProjectiles[i].update()
            if enemyProjectiles[i].dead:
                del enemyProjectiles[i]
        except:
            pass
p = player(150, 650)
def startGame(event):
    global gameState
    gameState = 1
def writeCheatCode(event):
    global cheatCode
    global opAttack
    global otherOPAttack
    global p
    cheatCode += event.char
    if cheatCode == "pra pra pra":
        opAttack = True
        tkinter.messagebox.showinfo(title="Hack Activado!",
                    message='Has activado el triple disparo.')
        cheatCode = ""
    elif cheatCode == "on fire":
        otherOPAttack = True
        tkinter.messagebox.showinfo(title="Hax Unlocked!",
                    message='RAFAGA !!!')
        cheatCode = ""
    elif cheatCode == "vida extra":
        p.hp += 1
        cheatCode = ""
def eraseCheatCode(event):
    global cheatCode
    cheatCode = ""
# MAKING SURE THAT THE CANVAS ACTUALLY RECEIVES KEYBOARD INPUT!!!!
disp.focus_set()
disp.bind("<Return>", startGame)
disp.bind("<Key>", writeCheatCode)
disp.bind("<W>", eraseCheatCode)
spawnAliens()
def drawBackground():
    pass
def menu():
    disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2 - 50,
                     text="Space Invaders", fill="white", font=menuFont)
    disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2 + 20,
                     text="Press ENTER to start.", fill="white", font=otherFont)
def draw():
    disp.delete("all")
    if gameState:
        drawBackground()
        p.update()
        drawShots()
        drawAliens()
        drawEnemyBullets()
        drawExplosions()
        disp.create_text(disp.winfo_width()/2-310, disp.winfo_height()/2-380,
                             text="Nivel Actual "+str(wavesSurvived), fill="white", font=otherFont)
        disp.create_text(disp.winfo_width()/2-160, disp.winfo_height()/2-380,
                             text="Score "+ str(Score), fill="White", font=otherFont)
        if len(aliens) == 0:
            spawnAliens()
        if wavesSurvived >= 4:
            disp.delete("all")
            disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2,
                                 text="You Win", fill="Blue", font=gOver)
        elif dead:
            disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2,
                                 text="GAME OVER", fill="red", font=gOver)
            disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2 + 30,
                             text="ROUNDS SURVIVED: " + str(wavesSurvived),
                             fill="yellow", font=otherFont)
    else:
        drawBackground()
        menu()
    root.after(25, draw)
draw()

root.mainloop()
