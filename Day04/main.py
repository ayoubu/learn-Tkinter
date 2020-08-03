import pygame
import sys
from pygame.locals import *
from random import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, image, position, speed,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.width, self.height = bg_size
    
    # 移动小球的位置
    def move(self):
        self.rect = self.rect.move(self.speed) 
        move_x,move_y = 0, 0
        #判断 X 位置是否越界, 重新初始化X的位置
        if self.rect.right < 0:
            self.rect.left = self.width
        if self.rect.left > self.width:
            self.rect.right = 0
        #判断 y 是否越界,重新初始化Y的位置
        if self.rect.top > self.height:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = self.height


def main():
    pygame.init()

    ball_image = "gray_ball.png"
    bg_image = "background.png"

    running = True
    bg_size = width, height = 1024, 681
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("Play the ball - Demo")

    # 设置背景
    background = pygame.image.load(bg_image).convert_alpha()
    
    balls = []
    for i in range(5):
        position = randint(0,width-100), randint(0, height -100)
        speed = [randint(-10,10), randint(-10,10)]
        ball = Ball(ball_image,position,speed, bg_size)
        balls.append(ball)

    # 设置游戏的帧率
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        # 将背景绘制在屏幕上
        screen.blit(background,(0,0))
        # 将五个小球绘制在屏幕之上
        for each in balls:
            each.move()
            screen.blit(each.image, each.rect)
        pygame.display.flip()
        clock.tick(30)
        

if __name__ == "__main__":
    main()