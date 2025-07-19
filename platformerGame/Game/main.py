import pygame
#https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/optimization


#initialize pygame
pygame.init()

#Framerate
clock = pygame.time.Clock()

#sounds we are going to use for our game
bulletSound = pygame.mixer.Sound('bullet.mp3')
hitSound = pygame.mixer.Sound('hit.mp3')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

bg_color = "grey"
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 480

#Our game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("First Game")

#Charecter Animation (the addition of images)
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft =  [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

#this will keep the score of the player
score = 0

#Object oriented Programming
#we are now going to create a class to hold our variables and make our code a more organized.
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y, 11, 29, 52) # The elements in the hitbox are (top left x, top left y, width, height)

        
    def draw(self,screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if not (self.standing):
            if self.left:
                screen.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(screen, (255,0,0), self.hitbox,2) # To draw the hit box around the player

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        screen.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i<300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
    
    
#here we create a class to create projectiles
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8*facing
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)

class enermy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.velocity = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
        

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
                
            if self.velocity > 0:
                screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else: 
                screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            #self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            pygame.draw.rect(screen, (255,0,0), self.hitbox,2) # Draws the hit box around the enemy
            pygame.draw.rect(screen, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def move(self):
        if self.velocity > 0:
            if self.x < self.velocity + self.path[1]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity*-1
                self.walkCount = 0
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity*-1
                self.walkCount = 0
                
        # NEW METHOD
    def hit(self):  # This will display when the enemy is hit
        hitSound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

# For moving a Charecter we have to define a couple of variables:
#jumping variables

#Drawing the background image at (0,0)
def redrawGameWindow():
    # global walkCount
    # We have 9 images for our walking animation, I want to show the same image for 3 frames
    # so I use the number 27 as an upper bound for walkCount because 27 / 3 = 9. 9 images shown
    # 3 times each animation.
    
    screen.blit(bg, (0,0)) #this will draw our background window
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    screen.blit(text, (300, 10))
    man.draw(screen)
    goblin.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()


#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(200,410,64,64)
goblin = enermy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = [] #this is for the projectiles
running = True
while running: #game loop
    #framerate
    clock.tick(27)

    #this is to check if the enermy has made contact with our player
    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
        
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))
            
    keys = pygame.key.get_pressed()
    
    
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        
        if len(bullets)<5:
            bullets.append(projectile(round(man.x+man.width//2), round(man.y+man.height//2), 6, "black", facing))
            
        shootLoop = 1
        
    if keys[pygame.K_LEFT] and man.x > man.velocity: 
        man.x -=man.velocity
        man.left = True
        man.right = False
        man.standing = False
        
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.velocity:  
        man.x += man.velocity
        man.left = False
        man.right = True
        man.standing = False
    
    else:
        man.standing = True
        man.walkCount = 0
         
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5
            man.jumpCount -= 1
        else:
            man.jumpCount = 10
            man.isJump = False
    
    redrawGameWindow()
    
pygame.quit()