"""
BingFu (兵符) — Lightweight Multi‑Agent Framework
Inspired by ancient Chinese warfare strategies.
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

__all__ = [
    "Agent",
    "Tool",
    "Memory",
    "Drum",
    "Gong",
    "Commander",
    "BingFu",
]
