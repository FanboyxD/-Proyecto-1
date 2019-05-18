import pygame
from pygame.locals import *
import os
import random
import sys
import _thread
import time
from threading import Timer
pygame.init()

win = pygame.display.set_mode((1920,1000))
pygame.display.set_caption("First Game")

walkRight = pygame.image.load('images/Right Car.png')
walkLeft = pygame.image.load('images/Left Car.png')
walkUp = pygame.image.load('images/Back Car.png')
walkDown = pygame.image.load('images/Front Car.png')
bg = pygame.image.load('images/bg.jpg').convert()
char = pygame.image.load('images/Back Car.png')
Score = 0

bulletSound = pygame.mixer.Sound("sonidos/car_shoot.wav")
crashSound = pygame.mixer.Sound("sonidos/car_crash.wav")
hitSound = pygame.mixer.Sound("sonidos/car_hit.wav")
moving = pygame.mixer.Sound("sonidos/car_moving.wav")
brake = pygame.mixer.Sound("sonidos/car_brake.wav")

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 4
        self.Brake = False
        self.BrakeCount = 1
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.standing = True
        self.hitbox = (self.x+20,self.y,28,60) #dimensiones de la hitbox del jugador

    def draw(self,win):
        if not(self.standing):
            if self.left:  
                win.blit(walkLeft, (self.x,self.y))                       
            if self.right:
                win.blit(walkRight, (self.x,self.y))
            if self.up:
                win.blit(walkUp, (self.x,self.y))
            if self.down:
                win.blit(walkDown, (self.x,self.y))
        else:
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            if self.left:
                win.blit(walkLeft[0],(self.x,self.y))
            if self.up:
                win.blit(walkUp[0],(self.x,self.y))
            if self.down:
                win.blit(walkDown[0],(self.x,self.y))
        self.hitbox = (self.x,self.y+1,30,20)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def hit(self): #reseteo en la posicion del jugador si muere
        self.x = 60
        self. y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans",100)
        text = font1.render("-5",1,(255,0,0))
        win.blit(text,(250-(text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class enemy(object):
    walkRight = [pygame.image.load("images/Enemy sprites Right.png")]
    walkLeft = [pygame.image.load("images/Enemy sprites Left.png")]
    walkUp = [pygame.image.load("images/Enemy sprites Up.png")]
    walkDown = [pygame.image.load("images/Enemy sprites Down.png")]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  #Limite en eje x de donde llega el enemigo
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
        print("1 hit + 1pto")

class obstacles(object):
    img = [pygame.image.load(os.path.join("images","wall.png")),pygame.image.load(os.path.join("images","cactus.png")),pygame.image.load(os.path.join("images","rocks.png"))]
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x+30,self.y+30,self.width-95,self.height-95)
        self.count = 0
    def draw(self,win):
        self.hitbox = (self.x+30,self.y+30,self.width-95,self.height-95)
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

class cactus(obstacles):
    img = pygame.image.load(os.path.join("images","cactus.png"))
    def draw(self,win):
        self.hitbox = (self.x,self.y,self.width-20,self.height-280)
        win.blit(self.img,(self.x,self.y))
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def collide(self,rect):
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
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0]+self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 15 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y),self.radius)

def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render("Score: "+str(Score),1,(255,0,0))#Score que se muestra en pantalla
    win.blit(text,((850,30)))
    timer = font.render("Next level in: "+str(seconds),1,(255,0,0))
    win.blit(timer,((1000,30)))
    car.draw(win)
    police.draw(win)        
    for x in objects:
        x.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

    
font = pygame.font.SysFont("comicsans",30,True,True)
police = enemy(100, 510, 35, 30, 1920)
fps = pygame.time.Clock()
pygame.time.set_timer(USEREVENT+1,500)
pygame.time.set_timer(USEREVENT+2,random.randrange(2000,3500))#tiempo en que salen los obstaculos
bullets = []
car = player(300,410,35,30)
shootLoop = 0   
run = True
objects = [] #lista donde estan los obstaculos


start_ticks=pygame.time.get_ticks() #starter tick

