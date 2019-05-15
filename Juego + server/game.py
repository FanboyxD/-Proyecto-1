#-------------------------------Librerias-------------------------------------
import pygame
from network import Network


#-------------------------------Sprites---------------------------------------
walkRight = pygame.image.load('images/Right Car.png')
walkLeft = pygame.image.load('images/Left Car.png')
walkUp = pygame.image.load('images/Back Car.png')
walkDown = pygame.image.load('images/Front Car.png')
char = pygame.image.load('images/Back Car.png')


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
            
    def move(self, dirn): #Movimiento
        #se definen las 3 direcciones posibles
        if dirn == 0: #izquierda
            self.x += self.velocity
        elif dirn == 1: #derecha
            self.x -= self.velocity
        elif dirn == 2: #abajo
            self.y -= self.velocity
        else: #arriba
            self.y += self.velocity

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

    def __init__(self, w, h):#se define ancho x alto, se importa la red del cliente, se establece la pos inicial de los jugadores
        #Variables necesarias para el puntaje y titulo de la ventana
        self.net = Network()
        self.score = 0
        self.banderas = 0 
        self.width = w
        self.height = h
        self.player = player(50, 50)
        self.player2 = player(100,100)
        self.canvas = Canvas(self.width, self.height, "Dakar Death")

    def run(self): #Corre el juego
        clock = pygame.time.Clock() 
        run = True #inicia el run
        bullets = [] #variable para las balas
        while run: 
            clock.tick(60) #tiempo en ms de refresco de la ventana

            for event in pygame.event.get(): #analiza cada evento
                if event.type == pygame.QUIT: #Si es click en la "x" de la ventana, sale del juego
                    run = False 

            for bullet in bullets: #analisa cada bala
                if bullet.x < 1920 and bullet.x > 0: #En caso de estar en la ventana se mueve la bala
                    bullet.x += bullet.vel
                elif bullet.y < 1000 and bullet.y > 0:
                    bullet.y += bullet.vel
                elif bullet.x > 1920 or bullet.x < 0 : #En caso de salir de la ventana desaparece la bala
                    bullets.pop(bullets.index(bullet))
                else:
                    bullets.pop(bullets.index(bullet))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]: #en caso de la tecla escape tambien sale
                    run = False

            if keys[pygame.K_c]:
                if self.player.left:
                    facing = -1
                elif self.player.right:
                    facing = 1
                if len(bullets) < 1:
                    bullets.append(projectile(round(self.player.x + 15),round(self.player.y + 10), 6, (200,10,56),facing))


            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - self.player.velocity:
                    self.player.move(0)
                    self.player.left = False
                    self.player.right = True
                    self.player.up = False
                    self.player.down = False

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)
                    self.player.left = True
                    self.player.right = False
                    self.player.up = False
                    self.player.down = False

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)
                    self.player.left = False
                    self.player.right = False
                    self.player.up = True
                    self.player.down = False

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)
                    self.player.left = False
                    self.player.right = False
                    self.player.up = False
                    self.player.down = True

            if 100 <= self.player.x <= 200 and 100 <= self.player.y <= 200:
                self.score -= 3

            if 500 <= self.player.x <= 600 and 700 <= self.player.y <= 800:
                self.score -= 3

            if 650 <= self.player.x <= 750 and 300 <= self.player.y <= 400:
                self.score -= 3

            if 1100 <= self.player.x <= 1200 and 400 <= self.player.y <= 500:
                self.score -= 3

            if 1275 <= self.player.x <= 1375 and 620 <= self.player.y <= 720:
                self.score -= 3

            if 1405 <= self.player.x <= 1505 and 222 <= self.player.y <= 322:
                self.score -= 3

            if 0 <= self.player.x <= 200 and 0 <= self.player.y <= 200:
                self.banderas += 1

            if 1720 <= self.player.x <= 1920 and 0 <= self.player.y <= 200:
                self.banderas += 1

            if 0 <= self.player.x <= 200 and 800 <= self.player.y <= 1000:
                self.banderas += 1

            if 1720 <= self.player.x <= 1920 and 800 <= self.player.y <= 1000:
                self.banderas += 1

            if self.banderas > 4:
                self.banderas = 4

            if self.score >= 50 and self.banderas == 4 and 860 <= self.player.x <= 1060 and 400 <= self.player.y <= 600:
                pass

            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            for bullet in bullets:
                bullet.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self): #Envia la pos al server

        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data): # Analisa los datos 
        try:
            d = data.split(":")[1].split(",") #Divide los datos
            return int(d[0]), int(d[1])
        except:
            return 0,0 #Si no hay datos la pos es 0,0


class Canvas:

    def __init__(self, w, h, name="None"): #Se crea un canvas con su ancho y altura
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)


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
        bg = pygame.image.load('images/bg.jpg').convert()#Convierte la imagen a un formato aceptado   
        self.screen.fill((255,255,255)) #Color de relleno
        self.screen.blit(bg, (0,0)) #Dibujado del background






