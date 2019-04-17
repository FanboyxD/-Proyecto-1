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
root = Tk()#Se crea la ventana/Titulo/Icono de la ventana/No se puede redimencionar
root.wm_title("Space Invaders NEO")
root.iconbitmap("SpIn.ico.ico")
root.resizable(width=False, height=False)
#-------------------Barra-de-menu------------------------------------------#

def salir(): #Esta funcion pregunta al usuario si desea salir al menu o cerrar el juego
    pregunta = tkinter.messagebox.askyesnocancel('Salir','''Si desea salir del juego seleccione: si
Si desea salir al menu seleccione: no''' )#cuadro de dialogo que contiene la pregunta

    if pregunta == True:#si selecciona "si" cierra la ventana
        root.destroy()
    elif pregunta == False:#en caso de seleccionar "no" reinicia las variables y lo devuelve al menu principal
        global gameState
        gameState = 0
        global p
        p = player(400,650)
        global wavesSurvived
        wavesSurvived = 0
        global Score
        Score = 0
        global shots
        shots = []
        global enemyProjectiles
        enemyProjectiles = []
        global aliens
        aliens = []
        global explosions
        explosions = []
        global AtaqueOP
        AtaqueOP = False
        global AtaqueOP2
        AtaqueOP2 = False
        global dead
        dead = False

#si selecciona "Cancelar" simplemente se cierra el cuadro de texto
    
def version():#funcion que muestra una ventana emergente con la version del programa
    tkinter.messagebox.showinfo("Space invaders",'''Instituto Tecnologico de Costa Rica
        Space Invaders v0.5''')#Cuadro de texto con la informacion

    

menubar = Menu(root)#Se crea la barra de menu
root.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)

filemenu.add_command(label="Quit", command=salir)#sub menu de "file"
menubar.add_cascade(label="File", underline=0, menu=filemenu)#menu en la barra de menu
aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label="Acerca de ...", command=version)#sub menu de "about"
menubar.add_cascade(label="About", underline=0, menu=aboutmenu)#menu en la barra


#--------------Canvas-o-Contenedores---------------------------#

disp = Canvas(root, width=800, height=800, bg="black")#Contenedor principal
disp.grid(row=0, column=0)
w = Label(disp, text = "Nivel 1")
#Variables necesarias para el funcionamiento del programa
shots = []
enemyProjectiles = []
aliens = []
explosions = []
AtaqueOP = False
AtaqueOP2 = False
wavesSurvived = 0
Score = 0
dead = False
gOver = tkinter.font.Font(family="Chiller", size=30, weight="bold")#Fuentes utilizadas en el programa
Fuente2 = tkinter.font.Font(family="OCR-A II", size=14)
FuenteMenu = tkinter.font.Font(family="Fixedsys", size=30)
gameState = 0
cheatCode = ""

#--------------------Clase-balas-----------------------------------#

class bullet():#se define la clase bullet que son las balas del jugador
    def __init__(self, x, y, xVel, yVel):#Se inicia segun los parametros posicion (x,y) y velocidad en eje x/y
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.sprites = [PhotoImage(file="laser.gif"),#se define cuales seran los sprites de la bala
                        PhotoImage(file="laser.gif")]
        self.playmusic = PlaySound('shoot.wav',SND_FILENAME|SND_ASYNC)#sonido que se reproduce al disparar
        self.timer = 0  #Tiempo y periodo para el control de las balas
        self.tPeriod = 0
        self.period = 5
        self.dead = False #se define que la bala existe 
    def draw(self):# se dibuja la bala
        disp.create_image(self.x, self.y - 25,
                          image=self.sprites[self.tPeriod],
                          anchor=NW)#Se crea la imagen de la bala, su posicion
        self.timer += 1
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= len(self.sprites)
    def checkCollisions(self):#Se revisa si la bala colisiona con algun alien
        for i in aliens:
            if i.x + 50 >= self.x and i.x <= self.x + 15 and i.y + 50 >= self.y \
               and i.y <= self.y + 25:
                self.dead = True #en caso de colisionar la bala deja de existir
                i.hp -= 1 #se resta un punto de vida a los aliens
                explosions.append(explosion(self.x + 7.5, self.y)) #se llama a la animacion de explosion con los parametros indicados
                self.explote=PlaySound('invaderkilled.wav',SND_FILENAME|SND_ASYNC) #sonido que se reproduce cuando la bala colisiona

    def update(self):#Actualizacion del estado de la bala
        self.draw()#llama a la funcion que dibuja la bala
        self.x += self.xVel #la bala cambia de posicion eje x y en caso de algunas balas eje y
        self.y += self.yVel
        #condiciones para que las balas no reboten
        if self.x >= disp.winfo_width() or self.x <= 0:
            self.xVel *= -1
        #Condicion para que las balas desaparezcan en caso de llegar hasta arriba
        if self.y + 25 >= disp.winfo_height() or self.y <= 0:
            self.dead = True
        
        self.checkCollisions() #se llama a la funcion checkcollisions

