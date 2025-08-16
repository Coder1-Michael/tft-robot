import os
import tkinter as tk
import threading
import time
import queue
from PIL import ImageGrab

class ResizableDraggableBox:
    def __init__(self, root, callback):
        self.screenshot_dir = "..\\assets\\screen_shots"
        self.root = root
        self.callback = callback  # 接收回调函数

        # 获取屏幕的宽度和高度
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 创建画布，设置为全屏
        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='white')
        self.canvas.pack()

        # 初始化方框的坐标和大小
        self.x1, self.y1, self.x2, self.y2 = 662, 1294, 1949, 1482

        # 创建方框
        self.rect = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline="red", width=2)

        # 方框的四个角：用于放大缩小
        self.corner_radius = 8
        self.corners = {
            'top_left': self.create_corner(self.x1, self.y1),
            'top_right': self.create_corner(self.x2, self.y1),
            'bottom_left': self.create_corner(self.x1, self.y2),
            'bottom_right': self.create_corner(self.x2, self.y2),
        }

        # 用于拖动的标志
        self.dragging = False
        self.resizing = None
        self.last_move_time = time.time()  # 用于控制更新频率

        # 绑定鼠标事件
        self.canvas.tag_bind(self.rect, '<ButtonPress-1>', self.on_press_rect)
        self.canvas.tag_bind(self.rect, '<B1-Motion>', self.on_move)
        self.canvas.tag_bind(self.rect, '<ButtonRelease-1>', self.on_release)

        for corner in self.corners.values():
            self.canvas.tag_bind(corner, '<ButtonPress-1>', self.on_press_corner)
            self.canvas.tag_bind(corner, '<B1-Motion>', self.on_resize)
            self.canvas.tag_bind(corner, '<ButtonRelease-1>', self.on_release)

    def create_corner(self, x, y):
        return self.canvas.create_oval(x - self.corner_radius, y - self.corner_radius,
                                       x + self.corner_radius, y + self.corner_radius,
                                       fill="blue", outline="black")

    def on_press_rect(self, event):
        self.dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_move(self, event):
        if self.dragging:
            # 限制更新频率，避免过于频繁的绘制
            if time.time() - self.last_move_time < 1:  # 每50ms更新一次
                return

            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y

            # 移动方框
            self.canvas.move(self.rect, dx, dy)
            for corner in self.corners.values():
                self.canvas.move(corner, dx, dy)

            # 更新起始位置
            self.drag_start_x = event.x
            self.drag_start_y = event.y

            # 更新坐标
            self.x1, self.y1, self.x2, self.y2 = self.canvas.coords(self.rect)
            self.update_coordinates()

            # 记录最后更新时间
            self.last_move_time = time.time()

    def on_release(self, event):
        self.dragging = False
        self.update_coordinates()
        self.callback(self.x1, self.y1, self.x2, self.y2)

    def on_press_corner(self, event):
        self.resizing = self.get_resizing_corner(event.x, event.y)
        self.resize_start_x = event.x
        self.resize_start_y = event.y

    def on_resize(self, event):
        if self.resizing:
            corner = self.resizing
            dx = event.x - self.resize_start_x
            dy = event.y - self.resize_start_y

            # 根据拖动的角来调整方框的大小
            if corner == 'top_left':
                self.x1 += dx
                self.y1 += dy
            elif corner == 'top_right':
                self.x2 += dx
                self.y1 += dy
            elif corner == 'bottom_left':
                self.x1 += dx
                self.y2 += dy
            elif corner == 'bottom_right':
                self.x2 += dx
                self.y2 += dy

            # 更新方框和角落的位置
            self.canvas.coords(self.rect, self.x1, self.y1, self.x2, self.y2)
            self.update_corners()

            # 更新起始位置
            self.resize_start_x = event.x
            self.resize_start_y = event.y

            # 更新坐标
            self.update_coordinates()

    def update_coordinates(self):
        # 每次坐标变化时，调用回调函数
        pass

    def update_corners(self):
        self.canvas.coords(self.corners['top_left'], self.x1 - self.corner_radius, self.y1 - self.corner_radius,
                           self.x1 + self.corner_radius, self.y1 + self.corner_radius)
        self.canvas.coords(self.corners['top_right'], self.x2 - self.corner_radius, self.y1 - self.corner_radius,
                           self.x2 + self.corner_radius, self.y1 + self.corner_radius)
        self.canvas.coords(self.corners['bottom_left'], self.x1 - self.corner_radius, self.y2 - self.corner_radius,
                           self.x1 + self.corner_radius, self.y2 + self.corner_radius)
        self.canvas.coords(self.corners['bottom_right'], self.x2 - self.corner_radius, self.y2 - self.corner_radius,
                           self.x2 + self.corner_radius, self.y2 + self.corner_radius)

    def get_resizing_corner(self, x, y):
        for corner, coords in self.corners.items():
            corner_coords = self.canvas.coords(coords)
            if (corner_coords[0] <= x <= corner_coords[2]) and (corner_coords[1] <= y <= corner_coords[3]):
                return corner
        return None

def run(draw_finsh):
    root = tk.Tk()
    root.title("透明可拖拽缩放方框")

    # 去掉窗口装饰
    root.overrideredirect(True)

    # 设置窗口总在最前面
    root.wm_attributes("-topmost", 1)

    # 获取屏幕的宽度和高度，并将窗口调整为全屏
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.wm_attributes("-transparentcolor", "white")  # 试着注释掉这行代码
    # 创建可拖拽和缩放的方框，传入回调函数
    ResizableDraggableBox(root, draw_finsh)

    # 运行主循环
    root.mainloop()
