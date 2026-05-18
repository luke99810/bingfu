# BingFu (兵符) — Lightweight Multi‑Agent Framework

[中文](#兵符-bingfu--轻量级多智能体框架)

---

## English

### 🎯 Introduction

**BingFu (兵符)** is a lightweight multi‑agent framework inspired by ancient Chinese warfare.  
It allows you to create **single agents** or **multi‑agent systems** that communicate using **war‑style signals**:

- **Drum (击鼓)** — start an agent or a mission.
- **Gong (鸣金)** — stop an agent or abort a mission.

The framework is designed to be simple, extensible, and fun, with a nod to Chinese military strategy.

### ✨ Features (特性)

- **Lightweight**: Minimal dependencies, fast to get started.
- **Single & Multi‑Agent**: Support both solo agents and coordinated teams.
- **Signal System**: Drum/Gong signals for clear control flow.
- **Extensible**: Easily add custom agents, tools, and memory.
- **Chinese Cultural Twist**: Naming and concepts from ancient Chinese warfare.
- **Tactics Engine**: Built‑in Sun Tzu's Art of War strategy support.
- **Famous Generals**: Pre‑built agents inspired by legendary Chinese generals.
- **Visualization Ready**: Future desktop window visualization support (tkinter/PyQt/pywebview).

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/luke99810/bingfu.git
cd bingfu

# Install the package (editable mode)
pip install -e .
```

Or install directly from PyPI (after publication):

```bash
pip install bingfu
```

### 🚀 Quick Start

```python
from bingfu import BingFu, Agent

# Create a single agent
agent = Agent(name="Scout")

# Create the BingFu master
master = BingFu()
master.add_agent(agent)

# Send drum signal (start)
master.drum("Scout", "Explore the area")

# Send gong signal (stop)
master.gong("Scout")
```

For multi‑agent coordination, see the `examples/` directory.

### 📚 Documentation

Full documentation is coming soon. For now, check the `examples/` folder and the source code.

### 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

### 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 中文

### 🎯 简介

**兵符 (BingFu)** 是一个受中国古代战争启发的轻量级多智能体框架。  
它允许你创建**单个智能体**或**多智能体系统**，并使用**战争风格的信号**进行通信：

- **击鼓** — 启动智能体或任务。
- **鸣金** — 停止智能体或中止任务。

该框架设计简洁、可扩展，并融入了中国军事策略的文化元素。

### ✨ 特性

- **轻量级**：依赖最少，快速上手。
- **单/多智能体**：支持独立智能体和协同团队。
- **信号系统**：击鼓/鸣金信号，控制流程清晰。
- **可扩展**：轻松添加自定义智能体、工具和记忆。
- **中国文化特色**：命名和概念源自中国古代战争。
- **孙子兵法战术引擎**：内置古代军事智慧。
- **古代名将Agent**：白起、韩信、项羽、诸葛亮等预置Agent。
- **可视化就绪**：未来支持桌面窗口可视化（tkinter/PyQt/pywebview）。

### 📦 安装

```bash
# 克隆仓库
git clone https://github.com/luke99810/bingfu.git
cd bingfu

# 安装包（可编辑模式）
pip install -e .
```

或者直接从 PyPI 安装（发布后）：

```bash
pip install bingfu
```

### 🚀 快速开始

```python
from bingfu import BingFu, Agent

# 创建单个智能体
agent = Agent(name="侦察兵")

# 创建兵符主对象
master = BingFu()
master.add_agent(agent)

# 发送击鼓信号（开始）
master.drum("侦察兵", "侦察区域")

# 发送鸣金信号（停止）
master.gong("侦察兵")
```

有关多智能体协调，请参阅 `examples/` 目录。

### 📚 文档

完整文档即将推出。目前，请查看 `examples/` 文件夹和源代码。

### 🤝 贡献

欢迎贡献！请提出问题或提交拉取请求。

### 📄 许可证

本项目采用 MIT 许可证 — 详情请参阅 [LICENSE](LICENSE) 文件。

---

## 🗂️ Project Structure (项目结构)

```
bingfu-framework/
├── bingfu/               # Main package (主包)
│   ├── __init__.py       # Package exports (包导出)
│   ├── agent.py          # Agent class (智能体)
│   ├── tool.py           # Tool class (工具)
│   ├── memory.py         # Memory class (记忆)
│   ├── signal.py         # Drum/Gong signals (信号)
│   ├── commander.py      # Multi‑agent coordinator (指挥官)
│   ├── tactics.py        # Sun Tzu tactics engine (战术引擎)
│   ├── bingfu.py        # Main BingFu class (主类)
│   └── cli.py           # Command‑line interface (CLI)
├── examples/             # Usage examples (使用示例)
│   ├── basic_usage.py   # Basic usage (基础用法)
│   ├── multi_agent.py   # Multi‑agent coordination (多智能体)
│   ├── custom_agent.py   # Custom agents (自定义智能体)
│   ├── tool_usage.py    # Tool usage (工具使用)
│   ├── memory_usage.py  # Memory management (记忆管理)
│   ├── famous_generals.py # Famous generals (古代名将)
│   └── cli_guide.py     # CLI guide (CLI指南)
├── tests/                # Unit tests (单元测试)
│   ├── test_agent.py
│   ├── test_signal.py
│   ├── test_commander.py
│   ├── test_tool.py
│   └── test_memory.py
├── pyproject.toml        # Project configuration (项目配置)
├── requirements.txt      # Fixed dependencies (固定依赖)
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
├── CHANGELOG.md         # Version history
├── config.yaml          # Example configuration
└── README.md            # This file (中英文)
```

---

## 📝 Development Status (开发状态)

- [x] Project initialization (项目初始化)
- [x] Configuration files (配置文件)
- [x] Core modules: Agent, Tool, Memory (核心模块)
- [x] Signal system: Drum/Gong (信号系统)
- [x] Commander (multi‑agent) (指挥系统)
- [x] Main BingFu class (兵符主类)
- [x] CLI interface (命令行界面)
- [x] Sun Tzu tactics engine (孙子兵法战术引擎)
- [x] Famous generals examples (古代名将示例)
- [x] Extended examples (扩展示例)
- [x] Unit tests (单元测试)
- [ ] Visualization (可视化) — 未来版本

### 🎯 Quick Demo (快速演示)

```python
# 孙子兵法战术引擎
from bingfu import TacticsEngine, TacticalContext

engine = TacticsEngine()
context = TacticalContext(
    self_strength=30000,
    enemy_strength=80000,
    terrain="山地",
    morale=70
)
result = engine.analyze(context)
print(result['recommended_tactic'])
```

---

## 🔗 Links (链接)

- **GitHub**: https://github.com/luke99810/bingfu
- **Issues**: https://github.com/luke99810/bingfu/issues
- **PyPI** (coming soon): https://pypi.org/project/bingfu/

---

## 📧 Contact (联系)

- **Author**: SuXin (州哥)
- **Email**: luke99810@example.com
- **GitHub**: [@luke99810](https://github.com/luke99810)
