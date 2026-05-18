"""
CLI module (命令行界面模块)
Provides command‑line interface to BingFu, inspired by ancient Chinese warfare.
"""

import argparse
import sys
from typing import Optional

from bingfu.bingfu import BingFu
from bingfu.agent import Agent
from bingfu.signal import drum, gong


def create_parser() -> argparse.ArgumentParser:
    """
    Create CLI argument parser (创建命令行参数解析器).
    
    Returns:
        argparse.ArgumentParser: Configured parser.
    """
    parser = argparse.ArgumentParser(
        prog="bingfu",
        description="BingFu (兵符) — Lightweight Multi‑Agent Framework",
        epilog="Example: bingfu drum MyAgent 'Do something'"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # drum command (击鼓命令)
    drum_parser = subparsers.add_parser(
        "drum",
        help="Send drum signal (击鼓) to start an agent"
    )
    drum_parser.add_argument("agent", help="Agent name")
    drum_parser.add_argument("task", help="Task description")
    
    # gong command (鸣金命令)
    gong_parser = subparsers.add_parser(
        "gong",
        help="Send gong signal (鸣金) to stop an agent"
    )
    gong_parser.add_argument("agent", help="Agent name")
    
    # add‑agent command (添加智能体命令)
    add_parser = subparsers.add_parser(
        "add‑agent",
        help="Add a new agent (添加智能体)"
    )
    add_parser.add_argument("name", help="Agent name")
    add_parser.add_argument("--role", help="Agent role (optional)")
    
    # status command (状态命令)
    subparsers.add_parser(
        "status",
        help="Show BingFu status (显示兵符状态)"
    )
    
    # version command (版本命令)
    subparsers.add_parser(
        "version",
        help="Show BingFu version (显示版本)"
    )
    
    return parser


def handle_drum(args: argparse.Namespace, master: BingFu) -> str:
    """Handle drum command (处理击鼓命令)."""
    result = master.drum(args.agent, args.task)
    return result


def handle_gong(args: argparse.Namespace, master: BingFu) -> str:
    """Handle gong command (处理鸣金命令)."""
    result = master.gong(args.agent)
    return result


def handle_add_agent(args: argparse.Namespace, master: BingFu) -> str:
    """Handle add‑agent command (处理添加智能体命令)."""
    agent = Agent(name=args.name, role=args.role)
    master.add_agent(agent)
    return f"✅ Agent '{args.name}' added."


def handle_status(master: BingFu) -> str:
    """Handle status command (处理状态命令)."""
    status = master.status()
    lines = [
        f"BingFu Status (兵符状态)",
        "─" * 40,
        f"Name: {status['name']}",
        f"Version: {status['version']}",
        f"Agents: {status['agent_count']},
        f"Tools: {status['tool_count']}",
        f"Memories: {status['memory_count']}",
        f"Commander: {'✅ Enabled' if status['commander_enabled'] else '⚫ Disabled'}",
    ]
    return "\n".join(lines)


def handle_version() -> str:
    """Handle version command (处理版本命令)."""
    return f"BingFu (兵符) v{master.version}"


def main() -> None:
    """
    Main CLI entry point (CLI 主入口).
    Inspired by ancient Chinese warfare: 兵符出，令必行。
    """
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize BingFu (初始化兵符)
    master = BingFu()
    
    # Dispatch commands (调度命令)
    result: Optional[str] = None
    
    if args.command == "drum":
        result = handle_drum(args, master)
    elif args.command == "gong":
        result = handle_gong(args, master)
    elif args.command == "add‑agent":
        result = handle_add_agent(args, master)
    elif args.command == "status":
        result = handle_status(master)
    elif args.command == "version":
        result = handle_version()
    
    if result:
        print(result)


if __name__ == "__main__":
    main()
