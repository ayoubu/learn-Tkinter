import pygame
import sys
from pygame.locals import *
from random import *
import math

'''
根据鼠标滑动的频率控制小球
    1.为每个小球设置一个不同的目标；
    2.创建一个motion变量来记录鼠标每一秒中产生的事件数量
    3.为小球创建一个check（）方法，用于判断在1秒钟时间内产生的事件数量匹配是否为此目标
    4.添加一个自定义事件，每一秒触发一次。调用每个萧秋水的check()检测是motion的值是否匹配某一个小球的目标，并将motion
     重新初始化，以便记录下1秒的鼠标事件数量
    5.每个小球应该添加一个control属性，用于记录当前的状态（绿色-》玩家控制；灰色-》随机移动）
    6.通过检查control属性决定绘制什么颜色的小球
'''

class Ball(pygame.sprite.Sprite):
    def __init__(self, gray_ball_image,green_ball_image, position, speed,bg_size, target):
        pygame.sprite.Sprite.__init__(self)

        self.gray_ball_image = pygame.image.load(gray_ball_image).convert_alpha()
        self.green_ball_image = pygame.image.load(green_ball_image).convert_alpha()
        self.rect = self.gray_ball_image.get_rect()
        self.rect.left, self.rect.top = position
        self.side = [choice([1,-1]),choice([-1,1])]     #单独定义小球的方向
        self.speed = speed
        self.target = target
        self.collide = False
        self.control = False
        self.width, self.height = bg_size
        self.radius = self.rect.width/2   #调用pygame自带碰撞检测函数的原型物体碰撞检测时，需要定义半径属性
    
    # 移动小球的位置
    def move(self):
        if self.control:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move(self.side[0]*self.speed[0],self.side[1]*self.speed[1]) 
        move_x,move_y = 0, 0
        #判断 X 位置是否越界, 重新初始化X的位置
        if self.rect.right <= 0:
            self.rect.left = self.width
        elif self.rect.left >= self.width:
            self.rect.right = 0
        #判断 y 是否越界,重新初始化Y的位置
        elif self.rect.top >= self.height:
            self.rect.bottom = 0
        elif self.rect.bottom <= 0:
            self.rect.top = self.height

    # 创建一个用于检查小球是否被选中的函数
    def check(self, motion):
        if self.target < motion < self.target + 5:
            return True
        else:
            return False

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

    gray_ball_image = "gray_ball.png"
    bg_image = "background.png"
    glass_image = "glass.png"
    mouse_image = "hand.png"
    green_ball_image = "green_ball.png"
    

    running = True
    bg_size = width, height = 1024, 681
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("Play the ball - Demo")

    # 设置背景
    background = pygame.image.load(bg_image).convert_alpha()

    # 创建五个黑洞的位置
    # hole = [(117,119,199,201),(225,227,390,392,),(503,505,320,322),\
    #     (698,700,192,194),(906,908,419,421)]
    hole = [(110,125,190,207),(215,230,385,399,),(500,509,310,329),\
        (690,709,190,199),(900,909,410,429)]
        
    #定义一个用于打印消息的列表
    msgs = []

    # 创建五个小球
    BALL_NUM = 5
    balls = []
    group = pygame.sprite.Group()   #创建一个pygame的Group()对象，用于碰撞检测

    for i in range(BALL_NUM):
        position = randint(0,width-100), randint(0, height -100)
        speed = [randint(1,10), randint(1,10)]
        ball = Ball(gray_ball_image, green_ball_image, position,speed, bg_size, 5*(i+1)) # 产生的事件数量 5*(i+1)
        #检测当前生成的小球是否与已生成的小球重合
        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):  
            ball.rect.left, ball.rect.top = randint(0,width-100), randint(0, height -100)
        balls.append(ball)
        group.add(ball)
    # 创建玻璃面板
    glass = Glass(glass_image, mouse_image, bg_size)
    # 添加一个自定义的事件
    MYTIMER = USEREVENT + 1  # USEREVENT已经使用过了，所以+1
    pygame.time.set_timer(MYTIMER, 1000)   #定义一个timer，每1000ms触发一次
    motion = 0  #用于记录1秒钟产生的事件数量

    #用于重复相应键盘按下的事件
    pygame.key.set_repeat(100,100)
    # 设置游戏的帧率
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == GAMEOVER:
                loser_sound.play()
                pygame.time.delay(3000)
                laugh_sound.play()
                pygame.time.delay(3000)
                running = False
            elif event.type == MYTIMER:
                if motion:
                    for each in balls:
                        if each.check(motion):
                            each.speed = [0,0]
                            each.control = True
                    motion = 0
            elif event.type == MOUSEMOTION:
                motion += 1

            elif event.type == KEYDOWN:
                if event.key == K_w:
                    for each in group:
                        if each.control:
                            each.speed[1] -= 1
                if event.key == K_s:
                    for each in group:
                        if each.control:
                            each.speed[1] += 1
                if event.key == K_a:
                    for each in group:
                        if each.control:
                            each.speed[0] -= 1
                if event.key == K_d:
                    for each in group:
                        if each.control:
                            each.speed[0] += 1
                if event.key == K_SPACE:
                    print("SPEACE")
                    for each in group:
                        for i in hole:
                            print(i)
                            if i[0] <= each.rect.left <= i[1] and\
                                i[2] <= each.rect.top <= i[3]:
                                print(each.rect)
                                hole_sound.play()
                                each.speed = [0,0]
                                group.remove(each)
                                temp = balls.pop(balls.index(each)) #将小球从原来位置取出
                                balls.insert(0,temp) #将小球放在第一个，之后会首先绘制
                                hole.remove(i)
                        if not hole:
                            pygame.mixer.music.stop()
                            winner_sound.play()
                            pygame.time.delay(3000)
                            msg = pygame.image.load("win.png").convert_alpha()
                            msg_pos = (width - msg.get_width())//2,\
                                (height - msg.get_height())//2
                            msgs.append((msg,msg_pos))
                            laugh_sound.play()
                        


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
            #放在这是因为需要小球先分开，再获取一个新的速度，不然小球还是会黏在一起
            if each.collide:
                each.speed = [randint(1,10),randint(1,10)]
                each.collide = False
            if each.control:
                screen.blit(each.green_ball_image, each.rect)   #绘制绿色小球
            else:
                screen.blit(each.gray_ball_image, each.rect)
        
        for each in group:
            group.remove(each)
            if pygame.sprite.spritecollide(each,group,False,pygame.sprite.collide_circle):
                each.side[0] = -each.side[0]    # 检测到碰撞后将方向取反
                each.side[1] = -each.side[1]
                each.collide = True
                if each.control:
                    each.side[0] = -1
                    each.side[1] = -1
                    each.control = False    #发生碰撞之后，小球脱离控制
            group.add(each)
        
        # 打印消息
        for msg in msgs:
            screen.blit(msg[0],msg[1])

        pygame.display.flip()
        clock.tick(30)
        

if __name__ == "__main__":
    main()