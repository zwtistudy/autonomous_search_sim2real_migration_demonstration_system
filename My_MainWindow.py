from PyQt5.QtWidgets import QMessageBox, QWidget, QMainWindow, QApplication

import 导航面板
from My_场景面板 import My_场景面板
# from My_LoginWindow import My_LoginWindow
from PyQt5 import QtCore, QtGui, QtWidgets


# # 适应高DPI设备
# QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
# # 适应Windows缩放
# QtGui.QGuiApplication.setAttribute(
#     QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
# )

class My_MainWindow(QMainWindow, 导航面板.Ui_Form):
    def __init__(self, parent=None):
        super(My_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.init()

    def init(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QtGui.QPixmap("./background.png")
        brush = QtGui.QBrush(pixmap)
        palette.setBrush(QtGui.QPalette.Window, brush)
        self.setPalette(palette)

        pixmap = QtGui.QPixmap("./GymCarRacing.png")
        self.pushButton.setIcon(QtGui.QIcon(pixmap))
        self.pushButton.setIconSize(QtCore.QSize(self.pushButton.width(), self.pushButton.height()))
        pixmap = QtGui.QPixmap("./Unity街道搜索.png")
        self.pushButton_2.setIcon(QtGui.QIcon(pixmap))
        self.pushButton_2.setIconSize(QtCore.QSize(self.pushButton_2.width(), self.pushButton_2.height()))
        pixmap = QtGui.QPixmap("./Unity迷宫搜索.png")
        self.pushButton_3.setIcon(QtGui.QIcon(pixmap))
        self.pushButton_3.setIconSize(QtCore.QSize(self.pushButton_3.width(), self.pushButton_3.height()))

        self.pushButton.clicked.connect(self.pushButton_1_clicked)
        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.pushButton_3.clicked.connect(self.pushButton_3_clicked)

    def pushButton_1_clicked(self):
        self.scene_window = My_场景面板(self, 'GymCarRacing')
        self.scene_window.show()
        self.hide()

    def pushButton_2_clicked(self):
        self.scene_window = My_场景面板(self, 'Unity街道搜索')
        self.scene_window.show()
        self.hide()

    def pushButton_3_clicked(self):
        self.scene_window = My_场景面板(self, 'Unity迷宫搜索')
        self.scene_window.show()
        self.hide()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = My_MainWindow()
    ui.show()
    sys.exit(app.exec_())
