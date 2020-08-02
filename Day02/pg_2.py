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

# 设置字体，使用pygame中的字体模块
font = pygame.font.Font(None, 20)

screen.fill(bg)


# 设置窗口的名字
pygame.display.set_caption("事件测试")

# 创建一个文件
f = open("record.txt", "w")

while True:
    for event in pygame.event.get():
        f.write(str(event) + '\n') # 写入到文件中

        if event.type == pygame.QUIT:
            f.close() # 在使用完之后一定要关闭
            sys.exit()

        screen.blit(font.render(str(event), True, (0,255,0)), (0, position)) # 第一个参数是显示的字符串，第二个是否平滑锯齿，第三个为颜色
