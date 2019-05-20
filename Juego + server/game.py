#-------------------------------Librerias-------------------------------------
import pygame
from network import Network
from pygame.locals import *
import os
import random
import sys
import _thread
import time
import json
from threading import Timer
pygame.init()
#-------------------------------Sprites---------------------------------------
walkRight = pygame.image.load('images/Right Car.png')
walkLeft = pygame.image.load('images/Left Car.png')
walkUp = pygame.image.load('images/Back Car.png')
walkDown = pygame.image.load('images/Front Car.png')
char = pygame.image.load('images/Back Car.png')

#-------------------------------Sonidos---------------------------------------
bulletSound = pygame.mixer.Sound("sonidos/car_shoot.wav")
crashSound = pygame.mixer.Sound("sonidos/car_crash.wav")
hitSound = pygame.mixer.Sound("sonidos/car_hit.wav")
moving = pygame.mixer.Sound("sonidos/car_moving.wav")
brake = pygame.mixer.Sound("sonidos/car_brake.wav")

#-------------------------------Jugador---------------------------------------
class player():
    width = height = 50 #Ancho y alto del jugador
    def __init__(self, startx, starty, color=(255,0,0)): #coordenadas iniciales y color
        self.x = startx     # se declaran las variables de coord, veloc de movimiento, y que inicie quieto
        self.y = starty
        self.velocity = 10
        self.color = color
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.Brake = False
        self.BrakeCount = 1
        self.hitbox = (self.x+20,self.y,28,60) #dimensiones de la hitbox del jugador

    def draw(self, win): #Dibujado del jugador 
        if self.left:  #En caso de ir a la izquierda
            win.blit(walkLeft, (self.x,self.y)) #dibuja el sprite de lado izquierdo                  
        elif self.right: #Lo mismo sucede para cada movimiento arriba, abajo, derecha
            win.blit(walkRight, (self.x,self.y))
        elif self.up:
            win.blit(walkUp, (self.x,self.y))
        elif self.down:
            win.blit(walkDown, (self.x,self.y))
        else:
            win.blit(walkUp, (self.x,self.y))
        self.hitbox = (self.x,self.y+1,30,20)
            
    def move(self, dirn): #Movimiento
        #se definen las 3 direcciones posibles
        if dirn == 0: #derecha
            self.x += self.velocity
        elif dirn == 1: #izquierda
            self.x -= self.velocity
        elif dirn == 2: #arriba
            self.y -= self.velocity
        else: #abajo
            self.y += self.velocity

    def hit(self,win): #reseteo en la posicion del jugador si muere
        self.x = 60
        self. y = 410
        self.walkCount = 0
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
            	if event.type == pygame.QUIT:
            		i=301
            		pygame.quit()

