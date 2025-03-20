import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("面向自主搜索任务的虚实迁移验证应用系统")
        self.setGeometry(100, 100, 1200, 800)

        # 导航面板布局
        self.nav_layout = QVBoxLayout()
        nav_title = QLabel("面向自主搜索任务的虚实迁移验证应用系统")
        nav_title.setStyleSheet("font-size: 20px; background-color: #f0f0f0; padding: 10px;")
        self.nav_layout.addWidget(nav_title)

        self.scene_buttons = []
        scenes = ["Gym CarRacing", "Unity街道搜索", "Unity迷宫搜索"]
        for scene in scenes:
            btn = QPushButton(scene)
            btn.clicked.connect(lambda _, s=scene: self.switch_scene(s))
            self.scene_buttons.append(btn)
            self.nav_layout.addWidget(btn)

        # 主内容区域
        self.stacked_widget = QStackedWidget()
        self.scene_pages = {}
        for scene in scenes:
            page = QWidget()
            tab_widget = QTabWidget()
            tab_widget.addTab(self.create_demo_panel(scene), "演示")
            tab_widget.addTab(self.create_train_panel(scene), "训练")
            layout = QVBoxLayout()
            layout.addWidget(tab_widget)
            page.setLayout(layout)
            self.scene_pages[scene] = page
            self.stacked_widget.addWidget(page)

        # 组合布局
        main_layout = QHBoxLayout()
        main_layout.addLayout(self.nav_layout)
        main_layout.addWidget(self.stacked_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def switch_scene(self, scene_name):
        self.stacked_widget.setCurrentWidget(self.scene_pages[scene_name])

    def create_demo_panel(self, scene):
        scene_index = ["Gym CarRacing", "Unity街道搜索", "Unity迷宫搜索"].index(scene) + 1
        panel = QWidget()
        panel.setStyleSheet(f"background-image: url(场景{scene_index}.jpg);")

        layout = QVBoxLayout()
        title = QLabel(f"{scene}演示")
        title.setStyleSheet("background-color: rgba(255,255,255,0.7); padding: 10px; font-size: 16px;")
        layout.addWidget(title)

        # 扰动幅度滑块
        slider = QSlider(Qt.Horizontal)
        slider.setRange(10, 400)
        slider.setValue(102)
        slider.setSingleStep(1)
        slider.valueChanged.connect(lambda v: self.update_amplitude_label(v))
        layout.addWidget(QLabel("扰动幅度"))
        layout.addWidget(slider)

        start_btn = QPushButton("开始演示")
        start_btn.clicked.connect(lambda: self.start_demo(scene, slider.value()))
        layout.addWidget(start_btn)

        panel.setLayout(layout)
        return panel

    def update_amplitude_label(self, value):
        print(f"当前扰动幅度：{value / 100:.2f}")

    def start_demo(self, scene, amplitude):
        commands = {
            "Gym CarRacing": r"cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe deduce_gym.py",
            "Unity街道搜索": r"cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe deduce.py",
            "Unity迷宫搜索": r"cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe PyQT_1.py ugv/ugv_search_mg --name 20240713002100dddd --ckpt 150189 --run --port 17635"
        }

        cmd = commands[scene]
        # 添加扰动幅度参数
        cmd += f" --amplitude {amplitude / 100:.2f}"

        self.execute_command(cmd)

    def execute_command(self, cmd):
        import subprocess
        powershell_cmd = f'powershell.exe -Command "{cmd}"'
        subprocess.Popen(powershell_cmd, shell=True)

    def create_train_panel(self, scene):
        scene_index = ["Gym CarRacing", "Unity街道搜索", "Unity迷宫搜索"].index(scene) + 1
        panel = QWidget()
        panel.setStyleSheet(f"background-image: url(场景{scene_index}.jpg);")

        layout = QVBoxLayout()
        title = QLabel(f"{scene}训练")
        title.setStyleSheet("background-color: rgba(255,255,255,0.7); padding: 10px; font-size: 16px;")
        layout.addWidget(title)

        form_layout = QFormLayout()

        # 算法选择
        algo_combo = QComboBox()
        algo_combo.addItems(["PPO", "SAC"])
        form_layout.addRow("算法", algo_combo)

        # 参数输入框
        inputs = [
            ("learning_rate", "0.0005"),
            ("gamma", "0.99"),
            ("lambda", "0.95"),
            ("updates", "390"),
            ("epochs", "3"),
            ("n_workers", "5"),
            ("recurrence_sequence_length", "8")
        ]

        for label_text, default in inputs:
            input_field = QLineEdit(default)
            form_layout.addRow(label_text, input_field)

        layout.addLayout(form_layout)

        start_btn = QPushButton("开始训练")
        start_btn.clicked.connect(lambda: self.start_train(scene))
        layout.addWidget(start_btn)

        panel.setLayout(layout)
        return panel

    def start_train(self, scene):
        train_commands = {
            "Gym CarRacing": r"cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe train_gymcarracing.py",
            "Unity街道搜索": r"cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe train_race.py",
            "Unity迷宫搜索": r"cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe train_search.py"
        }

        self.execute_command(train_commands[scene])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
