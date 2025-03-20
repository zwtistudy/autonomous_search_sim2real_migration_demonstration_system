import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import subprocess
import os


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("面向自主搜索任务的虚实迁移验证应用系统")
        self.geometry("1000x600")
        self.scene_commands = {
            "Gym CarRacing场景": {
                "演示": "cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe deduce_gym.py",
                "训练": "cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe train_gymcarracing.py"
            },
            "Unity街道搜索场景": {
                "演示": "cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe deduce.py",
                "训练": "cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe train_race.py"
            },
            "Unity迷宫搜索场景": {
                "演示": "cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe main.py ugv/ugv_search_mg --name 20240713002100dddd --ckpt 150189 --run --port 17635",
                "训练": "cd F:\\code\\rl\\recurrent-ppo-truncated-bptt2; F:\\condaenvs\\mlagents\\python.exe train_search.py"
            }
        }

        self.current_scene = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # 导航面板
        self.nav_frame = tk.Frame(self, bg="#f0f0f0", height=50)
        self.nav_frame.pack(fill=tk.X)

        scenes = ["Gym CarRacing场景", "Unity街道搜索场景", "Unity迷宫搜索场景"]
        for scene in scenes:
            btn = tk.Button(self.nav_frame, text=scene,
                            command=lambda s=scene: self.show_scene(s),
                            bg="#e0e0e0", relief=tk.FLAT,
                            font=("Arial", 12), padx=20, pady=5)
            btn.pack(side=tk.LEFT, padx=10, pady=5)

        # 主内容区域
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # 初始显示第一个场景
        self.show_scene(scenes[0])

    def show_scene(self, scene):
        self.current_scene.set(scene)

        # 清除当前内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # 创建场景面板
        scene_frame = tk.Frame(self.content_frame)
        scene_frame.pack(fill=tk.BOTH, expand=True)

        # 设置背景图片（假设场景图片已存在）
        try:
            bg_image = tk.PhotoImage(file=f"{scene[:-2]}.png")
            bg_label = tk.Label(scene_frame, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            pass

        # 标题
        title = tk.Label(scene_frame, text=scene,
                         font=("Arial", 16, "bold"),
                         bg="#f0f0f0", padx=20, pady=10)
        title.pack(pady=10)

        # 创建选项卡
        tab_control = ttk.Notebook(scene_frame)

        # 创建演示面板
        demo_tab = ttk.Frame(tab_control)
        self.create_demo_panel(demo_tab, scene)
        tab_control.add(demo_tab, text="演示")

        # 创建训练面板
        train_tab = ttk.Frame(tab_control)
        self.create_train_panel(train_tab, scene)
        tab_control.add(train_tab, text="训练")

        tab_control.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def scene_index(self, scene):
        return ["Gym CarRacing场景", "Unity街道搜索场景", "Unity迷宫搜索场景"].index(scene) + 1

    def create_demo_panel(self, parent, scene):
        # 扰动幅度滑块
        perturb_frame = tk.Frame(parent)
        perturb_frame.pack(pady=20)

        tk.Label(perturb_frame, text="扰动幅度", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        self.perturb_scale = tk.Scale(perturb_frame, from_=0.1, to=4.0, resolution=0.01,
                                      orient=tk.HORIZONTAL, length=300,
                                      font=("Arial", 10))
        self.perturb_scale.set(1.02)
        self.perturb_scale.pack(side=tk.LEFT, padx=10)

        # 开始演示按钮
        start_btn = tk.Button(parent, text="开始演示",
                              command=lambda: self.run_command(scene, "演示"),
                              bg="#4CAF50", fg="white",
                              font=("Arial", 12), padx=20, pady=5)
        start_btn.pack(side=tk.BOTTOM, pady=20, anchor=tk.SE)

    def create_train_panel(self, parent, scene):
        # 算法选择
        algo_frame = tk.Frame(parent)
        algo_frame.pack(pady=10)
        tk.Label(algo_frame, text="算法", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        self.algo_combo = ttk.Combobox(algo_frame, values=["PPO", "SAC"], font=("Arial", 10))
        self.algo_combo.set("PPO")
        self.algo_combo.pack(side=tk.LEFT, padx=10)

        # 参数输入框
        params = [
            ("learning_rate", 0.0005),
            ("gamma", 0.99),
            ("lambda", 0.95),
            ("updates", 390),
            ("epochs", 3),
            ("n_workers", 5),
            ("recurrence_sequence_length", 8)
        ]

        for param, default in params:
            frame = tk.Frame(parent)
            frame.pack(pady=5)
            tk.Label(frame, text=param, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
            entry = tk.Entry(frame, font=("Arial", 10), width=10)
            entry.insert(0, str(default))
            entry.pack(side=tk.LEFT, padx=10)
            setattr(self, f"{param}_entry", entry)

        # 开始训练按钮
        train_btn = tk.Button(parent, text="开始训练",
                              command=lambda: self.run_command(scene, "训练"),
                              bg="#2196F3", fg="white",
                              font=("Arial", 12), padx=20, pady=5)
        train_btn.pack(side=tk.BOTTOM, pady=20, anchor=tk.SE)

    def run_command(self, scene, mode):
        command = self.scene_commands[scene][mode]
        try:
            # 执行PowerShell命令
            subprocess.Popen(f'powershell.exe -Command "{command}"',
                             shell=True,
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
            messagebox.showinfo("成功", f"{mode}命令已执行")
        except Exception as e:
            messagebox.showerror("执行失败", f"执行出错：{str(e)}")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