#------------------------------Enemigos------------------------------------------------------------
class enemy(object):
    walkRight = [pygame.image.load("images/Enemy sprites Right.png")]
    walkLeft = [pygame.image.load("images/Enemy sprites Left.png")]
    walkUp = [pygame.image.load("images/Enemy sprites Up.png")]
    walkDown = [pygame.image.load("images/Enemy sprites Down.png")]
    
    def __init__(self, x, y, width, height, end1, end2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [end1, end2]  #Limite en eje x de donde llega el enemigo
        self.walkCount = 0
        self.vel = 5
        self.hitbox = (self.x+20,self.y,28,60)
        self.health = 8 #vida del enemigo
        self.visible = True
        
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 1:  
                self.walkCount = 0         
            if self.vel > 0: # si la velocidad es mayor a 0 se mueve a la derecha
                win.blit(self.walkRight[self.walkCount], (self.x,self.y))
                self.walkCount += 1
            else:  #Si no se mueve a la izquierda
                win.blit(self.walkLeft[self.walkCount], (self.x,self.y))
                self.walkCount += 1
            pygame.draw.rect(win,(0,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10)) #dimensiones de la barra de vida del enemigo
            pygame.draw.rect(win,(0,255,0),(self.hitbox[0],self.hitbox[1]-20,50-(5*(8-self.health)),10))#lo que se le rebaja de vida al enemigo
            self.hitbox = (self.x+0,self.y+6,35,20)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def move(self):
        if self.vel > 0:  # Si se mueve a la derecha
            if self.x < self.path[1] + self.vel: # Si aun no se ha alcanzado el limite a la derecha
                self.x += self.vel
            else: # Change direction and move back the other way
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else: # Si se mueve a la izquierda
            if self.x > self.path[0] - self.vel: # Si aun no se ha alcanzado el limite a la izquierda
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        if self.health > 1:
            self.health -= 1 #cantidad de vida que se le rebaja al enemigo
        else:
            self.visible = False
        print("1 hit + 50ptos")

#-----------------------------Obstaculos-----------------------------------------------------------
class obstacles(object):
    img = [pygame.image.load(os.path.join("images","wall.png")),pygame.image.load(os.path.join("images","cactus.png")),pygame.image.load(os.path.join("images","rocks.png"))]
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.count = 0
        self.hitbox = (self.x+30,self.y+30,self.width-40,self.height-40)
    def draw(self,win):
        self.hitbox = (self.x+30,self.y+30,self.width-40,self.height-40)
        if self.count>=1:
            self.count = 0
        win.blit(self.img[self.count], (self.x,self.y))
        self.count += 1
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0]+self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

class cactus(obstacles): #cactus que forma parte de los obstaculos
    img = pygame.image.load(os.path.join("images","cactus.png"))
    def draw(self,win):
        self.hitbox = (self.x,self.y,self.width-20,self.height-280)
        win.blit(self.img,(self.x,self.y))
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def collide(self,rect):
        self.hitbox = (self.x,self.y,self.width-20,self.height-280)        
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0]+self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False
            		
class rocks(obstacles):
    img = pygame.image.load(os.path.join("images","rocks.png"))
    def draw(self,win):
        self.hitbox = (self.x,self.y+25,self.width-28,self.height-90)
        win.blit(self.img,(self.x,self.y))
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def collide(self,rect):
        self.hitbox = (self.x,self.y+25,self.width-28,self.height-90)
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0]+self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

#------------------------------Balas---------------------------------------------------------------
class projectile(object):
    def __init__(self,x,y,radius,color,facing): #se definen sus coord, radio, color, si van a la izquierda o derecha y a que velocidad 
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 15 * facing

    def draw(self,win): #dibuja la bala
        pygame.draw.circle(win, self.color, (self.x,self.y),self.radius)

