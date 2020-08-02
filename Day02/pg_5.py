import pygame
import sys
from pygame.locals import *

'''
控制小兔子的方向
'''
# 初始化Pygame
pygame.init()

size = width, height = 1200, 600

bg = (255,255,255)  #RGB
speed = [5,0]
# 创建指定大小的窗口
screen = pygame.display.set_mode(size, RESIZABLE)
# 设置窗口标题
pygame.display.set_caption("初次见面，请多关照")

# 加载图片
turtle = pygame.image.load("02.png") #surface对象指的是图像对象
turtle_right = pygame.transform.rotate(turtle,270)
turtle_bottom= pygame.transform.rotate(turtle,180)
turtle_left = pygame.transform.rotate(turtle,90)
turtle_top = turtle
turtle = turtle_top

fullscreen = False
# 获取图像的位置矩形
position = turtle.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == KEYDOWN:
            
            # 全屏 F11
            if event.key == K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    size = width, height = 1900, 1080
                    screen = pygame.display.set_mode(size, FULLSCREEN | HWSURFACE)
                else:
                    size = width, height = 1200, 600
                    screen = pygame.display.set_mode(size)
                    
        # 用户调整窗口尺寸
        if event.type == VIDEORESIZE:
            size = event.size
            width, height = size
            #if width > turtle.get_width() and height > turtle.get_height():
                #screen = pygame.display.set_mode(size, RESIZABLE)
            if width <= turtle.get_width():
                width = turtle.get_width() + 5
                size = width, height
            elif height <= turtle.get_height():
                height = turtle.get_height() + 5
                size = width, height
            elif width <= turtle.get_width() and height <= turtle.get_height():
                width = turtle.get_width() + 5
                height = turtle.get_height() + 5
                size = width, height
            screen = pygame.display.set_mode(size, RESIZABLE)
                
        # 重新调整位置
        if position.right > width:
            position.right = width -1
        if position.bottom > height:
            position.bottom = height -1


    
    # 移动图像
    position = position.move(speed)

    if position.right > width:
        turtle = turtle_right
        position = turtle_rect = turtle.get_rect()
        position.left = width - turtle_rect.width
        speed =  [0,5]
    if position.bottom > height:
        turtle = turtle_bottom
        position = turtle_rect = turtle.get_rect()
        position.left = width - turtle_rect.width
        position.top = height - turtle_rect.height
        speed =  [-5,0]
    if position.left <0:
        turtle = turtle_left
        position = turtle_rect = turtle.get_rect()
        position.top = height - turtle_rect.height
        speed =  [0,-5]
    if position.top <0:
        turtle = turtle_top
        position = turtle_rect = turtle.get_rect()
        speed =  [5, 0]
    
    # 填充背景
    screen.fill(bg)
    # 更新图像
    screen.blit(turtle,position)
    # 更新界面
    pygame.display.flip()
    # 延时10毫秒
    pygame.time.delay(10)   #不要轻易调节这个
    