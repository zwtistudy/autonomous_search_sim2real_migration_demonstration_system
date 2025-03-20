from 导航面板 import *


# 设置背景为./background.png
def set_background(Form):
    Form.setAutoFillBackground(True)
    palette = Form.palette()
    pixmap = QtGui.QPixmap("./background.png")
    brush = QtGui.QBrush(pixmap)
    palette.setBrush(QtGui.QPalette.Window, brush)
    Form.setPalette(palette)


# 设置pushButton的背景为./GymCarRacing.png
def set_pushbutton_background(pushButton):
    pixmap = QtGui.QPixmap("./GymCarRacing.png")
    pushButton.setIcon(QtGui.QIcon(pixmap))
    pushButton.setIconSize(QtCore.QSize(pushButton.width(), pushButton.height()))


# 设置pushButton_2的背景为./Unity街道搜索.png
def set_pushbutton_2_background(pushButton_2):
    pixmap = QtGui.QPixmap("./Unity街道搜索.png")
    pushButton_2.setIcon(QtGui.QIcon(pixmap))
    pushButton_2.setIconSize(QtCore.QSize(pushButton_2.width(), pushButton_2.height()))


# 设置pushButton_3的背景为./Unity迷宫搜索.png
def set_pushbutton_3_background(pushButton_3):
    pixmap = QtGui.QPixmap("./Unity迷宫搜索.png")
    pushButton_3.setIcon(QtGui.QIcon(pixmap))
    pushButton_3.setIconSize(QtCore.QSize(pushButton_3.width(), pushButton_3.height()))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("虚实迁移验证系统")
        self.setGeometry(100, 100, 1200, 800)

        # 创建堆叠窗口
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 添加各个页面
        self.navigation_page = NavigationPage(self)
        self.stacked_widget.addWidget(self.navigation_page)

        # 保存页面引用的字典
        self.pages = {}

        # 设置样式
        self.setStyleSheet("""
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: white;
                padding: 20px;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                margin: 10px;
            }
            QSlider::groove:horizontal {
                height: 10px;
                background: #555;
            }
            QSlider::handle:horizontal {
                background: #fff;
                width: 20px;
                margin: -5px 0;
            }
        """)

    def show_scene_page(self, scene_name, background_path):
        if scene_name not in self.pages:
            self.pages[scene_name] = ScenePage(scene_name, background_path, self)
            self.stacked_widget.addWidget(self.pages[scene_name])
        self.stacked_widget.setCurrentWidget(self.pages[scene_name])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    set_background(Form)
    set_pushbutton_background(ui.pushButton)
    set_pushbutton_2_background(ui.pushButton_2)
    set_pushbutton_3_background(ui.pushButton_3)
    Form.show()
    sys.exit(app.exec_())
