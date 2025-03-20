from PyQt5.QtWidgets import QMessageBox, QWidget, QMainWindow, QApplication

import MainWindow
from My_LoginWindow import My_LoginWindow


class My_MainWindow(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(My_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.init()

    def init(self):
        self.pushButton.clicked.connect(self.pushButton_clicked)

    def username_slot(self, username):
        self.label_2.setText(username)

    def password_slot(self, password):
        self.label_4.setText(password)

    def pushButton_clicked(self):
        # QMessageBox.about(self, "About", "Hello World!")
        login_dioalog = My_LoginWindow(self)
        login_dioalog.username_signal.connect(self.username_slot)
        login_dioalog.password_signal.connect(self.password_slot)
        login_dioalog.show()
        # 隐藏主窗口
        self.hide()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = My_MainWindow()
    ui.show()
    sys.exit(app.exec_())
