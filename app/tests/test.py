import sys
from PySide6 import QtCore, QtWidgets, QtGui
from datetime import datetime

class TaskManagerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日常任务管理器")
        self.tasks = []
        self.init_ui()

    def init_ui(self):
        # 主布局
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # 标题
        title_label = QtWidgets.QLabel("📋 日常任务管理器")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_font = QtGui.QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # 添加任务区域
        add_task_group = QtWidgets.QGroupBox("添加新任务")
        add_task_layout = QtWidgets.QHBoxLayout()
        
        self.task_input = QtWidgets.QLineEdit()
        self.task_input.setPlaceholderText("输入任务内容...")
        self.task_input.returnPressed.connect(self.add_task)
        
        self.add_button = QtWidgets.QPushButton("添加任务")
        self.add_button.clicked.connect(self.add_task)
        
        add_task_layout.addWidget(self.task_input)
        add_task_layout.addWidget(self.add_button)
        add_task_group.setLayout(add_task_layout)
        main_layout.addWidget(add_task_group)
        
        # 任务列表
        self.task_list = QtWidgets.QListWidget()
        self.task_list.setAlternatingRowColors(True)
        main_layout.addWidget(QtWidgets.QLabel("任务列表:"))
        main_layout.addWidget(self.task_list)
        
        # 操作按钮区域
        button_layout = QtWidgets.QHBoxLayout()
        
        self.complete_button = QtWidgets.QPushButton("标记完成")
        self.complete_button.clicked.connect(self.complete_task)
        
        self.delete_button = QtWidgets.QPushButton("删除任务")
        self.delete_button.clicked.connect(self.delete_task)
        
        self.clear_all_button = QtWidgets.QPushButton("清空所有")
        self.clear_all_button.clicked.connect(self.clear_all_tasks)
        
        button_layout.addWidget(self.complete_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_all_button)
        main_layout.addLayout(button_layout)
        
        # 统计信息
        self.stats_label = QtWidgets.QLabel("总任务: 0 | 已完成: 0 | 待完成: 0")
        self.stats_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.stats_label)
        
        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Microsoft YaHei', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
            QListWidget {
                border: 2px solid #ddd;
                border-radius: 4px;
                background-color: white;
                alternate-background-color: #f9f9f9;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
        """)

    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            timestamp = datetime.now().strftime("%H:%M")
            task_item = QtWidgets.QListWidgetItem(f"⏰ {timestamp} - {task_text}")
            task_item.setFlags(task_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            task_item.setCheckState(QtCore.Qt.Unchecked)
            self.task_list.addItem(task_item)
            self.task_input.clear()
            self.update_stats()

    def complete_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            if current_item.checkState() == QtCore.Qt.Unchecked:
                current_item.setCheckState(QtCore.Qt.Checked)
                # 添加删除线效果
                font = current_item.font()
                font.setStrikeOut(True)
                current_item.setFont(font)
            else:
                current_item.setCheckState(QtCore.Qt.Unchecked)
                # 移除删除线效果
                font = current_item.font()
                font.setStrikeOut(False)
                current_item.setFont(font)
            self.update_stats()

    def delete_task(self):
        current_row = self.task_list.currentRow()
        if current_row >= 0:
            self.task_list.takeItem(current_row)
            self.update_stats()

    def clear_all_tasks(self):
        reply = QtWidgets.QMessageBox.question(
            self, 
            "确认清空", 
            "确定要清空所有任务吗？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.task_list.clear()
            self.update_stats()

    def update_stats(self):
        total_tasks = self.task_list.count()
        completed_tasks = 0
        
        for i in range(total_tasks):
            item = self.task_list.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                completed_tasks += 1
        
        pending_tasks = total_tasks - completed_tasks
        self.stats_label.setText(f"总任务: {total_tasks} | 已完成: {completed_tasks} | 待完成: {pending_tasks}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = TaskManagerWidget()
    widget.resize(600, 500)
    widget.show()

    sys.exit(app.exec())
