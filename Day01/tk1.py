import tkinter as tk 
app = tk.Tk()  # 生成一个窗口的实例，俗称root窗口
app.title("FishC Deom")

theLabel = tk.Label(app, text="我的第二个窗口程序")
theLabel.pack()

app.mainloop()