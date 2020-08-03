import pygame
import sys
from pygame.locals import *

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
pygame.init()
pygame.mixer.init()  #初始化混音器

bg_size = width, heigth = 400, 600
bg_color = (200,200,200)

#创建窗口
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("播放音效")


#设置背景音
pygame.mixer.music.load("bg_music.ogg")
pygame.mixer.music.play(1)
pause = False
#设置播放和暂停的图标
pause_img = pygame.image.load("pause.png").convert_alpha()
unpause_img = pygame.image.load("unpause.png").convert_alpha()
pause_rect = pause_img.get_rect()
pause_rect.left,pause_rect.top = (width-pause_rect.width)//2,(heigth-pause_rect.height)//2

#设置音效
cat_sound = pygame.mixer.Sound("cat.wav")
dag_sound = pygame.mixer.Sound("dog.wav")

 # 设置游戏的帧率,用于限制CPU
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                pause = not pause

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:       #用于检测鼠标 -1:左键 2:中间键 3:右键
                cat_sound.play()
            if event.button == 3:
                dag_sound.play()
    screen.fill(bg_color)

    if pause:
        screen.blit(pause_img,pause_rect)
        pygame.mixer.music.pause()
    else:
        screen.blit(unpause_img,pause_rect)
        pygame.mixer.music.unpause()
    
    pygame.display.flip()
    clock.tick(30)
        
