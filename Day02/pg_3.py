import pygame
import sys

# 初始化 pygame
pygame.init()

# 设置一个界面的尺寸
size = width, height = 600, 400
# 创建一个一个窗口的大小
screen = pygame.display.set_mode(size)
#设置背景色
bg = (0,0,0)
screen.fill(bg)
# 设置字体，使用pygame中的字体模块
font = pygame.font.Font(None, 20)

# 设置窗口的名字
pygame.display.set_caption("事件测试")

position = 0 # 设置初始位置
line_height = font.get_linesize()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        screen.blit(font.render(str(event), True, (0,255,0)), (0, position)) # 第一个参数是显示的字符串，第二个是否平滑锯齿，第三个为颜色

        position += line_height

        if position > height:
            position = 0
            screen.fill(bg)
    pygame.display.flip()
