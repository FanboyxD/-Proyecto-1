#----------------------------------librerias--------------------------------#
from tkinter import *
import random
import tkinter.font
import tkinter.messagebox
import json
import time
import csv
from winsound import*
import threading
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
        global name
        name = []
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
        playbut.place(x=350,y=480)
        savename.place(x=450,y=450)
        textField.place(x=320,y=450)
        textField.config(state=NORMAL)
        data.set("")

#si selecciona "Cancelar" simplemente se cierra el cuadro de texto
    
def version():#funcion que muestra una ventana emergente con la version del programa
    tkinter.messagebox.showinfo("Space invaders",'''Instituto Tecnologico de Costa Rica
        Space Invaders v1.0''')#Cuadro de texto con la informacion

    

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
name=[]
dead = False
gOver = tkinter.font.Font(family="Chiller", size=30, weight="bold")#Fuentes utilizadas en el programa
Fuente2 = tkinter.font.Font(family="OCR-A II", size=14)
FuenteMenu = tkinter.font.Font(family="Fixedsys", size=30)
gameState = 0
cheatCode = ""

#--------------------Clase-balas-----------------------------------#

class bullet(threading.Thread):#se define la clase bullet que son las balas del jugador
    def __init__(self, x, y, xVel, yVel):#Se inicia segun los parametros posicion (x,y) y velocidad en eje x/y
        threading.Thread.__init__(self, name="bullet",target=bullet.draw,args=(self))
        threading.Thread.__init__(self, name="bullet",target=bullet.checkCollisions,args=(self))
        threading.Thread.__init__(self, name="bullet",target=bullet.update,args=(self))
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.sprites = [PhotoImage(file="laser.gif"),#se define cuales seran los sprites de la bala
                        PhotoImage(file="laser.gif")]
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
        self.shotDown = shotDown #si el objeto puede ser derribado usa los siguientes sprites
        self.sprites = [PhotoImage(file="asteroid.gif"),
                        PhotoImage(file="asteroid.gif")]
        if not self.shotDown: #si el objeto no puede ser derribado usa los siguientes sprites
            self.sprites = [PhotoImage(file="AlienBullet1.gif"),
                            PhotoImage(file="AlienBullet2.gif"),
                            PhotoImage(file="AlienBullet3.gif")]
    def checkCollisions(self):
        global Score
        if self.shotDown: #si el objeto puede ser derribado
            for i in shots:
                if i.x + 15 >= self.x and i.x <= self.x + 15 and i.y + 25 >= self.y \
                and i.y <= self.y + 25:
                    Score += 1 #suma 1 punto por destruir asteroide
                    self.dead = True #el objeto desaparece
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

class alien(threading.Thread):#se define la clase de los invaders
    def __init__(self, x, y, t): #inicia con posicion x/y y el tipo de alien
        threading.Thread.__init__(self,name="alien",target=alien.draw,args=(self))
        threading.Thread.__init__(self,name="alien",target=alien.update,args=(self))
        self.x = x
        self.y = y
        self.t = t
        # alien de un hit o hp, no ataca al jugador
        if self.t == 1:
            self.sprites = [PhotoImage(file="invader.gif"),
                            PhotoImage(file="enemy1_2.gif")]
            self.period = 60
            self.moveSpeed = 3
            self.hp = 1
        # alien de 3 hits o hp, no ataca al jugador
        if self.t == 2:
            self.sprites = [PhotoImage(file="enemy2_1.gif"),
                            PhotoImage(file="enemy2_2.gif")]
            self.period = 55
            self.moveSpeed = 3
            self.hp = 3

        # alien de un hit o hp, ataca al jugador
        if self.t == 3:
            self.sprites = [PhotoImage(file="enemy3_1.gif"),
                            PhotoImage(file="enemy3_2.gif")]
            self.period = 40
            self.hp = 1
            self.period = 38
            self.moveSpeed = 2
            self.hp = 1

        #alien de 3 hits o hp, ataca al jugador
        if self.t == 4:
            self.sprites = [PhotoImage(file="Missile Alien.gif"),
                            PhotoImage(file="Missile Alien.gif")]
            self.period = 22
            self.moveSpeed = 2
            self.hp = 3

        #caso que el tipo no cumpla las condiciones    
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
        #aumenta 5 puntos el score y el invader muere
            Score += 5
            self.dead = True
        if self.t == 3 and self.tPeriod == len(self.sprites) - 1 \
           and self.timer == self.period - 1 \
           and random.random() < 20: #si el alien es de tipo 3 dispara de manera random
            enemyProjectiles.append(enemyBullet(self.x + 50, self.y + 50, 0, 7,
                                                False)) #llama a la funcion de balas enemigas
        if self.t == 1 and self.tPeriod == len(self.sprites) - 1 \
           and self.timer == self.period - 1 \
           and random.random() < 8: #si el alien es de tipo 3 dispara de manera random
            enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 7,
                                                True))
        if self.t == 4 and self.tPeriod == len(self.sprites) - 1 and \
           self.timer == 0: #si es de tipo 4 tiene varios tipos de disparos y de manera random
            if random.random() < 0.1:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 1, 7,
                                                    True))
            else:
                enemyProjectiles.append(enemyBullet(self.x + 25, self.y + 50, 0, 4,
                                                    False))