#---------------------------Juego------------------------------------------------------------------
class Game:

    def __init__(self, w, h,name):#se define ancho x alto, se importa la red del cliente, se establece la pos inicial de los jugadores
        #Variables necesarias para el puntaje y titulo de la ventana
        self.net = Network()
        self.score = 0 #Score del jugador1
        self.score2 = 0 #Score del jugador2
        self.banderas = 0
        self.banderas2 = 0
        self.width = w
        self.height = h
        self.name = name
        self.player = player(50, 210)
        self.player2 = player(100,100)
        self.bullet2 = projectile(-10,round(self.player2.y + 17),6,(0,15,240),0)
        self.canvas = Canvas(self.width, self.height, "Dakar Death")
        self.police = enemy(100, 500, 35, 30, 0, 1920)

    def run(self): #Corre el juego
        clock = pygame.time.Clock() 
        run = True #inicia el run
        bullets = [] #variable para las balas
        font = pygame.font.SysFont("comicsans",30,True,True)

        pygame.time.set_timer(USEREVENT+1,500)
        pygame.time.set_timer(USEREVENT+2,random.randrange(2000,3500))#tiempo en que salen los obstaculos
        shootLoop = 0
        objects = [] #lista donde estan los obstacus
        self.Level = 1
        self.bulletx = -10
        self.bullety = round(self.player2.y + 17)
        start_ticks=pygame.time.get_ticks() #starter tick
        while run:
            seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
            clock.tick(30) #tiempo en ms de refresco de la ventana
    
            if seconds>120: #Tiempo antes de subir de nivel
                self.Level += 1 #Aumenta la variable de nivel
    
            for objectt in objects: #Borra los obstaculos cuando salen de la pantalla
                if objectt.collide(self.player.hitbox):
                    pygame.time.delay(1000)
                    self.score -= 1
                objectt.x -= 1.4
                if objectt.x < -objectt.width * -1:
                    objects.pop(objects.index(objectt))
            for event in pygame.event.get(): #analiza cada evento
                if event.type == pygame.QUIT: #Si es click en la "x" de la ventana, sale del juego
                    run = False 
                if event.type == USEREVENT+1:
                    self.player.velocity += 1
                    self.player.velocity -=1
                if event.type == USEREVENT+2:
                    r=random.randrange(0,2)#Genera spawns aleatorios
                    if r == 0:
                        objects.append(obstacles(1920,400,64,64))#coordenadas de spawn de los muros
                    else:
                        objects.append(cactus(1920,600,48,320)) #coordenadas de spawn de los cactus
                        objects.append(rocks(1920,200,64,64))
                        

            if self.police.visible == True:
                if self.player.hitbox[1] < self.police.hitbox[1]+self.police.hitbox[3] and self.player.hitbox[1]+self.player.hitbox[3] > self.police.hitbox[1]: #Rango donde el judagor recibe daño
                    if self.player.hitbox[0] + self.player.hitbox[2] > self.police.hitbox[0] and self.player.hitbox[0] < self.police.hitbox[0] + self.police.hitbox[2]:#Rango donde el judagor recibe daño
                        moving.stop()
                        crashSound.play()
                        self.player.hit(self.canvas.get_canvas())
                        font1 = pygame.font.SysFont("comicsans",100)
                        perdida = font1.render("-5",1,(255,0,0))
                        self.canvas.get_canvas().blit(perdida,((850,500)))
                        self.score -= 5
   
            for bullet in bullets: #analisa cada bala
                if self.police.visible == True:
                    if bullet.y - bullet.radius < self.police.hitbox[1]+self.police.hitbox[3] and bullet.y + bullet.radius > self.police.hitbox[1]:#Rango para golpear al enemigo
                        if bullet.x + bullet.radius > self.police.hitbox[0] and bullet.x - bullet.radius < self.police.hitbox[0] + self.police.hitbox[2]:#Rango para golpear al enemigo
                            self.police.hit()
                            bullets.pop(bullets.index(bullet))
                            self.score += 50
                            hitSound.play()
                            moving.stop() #sonidos
                if bullet.x < 1920 and bullet.x > 0: #En caso de estar en la ventana se mueve la bala
                    bullet.x += bullet.vel
                    self.bulletx = bullet.x
                else:
                    bullets.pop(bullets.index(bullet))
    
            if shootLoop > 0: #limitador de disparos
                shootLoop += 1
            if shootLoop > 3:
                shootLoop = 0


            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]: #en caso de la tecla escape tambien sale
                    run = False

            if keys[pygame.K_c]: #si presiona la tecla "c" dispara una bala(solo una a la vez)
                moving.stop() #sonidos
                bulletSound.play()            
                if self.player.left: #direccion de la bala
                    facing = -1
                elif self.player.right:
                    facing = 1
                if len(bullets) < 1: #limite de balas estblecido a 1
                    bullets.append(projectile(round(self.player.x + 15),round(self.player.y + 10), 6, (200,10,56),facing))

            if not(self.player.Brake):
                if keys[pygame.K_RIGHT]: #si presiona la flecha derecha
                    if self.player.x <= self.width - self.player.velocity: #Mueve al jugador
                        self.player.move(0)#lo mueve a la derecha
                        self.player.left = False
                        self.player.right = True #pone el sprite de la derecha
                        self.player.up = False
                        self.player.down = False
                        moving.play() #sonidos

                if keys[pygame.K_LEFT]: #si presiona la flecha izquierda
                    if self.player.x >= self.player.velocity: #mueve al jugador
                        self.player.move(1) #lo mueve a la iquierda
                        self.player.left = True #sprite de la izquiera
                        self.player.right = False
                        self.player.up = False
                        self.player.down = False
                        moving.play() #sonidos

                if keys[pygame.K_UP]: #si presiona la flecha de arriba pasa lo mismo que anteriormente pero con otra direccion
                    if self.player.y >= self.player.velocity:
                        self.player.move(2)
                        self.player.left = False
                        self.player.right = False
                        self.player.up = True
                        self.player.down = False
                        moving.play() #sonidos

                if keys[pygame.K_DOWN]:# de la misma manera si es hacia abajo
                    if self.player.y <= self.height - self.player.velocity:
                        self.player.move(3)
                        self.player.left = False
                        self.player.right = False
                        self.player.up = False
                        self.player.down = True
                        moving.play() #sonidos

                if keys[pygame.K_SPACE]:
                    moving.stop()
                    self.player.Brake = True
                    self.player.right = False
                    self.player.left = False
                    self.player.up = True
                    self.player.down = False
                    brake.play() #sonidos
            else:
                if  self.player.BrakeCount >= -0:
                    self.player.y -= (self.player.BrakeCount * abs(self.player.BrakeCount))
                    self.player.BrakeCount -= 1
                else: 
                    self.player.BrakeCount = 0
                    self.player.Brake = False


            #Zonas dañinas para el jugador (6 total)
            if 100 <= self.player.x <= 200 and 100 <= self.player.y <= 200: #medidas de las zonas dañinas
                self.score -= 1

            if 500 <= self.player.x <= 600 and 700 <= self.player.y <= 800:
                self.score -= 1

            if 650 <= self.player.x <= 750 and 300 <= self.player.y <= 400:
                self.score -= 1

            if 1100 <= self.player.x <= 1200 and 400 <= self.player.y <= 500:
                self.score -= 1

            if 1275 <= self.player.x <= 1375 and 620 <= self.player.y <= 720:
                self.score -= 1

            if 1405 <= self.player.x <= 1505 and 222 <= self.player.y <= 322:
                self.score -= 1

            #Zona de banderas (requisito para la meta,se encuentran en las esquinas)
            if 0 <= self.player.x <= 200 and 0 <= self.player.y <= 200: #medidas de los espacios para recoger la bandera
                self.banderas += 1

            if 1720 <= self.player.x <= 1920 and 0 <= self.player.y <= 200:
                self.banderas += 1

            if 0 <= self.player.x <= 200 and 800 <= self.player.y <= 1000:
                self.banderas += 1

            if 1720 <= self.player.x <= 1920 and 800 <= self.player.y <= 1000:
                self.banderas += 1

            if self.banderas > 4:#En caso de recoger las 4 banderas no se suman mas banderas
                self.banderas = 4

            #Si se cumple lo siguiente y el jugador accede a la zona de la meta, gana el juego
            if self.score >= 300 and self.banderas == 4 and 860 <= self.player.x <= 1060 and 400 <= self.player.y <= 600:
                winner = font.render("You win",1,(255,0,0))#Score que se muestra en pantalla
                self.canvas.get_canvas().blit(winner,((850,500)))
                #highscore()

            if self.score2 >= 50 and self.banderas2 == 4 and 860 <= self.player2.x <= 1060 and 400 <= self.player2.y <= 600:
                loser = font.render("You lose",1,(255,0,0))#Score que se muestra en pantalla
                self.canvas.get_canvas().blit(loser,((850,500)))
                highscore()

            #Actualizacion de datos-------------------------------------------------------------------------------------------------------------------------
            self.player2.x, self.player2.y = self.parse_data(self.send_data()) #Recibe los datos del jugador 2 y a su vez envia los del jugador 1
            self.bullet2.y = round(self.player2.y + 17)
            self.bullet2.x, self.score2, self.banderas2 = self.parse_data2(self.send_data())
            self.police.draw(self.canvas.get_canvas())
            self.canvas.draw_background() #Dibuja el fond
            self.player.draw(self.canvas.get_canvas())#Dibuja al jugador 1
            for bullet in bullets:#dibuja las balas que existan
                bullet.draw(self.canvas.get_canvas())
            for x in objects:
                x.draw(self.canvas.get_canvas())

            text = font.render("Score: "+str(self.score),1,(255,0,0))#Score que se muestra en pantalla
            self.canvas.get_canvas().blit(text,((850,30)))
            timer = font.render("Next level in: "+str(seconds),1,(255,0,0))
            self.canvas.get_canvas().blit(timer,((1000,30)))

            if self.bullet2.x < 1920 and self.bullet2.x > 0: #En caso de estar en la ventana se mueve la bala
                    self.bullet2.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas()) #dibuja al jugador 2
            self.canvas.update() #actualiza la ventana

        pygame.quit()#Elimina la ventana de pygame

    def send_data(self): #Envia la pos al server

        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y) + ":" + str(self.bulletx) + "," + str(self.score) + "," + str(self.banderas) #La guarda en forma [id:posx,posy]
        reply = self.net.send(data) #Envia los datos
        return reply

    @staticmethod
    def parse_data(data): # Analisa los datos para el jugador 2
        try:
            d = data.split(":")[1].split(",") #Divide los datos
            return int(d[0]), int(d[1]) #Pos eje x/y
        except:
            return 0,0 #Si no hay datos la pos es 0,0

    @staticmethod
    def parse_data2(data): # Analisa los datos para las balas del jugador2
        try:
            dat = data.split(":")[2].split(",") #Divide los datos
            return int(dat[0]), int(dat[1]), int(dat[2]) #Pos eje x/score del jugador2
        except:
            return round(self.player2.y + 17) #Si no hay datos la pos es 0,0

    def highscore(self):
        with open('puntajes.json') as file: #abre el doc
            puntajes = json.load(file)

        if self.score>puntajes['Scores'][0]: #si el puntaje es mayor al mas alto lo guarda y corre todos un espacio sacando al quinto

            puntajes['Scores'] = [self.score] + puntajes['Scores'][:-1]
            puntajes["Nombres"] = [name] + puntajes["Nombres"][:-1]
            with open('puntajes.json','w') as file:
                json.dump(puntajes,file)
        elif self.score == puntajes['Scores'][0]: #si es igual no lo guarda 
            pass

        elif self.score>puntajes['Scores'][1]: #si es mayor al segundo deja al primero y corre los demas un espacio

            puntajes['Scores'] = puntajes['Scores'][0:1] + [self.score] + puntajes['Scores'][1:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:1] + [name] + puntajes["Nombres"][1:-1]
            with open('puntajes.json','w') as file:
                json.dump(puntajes,file)
        elif self.score == puntajes['Scores'][1]: #si es igual no lo guarda
            pass

        elif self.score>puntajes['Scores'][2]: #si es mayor al tercero deja el 1 y 2 y corre los demas un espacio

            puntajes['Scores'] = puntajes['Scores'][0:2] + [self.score] + puntajes['Scores'][2:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:2] + [name] + puntajes["Nombres"][2:-1]
            with open('puntajes.json','w') as file:
                json.dump(puntajes,file)
        elif self.score == puntajes['Scores'][2]: #si es igual no lo guarda
            pass

        elif self.score>puntajes['Scores'][3]: #si es mayor al cuarto deja los primeros y corre un espacio

            puntajes['Scores'] = puntajes['Scores'][0:3] + [self.score] + puntajes['Scores'][3:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:3] + [name] + puntajes["Nombres"][3:-1]
            with open('puntajes.json','w') as file:
                json.dump(puntajes,file)
        elif self.score == puntajes['Scores'][3]: #si es igual no lo guarda
            pass

        elif self.score>puntajes['Scores'][4]: #si es mayor al ultimo lo reemplaza

            puntajes['Scores'] = puntajes['Scores'][0:4] + [self.score]
            puntajes["Nombres"] = puntajes["Nombres"][0:4] + [name]
            with open('puntajes.json','w') as file:
                json.dump(puntajes,file)
        elif self.score == puntajes['Scores'][4]:#si es igual no se guarda
            pass                
        #Comprueba el score del jugador2-----------------------------------------------------------------------------------------------------
        with open('puntajes.json') as file: #abre el doc
            puntajes = json.load(file)

        if self.score2>puntajes['Scores'][0]: #si el puntaje es mayor al mas alto lo guarda y corre todos un espacio sacando al quinto

            puntajes['Scores'] = [self.score2] + puntajes['Scores'][:-1]
            puntajes["Nombres"] = [name] + puntajes["Nombres"][:-1]
            with open('puntajes.json','w') as file:
                json.dump(puntajes,file)
        elif self.score2 == puntajes['Scores'][0]: #si es igual no lo guarda 
            pass

        elif self.score2>puntajes['Scores'][1]: #si es mayor al segundo deja al primero y corre los demas un espacio

            puntajes['Scores'] = puntajes['Scores'][0:1] + [self.score2] + puntajes['Scores'][1:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:1] + [name] + puntajes["Nombres"][1:-1]
            with open('puntajes.json','w') as file:
                json.dump(puntajes,file)
        elif self.score2 == puntajes['Scores'][1]: #si es igual no lo guarda
            pass

        elif self.score2>puntajes['Scores'][2]: #si es mayor al tercero deja el 1 y 2 y corre los demas un espacio

            puntajes['Scores'] = puntajes['Scores'][0:2] + [self.score2] + puntajes['Scores'][2:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:2] + [name] + puntajes["Nombres"][2:-1]
            with open('puntajes.json','w') as file:
                json.dump(puntajes,file)
        elif self.score2 == puntajes['Scores'][2]: #si es igual no lo guarda
            pass

        elif self.score2>puntajes['Scores'][3]: #si es mayor al cuarto deja los primeros y corre un espacio

            puntajes['Scores'] = puntajes['Scores'][0:3] + [self.score2] + puntajes['Scores'][3:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:3] + [name] + puntajes["Nombres"][3:-1]
            with open('puntajes.json','w') as file:
                json.dump(puntajes,file)
        elif self.score2 == puntajes['Scores'][3]: #si es igual no lo guarda
            pass

        elif self.score2>puntajes['Scores'][4]: #si es mayor al ultimo lo reemplaza

            puntajes['Scores'] = puntajes['Scores'][0:4] + [self.score2]
            puntajes["Nombres"] = puntajes["Nombres"][0:4] + [name]
            with open('puntajes.json','w') as file:
                json.dump(puntajes,file)
        elif self.score2 == puntajes['Scores'][4]:#si es igual no se guarda
            pass

#------------------------------------------Canvas---------------------------------------------------------
class Canvas:

    def __init__(self, w, h, namec="None"): #Se crea un canvas con su ancho y altura
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(namec)


    @staticmethod
    def update():
        pygame.display.update() #Actializa la pantalla

    def draw_text(self, text, size, x, y): #Dibujado de texto 
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

    def get_canvas(self): #Obtiene lo que esta en pantalla
        return self.screen

    def draw_background(self): #Carga la imagen del fondo y la dibuja
        #bg = pygame.image.load('images/bg.jpg').convert()
        self.screen.fill((255,255,255)) #Color de relleno
        #self.screen.blit(bg, (0,0)) #Dibujado del background






