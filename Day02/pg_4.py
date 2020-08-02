import pygame
import sys
from pygame.locals import *

'''
控制小兔子的方向
'''
# 初始化Pygame
pygame.init()

size = width, height = 1200, 600
speed = [-1,1]
bg = (255,255,255)

# 创建指定大小的窗口
screen = pygame.display.set_mode(size, RESIZABLE)
# 设置窗口标题
pygame.display.set_caption("初次见面，请多关照")

fullscreen = False

# 加载图片
turtle = pygame.image.load("02.png") #surface对象指的是图像对象
flip = True
# 获取图像的位置矩形
position = turtle.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                speed = [0, 1]
            if event.key == K_UP:
                speed = [0, -1]
            if event.key == K_LEFT:
                if flip:
                    turtle = pygame.transform.flip(turtle, True, False)
                    flip = not flip
                speed = [-1, 0]
            if event.key == K_RIGHT:
                if not flip:
                    turtle = pygame.transform.flip(turtle, True, False)
                    flip = not flip
                speed = [1, 0]
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

    if position.left < 0 or position.right > width:
        # 翻转图像
        turtle = pygame.transform.flip(turtle, True, False)
        flip = not flip
        # 反向移动
        speed[0] = -speed[0]
    if position.top < 0 or position.bottom > height:
        speed[1] = -speed[1]
    
    # 填充背景
    screen.fill(bg)
    # 更新图像
    screen.blit(turtle,position)
    # 更新界面
    pygame.display.flip()
    # 延时10毫秒
    if fullscreen:
        pygame.time.delay(2)
    else:
        pygame.time.delay(10)
    