import random
import sys
import time

import pygame

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0) # Based on RGB

display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Race like')
clock = pygame.time.Clock() # Defining the clock

carImg = pygame.image.load('race_car.png')



def generateRGB():
    r = random.randrange(0, 217)
    g = random.randrange(0, 217)
    b = random.randrange(0, 217)
    return (r, g, b)

def create_text(text):
    myFont = pygame.font.Font('freesansbold.ttf', 75)
    # 1l Creates a surface
    textSurface = myFont.render(text, True, red)
    textRect = textSurface.get_rect()
    textRect.center = (display_width // 2, display_height // 2)
    return (textSurface, textRect)
    

def showMessage(message):
    textSurface, textRect = create_text(message)
    screen.blit(textSurface, textRect)
    pygame.display.update()
    time.sleep(2)

def showScore(score):
    font = pygame.font.SysFont(None, 50)
    surface = font.render("score: " + str(score), True, black)
    screen.blit(surface, (0, 0))

class Object:
    def __init__(self, x, y, fallSpeed, width, height, color):
        self.x = x
        self.y = y
        self.fallSpeed = fallSpeed
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self):
        self.y += self.fallSpeed
        rect = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)

genInterval = 1000

while True:
    # Car
    x = display_width * 0.45
    y = display_height * 0.8
    x_vel = 0
    horizontal_speed = 5
    (car_width,car_height) = carImg.get_rect().size

    score = 0
    objs = []
    # object generation properties
    objWidth = 100
    fallSpeed = 7
    

    eventGenObj = pygame.USEREVENT + 1
    pygame.time.set_timer(eventGenObj, int(genInterval))

    gameExit = False
    while not gameExit:
        for event in pygame.event.get(): # Event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == eventGenObj:
                # DefObject
                initYPos = -300
                objIns = Object(
                    random.randrange(0, display_width - objWidth),
                    initYPos,
                    fallSpeed,
                    objWidth,
                    100,
                    generateRGB()
                )
                objs.append(objIns)
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_RIGHT]:
                x_vel = 0
            elif keys_pressed[pygame.K_LEFT]:
                x_vel = -horizontal_speed
            elif keys_pressed[pygame.K_RIGHT]:
                x_vel = horizontal_speed
            else:
                x_vel = 0

        x += x_vel

        for obj in objs:
            # Car and Object collision
            objectBottom = obj.y + obj.height
            if objectBottom > y:
                # I don't understand what I wrote but it works XD
                if obj.x < (x + car_width) and (obj.x + obj.width) > x:
                    gameExit = True
                    showMessage("You crashed")
                    break
            # Object out of screen Logic
            if obj.y > display_height:
                objs.remove(obj)
                # Score and challenge
                if score >= 15:
                    genInterval *= 0.72
                    gameExit = True
                    showMessage("NEXT LEVEL")
                    break
                score += 1
                fallSpeed += 0.1
                objWidth += 1

        # Clear the screen / The background
        screen.fill(white)

        screen.blit(carImg, (x, y))

        for obj in objs:
            obj.draw()

        """Score should be the last to draw
        so that nothing ovelaps on top of it"""
        showScore(score)

        # Bundries logic
        if x < 0 or x > display_width - car_width:
            showMessage("You crashed")
            break

        

        pygame.display.update()
        clock.tick(60)

# TODO Fix sleep issue
