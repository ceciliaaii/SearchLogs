import re
import time
import sys
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QGuiApplication
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置背景图片
        palette = self.palette()
        pixmap = QPixmap("images/image.png").scaled(self.size())
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)
        # 设置窗口标题和大小
        self.setWindowTitle("Web日志筛选工具 Autor@hancool")
        self.setGeometry(0, 0, 660, 450)
        # 设置窗口位置
        # self.move(300, 300)
        self.center()

        # 创建控件
        self.label1 = QLabel("日志文件地址：")
        self.label1.setStyleSheet("color: rgb(255, 255, 255);")
        self.lineedit1 = QLineEdit()
        self.button1 = QPushButton("选择文件")
        self.button1.clicked.connect(self.select_file)
        self.label2 = QLabel("IP地址：")
        self.label2.setStyleSheet("color: rgb(255, 255, 255);")
        self.lineedit2 = QLineEdit()
        self.button2 = QPushButton("开始筛选")
        self.button2.clicked.connect(self.filter_logs)
        self.result_label = QLabel("筛选结果：")

        # 创建垂直布局并添加控件
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.lineedit1)
        layout.addWidget(self.button1)
        layout.addWidget(self.label2)
        layout.addWidget(self.lineedit2)
        layout.addWidget(self.button2)
        layout.addWidget(self.result_label)

        # 设置布局
        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择日志文件", "", "Log Files (*.log)")
        self.lineedit1.setText(file_path)

    def center(self):
        # 获取显示器的大小和位置信息
        screen = QGuiApplication.primaryScreen()
        screen_rect = screen.geometry()
        size = self.geometry()
        # 计算窗口应该位于屏幕的中心位置，并将其移动到该位置
        x = int((screen_rect.width() - size.width()) / 2)
        y = int((screen_rect.height() - size.height()) / 2)
        self.move(x, y)

    def filter_logs(self):
        fileaddr = self.lineedit1.text()
        # 将地址中的双引号去掉
        fileaddr = fileaddr.replace('"', '')
        fileA = open(fileaddr, 'r', encoding='utf-8')
        my_ip = self.lineedit2.text()
        filtered_logs = []
        for line in fileA:
            ip = re.findall(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)[0]
            if ip == my_ip:
                filtered_logs.append(line)
        for line in filtered_logs:
            # 筛选的日志输出到新文件，文件名为result+当前时间
            fileA = open('result' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.txt', 'a+',
                         encoding='utf-8')
            fileA.write(line)
            fileA.close()

        # 显示筛选结果
        self.result_label.setText("筛选结果：共筛选出" + str(len(filtered_logs)) + "条日志\n看累了，别忘了奖励自己哟~")
        # 设置颜色为白色，字号20
        self.result_label.setStyleSheet("color:white;font-size:20px")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
