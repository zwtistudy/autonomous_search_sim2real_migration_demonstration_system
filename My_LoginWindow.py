from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets

import LoginWindowui


class My_LoginWindow(QDialog, LoginWindowui.Ui_Form):
    username_signal = QtCore.pyqtSignal(str)
    password_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(My_LoginWindow, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.init()

    def init(self):
        self.lineEdit.textChanged.connect(self.update_username)
        self.lineEdit_2.textChanged.connect(self.update_password)

    def update_username(self):
        self.username_signal.emit(self.lineEdit.text())

    def update_password(self):
        self.password_signal.emit(self.lineEdit_2.text())

    def closeEvent(self, event):
        self.hide()
        event.accept()
        self.parent.show()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myWindow = My_LoginWindow()
    myWindow.show()
    sys.exit(app.exec_())
