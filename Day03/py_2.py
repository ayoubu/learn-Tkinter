import pygame
import sys
from pygame.locals import *

pygame.init()

size = width, height = 500, 600
bg = (255,255,255)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("裁剪功能演示")

oturtle = pygame.image.load("02.png")
#turtle = pygame.transform.chop(oturtle,(200,200,100,100))
turtle = oturtle
position = turtle.get_rect()
position.center = width//2, height//2

clicked = False
mouse_down = False
start_x, start_y = 0, 0
end_x, end_y = 0, 0
draw_rect = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        #鼠标点击事件捕捉
        if event.type == MOUSEBUTTONDOWN:
            start_pos = pygame.mouse.get_pos()
            clicked = False
            draw_rect = False
            mouse_down = True
            print("MOUSEBUTTONDOWN")
        if event.type == MOUSEBUTTONUP:
            mouse_down = False
            if not draw_rect:
                clicked = True
            print("MOUSEBUTTONUP")
        if event.type == MOUSEMOTION:
            if mouse_down:
                end_pos = pygame.mouse.get_pos()
                start_x = start_pos[0]
                start_y = start_pos[1]
                end_x = end_pos[0] - start_pos[0]   #获取x的偏移量
                end_y = end_pos[1] - start_pos[1]  #获取y的偏移量
                draw_rect = True 
                print("MOUSEMOTION")
    
    screen.fill(bg)
    screen.blit(turtle,position)
    pygame.draw.rect(screen,(0,0,0), position, 1)
    if draw_rect:
        pygame.draw.rect(screen,(0,0,0),(start_x, start_y, end_x, end_y), 1)

    pygame.display.flip()
    clock.tick(30)