while run:
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
    fps.tick(144)

    if seconds>120: #Tiempo antes de subir de nivel
        Level += 1 #Aumenta la variable de nivel
    
    
    for objectt in objects: #Borra los obstaculos cuando salen de la pantalla
        if objectt.collide(car.hitbox):
            pygame.time.delay(1000)
            Score -= 1
        objectt.x -= 1.4
        if objectt.x < -objectt.width * -1:
            objects.pop(objects.index(objectt))
            
    if police.visible == True:
        if car.hitbox[1] < police.hitbox[1]+police.hitbox[3] and car.hitbox[1]+car.hitbox[3] > police.hitbox[1]: #Rango donde el judagor recibe daño
            if car.hitbox[0] + car.hitbox[2] > police.hitbox[0] and car.hitbox[0] < police.hitbox[0] + police.hitbox[2]:#Rango donde el judagor recibe daño
                moving.stop()
                crashSound.play()
                car.hit()
                Score -= 5
    
    if shootLoop > 0: #limitador de disparos
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == USEREVENT+1:
            car.vel += 1
            car.vel -=1
        if event.type == USEREVENT+2:
            r=random.randrange(0,2)#Genera spawns aleatorios
            if r == 0:
                objects.append(obstacles(1920,400,64,64))#coordenadas de spawn de los muros
            else:
                objects.append(cactus(1920,600,48,320)) #coordenadas de spawn de los cactus
                objects.append(rocks(1920,200,64,64))
                
    for bullet in bullets:
        if police.visible == True:
            if bullet.y - bullet.radius < police.hitbox[1]+police.hitbox[3] and bullet.y + bullet.radius > police.hitbox[1]:#Rango para golpear al enemigo
                if bullet.x + bullet.radius > police.hitbox[0] and bullet.x - bullet.radius < police.hitbox[0] + police.hitbox[2]:#Rango para golpear al enemigo
                    police.hit()
                    bullets.pop(bullets.index(bullet))
                    Score += 1
                    hitSound.play()
                    moving.stop() #sonidos
                
        if bullet.x < 1920 and bullet.x > 0:
            bullet.x += bullet.vel
        elif bullet.y < 1000 and bullet.y > 0:
            bullet.y += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_c] and shootLoop == 0:
        moving.stop() #sonidos
        bulletSound.play()
        if car.left:
            facing = -1
        elif car.right:
            facing = 1
        if len(bullets) < 1:
            bullets.append(projectile(round(car.x + (car.width//2)),round(car.y + (car.height//2)), 6, (200,10,56),facing))
        shootLoop = 1
        
    if not(car.Brake):
        if keys[pygame.K_LEFT] and car.x > car.vel: 
            car.x -= car.vel
            car.left = True
            car.right = False
            car.up = False
            car.down = False
            car.standing = False
            moving.play() #sonidos

        if keys[pygame.K_RIGHT] and car.x < 1920 - car.vel - car.width:  
            car.x += car.vel
            car.right = True
            car.left = False
            car.up = False
            car.down = False
            car.standing = False
            moving.play() #sonidos
            
        if keys[pygame.K_UP] and car.y > car.vel:
            car.y -= car.vel
            car.left = False
            car.right = False
            car.up = True
            car.down = False
            car.standing = False
            moving.play() #sonidos
            
        if keys[pygame.K_DOWN] and car.y < 1000 - car.height - car.vel:
            car.y += car.vel
            car.left = False
            car.up = False
            car.down = True
            car.right = False
            car.standing = False
            moving.play()#sonidos
            
        if keys[pygame.K_SPACE]:
            moving.stop()
            car.Brake = True
            car.right = False
            car.left = False
            car.up = True
            car.down = False
            brake.play() #sonidos
    else:
        if  car.BrakeCount >= -0:
            car.y -= (car.BrakeCount * abs(car.BrakeCount))
            car.BrakeCount -= 1
        else: 
            car.BrakeCount = 0
            car.Brake = False
    pygame.display.update() 
    redrawGameWindow()
pygame.quit()
