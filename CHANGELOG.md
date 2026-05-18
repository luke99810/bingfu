# Changelog (变更日志)

All notable changes to the **BingFu (兵符)** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] (未发布)

### Added (新增)

- **孙子兵法战术引擎**
  - `bingfu/tactics.py` — 完整的孙子兵法十三篇战术实现
    - `TacticsEngine` 类：战场态势分析
    - `SunTzuAgent` 类：智能军师Agent
    - `TacticType` 枚举：13种战术类型
    - `TacticalContext` 模型：战术上下文

- **古代名将示例**
  - `examples/famous_generals.py` — 十大名将Agent实现
    - 白起、韩信、项羽、诸葛亮、岳飞等
    - 完整战役模拟场景

- **工具与记忆示例**
  - `examples/tool_usage.py` — 工具使用完整示例
  - `examples/memory_usage.py` — 记忆系统完整示例

- **CLI指南**
  - `examples/cli_guide.py` — 完整CLI使用文档

- **单元测试补全**
  - `tests/test_tool.py` — Tool类完整测试
  - `tests/test_memory.py` — Memory类完整测试

### Changed (变更)
- 更新README，添加新功能说明
- 更新`__init__.py`，导出tactics模块
- 完善项目结构文档

---

## [0.2.0] - 2026-05-18

### Added (新增)

- **孙子兵法战术引擎**
  - `bingfu/tactics.py` — 完整的孙子兵法十三篇战术实现
    - `TacticsEngine` 类：战场态势分析
    - `SunTzuAgent` 类：智能军师Agent
    - `TacticType` 枚举：13种战术类型
    - `TacticalContext` 模型：战术上下文

- **古代名将示例**
  - `examples/famous_generals.py` — 十大名将Agent实现
    - 白起、韩信、项羽、诸葛亮、岳飞等
    - 完整战役模拟场景

- **工具与记忆示例**
  - `examples/tool_usage.py` — 工具使用完整示例
  - `examples/memory_usage.py` — 记忆系统完整示例

- **CLI指南**
  - `examples/cli_guide.py` — 完整CLI使用文档

- **单元测试补全**
  - `tests/test_tool.py` — Tool类完整测试
  - `tests/test_memory.py` — Memory类完整测试

### Changed (变更)
- 更新README，添加新功能说明
- 更新`__init__.py`，导出tactics模块
- 完善项目结构文档

---

## [0.3.0] - 2026-05-18

### Added (新增)

- **中军帐可视化模块** 🆕
  - `bingfu/visual/` — Tkinter桌面可视化组件
    - `styles.py` — 古代军事风格配色与字体常量
    - `components.py` — UI组件库（GeneralCard, BattleStatusPanel, ReportPanel等）
    - `console.py` — `MilitaryCommandConsole` 主控制台

- **可视化组件**
  - `GeneralCard` — 将领卡片（状态指示器、角色显示）
  - `BattleStatusPanel` — 战役态势面板（双方兵力、战略建议）
  - `ReportPanel` — 军情速递面板（报告列表、类型区分）
  - `StatsBar` — 底部状态栏（统计信息）
  - `CommandInput` — 命令输入框
  - `StyledFrame` — 金色边框样式框架

- **控制台功能**
  - 将领状态管理（添加/移除/更新）
  - 实时战役态势更新
  - 军情报告系统（info/warning/danger/success）
  - 命令行交互（/add, /remove, /report, /battle, /help, /clear）
  - 击鼓/鸣金快捷操作
  - 日志输出区域
  - 孙子兵法战术建议区

- **示例文件**
  - `examples/console_demo.py` — 中军帐演示（基础/集成/实时模式）

### Changed (变更)
- 更新README添加可视化模块文档
- 更新项目结构说明
- 更新开发状态（可视化已标记完成）

---

## [0.1.0] - 2026-05-18

### Added (新增)
- Initial project scaffolding (初始项目脚手架)
- Basic package structure (基础包结构)
- Placeholder for core modules (核心模块占位符)

---

## Template for future versions (未来版本模板)

## [X.Y.Z] - YYYY-MM-DD

### Added (新增)
- 

### Changed (变更)
- 

### Deprecated (弃用)
- 

### Removed (移除)
- 

### Fixed (修复)
- 

### Security (安全)
- 
