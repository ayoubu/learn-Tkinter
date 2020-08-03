import pygame
import sys
from pygame.locals import *
from random import *
import math

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

def Crash_test(balls):
    count = len(balls)
    for i in range(count):
        for j in range(i+1,count):
            x2 = (balls[i].rect.centerx - balls[j].rect.centerx) * \
                 (balls[i].rect.centerx - balls[j].rect.centerx)
            y2 = (balls[i].rect.centery - balls[j].rect.centery) * \
                 (balls[i].rect.centery - balls[j].rect.centery)
            distance = math.sqrt(x2 + y2)
            if distance < 100:
                print("糟糕，球撞在一起了...")

def collide_check(item, target):
    col_balls = []
    for each in target:
        distance = math.sqrt(math.pow((item.rect.centerx-each.rect.centerx),2) +\
             math.pow((item.rect.centery-each.rect.centery),2))
        if distance <= (item.rect.width + each.rect.width)/2:
            col_balls.append(each)
    return col_balls



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
    # 创建五个小球
    BALL_NUM = 5
    balls = []
    for i in range(BALL_NUM):
        position = randint(0,width-100), randint(0, height -100)
        speed = [randint(-10,10), randint(-10,10)]
        ball = Ball(ball_image,position,speed, bg_size)
        while collide_check(ball, balls):  #检测当前生成的小球是否与已生成的小球重合
            ball.rect.left, ball.rect.top = randint(0,width-100), randint(0, height -100)
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
        
        for i in range(BALL_NUM):
            item = balls.pop(i)     #使用pop方法取出第i个小球
            if collide_check(item, balls):
                item.speed[0] = -item.speed[0]
                item.speed[1] = -item.speed[1]
            balls.insert(i,item)   #使用insert方法将小球放回原位
        pygame.display.flip()
        clock.tick(30)
        

if __name__ == "__main__":
    main()