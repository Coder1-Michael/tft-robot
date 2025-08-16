import tkinter as tk
import threading
import time

# 创建回合区域的绘制类
class RoundAreaBox:
    def __init__(self, root, round_area):
        self.root = root
        self.round_area = round_area  # 回合数区域的坐标 (x1, y1, x2, y2)

        # 获取屏幕宽度和高度
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 创建画布，设置为全屏
        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='white')
        self.canvas.pack()

        # 创建回合数区域的矩形框
        self.rect = self.canvas.create_rectangle(self.round_area[0], self.round_area[1],
                                                  self.round_area[2], self.round_area[3],
                                                  outline="blue", width=3)

        # 设置回合数区域矩形框始终在最上层显示
        self.canvas.tag_raise(self.rect)

    def update_round_area(self, round_area):
        # 更新回合数区域的坐标并重新绘制
        self.round_area = round_area
        self.canvas.coords(self.rect, self.round_area[0], self.round_area[1],
                           self.round_area[2], self.round_area[3])


def draw_round_area_box(round_area):
    """启动一个线程来绘制回合数区域的矩形框"""
    root = tk.Tk()
    root.title("回合数区域边框")

    # 去掉窗口装饰
    root.overrideredirect(True)

    # 设置透明色为白色背景
    root.wm_attributes("-transparentcolor", "white")

    # 设置窗口总在最前面
    root.wm_attributes("-topmost", 1)

    # 获取屏幕宽度和高度，并将窗口调整为全屏
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # 创建回合数区域边框
    round_area_box = RoundAreaBox(root, round_area)

    # 定时更新回合数区域的边框
    def update_box():
        while True:
            round_area_box.update_round_area(round_area)
            time.sleep(1)  # 每秒更新一次

    # 启动回合数区域边框更新线程
    threading.Thread(target=update_box, daemon=True).start()

    # 运行 Tkinter 的主循环
    root.mainloop()
