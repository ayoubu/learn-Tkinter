from tkinter import *

root = Tk()

textLable = Label(root, 
                  text="您所下载的影片包含有未成年人限制内容，\n请满18周岁后再点击观看！", 
                  justify=LEFT, #text Label 左对齐
                  padx=10,
                  pady=10
                )
textLable.pack()

photo = PhotoImage(file='images.png')
imgLabel =  Label(root, image=photo)
imgLabel.pack(side=RIGHT)  #图像右对齐

mainloop()

