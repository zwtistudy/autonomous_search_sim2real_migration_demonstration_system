import sys

from PyQt5.QtWidgets import QApplication

from My_MainWindow import My_MainWindow
from PyQt5 import QtGui, QtCore

# 适应高DPI设备
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
# 适应Windows缩放
QtGui.QGuiApplication.setAttribute(
    QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = My_MainWindow()
    ui.show()
    sys.exit(app.exec_())