#-----------------------------------Spawn de invaders/aliens-------------------------------------------------#

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
    wavesSurvived += 1 #cada vez que el ciclo se completa aumenta 1 la variable oleadassobrevividas

#---------------------------------Clase-Jugador----------------------------------------------------------#

class player(threading.Thread): #Se define la clase jugador 
    def __init__(self, x, y): #inicia con posicion y su respectivo sprite
        threading.Thread.__init__(self,name="player",target=player.draw,args=(self))
        threading.Thread.__init__(self,name="player",target=player.update,args=(self))
        self.x = x
        self.y = y
        self.sprites = [PhotoImage(file="ship.gif"),
                        PhotoImage(file="ship.gif")]
        self.timer = 0   #Tiempos para control de la nave
        self.tPeriod = 0
        self.period = 1
        self.left = False  #la nave tiene un estado inicial quieto
        self.right = False
        self.up = False
        self.down = False
        self.hp = 1 #El jugador comienza con un punto de hp
        # Se definen las teclas que seran usadas para mover al jugador
        disp.bind("<Left>", self.moveLeft)
        disp.bind("<Right>", self.moveRight)
        disp.bind("<KeyRelease-Left>", self.stopLeft)
        disp.bind("<KeyRelease-Right>", self.stopRight)
        disp.bind("<Up>", self.moveUp)
        disp.bind("<Down>", self.moveDown)
        disp.bind("<KeyRelease-Up>", self.stopUp)
        disp.bind("<KeyRelease-Down>", self.stopDown)
        disp.bind("<KeyRelease-space>", self.spawnBullet)

    def draw(self): #funcion que dibuja al jugador 
        disp.create_image(self.x, self.y,
                          image=self.sprites[self.tPeriod],
                          anchor=NW) #crea la imagen con la posicion dada de x/y
        self.timer += 1  #cambio de los tiempos
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= len(self.sprites)
        disp.create_text(self.x + 25, self.y - 20, text="HP: " + str(self.hp),
                         fill="white", font=Fuente2)  #texto que indica el hp
    def update(self): #actualizacion del jugador
        global dead   #llama a la variable dead
        if self.hp > 0: #movimientos si el jugador tiene hp
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
            self.draw() #llama funcion dibujar
        else:
            dead = True  #si se queda sin hp muere
        for i in aliens: #menos un punto de hp si toca al invader
            if i.x + 50 >= self.x and i.x <= self.x + 50 and i.y + 50 >= self.y \
                and i.y <= self.y + 50:
                self.hp = -1 
        for j in enemyProjectiles: #menos un punto de hp si es impactado por una bala enemiga
            if j.x + 15 >= self.x and j.x <= self.x + 50 and j.y + 25 >= self.y \
                and j.y <= self.y + 50:
                self.hp -= 1
                j.dead = True

    #se definen los eventos de las teclas(movimiento)
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
    def spawnBullet(self, event): #funcion que spawnea las balas
        self.playmusic = PlaySound('shoot.wav',SND_FILENAME|SND_ASYNC)#sonido que se reproduce al disparar
        if self.hp > 0: #debe tener hp
            global shots
            shots.append(bullet(self.x + 25, self.y, 0, -20))
            if AtaqueOP: #si esta activado el hack de 3 disparos
                shots.append(bullet(self.x + 25, self.y, -3, -20))
                shots.append(bullet(self.x + 25, self.y, 3, -20))
            if AtaqueOP2: #si esta activado el hack de rafaga
                shots.append(bullet(self.x + 25, self.y + 25, 0, -20))
                shots.append(bullet(self.x + 25, self.y - 25, 0, -20))
                shots.append(bullet(self.x + 25, self.y - 50, 0, -20))
                shots.append(bullet(self.x + 25, self.y - 75, 0, -20))
            
