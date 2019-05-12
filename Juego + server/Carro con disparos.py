import pygame
pygame.init()

win = pygame.display.set_mode((1920,1000))
pygame.display.set_caption("First Game")

walkRight = pygame.image.load('images/Right Car.png')
walkLeft = pygame.image.load('images/Left Car.png')
walkUp = pygame.image.load('images/Back Car.png')
walkDown = pygame.image.load('images/Front Car.png')
bg = pygame.image.load('images/bg.jpg').convert()
char = pygame.image.load('images/Back Car.png')


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.Brake = False
        self.BrakeCount = 1
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.standing = True

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
    car.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

fps = pygame.time.Clock()
bullets = []
car = player(300,410,35,30)        
run = True
while run:
    fps.tick(144)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 1920 and bullet.x > 0:
            bullet.x += bullet.vel
        elif bullet.y < 1000 and bullet.y > 0:
            bullet.y += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_c]:
        if car.left:
            facing = -1
        elif car.right:
            facing = 1
        if len(bullets) < 1:
            bullets.append(projectile(round(car.x + (car.width//2)),round(car.y + (car.height//2)), 6, (200,10,56),facing))
            
        
    if not(car.Brake):
        if keys[pygame.K_LEFT] and car.x > car.vel: 
            car.x -= car.vel
            car.left = True
            car.right = False
            car.up = False
            car.down = False
            car.standing = False

        if keys[pygame.K_RIGHT] and car.x < 1920 - car.vel - car.width:  
            car.x += car.vel
            car.right = True
            car.left = False
            car.up = False
            car.down = False
            car.standing = False
            
        if keys[pygame.K_UP] and car.y > car.vel:
            car.y -= car.vel
            car.left = False
            car.right = False
            car.up = True
            car.down = False
            car.standing = False

        if keys[pygame.K_DOWN] and car.y < 1000 - car.height - car.vel:
            car.y += car.vel
            car.left = False
            car.up = False
            car.down = True
            car.right = False
            car.standing = False

        if keys[pygame.K_SPACE]:
            car.Brake = True
            car.right = False
            car.left = False
            car.up = True
            car.down = False
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
