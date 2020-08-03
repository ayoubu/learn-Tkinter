import pygame
import sys
from pygame.locals import *
from random import *
import math

'''
向界面中添加一个摩擦摩擦的地方
'''

class Ball(pygame.sprite.Sprite):
    def __init__(self, image, position, speed,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.width, self.height = bg_size
        self.radius = self.rect.width/2   #调用pygame自带碰撞检测函数的原型物体碰撞检测时，需要定义半径属性
    
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

class Glass(pygame.sprite.Sprite):
    def __init__(self, glass_image,mouse_image, bg_size):
        #初始化动画精灵
        pygame.sprite.Sprite.__init__(self)     # 记得添加self

        self.glass_image = pygame.image.load(glass_image).convert_alpha()
        self.glass_rect = self.glass_image.get_rect()
        self.glass_rect.left, self.glass_rect.top = \
            (bg_size[0]-self.glass_rect.width)//2, \
            bg_size[1]-self.glass_rect.height

        self.mouse_image = pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left,self.mouse_rect.top = self.glass_rect.left, self.glass_rect.top
        pygame.mouse.set_visible(False)


def main():
    pygame.init()
    pygame.mixer.init()

    # 设置背景音效
    pygame.mixer.music.load("bg_music.ogg")
    pygame.mixer.music.play()

    #添加音效
    loser_sound = pygame.mixer.Sound("loser.wav")
    laugh_sound = pygame.mixer.Sound("laugh.wav")
    winner_sound = pygame.mixer.Sound("winner.wav")
    hole_sound = pygame.mixer.Sound("hole.wav")

    #音乐播放结束时游戏结束
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)

    ball_image = "gray_ball.png"
    bg_image = "background.png"
    glass_image = "glass.png"
    mouse_image = "hand.png"

    running = True
    bg_size = width, height = 1024, 681
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("Play the ball - Demo")

    # 设置背景
    background = pygame.image.load(bg_image).convert_alpha()
    # 创建五个小球
    BALL_NUM = 5
    balls = []
    group = pygame.sprite.Group()   #创建一个pygame的Group()对象，用于碰撞检测

    for i in range(BALL_NUM):
        position = randint(0,width-100), randint(0, height -100)
        speed = [randint(-10,10), randint(-10,10)]
        ball = Ball(ball_image,position,speed, bg_size)
        #检测当前生成的小球是否与已生成的小球重合
        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):  
            ball.rect.left, ball.rect.top = randint(0,width-100), randint(0, height -100)
        balls.append(ball)
        group.add(ball)
    glass = Glass(glass_image, mouse_image, bg_size)
    # 设置游戏的帧率
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == GAMEOVER:
                loser_sound.play()
                pygame.time.delay(3000)
                laugh_sound.play()
                pygame.time.delay(3000)
                running = False

        # 将背景绘制在屏幕上
        screen.blit(background,(0,0))
        screen.blit(glass.glass_image,glass.glass_rect)   # 每一帧都绘制一次玻璃面板
        #先获取鼠标的位置
        glass.mouse_rect.left, glass.mouse_rect.top = pygame.mouse.get_pos()
        if glass.mouse_rect.left < glass.glass_rect.left:
            glass.mouse_rect.left = glass.glass_rect.left
        if glass.mouse_rect.left > glass.glass_rect.right - glass.mouse_rect.width:
            glass.mouse_rect.left = glass.glass_rect.right - glass.mouse_rect.width
        if glass.mouse_rect.top < glass.glass_rect.top:
            glass.mouse_rect.top = glass.glass_rect.top
        if glass.mouse_rect.top > glass.glass_rect.bottom - glass.mouse_rect.height:
            glass.mouse_rect.top = glass.glass_rect.bottom - glass.mouse_rect.height
       
        screen.blit(glass.mouse_image, glass.mouse_rect)   # 每一帧都画一次鼠标的位置

        # 将五个小球绘制在屏幕之上
        for each in balls:
            each.move()
            screen.blit(each.image, each.rect)
        
        for each in group:
            group.remove(each)
            if pygame.sprite.spritecollide(each,group,False,pygame.sprite.collide_circle):
                each.speed[0] = -each.speed[0]
                each.speed[1] = -each.speed[1]
            group.add(each)
        pygame.display.flip()
        clock.tick(30)
        

if __name__ == "__main__":
    main()