#--------------------------------------Bala-enemiga-----------------------------------------#

class enemyBullet(bullet): #Clase para las balas enemigas
    def __init__(self, x, y, xVel, yVel, shotDown): #posicion eje x/y velocidad y si es derribado
        super().__init__(x, y, xVel, yVel)
        self.shotDown = shotDown
        if not self.shotDown: #en caso de no haber sido derribada la bala se dibujan los sprites
            self.sprites = [PhotoImage(file="AlienBullet1.gif"),
                            PhotoImage(file="AlienBullet2.gif"),
                            PhotoImage(file="AlienBullet3.gif")]
    def checkCollisions(self):

        if self.shotDown: #en caso de derribar la bala
            for i in shots:
                if i.x + 15 >= self.x and i.x <= self.x + 15 and i.y + 25 >= self.y \
                and i.y <= self.y + 25:
                    self.dead = True #la bala desaparece 
                    j.dead = True
                    explosions.append(explosion(self.x + 7.5, self.y + 12.5)) #se llama a la funcion explosion con los parametros indicados
            

class explosion(): #clase de las explociones
    def __init__(self, x, y): #se inicializa con la posicion x/y 
        self.x = x
        self.y = y
        self.sprites = [PhotoImage(file="explosionpurple.gif"), #se crean los sprites de la explosion
                        PhotoImage(file="explosionpurple.gif")]
        self.timer = 0

    def draw(self): #funcion encargada de dibujar las explosiones
        disp.create_image(self.x, self.y - 25,
                          image=self.sprites[self.timer % len(self.sprites)],
                          anchor=NW) #se crea la imagen con posicion x/y y espacio que ocupa
        self.timer += 1
        if self.timer >= len(self.sprites): #se elimina la animacion
            self.dead = True

#---------------------------clase-aliens-------------------------------------------------------------------------------#