#---------------------------Dibujar-balas-------------------------------------------#

def drawShots(): # funcion que dibuja las balas
    for i in range(len(shots)):
        try:
            shots[i].update()# actualiza las balas, en caso de colision la borra
            if shots[i].dead:
                del shots[i]
        except:
            pass
t1 = threading.Thread(name = "hilo1", target = drawShots, args=())
t1.start()#comienza hilo1
t1.join()#termina hilo1
#--------------------------Dibujar-Aliens--------------------------------------------#

def drawAliens(): #funcion que dibuja aliens
    for i in range(len(aliens)):#dibuja la cantidad de aliens que haya
        try:
            aliens[i].update() #actualiza aliens, en caso de estar muerto lo borra
            if aliens[i].dead:
                del aliens[i]
        except:
            pass
t2 = threading.Thread(name = "hilo2", target = drawAliens, args=())
t2.start()#comienza hilo3
t2.join()#termina hilo2
#------------------------Dibujar-explosiones-----------------------------------------#

def drawExplosions():
    for i in range(len(explosions)): #dibuja la cantidad de explosiones que haya
        try:
            explosions[i].draw()
            if explosions[i].dead:#elimina las explosiones
                del explosions[i]
        except:
            pass
t3 = threading.Thread(name = "hilo3", target = drawExplosions, args=())
t3.start()#comienza hilo3
t3.join()#termina hilo3
#------------------------Dibuja-balas-enemigas---------------------------------------#

def drawEnemyBullets():
    for i in range(len(enemyProjectiles)):# dibuja la cantidad de balas enemigas segun aparescan
        try:
            enemyProjectiles[i].update() #actualiza las balas y si colisionan las borra
            if enemyProjectiles[i].dead:
                del enemyProjectiles[i]
        except:
            pass

#p es el jugador y se indica como la clase player con su posicion
p = player(150, 650)
t4 = threading.Thread(name = "hilo4", target = drawEnemyBullets, args=())
t4.start()#comienza hilo4
t4.join()#termina hilo4

#--------------------------inicia-el-juego------------------------------------------#

def startGame():  #funcion para iniciar al juego
    global gameState  #se llama a las variables globales estado del juego y nombre
    global name
    if len (name) > 0: #si hay un nombre el juego puede comenzar
        lectura()

        savename.place_forget()#se quitan los botones y el cuadro de texto y se desabilita
        playbut.place_forget()
        textField.config(state=DISABLED)
        textField.place_forget()

        disp.focus_set() #Nos aseguramos de que el contenedor/canvas reciba las teclas
        disp.bind("<Key>", writeCheatCode)
        disp.bind("<q>", eraseCheatCode)

        gameState = 1 #variable que al estar en 1 inicia el juego
    else:
        tkinter.messagebox.showinfo(message="Name must have at least 1 character") #si no hay un nombre establecido no se puede jugar

#-----------------------lee-el-csv-----------------------------------------------------------#

def lectura(): #funcion que lee el documento para la revision del usuario
    global name
    doc = open("Usuarios.csv","r") #se abre el doc
    documento = csv.reader(doc) #se lee
    documento2=list(documento)
    doc.close()# se cierra el doc
    comprobar_user(name,documento2,0)#se llama a la funcion comprobar

#---------------------Se comprueba-el-usuario-------------------------------------------------#

def comprobar_user(name,documento2,i): #funcion que comprueba si el usuario ya se encuentra en el doc
#se utiliza un programa de recursion realizado en practicas anteriores
    if i == len(documento2): # si no lo encuentra lo guarda
        with open("Usuarios.csv","a", newline = '') as doc_usuarioscsv:
            csv_data = csv.writer(doc_usuarioscsv)
            csv_data.writerows([[name]])
        doc_usuarioscsv.close() 
    elif [name] == documento2[i]:
        pass #si se encuentra el usuario no lo guarda pero igual se utiliza para el puntaje
    else:
        comprobar_user(name,documento2,i+1) #recursion

#------------------------------Hacks-del-juego------------------------------------------------#

