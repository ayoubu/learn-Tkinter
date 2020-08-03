import pygame
import sys
from pygame.locals import *
from random import *
import math

'''
播放音效： 使用pygame.mixer.Sound() 模块
        ————play()              播放音效
        ————stop()              停止播放
        ————fadeout()           淡出
        ————set_valume()        设置音量
        ————get_valume()        获取音量
        ————get_num_channels()  计算该音效播放了多少次
        ————get_length()        获得该音效的长度
        ————get_raw()           将该音效以二进制格式的字符串返回
播放背景音：使用pygame.mixer.music() 
        ————load()
        ————play()
        ————rewind()            重新播放
        ————stop()
        ————pause()
        ————unpause()           恢复播放
        ————fadeout()           淡出
        ————set_volume()
        ————queue()             将音乐文件放入待播放的列表中
        ————set_endevent()      在播放完音乐的时候发送事件
        ————get_endevent()      获取音乐播放完毕时发送的事件类型
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