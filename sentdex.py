import random
import pygame
import time
import sys

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


while True:
    # Car
    x = display_width * 0.45
    y = display_height * 0.8
    x_vel = 0
    horizontal_speed = 5
    (car_width,car_height) = carImg.get_rect().size

    # Object
    rectX = random.randrange(0, display_width)
    rectY = -300
    rectYN = rectY
    rectYSpeed = 7
    rectW = 100
    rectH = 100
    rectColor = generateRGB()

    score = 0

    gameExit = False
    # WHILE LOOP
    while not gameExit:
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
        rect = (rectX, rectYN, rectW, rectH)
        pygame.draw.rect(gameDisplay, rectColor, rect)
        rectYN += rectYSpeed
        showScore(score)
        # Object out of screen Logic
        if rectYN > display_height:
            rectYN = rectY
            rectX = random.randrange(0, display_width)
            # Score logic and challenge
            score += 1
            rectYSpeed += 1
            horizontal_speed += 1
            rectW += 1
            rectColor = generateRGB()

        # Bundries logic
        if x < 0 or x > display_width - car_width:
            crash()
            break

        # Car and Object collision
        objectBottom = rectYN + rectH
        if objectBottom > y:
            # I don't understand what I wrote but it works XD
            if rectX < (x + car_width) and (rectX + rectW) > x:
                crash()
                break

        pygame.display.update()
        clock.tick(60)

# TODO multiple blocks