def writeCheatCode(event): #evento que activa el juego
    global cheatCode #se llaman las variables de los hacks
    global AtaqueOP
    global AtaqueOP2
    global p         #se llama al jugador
    cheatCode += event.char  #a la variable cheatcode se le une las teclas que el jugador digite
    if cheatCode == "pra pra pra": #si el hack es igual a la palabra se activa el triple disparo
        AtaqueOP = True
        tkinter.messagebox.showinfo(title="Hack Activado!",
                    message='Has activado el triple disparo.')
        cheatCode = ""  #el codigo vuelve a estar vacio
    elif cheatCode == "on fire": #si es igual activa el disparo en rafaga
        AtaqueOP2 = True
        tkinter.messagebox.showinfo(title="Hack Activado!",
                    message='RAFAGA !!!')
        cheatCode = ""
    elif cheatCode == "hongo verde": #si es igual suma un punto de hp
        p.hp += 1
        cheatCode = ""

def eraseCheatCode(event): #evento que reinicia lo digitado en el hack
    global cheatCode
    cheatCode = "" #al teclear la letra "q" el codigo queda vacio

#----------------------se-dibuja-el-fondo-------------------------------------------#

def drawBackground():
    pass

#----------------------se-crea-el-menu----------------------------------------------#

def menu():
    disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2 - 50, #titulo y subtitulo + poscicion calculada por el alto y ancho
                     text="Space Invaders", fill="white", font=FuenteMenu)
    disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2 + 20,
                     text="Create Nick Name", fill="white", font=Fuente2)

#----------------------------Usuairio-----------------------------------------------#

def usuario(): #funcion que obtiene el usuario y lo garda en una variable
    global name
    global texto
    name=data.get()
        
data = StringVar() #se define que es de tipo str<
textField = Entry(disp,textvariable=data) #entry para insertar el usuario y poscicion
textField.place(x=320,y=450)
savename=Button(disp, text="Set Nick Name",command=usuario) #boton para guardar el usuario y poscicion
savename.place(x=450,y=450)
playbut=Button(disp, text=" Play ", font=21, command=startGame)#boton para iniciar el juego
playbut.place(x=350,y=480)

#--------------------------------------------imprime-los-highscores-----------------------------#

def imprimirscore():

    with open('puntajes.json') as file:   #abre el doc de puntajes
                scores = json.load(file)
    disp.create_text(disp.winfo_width()/2, 320, 
                             text=str(scores["Nombres"][0]) +" "+ str(scores["Scores"][0]),fill="yellow", font=Fuente2) #crea un texto con el jugador con el punteje mas alto
    disp.create_text(disp.winfo_width()/2, 350,
                             text=str(scores["Nombres"][1]) +" "+ str(scores["Scores"][1]),fill="yellow", font=Fuente2) #segundo puntaje mas alto
    disp.create_text(disp.winfo_width()/2, 380,
                             text=str(scores["Nombres"][2]) +" "+ str(scores["Scores"][2]),fill="yellow", font=Fuente2)  #tercer puntaje mas alto
    disp.create_text(disp.winfo_width()/2, 410,
                             text=str(scores["Nombres"][3]) +" "+ str(scores["Scores"][3]),fill="yellow", font=Fuente2)  #cuarto mas alto
    disp.create_text(disp.winfo_width()/2, 440,
                             text=str(scores["Nombres"][4]) +" "+ str(scores["Scores"][4]),fill="yellow", font=Fuente2)  #quinto mas alto

#-------------------------------------------se-guardan-los-scores-----------------------------------------------#

