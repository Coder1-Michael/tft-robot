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
        self.x1, self.y1, self.x2, self.y2 = 200, 150, 400, 350

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

    def take_screenshot(self):
        # 截取方框区域的屏幕截图
        bbox = (self.x1, self.y1, self.x2, self.y2)

        # 生成截图文件名，使用当前时间戳避免文件覆盖
        timestamp = int(time.time())  # 使用时间戳作为文件名的一部分
        screenshot = ImageGrab.grab(bbox)  # 截取方框范围的区域

        # 获取截图的宽度和高度
        screenshot_width, screenshot_height = screenshot.size

        # 计算每一小图的宽度（纵向高度保持不变）
        sub_width = screenshot_width // 5  # 横向切割成五份

        # 切割并保存小图
        for i in range(5):
            left = i * sub_width
            right = (i + 1) * sub_width if i < 4 else screenshot_width  # 最后一块图的右边界
            # 截取每一块小图，保持原高度
            sub_image = screenshot.crop((left, 0, right, screenshot_height))
            sub_image_path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}_{i}.png")
            sub_image.save(sub_image_path)
            print(f"小图已保存：{sub_image_path}")

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

    # 设置透明色为白色背景
    root.wm_attributes("-transparentcolor", "white")

    # 设置窗口总在最前面
    root.wm_attributes("-topmost", 1)

    # 获取屏幕的宽度和高度，并将窗口调整为全屏
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # 创建可拖拽和缩放的方框，传入回调函数
    ResizableDraggableBox(root, draw_finsh)

    # 运行主循环
    root.mainloop()
