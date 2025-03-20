import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QSlider, QComboBox, QLineEdit, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QBrush, QPalette
from PyQt5.QtCore import Qt, QProcess


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

    def show_demo_page(self, scene_name):
        page_key = f"{scene_name}_demo"
        if page_key not in self.pages:
            self.pages[page_key] = DemoPage(scene_name, self)
            self.stacked_widget.addWidget(self.pages[page_key])
        self.stacked_widget.setCurrentWidget(self.pages[page_key])

    def show_train_page(self, scene_name):
        page_key = f"{scene_name}_train"
        if page_key not in self.pages:
            self.pages[page_key] = TrainPage(scene_name, self)
            self.stacked_widget.addWidget(self.pages[page_key])
        self.stacked_widget.setCurrentWidget(self.pages[page_key])


class NavigationPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        # 标题
        title_label = QLabel("面向自主搜索任务的虚实迁移验证应用系统")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)

        # 场景按钮布局
        btn_layout = QHBoxLayout()

        # 创建场景按钮
        scenes = [
            ("Gym CarRacing", "Gym CarRacing.jpg"),
            ("Unity街道搜索", "Unity街道搜索.jpg"),
            ("Unity迷宫搜索", "Unity迷宫搜索.jpg")
        ]

        for name, img in scenes:
            btn = QPushButton()
            btn.setIcon(QIcon(img))
            btn.setIconSize(self.parent.size() * 0.3)
            btn.setText(name)
            btn.setStyleSheet("text-align: bottom;")
            btn.clicked.connect(lambda _, n=name, i=img: parent.show_scene_page(n, i))
            btn_layout.addWidget(btn)

        # 设置背景
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap("background1.jpg")
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.Window, brush)  # 使用 QPalette.Window 作为角色

        self.setPalette(palette)

        # 组合布局
        layout.addWidget(title_label)
        layout.addLayout(btn_layout)
        self.setLayout(layout)


class ScenePage(QWidget):
    def __init__(self, scene_name, background_path, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        # 标题
        title_label = QLabel(scene_name)
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)

        # 功能按钮
        btn_layout = QHBoxLayout()
        demo_btn = QPushButton("演示")
        train_btn = QPushButton("训练")

        demo_btn.clicked.connect(lambda: parent.show_demo_page(scene_name))
        train_btn.clicked.connect(lambda: parent.show_train_page(scene_name))

        btn_layout.addWidget(demo_btn)
        btn_layout.addWidget(train_btn)

        # 返回按钮
        back_btn = QPushButton("返回")
        back_btn.clicked.connect(lambda: parent.stacked_widget.setCurrentIndex(0))

        # 设置背景
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap(background_path)
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.Window, brush)  # 统一使用 QPalette.Window
        self.setPalette(palette)

        # 组合布局
        layout.addWidget(title_label)
        layout.addLayout(btn_layout)
        layout.addWidget(back_btn)
        self.setLayout(layout)


class DemoPage(QWidget):
    def __init__(self, scene_name, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        # 标题
        title_label = QLabel(f"{scene_name} 演示")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)

        # 扰动幅度设置
        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 40)  # 0.1-4转换为整数
        self.slider.setValue(10)  # 默认1.02转换为10.2，取整为10
        self.slider.setTickInterval(1)
        self.slider_label = QLabel("1.02")

        slider_layout.addWidget(QLabel("扰动幅度:"))
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.slider_label)

        # 开始演示按钮
        start_btn = QPushButton("开始演示")
        start_btn.clicked.connect(lambda: self.run_command(scene_name, 'demo'))

        # 返回按钮
        back_btn = QPushButton("返回")
        back_btn.clicked.connect(self.go_back)

        # 设置背景
        self.setAutoFillBackground(True)
        pixmap = QPixmap(f"{scene_name}.jpg")
        brush = QBrush(pixmap)
        palette = self.palette()
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

        # 组合布局
        layout.addWidget(title_label)
        layout.addLayout(slider_layout)
        layout.addWidget(start_btn)
        layout.addWidget(back_btn)
        self.setLayout(layout)

        # 连接滑块事件
        self.slider.valueChanged.connect(self.update_slider_label)

    def update_slider_label(self, value):
        real_value = value / 10
        self.slider_label.setText(f"{real_value:.2f}")

    def go_back(self):
        self.parent.stacked_widget.setCurrentIndex(0)

    def run_command(self, scene_name, mode):
        commands = {
            'Gym CarRacing': {
                'demo': 'cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe deduce_gym.py',
                'train': 'cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe train_gymcarracing.py'
            },
            'Unity街道搜索': {
                'demo': 'cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe deduce.py',
                'train': 'cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe train_race.py'
            },
            'Unity迷宫搜索': {
                'demo': 'cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe PyQT_1.py ugv/ugv_search_mg --name 20240713002100dddd --ckpt 150189 --run --port 17635',
                'train': 'cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe train_search.py'
            }
        }

        cmd = commands[scene_name][mode].split(';')
        process = QProcess()
        process.setWorkingDirectory("F:\\code\\rl\\recurrent-ppo-truncated-bptt2")
        process.start(cmd[0], cmd[1:])
        process.waitForFinished()


