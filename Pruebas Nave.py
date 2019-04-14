# Import tkinter library.
from tkinter import *
import random
import tkinter.font
import tkinter.messagebox
import json 
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
# Bullet Class
class bullet():
    def __init__(self, x, y, xVel, yVel):
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.sprites = [PhotoImage(file="laser.gif"),
                        PhotoImage(file="laser.gif")]
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
        for i in aliens:
            if i.x + 50 >= self.x and i.x <= self.x + 15 and i.y + 50 >= self.y \
               and i.y <= self.y + 25:
                self.dead = True
                i.hp -= 1
                explosions.append(explosion(self.x + 7.5, self.y))

##        for j in enemyProjectiles:
##            if j.shotDown:
##                if j.x + 15 >= self.x and j.x <= self.x + 15 and j.y + 25 >= self.y \
##                and j.y <= self.y + 25:
##                    self.dead = True
##                    j.dead = True
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
        elif random.random() < 0.05:
            self.sprites = [PhotoImage(file="Coke Can.gif")]
        else:
            self.sprites = [PhotoImage(file="Missile1.gif"),
                            PhotoImage(file="Missile2.gif")]
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
        self.upgrad = False
        # One-hit wonder alien, no attack
        if self.t == 1:
            self.sprites = [PhotoImage(file="invader.gif"),
                            PhotoImage(file="enemy1_2.gif")]
            self.period = 15
            self.moveSpeed = 3
            self.hp = 1
            if hardMode:
                self.t = 3
                self.upgrad = True
        # 3-hit alien, no attack
        if self.t == 2:
            self.sprites = [PhotoImage(file="enemy2_1.gif"),
                            PhotoImage(file="enemy2_2.gif")]
            self.period = 12
            self.moveSpeed = 3
            self.hp = 3
            if hardMode:
                self.sprites = [PhotoImage(file="StrongAlien1.gif"),
                                PhotoImage(file="StrongAlien2.gif")]
                self.period = 10
                self.hp = 5
        # One-hit alien, bullet spawner
        if self.t == 3:
            self.sprites = [PhotoImage(file="enemy3_2.gif"),
                            PhotoImage(file="enemy3_1.gif"),
                            PhotoImage(file="enemy3_2.gif"),
                            PhotoImage(file="enemy3_1.gif"),
                            PhotoImage(file="enemy3_2.gif")]
            self.period = 6
            self.moveSpeed = 3
            self.hp = 1
            if hardMode and not self.upgrad:
                self.t = 4
                self.moveSpeed = 3.5
                self.upgrad = True
        if self.t == 4:
            self.sprites = [PhotoImage(file="BlasterAlien1.gif"),
                            PhotoImage(file="BlasterAlien1.gif"),
                            PhotoImage(file="BlasterAlien1.gif"),
                            PhotoImage(file="BlasterAlien1.gif"),
                            PhotoImage(file="BlasterAlien2.gif"),
                            PhotoImage(file="BlasterAlien3.gif"),
                            PhotoImage(file="BlasterAlien2.gif"),
                            PhotoImage(file="BlasterAlien1.gif"),
                            PhotoImage(file="BlasterAlien1.gif"),
                            PhotoImage(file="BlasterAlien4.gif"),
                            PhotoImage(file="BlasterAlien5.gif"),
                            PhotoImage(file="BlasterAlien6.gif"),
                            PhotoImage(file="BlasterAlien7.gif"),
                            PhotoImage(file="BlasterAlien7.gif")]
            self.period = 7
            self.moveSpeed = 2
            self.hp = 3
            if hardMode and not self.upgrad:
                self.t = 5
        if self.t == 5:
            self.sprites = [PhotoImage(file="mystery.gif"),
                            PhotoImage(file="mystery.gif")]
            self.period = 2
            self.moveSpeed = 2
            self.hp = 10
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
            subprocess.Popen(["aplay",
                              "C://Kevin/Kevin's Stuff/Python Stuff/Space Invaders/Shot.wav"])
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
            #subprocess.Popen(["afplay", "Shot.wav"])
        if self.t == 5 and self.tPeriod == 0 and self.timer == 0 and \
           random.random() < 0.5:
            if random.random() < 0.1:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 1, 7,
                                                    False))
            else:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 1, 7,
                                                    True))
            #subprocess.Popen(["afplay", "Shot.wav"])
# Make a 8rowx6column grid of aliens.
def spawnAliens():
    global wavesSurvived
    for i in range(0, 400, 50):
        for j in range(0, 300, 50):
            chancy = random.random()
            if wavesSurvived <= 2:
                aliens.append(alien(i, j, 1))
            elif wavesSurvived <= 3:
                aliens.append(alien(i, j, random.randint(1, 2)))
            elif wavesSurvived <= 7:
                if j >= 200:
                    aliens.append(alien(i, j, 3))
                else:
                    if chancy <= 0.5 + ((wavesSurvived - 4)/10):
                        aliens.append(alien(i, j, 2))
                    else:
                        aliens.append(alien(i, j, 1))
            elif wavesSurvived <= 10:
                aliens.append(alien(i, j, random.randint(1, 3)))
            elif wavesSurvived <= 15:
                if chancy <= 0.05 + ((wavesSurvived - 11)/25):
                    aliens.append(alien(i, j, 4))
                else:
                    aliens.append(alien(i, j, random.randint(1, 2)))
            elif wavesSurvived <= 20:
                aliens.append(alien(i, j, random.randint(1, 4)))
            elif wavesSurvived <= 25:
                aliens.append(alien(i, j, random.randint(2, 4)))
            else:
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
p = player(150, 700)
def startGame(event):
    global gameState
    gameState = 1
def writeCheatCode(event):
    global cheatCode
    global hardMode
    global opAttack
    global otherOPAttack
    global p
    cheatCode += event.char
    if cheatCode == "hard":
        hardMode = True
        tkinter.messagebox.showwarning(title="WARNING! WARNING!",
                    message='''
    HARD MODE is on.
    Prepare yourself.

    You're gonna have a BAD time.''')
        cheatCode = ""
    elif cheatCode == "oh baby a triple":
        opAttack = True
        if hardMode:
            tkinter.messagebox.showinfo(title="Hax Unlocked!",
                    message='''
    You're probably gonna need this to pass HARD MODE.
    Good luck getting to round 25.
    ''')
        else:
            tkinter.messagebox.showinfo(title="Hax Unlocked!",
                    message='''...
Triple Deluxe Shot is now ON.
    ''')
        cheatCode = ""
    elif cheatCode == "the other one":
        otherOPAttack = True
        tkinter.messagebox.showinfo(title="Hax Unlocked!",
                    message='LAZOR SHOT ON!!!')
        cheatCode = ""
    elif cheatCode == "hp up":
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
        if len(aliens) == 0:
            spawnAliens()
        if dead:
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
