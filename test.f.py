import pygame
import sys
from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode((640,480))
xpos=50
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    #xpos+=1
    pressed_keys=pygame.key.get_pressed()
    if pressed_keys[K_RIGHT]:
        xpos+=1
    if pressed_keys[K_LEFT]:
        xpos-=1
    screen.fill((255,255,255))
    pygame.draw.circle(screen,(0,255,0),(xpos,200),20)
    pygame.display.update()