class TrainPage(QWidget):
    def __init__(self, scene_name, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        # 标题
        title_label = QLabel(f"{scene_name} 训练")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)

        # 参数设置布局
        form_layout = QVBoxLayout()

        # 算法选择
        algo_layout = QHBoxLayout()
        algo_label = QLabel("算法:")
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["PPO", "SAC"])
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algo_combo)

        # 学习率
        lr_layout = QHBoxLayout()
        lr_label = QLabel("learning_rate:")
        self.lr_edit = QLineEdit("0.0005")
        lr_layout.addWidget(lr_label)
        lr_layout.addWidget(self.lr_edit)

        # gamma
        gamma_layout = QHBoxLayout()
        gamma_label = QLabel("gamma:")
        self.gamma_edit = QLineEdit("0.99")
        gamma_layout.addWidget(gamma_label)
        gamma_layout.addWidget(self.gamma_edit)

        # lambda
        lambda_layout = QHBoxLayout()
        lambda_label = QLabel("lambda:")
        self.lambda_edit = QLineEdit("0.95")
        lambda_layout.addWidget(lambda_label)
        lambda_layout.addWidget(self.lambda_edit)

        # updates
        updates_layout = QHBoxLayout()
        updates_label = QLabel("updates:")
        self.updates_edit = QLineEdit("390")
        updates_layout.addWidget(updates_label)
        updates_layout.addWidget(self.updates_edit)

        # epochs
        epochs_layout = QHBoxLayout()
        epochs_label = QLabel("epochs:")
        self.epochs_edit = QLineEdit("3")
        epochs_layout.addWidget(epochs_label)
        epochs_layout.addWidget(self.epochs_edit)

        # n_workers
        workers_layout = QHBoxLayout()
        workers_label = QLabel("n_workers:")
        self.workers_edit = QLineEdit("5")
        workers_layout.addWidget(workers_label)
        workers_layout.addWidget(self.workers_edit)

        # recurrence_sequence_length
        seq_layout = QHBoxLayout()
        seq_label = QLabel("sequence_length:")
        self.seq_edit = QLineEdit("8")
        seq_layout.addWidget(seq_label)
        seq_layout.addWidget(self.seq_edit)

        # 添加到表单布局
        form_layout.addLayout(algo_layout)
        form_layout.addLayout(lr_layout)
        form_layout.addLayout(gamma_layout)
        form_layout.addLayout(lambda_layout)
        form_layout.addLayout(updates_layout)
        form_layout.addLayout(epochs_layout)
        form_layout.addLayout(workers_layout)
        form_layout.addLayout(seq_layout)

        # 按钮布局
        btn_layout = QHBoxLayout()
        start_btn = QPushButton("开始训练")
        back_btn = QPushButton("返回")

        start_btn.clicked.connect(lambda: self.run_command(scene_name))
        back_btn.clicked.connect(self.go_back)

        btn_layout.addWidget(start_btn)
        btn_layout.addWidget(back_btn)

        # 设置背景
        self.setAutoFillBackground(True)
        pixmap = QPixmap(f"{scene_name}.jpg")
        brush = QBrush(pixmap)
        palette = self.palette()
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

        # 组合布局
        layout.addWidget(title_label)
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def go_back(self):
        self.parent.stacked_widget.setCurrentIndex(0)

    def run_command(self, scene_name):
        # 这里可以添加参数处理逻辑，但根据需求说明参数仅展示
        # 直接使用预定义的训练命令
        commands = {
            'Gym CarRacing': 'cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe train_gymcarracing.py',
            'Unity街道搜索': 'cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe train_race.py',
            'Unity迷宫搜索': 'cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe train_search.py'
        }

        process = QProcess()
        process.setWorkingDirectory("F:\\code\\rl\\recurrent-ppo-truncated-bptt2")
        process.start(commands[scene_name])
        process.waitForFinished()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())