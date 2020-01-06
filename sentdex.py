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
gameDisplay = pygame.display.set_mode((display_width, display_height))
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
    

def crash():
    textSurface, textRect = create_text('You crashed')
    gameDisplay.blit(textSurface, textRect)
    pygame.display.update()
    time.sleep(2)

def showScore(score):
    font = pygame.font.SysFont(None, 50)
    surface = font.render("score: " + str(score), True, black)
    gameDisplay.blit(surface, (0, 0))

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
        pygame.draw.rect(gameDisplay, self.color, rect)


while True:
    # Car
    x = display_width * 0.45
    y = display_height * 0.8
    x_vel = 0
    horizontal_speed = 5
    (car_width,car_height) = carImg.get_rect().size

    # Object
    initYPos = -300
    rect1 = Object(
        random.randrange(0, display_width),
        initYPos,
        7,
        100,
        100,
        generateRGB()
    )
    score = 0

    while True:
        for event in pygame.event.get(): # Event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

        # Clear the screen / The background
        gameDisplay.fill(white)

        gameDisplay.blit(carImg, (x, y))
        rect1.draw()
        showScore(score)
        # Object out of screen Logic
        if rect1.y > display_height:
            rect1.y = initYPos
            rect1.x = random.randrange(0, display_width)
            # Score logic and challenge
            score += 1
            rect1.fallSpeed += 1
            horizontal_speed += 1
            rect1.width += 5
            rect1.color = generateRGB()

        # Bundries logic
        if x < 0 or x > display_width - car_width:
            crash()
            break

        # Car and Object collision
        objectBottom = rect1.y + rect1.height
        if objectBottom > y:
            # I don't understand what I wrote but it works XD
            if rect1.x < (x + car_width) and (rect1.x + rect1.width) > x:
                crash()
                break

        pygame.display.update()
        clock.tick(60)

# TODO multiple blocks