class alien():#se define la clase de los invaders
    def __init__(self, x, y, t): #inicia con posicion x/y y el tipo de alien
        self.x = x
        self.y = y
        self.t = t
        # alien de un hit o hp, no ataca al jugador
        if self.t == 1:
            self.sprites = [PhotoImage(file="invader.gif"),
                            PhotoImage(file="enemy1_2.gif")]
            self.period = 15
            self.moveSpeed = 3
            self.hp = 1
        # alien de 3 hits o hp, no ataca al jugador
        if self.t == 2:
            self.sprites = [PhotoImage(file="enemy2_1.gif"),
                            PhotoImage(file="enemy2_2.gif")]
            self.period = 12
            self.moveSpeed = 3
            self.hp = 3

        # alien de un hit o hp, ataca al jugador
        if self.t == 3:
            self.sprites = [PhotoImage(file="enemy3_1.gif"),
                            PhotoImage(file="enemy3_2.gif")]
            self.period = 6
            self.hp = 1
            self.period = 7
            self.moveSpeed = 2
            self.hp = 1

        #alien de 3 hits o hp, ataca al jugador
        if self.t == 4:
            self.sprites = [PhotoImage(file="Missile Alien.gif"),
                            PhotoImage(file="Missile Alien.gif")]
            self.period = 7
            self.moveSpeed = 2
            self.hp = 3

        #caso que el tipo no cumpla alas condiciones    
        self.xVel = self.moveSpeed
        self.timer = 0
        self.tPeriod = 0
        self.moveDownTimer = 0
        self.moveNext = True
    def draw(self): #funcion que dibuja los aliens
        disp.create_image(self.x, self.y - 25,
                          image=self.sprites[self.tPeriod],
                          anchor=NW)#crea la imagen con su pos x/y
        self.timer += 1 #cambio de tiempos
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= len(self.sprites)
    def update(self): #actuliza lo que pasa con el invader
        global Score #se llama a la variable global score para almacenar el puntaje
        self.draw() # se llama a la funcion que dibuja al alien
        self.x += self.xVel #cada x aumenta con la velocidad
        if self.x <= 0 or self.x + 50 >= disp.winfo_width():#condicion para ver donde se encuentra el alien
            # aumenta la veloc del invader y baja de fila
            self.xVel *= -1.15
            self.y += 50
        if self.hp <= 0: #si la vida del alien es 0 o menor
        #aumenta 1 punto el score y el invader muere
            Score += 1
            self.dead = True
        if self.t == 3 and self.tPeriod == len(self.sprites) - 1 \
           and self.timer == self.period - 1 \
           and random.random() < 0.3: #si el alien es de tipo 3 dispara de manera random
            enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 7,
                                                False)) #llama a la funcion de balas enemigas
        if self.t == 4 and self.tPeriod == len(self.sprites) - 1 and \
           self.timer == 0: #si es de tipo 4 tiene varios tipos de disparos y de manera random
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

#-----------------------------------Spawn de invaders/aliens------------------------------------#

def spawnAliens():#fucion encargada de pasar los parametros de spawn
    global wavesSurvived #llama la variable oleadas sobrevividas
    for i in range(0, 400, 50): #for con rango de aparicion para eje x
        for j in range(0, 300, 50):#for con rango de aparicion para eje y 
            if wavesSurvived <= 0: #si no ha sobrevivido ninguna oleada
                aliens.append(alien(i, j, random.randint(1,2))) #aparece aliens de tipo 1 y 2 de manera random
            elif wavesSurvived <= 1: #si ha sobrevivido una oleada 
                aliens.append(alien(i, j, random.randint(1, 3))) #aparece aliens de tipo 1,2 y 3 de manera random
            elif wavesSurvived <=2 :#si sobrevive 2 oleadas 
                if 100<= j <= 300: #condicion para disminuir la cantidas de aliens y en que lugar hacen spawn
                    aliens.append(alien(i, j, random.randint(2, 4))) #aparece aliens de tipo 2,3,4 de forma aleatorea
    p.hp = 1 #el jugador "p" tiene como parametro de hp un 1
    wavesSurvived += 1 #cada vez que el ciclo se completa aumenta 1 la variable oleadassobrevividas
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
                         fill="white", font=Fuente2)
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
            if AtaqueOP:
                shots.append(bullet(self.x + 25, self.y, -3, -20))
                shots.append(bullet(self.x + 25, self.y, 3, -20))
            if AtaqueOP2:
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
    global AtaqueOP
    global AtaqueOP2
    global p
    cheatCode += event.char
    if cheatCode == "pra pra pra":
        AtaqueOP = True
        tkinter.messagebox.showinfo(title="Hack Activado!",
                    message='Has activado el triple disparo.')
        cheatCode = ""
    elif cheatCode == "on fire":
        AtaqueOP2 = True
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
disp.bind("<q>", eraseCheatCode)
spawnAliens()
def drawBackground():
    pass
def menu():
    disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2 - 50,
                     text="Space Invaders", fill="white", font=FuenteMenu)
    disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2 + 20,
                     text="Press ENTER to start.", fill="white", font=Fuente2)
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
                             text="Nivel Actual "+str(wavesSurvived), fill="white", font=Fuente2)
        disp.create_text(disp.winfo_width()/2-160, disp.winfo_height()/2-380,
                             text="Score "+ str(Score), fill="White", font=Fuente2)
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
                             fill="yellow", font=Fuente2)
    else:
        drawBackground()
        menu()
    root.after(25, draw)
draw()

root.mainloop()
