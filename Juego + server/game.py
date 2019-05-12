import pygame
from network import Network



walkRight = pygame.image.load('images/Right Car.png')
walkLeft = pygame.image.load('images/Left Car.png')
walkUp = pygame.image.load('images/Back Car.png')
walkDown = pygame.image.load('images/Front Car.png')
char = pygame.image.load('images/Back Car.png')

class player():
    width = height = 50
    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 10
        self.color = color
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def draw(self, win):
        if self.left:  
            win.blit(walkLeft, (self.x,self.y))                       
        elif self.right:
            win.blit(walkRight, (self.x,self.y))
        elif self.up:
            win.blit(walkUp, (self.x,self.y))
        elif self.down:
            win.blit(walkDown, (self.x,self.y))
        else:
            win.blit(walkUp, (self.x,self.y))
            
    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = player(50, 50)
        self.player2 = player(100,100)
        self.canvas = Canvas(self.width, self.height, "Dakar Death")

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

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

            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)


    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        bg = pygame.image.load('images/bg.jpg').convert()       
        self.screen.fill((255,255,255))
        self.screen.blit(bg, (0,0))






