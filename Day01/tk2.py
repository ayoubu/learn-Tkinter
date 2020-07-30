import tkinter as tk
'''
初始Tkinter，简单的添加按钮，以及按钮的相应函数。
'''
class APP:
    def __init__(self, master):
        frame = tk.Frame(master)  #frame框架用于组件的分组
        frame.pack(side=tk.LEFT, padx=10, pady=10)  #设置标签的位置,设置和间距。
        #设置按钮显示的名称、背景色、字体的颜色，响应的函数
        self.hi_there = tk.Button(frame, text = "打招呼", bg="black", fg="blue", command=self.say_hi)
        self.hi_there.pack()
    def say_hi(self):
        print("小宝贝，我想死你了...")

root = tk.Tk()
app = APP(root)

root.mainloop()