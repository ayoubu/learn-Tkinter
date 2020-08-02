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

mouse_down = False
move_rect = False
select_rect = pygame.Rect(0,0,0,0)
rect_x, rect_y = 0,0
draw_rect = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        #鼠标点击事件捕捉
        if event.type == MOUSEBUTTONDOWN:
            move_rect = False
            start_pos = pygame.mouse.get_pos()
            
            if start_pos[0] > select_rect.left and start_pos[0] < select_rect.right \
                and start_pos[1] > select_rect.top and start_pos[1] <  select_rect.bottom:
                move_rect = True
                print("move_rect = True")
            else:
                select_rect.left, select_rect.top = start_pos
            draw_rect = False
            mouse_down = True
            print("MOUSEBUTTONDOWN")
        if event.type == MOUSEBUTTONUP:
            mouse_down = False
            # if draw_rect:
            #     move_rect = False
            print("MOUSEBUTTONUP")
        if event.type == MOUSEMOTION:
            if mouse_down:
                if move_rect:
                    pos = pygame.mouse.get_pos()
                    rect_x = pos[0]
                    rect_y = pos[1]
                else:
                    end_pos = pygame.mouse.get_pos()
                    select_rect.width, select_rect.height = end_pos[0] - start_pos[0], \
                        end_pos[1] - start_pos[1] 
                    draw_rect = True 
                    print("MOUSEMOTION")
                    
    
    screen.fill(bg)
    screen.blit(turtle,position)
    pygame.draw.rect(screen,(0,0,0), position, 1)
    if draw_rect:
        pygame.draw.rect(screen,(0,0,0),select_rect, 1)
    if move_rect:
        capture = screen.subsurface(select_rect).copy()
        cap_rect = capture.get_rect()
        cap_rect.center = rect_x ,rect_y
        screen.blit(capture,cap_rect)
        print("move_rect")


    pygame.display.flip()
    clock.tick(30)