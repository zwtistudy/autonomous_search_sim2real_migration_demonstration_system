# 演示系统

## 界面功能设计

### 导航面板

标题：画面正上方，“面向自主搜索任务的虚实迁移验证应用系统”，加大加粗

背景图片：背景1.jpg

选择场景（主要）：一共有3个场景，分别是Gym CarRacing场景、Unity街道搜索场景和Unity迷宫搜索场景，占画面主体。场景选择贴图：Gym CarRacing.jpg、Unity街道搜索.jpg和Unity迷宫搜索.jpg

选择场景后跳转到场景面板

### 场景面板

标题：场景名称

背景图片：对应的场景.jpg

选择功能：演示和训练。占画面主体。

返回按钮：返回到上一层

根据选择跳转到演示或者训练面板

### 演示面板

标题：场景名称+演示

背景图片：对应的场景jpg

界面主体是场景设置（仅作展示使用，不参与具体的命令构成）

扰动幅度（滑块实现，值域0.1-4）：默认1.02

返回按钮：返回到上一层

右下角是“开始演示”按钮，按钮绑定到一个powershell命令。

### 训练面板

标题：场景名称+训练

背景图片：对应的场景jpg

界面主体是训练超参数设置（仅作展示使用，不参与具体的命令构成）

* 算法（下拉框）：PPO/SAC
* learning_rate（输入框）：默认0.0005
* gamma（输入框）：默认0.99
* lamda（输入框）：默认0.95
* updates（输入框）：默认390
* epochs（输入框）：默认3
* n_workers（输入框）：默认5
* recurrence_sequence_length（输入框）：数字8

右下角是“开始训练”按钮，按钮绑定到一个powershell命令。

返回按钮：返回到上一层

## 功能实现

### 演示命令

Gym CarRacing：

```bash
cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe deduce_gym.py
```

Unity街道搜索：

```bash
cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe deduce.py
```

Unity迷宫搜索：

```bash
cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe PyQT_1.py ugv/ugv_search_mg --name 20240713002100dddd --ckpt 150189 --run --port 17635
```

### 训练命令

Gym CarRacing：

```bash
cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe train_gymcarracing.py
```

Unity街道搜索：

```bash
cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe train_race.py
```

Unity迷宫搜索：

```bash
cd F:\code\rl\recurrent-ppo-truncated-bptt2; F:\condaenvs\mlagents\python.exe train_search.py
```

---

请你用PyQT5实现
