from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets

import 训练面板


class My_训练面板(QWidget, 训练面板.Ui_Form):
    username_signal = QtCore.pyqtSignal(str)
    password_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, scene_name=None):
        super(My_训练面板, self).__init__(None)
        self.scene_name = scene_name
        self.parent = parent
        self.setupUi(self)
        self.init()

    def init(self):
        self.label.setText(self.scene_name)

        if self.scene_name == 'GymCarRacing':
            pixmap = QtGui.QPixmap("assert/GymCarRacing.png")
        elif self.scene_name == 'Unity街道搜索':
            pixmap = QtGui.QPixmap("assert/Unity街道搜索.png")
        elif self.scene_name == 'Unity迷宫搜索':
            pixmap = QtGui.QPixmap("assert/Unity迷宫搜索.png")
        else:
            pixmap = QtGui.QPixmap("assert/background.png")

        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        brush = QtGui.QBrush(pixmap)
        palette.setBrush(QtGui.QPalette.Window, brush)
        self.setPalette(palette)

        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.pushButton_3.clicked.connect(self.pushButton_3_clicked)

    def pushButton_3_clicked(self):
        if self.parent:
            self.parent.show()
        self.hide()

    def pushButton_clicked(self):
        if self.scene_name == 'GymCarRacing':
            cmd = r'cd /d F:\code\rl\recurrent-ppo-truncated-bptt2 && F:\condaenvs\mlagents\python.exe train_gymcarracing.py'
        elif self.scene_name == 'Unity街道搜索':
            cmd = r'cd /d F:\code\rl\recurrent-ppo-truncated-bptt2 && F:\condaenvs\mlagents\python.exe train_race.py'
        elif self.scene_name == 'Unity迷宫搜索':
            cmd = r'cd /d F:\code\rl\recurrent-ppo-truncated-bptt2 && F:\condaenvs\mlagents\python.exe train_search.py'
        # 执行powershell命令
        import subprocess
        terminal_command = f'start cmd.exe /k "{cmd}"'
        subprocess.Popen(terminal_command, shell=True)

    def closeEvent(self, event):
        self.hide()
        event.accept()
        if self.parent:
            self.parent.show()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myWindow = My_训练面板()
    myWindow.show()
    sys.exit(app.exec_())