def highscore(): #funcion que comprueba si se deben guardar
    with open('puntajes.json') as file: #abre el doc
        puntajes = json.load(file)

    if Score>puntajes['Scores'][0]: #si el puntaje es mayor al mas alto lo guarda y corre todos un espacio sacando al quinto

        puntajes['Scores'] = [Score] + puntajes['Scores'][:-1]
        puntajes["Nombres"] = [name] + puntajes["Nombres"][:-1]
        with open('puntajes.json','w') as file:
            json.dump(puntajes,file)
    elif Score == puntajes['Scores'][0]: #si es igual no lo guarda 
        pass

    elif Score>puntajes['Scores'][1]: #si es mayor al segundo deja al primero y corre los demas un espacio

        puntajes['Scores'] = puntajes['Scores'][0:1] + [Score] + puntajes['Scores'][1:-1]
        puntajes["Nombres"] = puntajes["Nombres"][0:1] + [name] + puntajes["Nombres"][1:-1]
        with open('puntajes.json','w') as file:
            json.dump(puntajes,file)
    elif Score == puntajes['Scores'][1]: #si es igual no lo guarda
        pass

    elif Score>puntajes['Scores'][2]: #si es mayor al tercero deja el 1 y 2 y corre los demas un espacio

        puntajes['Scores'] = puntajes['Scores'][0:2] + [Score] + puntajes['Scores'][2:-1]
        puntajes["Nombres"] = puntajes["Nombres"][0:2] + [name] + puntajes["Nombres"][2:-1]
        with open('puntajes.json','w') as file:
            json.dump(puntajes,file)
    elif Score == puntajes['Scores'][2]: #si es igual no lo guarda
        pass

    elif Score>puntajes['Scores'][3]: #si es mayor al cuarto deja los primeros y corre un espacio

        puntajes['Scores'] = puntajes['Scores'][0:3] + [Score] + puntajes['Scores'][3:-1]
        puntajes["Nombres"] = puntajes["Nombres"][0:3] + [name] + puntajes["Nombres"][3:-1]
        with open('puntajes.json','w') as file:
            json.dump(puntajes,file)
    elif Score == puntajes['Scores'][3]: #si es igual no lo guarda
        pass

    elif Score>puntajes['Scores'][4]: #si es mayor al ultimo lo reemplaza

        puntajes['Scores'] = puntajes['Scores'][0:4] + [Score]
        puntajes["Nombres"] = puntajes["Nombres"][0:4] + [name]
        with open('puntajes.json','w') as file:
            json.dump(puntajes,file)
    elif Score == puntajes['Scores'][4]:#si es igual no se guarda
        pass


#----------------------------------dibujado-------------------------------------------#

def draw(): #funcion que dibuja el juego
    disp.delete("all")#se refrezca lo que aparece en pantalla y borra lo anterior
    if gameState: #si la variable tiene 1 comienza el juego
        drawBackground()#se dibuja el fondo
        p.update() #se actualiza al jugador
        drawShots() #se dibujan los disparos/aliens/balas enemigas/explosiones
        drawAliens()
        drawEnemyBullets()
        drawExplosions()
        disp.create_text(disp.winfo_width()/2-310, disp.winfo_height()/2-380,
                             text="Nivel Actual "+str(wavesSurvived), fill="white", font=Fuente2) #muestra en que nivel se encuentra el jugador
        disp.create_text(disp.winfo_width()/2-160, disp.winfo_height()/2-380,
                             text="Score "+ str(Score), fill="White", font=Fuente2)  #muestra el puntaje en tiempo real
        if len(aliens) == 0: #en caso de no haber aliens genera mas
            spawnAliens()
        if wavesSurvived >= 4: #si llega a 4 oleadas significa que gano el juego
            disp.delete("all") #se elimina todo
            disp.create_text(disp.winfo_width()/2, 200,
                                 text="You Win", fill="Blue", font=gOver) #texto que indica que gano
            disp.create_text(disp.winfo_width()/2, 290,
                                 text="HIGH SCORES", fill="Blue", font=gOver) #titulo high scores
            highscore() #llama a la funcion que guarda los scores
            imprimirscore() #funcion que imprime los scores
#- - - - - - - - - -muerted del jugador- - - - - - - - - - - - - - - - - - - - - -#
        elif dead: #en caso de morir

            disp.create_text(disp.winfo_width()/2, 200,
                                 text="GAME OVER", fill="red", font=gOver) #texto que indica "game over"
            disp.create_text(disp.winfo_width()/2, 230,
                             text="ROUNDS SURVIVED: " + str(wavesSurvived),
                             fill="yellow", font=Fuente2) #texto que muestra cuantas oleadas sobrevivio
            disp.create_text(disp.winfo_width()/2, 290,
                                 text="HIGH SCORES", fill="red", font=gOver)#titulo highscores
            highscore() #funcion guarda scores
            imprimirscore() #imprime los scores
    else: #si no esta la variable gamestate como 1 dibuja el fondo y llama al menu
        drawBackground()
        menu() #llama al menu
    root.after(25, draw) #cada cuanto llama a la funcion(25ms)
draw() # se llama a la funcion dibujar 
root.mainloop() #se cierra el loop de la ventana 
