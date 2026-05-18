# Changelog (变更日志)

All notable changes to the **BingFu (兵符)** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] (未发布)

### Added (新增)
- **Project Structure (项目结构)**
  - `pyproject.toml` — Project configuration with dependencies
  - `README.md` — Complete Chinese/English documentation
  - `.gitignore` — Python project ignore rules
  - `LICENSE` — MIT License
  - `CHANGELOG.md` — Version history
  - `config.yaml` — Complete configuration example

- **Core Modules (核心模块)**
  - `bingfu/__init__.py` — Package initialization, exports all classes
  - `bingfu/agent.py` — Agent class with drum/gong signals, tools, memory
  - `bingfu/tool.py` — Tool class for creating reusable tools
  - `bingfu/memory.py` — Memory class (file-based or in-memory)
  - `bingfu/signal.py` — Drum/Gong signal system (击鼓/鸣金)
  - `bingfu/commander.py` — Multi-agent coordinator (指挥系统)
  - `bingfu/bingfu.py` — Main BingFu class (兵符主类)
  - `bingfu/cli.py` — Command-line interface (命令行界面)

- **Examples (示例)**
  - `examples/basic_usage.py` — Basic usage with single agent
  - `examples/multi_agent.py` — Multi-agent coordination examples
  - `examples/custom_agent.py` — Custom agent with tools and memory

- **Tests (测试)**
  - `tests/__init__.py` — Test package initialization
  - `tests/test_agent.py` — Agent class unit tests
  - `tests/test_signal.py` — Signal class unit tests
  - `tests/test_commander.py` — Commander class unit tests

### Changed (变更)
- Updated author email to match GitHub username (luke99810)
- Updated README with complete development status

### Deprecated (弃用)
- None

### Removed (移除)
- Mini-program related planning (removed mini-program references)

### Fixed (修复)
- None

### Security (安全)
- None

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
