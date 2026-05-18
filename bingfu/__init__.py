"""
BingFu (兵符) — Lightweight Multi‑Agent Framework
Inspired by ancient Chinese warfare strategies.

兵符 · 轻量级多智能体框架
以中国古代军事智慧为灵感的多智能体协作框架
"""

__version__ = "0.1.0"
__author__ = "SuXin (州哥)"
__email__ = "luke99810@example.com"

from bingfu.agent import Agent
from bingfu.tool import Tool
from bingfu.memory import Memory
from bingfu.signal import Drum, Gong
from bingfu.commander import Commander
from bingfu.bingfu import BingFu
from bingfu.tactics import TacticsEngine, SunTzuAgent, TacticType, TacticalContext

__all__ = [
    # 核心模块
    "Agent",
    "Tool",
    "Memory",
    "Drum",
    "Gong",
    "Commander",
    "BingFu",
    # 战术引擎
    "TacticsEngine",
    "SunTzuAgent",
    "TacticType",
    "TacticalContext",
]
