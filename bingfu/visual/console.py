"""
BingFu 中军帐主控制台
古代军事风格的Multi-Agent可视化监控界面
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime

from .styles import COLORS, FONTS, ICONS
from .components import (
    GeneralCard, BattleStatusPanel, ReportPanel,
    StatsBar, CommandInput, StyledFrame
)
from ..commander import Commander
from ..memory import Memory


class MilitaryCommandConsole:
    """
    中军帐可视化控制台

    提供古代军事风格的Multi-Agent框架可视化界面，
    支持将领状态监控、战役态势分析、军情速递等功能。

    使用示例:
    ```python
    from bingfu.visual import MilitaryCommandConsole

    # 创建控制台
    console = MilitaryCommandConsole()

    # 添加将领
    console.add_general("韩信", "online", "统帅", "正在分析战场形势")

    # 添加军情报告
    console.add_report("侦察回报", "发现敌军粮草运输队", "success")

    # 启动
    console.run()
    ```
    """

    def __init__(
        self,
        title: str = "兵符 · 中军帐",
        width: int = 1200,
        height: int = 800,
        commander: Optional[Commander] = None,
        memory: Optional[Memory] = None
    ):
        """
        初始化控制台

        Args:
            title: 窗口标题
            width: 窗口宽度
            height: 窗口高度
            commander: 可选的Commander实例，用于与框架集成
            memory: 可选的Memory实例，用于状态持久化
        """
        self.title = title
        self.width = width
        self.height = height
        self.commander = commander
        self.memory = memory

        # 内部状态
        self.generals: Dict[str, Dict] = {}
        self.reports: List[Dict] = []
        self.is_running = False

        # 命令历史
        self.command_history: List[str] = []
        self.history_index = -1

        # 创建窗口
        self._root: Optional[tk.Tk] = None
        self._create_window()

    def _create_window(self):
        """创建主窗口"""
        self._root = tk.Tk()
        self._root.title(self.title)
        self._root.geometry(f"{self.width}x{self.height}")
        self._root.minsize(900, 600)

        # 设置主题色
        self._root.configure(bg=COLORS["bg_dark"])

        # 阻止窗口关闭时自动销毁
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

        # 构建UI
        self._build_ui()

    def _build_ui(self):
        """构建用户界面"""
        # 标题栏
        self._create_title_bar()

        # 主内容区 - 使用PanedWindow实现可调节布局
        main_paned = tk.PanedWindow(
            self._root,
            bg=COLORS["bg_dark"],
            sashrelief="groove",
            sashwidth=5,
            handlesize=10,
            handlepad=5
        )
        main_paned.pack(fill="both", expand=True)

        # 左侧面板 - 将领名录
        left_panel = self._create_left_panel(main_paned)
        main_paned.add(left_panel, width=280)

        # 中间面板 - 战役态势
        center_panel = self._create_center_panel(main_paned)
        main_paned.add(center_panel, width=400)

        # 右侧面板 - 军情速递
        right_panel = self._create_right_panel(main_paned)
        main_paned.add(right_panel)

        # 底部状态栏
        self.stats_bar = StatsBar(self._root)
        self.stats_bar.pack(side="bottom", fill="x")

        # 命令输入区
        self.command_input = CommandInput(
            self._root,
            on_submit=self._handle_command
        )
        self.command_input.pack(side="bottom", fill="x", pady=(0, 5))

        # 日志输出区
        self.log_area = scrolledtext.ScrolledText(
            self._root,
            height=8,
            font=FONTS["mono"],
            bg=COLORS["bg_dark"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["gold"],
            relief="flat",
            state="disabled"
        )
        self.log_area.pack(side="bottom", fill="x", padx=5, pady=(0, 5))

        # 初始化日志
        self._log("系统启动中...")

    def _create_title_bar(self):
        """创建标题栏"""
        title_frame = tk.Frame(self._root, bg=COLORS["bg_dark"], height=50)
        title_frame.pack(fill="x", pady=(0, 5))
        title_frame.pack_propagate(False)

        # 左侧装饰
        left_decor = tk.Label(
            title_frame,
            text="╔══╗",
            font=("Consolas", 12),
            bg=COLORS["bg_dark"],
            fg=COLORS["gold"]
        )
        left_decor.pack(side="left", padx=(20, 5))

        # 标题
        title_label = tk.Label(
            title_frame,
            text=self.title,
            font=FONTS["title"],
            bg=COLORS["bg_dark"],
            fg=COLORS["gold"]
        )
        title_label.pack(side="left")

        # 右侧装饰
        right_decor = tk.Label(
            title_frame,
            text="╔══╗",
            font=("Consolas", 12),
            bg=COLORS["bg_dark"],
            fg=COLORS["gold"]
        )
        right_decor.pack(side="right", padx=(5, 20))

        # 副标题
        subtitle_label = tk.Label(
            title_frame,
            text="Multi-Agent 战役指挥系统",
            font=FONTS["small"],
            bg=COLORS["bg_dark"],
            fg=COLORS["text_muted"]
        )
        subtitle_label.pack(side="right", padx=(10, 5))

    def _create_left_panel(self, parent) -> tk.Frame:
        """创建左侧面板 - 将领名录"""
        frame = tk.Frame(parent, bg=COLORS["bg_dark"])

        # 标题
        header = tk.Frame(frame, bg=COLORS["gold_dark"], height=35)
        header.pack(fill="x", padx=5, pady=(5, 0))
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"  {ICONS['general']} 将领名录  ",
            font=FONTS["subtitle"],
            bg=COLORS["gold_dark"],
            fg=COLORS["bg_dark"]
        ).pack(side="left", pady=5)

        # 滚动区域
        canvas_frame = tk.Frame(frame, bg=COLORS["bg_dark"])
        canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(canvas_frame)
        scrollbar.pack(side="right", fill="y")

        self.generals_canvas = tk.Canvas(
            canvas_frame,
            bg=COLORS["bg_dark"],
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.generals_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.generals_canvas.yview)

        self.generals_frame = tk.Frame(self.generals_canvas, bg=COLORS["bg_dark"])
        self.generals_canvas.create_window((0, 0), window=self.generals_frame, anchor="nw")

        self.generals_frame.bind("<Configure>",
            lambda e: self.generals_canvas.configure(scrollregion=self.generals_canvas.bbox("all")))

        # 操作按钮
        btn_frame = tk.Frame(frame, bg=COLORS["bg_dark"])
        btn_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(
            btn_frame,
            text=f"{ICONS['drum']} 击鼓",
            font=FONTS["body"],
            bg=COLORS["status_online"],
            fg=COLORS["bg_dark"],
            command=self._on_drum,
            relief="flat",
            cursor="hand2"
        ).pack(side="left", padx=2, expand=True, fill="x")

        tk.Button(
            btn_frame,
            text=f"{ICONS['bell']} 鸣金",
            font=FONTS["body"],
            bg=COLORS["status_offline"],
            fg=COLORS["bg_dark"],
            command=self._on_bell,
            relief="flat",
            cursor="hand2"
        ).pack(side="left", padx=2, expand=True, fill="x")

        return frame

    def _create_center_panel(self, parent) -> tk.Frame:
        """创建中间面板 - 战役态势"""
        frame = tk.Frame(parent, bg=COLORS["bg_dark"])

        # 战役态势面板
        self.battle_panel = BattleStatusPanel(frame)
        self.battle_panel.pack(fill="both", expand=True, padx=5, pady=5)

        # 战术建议区
        tactics_frame = StyledFrame(frame, title="孙子兵法 · 战术建议")
        tactics_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.tactics_text = tk.Text(
            tactics_frame,
            font=FONTS["body"],
            bg=COLORS["bg_medium"],
            fg=COLORS["text_primary"],
            relief="flat",
            height=8,
            wrap="word"
        )
        self.tactics_text.pack(fill="both", expand=True, padx=5, pady=5)

        return frame

    def _create_right_panel(self, parent) -> tk.Frame:
        """创建右侧面板 - 军情速递"""
        frame = tk.Frame(parent, bg=COLORS["bg_dark"])

        # 军情速递面板
        self.report_panel = ReportPanel(frame)
        self.report_panel.pack(fill="both", expand=True, padx=5, pady=5)

        return frame

    # ========== 公共API ==========

    def add_general(
        self,
        name: str,
        status: str = "offline",
        role: str = "",
        message: str = ""
    ):
        """
        添加或更新将领

        Args:
            name: 将领名称
            status: 状态 (online/busy/idle/offline)
            role: 角色
            message: 当前消息
        """
        self.generals[name] = {
            "status": status,
            "role": role,
            "message": message
        }
        self._refresh_generals()
        self._update_stats()
        self._log(f"将领 {name} 状态更新: {status}")

    def remove_general(self, name: str):
        """移除将领"""
        if name in self.generals:
            del self.generals[name]
            self._refresh_generals()
            self._update_stats()
            self._log(f"将领 {name} 已撤离")

    def add_report(
        self,
        title: str,
        content: str,
        report_type: str = "info"
    ):
        """
        添加军情报告

        Args:
            title: 报告标题
            content: 报告内容
            report_type: 报告类型 (info/warning/danger/success)
        """
        self.reports.append({
            "title": title,
            "content": content,
            "type": report_type,
            "timestamp": datetime.now()
        })
        self.report_panel.add_report(title, content, report_type)
        self._log(f"收到军情: {title}", level=report_type)

    def update_battle_status(
        self,
        own_strength: int,
        enemy_strength: int,
        strategy: str = ""
    ):
        """更新战役态势"""
        self.battle_panel.update(own_strength, enemy_strength, strategy)

    def add_tactics(self, tactics: str):
        """添加战术建议"""
        self.tactics_text.insert("end", f"\n• {tactics}")
        self.tactics_text.see("end")

    def clear_tactics(self):
        """清空战术建议"""
        self.tactics_text.delete("1.0", "end")

    def set_commander(self, commander: Commander):
        """设置Commander实例"""
        self.commander = commander

    def set_memory(self, memory: Memory):
        """设置Memory实例"""
        self.memory = memory

    # ========== 内部方法 ==========

    def _refresh_generals(self):
        """刷新将领列表"""
        # 清除现有卡片
        for widget in self.generals_frame.winfo_children():
            widget.destroy()

        # 重新创建卡片
        for name, info in self.generals.items():
            card = GeneralCard(
                self.generals_frame,
                name=name,
                status=info["status"],
                role=info["role"],
                message=info["message"]
            )
            card.pack(fill="x", pady=3, padx=3)

    def _update_stats(self):
        """更新统计信息"""
        online = sum(1 for g in self.generals.values() if g["status"] == "online")
        busy = sum(1 for g in self.generals.values() if g["status"] == "busy")
        total = len(self.generals)

        self.stats_bar.update(
            generals=f"{online}",
            tasks=f"{total}",
            completed=f"{int(busy/total*100) if total > 0 else 0}%",
            running=f"{busy}"
        )

    def _log(self, message: str, level: str = "info"):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        colors = {
            "info": COLORS["text_secondary"],
            "warning": COLORS["status_busy"],
            "danger": COLORS["status_offline"],
            "success": COLORS["status_online"]
        }
        color = colors.get(level, COLORS["text_secondary"])

        self.log_area.config(state="normal")
        self.log_area.insert("end", f"[{timestamp}] {message}\n", level)
        self.log_area.tag_config(level, foreground=color)
        self.log_area.see("end")
        self.log_area.config(state="disabled")

    def _handle_command(self, command: str):
        """处理用户命令 —— 支持斜杠命令 + 自然语言"""
        if not command.strip():
            return

        self._log(f"传达军令: {command}")

        # 添加到历史
        self.command_history.append(command)
        self.history_index = len(self.command_history)

        # 斜杠命令优先解析
        if command.startswith("/help"):
            self._show_help()
        elif command.startswith("/add "):
            self._cmd_add_general(command[5:])
        elif command.startswith("/remove "):
            self._cmd_remove_general(command[8:])
        elif command.startswith("/report "):
            parts = command[8:].split(" ", 1)
            if len(parts) == 2:
                self.add_report(parts[0], parts[1])
        elif command.startswith("/battle "):
            self._cmd_update_battle(command[8:])
        elif command == "/clear":
            self.log_area.config(state="normal")
            self.log_area.delete("1.0", "end")
            self.log_area.config(state="disabled")
        elif command.startswith("/"):
            self._log("未知指令，输入 /help 查看斜杠命令帮助")
        else:
            # 自然语言理解层
            self._handle_natural_language(command)

    def _handle_natural_language(self, text: str):
        """
        自然语言指令处理器
        基于关键词匹配，将自然语言映射到具体操作
        """
        t = text.lower()

        # ── 查询类 ──────────────────────────────────────────────
        # 查询将领数量
        if any(kw in t for kw in ["将士数量", "将领数量", "几位将领", "多少将领",
                                   "有哪些将领", "将领名单", "点兵", "兵力情况"]):
            total = len(self.generals)
            online = sum(1 for g in self.generals.values() if g["status"] == "online")
            busy   = sum(1 for g in self.generals.values() if g["status"] == "busy")
            idle   = sum(1 for g in self.generals.values() if g["status"] == "idle")
            offline = sum(1 for g in self.generals.values() if g["status"] == "offline")
            names = "、".join(self.generals.keys()) if self.generals else "（无）"
            self._log(f"📊 军中共有将领 {total} 位：{names}")
            self._log(f"   在线 {online} | 作战中 {busy} | 待命 {idle} | 离线 {offline}")
            return

        # 查询战况/当前态势
        if any(kw in t for kw in ["战况", "战情", "态势", "敌情", "战场形势",
                                   "目前情况", "当前情况", "现在怎么样", "形势"]):
            try:
                own_txt   = self.battle_panel.own_label.cget("text")
                enemy_txt = self.battle_panel.enemy_label.cget("text")
                strategy  = self.battle_panel.strategy_label.cget("text")
                self._log(f"⚔️  当前战役态势：")
                self._log(f"   己方兵力：{own_txt} | 敌方兵力：{enemy_txt}")
                self._log(f"   战略建议：{strategy}")
            except Exception:
                self._log("⚔️  暂无战役态势数据")
            return

        # 查询军情报告
        if any(kw in t for kw in ["军情", "情报", "报告", "有何军情", "战报"]):
            if self.reports:
                self._log(f"📋 共收到 {len(self.reports)} 条军情：")
                for r in self.reports[-3:]:  # 显示最近3条
                    self._log(f"   [{r.get('type','info').upper()}] {r['title']}：{r['content'][:40]}")
            else:
                self._log("📋 暂无军情报告")
            return

        # ── 操作类 ──────────────────────────────────────────────
        # 添加将领（识别格式：添加将领 <名字> [状态] [角色]）
        if any(kw in t for kw in ["添加将领", "加入将领", "新增将领", "招募将领", "部署将领"]):
            # 提取名字（取命令中的最后一个"词"，或提示用斜杠命令）
            words = text.replace("添加将领", "").replace("加入将领", "") \
                        .replace("新增将领", "").replace("招募将领", "") \
                        .replace("部署将领", "").strip().split()
            if words:
                name = words[0]
                status = words[1] if len(words) > 1 else "online"
                role   = words[2] if len(words) > 2 else ""
                self.add_general(name, status, role)
                self._log(f"✅ 将领 {name} 已加入麾下")
            else:
                self._log("请指定将领姓名，例如：添加将领 张辽 online 前锋")
            return

        # 移除/撤退将领
        if any(kw in t for kw in ["移除将领", "撤退将领", "撤销将领", "删除将领", "将领撤离"]):
            words = text.replace("移除将领", "").replace("撤退将领", "") \
                        .replace("撤销将领", "").replace("删除将领", "") \
                        .replace("将领撤离", "").strip().split()
            if words:
                name = words[0]
                self.remove_general(name)
                self._log(f"✅ 将领 {name} 已撤离")
            else:
                self._log("请指定将领姓名，例如：移除将领 张辽")
            return

        # 出击/击鼓
        if any(kw in t for kw in ["出击", "击鼓", "全军出击", "进攻", "冲锋", "发动进攻"]):
            self._on_drum()
            return

        # 收兵/鸣金
        if any(kw in t for kw in ["收兵", "鸣金", "撤退", "退兵", "鸣金收兵"]):
            self._log("提示：收兵请点击界面左下角「鸣金」按钮，需确认操作")
            return

        # 清空日志
        if any(kw in t for kw in ["清空日志", "清除日志", "清空记录", "清屏"]):
            self.log_area.config(state="normal")
            self.log_area.delete("1.0", "end")
            self.log_area.config(state="disabled")
            self._log("日志已清空")
            return

        # 更新战役态势（识别数字）
        import re
        nums = re.findall(r'\d+', text)
        if len(nums) >= 2 and any(kw in t for kw in ["兵力", "对阵", "我军", "敌军", "更新战役", "更新态势"]):
            own, enemy = int(nums[0]), int(nums[1])
            strategy = "形势更新中"
            # 提取策略描述（引号内容 或 最后的词语）
            quote = re.findall(r'[「"](.*?)[」"]', text)
            if quote:
                strategy = quote[0]
            self.update_battle_status(own, enemy, strategy)
            self._log(f"✅ 战役态势已更新：己方 {own} | 敌方 {enemy}")
            return

        # 帮助
        if any(kw in t for kw in ["帮助", "help", "怎么用", "命令列表", "有什么命令"]):
            self._show_help_natural()
            return

        # ── 未能识别 ──────────────────────────────────────────
        self._log(f"❓ 未能识别指令「{text}」")
        self._log("   支持自然语言，如：战况如何 / 统计将士数量 / 全军出击")
        self._log("   或输入 /help 查看斜杠命令，输入「帮助」查看自然语言用法")

    def _cmd_add_general(self, args: str):
        """添加将领命令"""
        parts = args.split(" ", 2)
        name = parts[0]
        status = parts[1] if len(parts) > 1 else "offline"
        role = parts[2] if len(parts) > 2 else ""
        self.add_general(name, status, role)

    def _cmd_remove_general(self, name: str):
        """移除将领命令"""
        self.remove_general(name)

    def _cmd_update_battle(self, args: str):
        """更新战役命令"""
        parts = args.split()
        if len(parts) >= 2:
            try:
                own = int(parts[0])
                enemy = int(parts[1])
                strategy = parts[2] if len(parts) > 2 else ""
                self.update_battle_status(own, enemy, strategy)
            except ValueError:
                self._log("格式错误: /battle 己方兵力 敌方兵力 [策略]")

    def _show_help(self):
        """显示帮助"""
        help_text = """
╔════════════════════════════════════════════╗
║  兵符 · 中军帐 命令帮助                       ║
╠════════════════════════════════════════════╣
║  /add <将领> [状态] [角色]                   ║
║      添加将领 (状态: online/busy/idle/offline)║
║                                             ║
║  /remove <将领>                              ║
║      移除将领                                ║
║                                             ║
║  /report <标题> <内容>                       ║
║      添加军情报告                            ║
║                                             ║
║  /battle <己方> <敌方> [策略]                ║
║      更新战役态势                            ║
║                                             ║
║  /clear                                      ║
║      清空日志                                ║
╚════════════════════════════════════════════╝
"""
        self.log_area.config(state="normal")
        self.log_area.insert("end", help_text)
        self.log_area.see("end")
        self.log_area.config(state="disabled")

    def _show_help_natural(self):
        """显示自然语言帮助"""
        help_text = """
╔════════════════════════════════════════════════╗
║  兵符 · 中军帐 自然语言指令说明                     ║
╠════════════════════════════════════════════════╣
║  【查询类】                                       ║
║  统计我军将士数量 / 有哪些将领 / 点兵               ║
║  目前战况如何 / 当前态势 / 战场形势                  ║
║  有何军情 / 战报 / 情报                            ║
║                                                 ║
║  【操作类】                                       ║
║  添加将领 张辽 online 前锋                         ║
║  移除将领 张辽                                    ║
║  全军出击 / 出击 / 进攻                            ║
║  清空日志 / 清屏                                  ║
║  更新战役 我军30000 敌军80000 「以逸待劳」           ║
║                                                 ║
║  【斜杠命令】输入 /help 查看                        ║
╚════════════════════════════════════════════════╝
"""
        self.log_area.config(state="normal")
        self.log_area.insert("end", help_text)
        self.log_area.see("end")
        self.log_area.config(state="disabled")

    def _on_drum(self):
        """击鼓 - 全军出击"""
        self._log("🥁 击鼓！全军出击！")
        for name, info in self.generals.items():
            if info["status"] in ("online", "idle"):
                info["status"] = "busy"
        self._refresh_generals()
        self._update_stats()

    def _on_bell(self):
        """鸣金 - 收兵"""
        result = messagebox.askyesno("鸣金收兵", "确定要鸣金收兵吗？")
        if result:
            self._log("🔔 鸣金！收兵回营！")
            for name, info in self.generals.items():
                info["status"] = "offline"
            self._refresh_generals()
            self._update_stats()

    def _on_close(self):
        """窗口关闭处理"""
        result = messagebox.askyesno("退出", "确定要关闭中军帐吗？")
        if result:
            self.is_running = False
            self._root.destroy()

    def run(self, blocking: bool = True):
        """
        运行控制台

        Args:
            blocking: 是否阻塞运行
        """
        self.is_running = True
        self._log("兵符 · 中军帐 已启动")
        self._log("支持自然语言指令，如：战况如何 / 统计将士数量 / 全军出击")
        self._log("输入「帮助」查看自然语言用法，或输入 /help 查看斜杠命令")

        # 初始化示例数据
        self._init_demo_data()

        if blocking:
            self._root.mainloop()
        else:
            # 非阻塞模式 - 在新线程中运行
            thread = threading.Thread(target=self._root.mainloop, daemon=True)
            thread.start()

    def _init_demo_data(self):
        """初始化演示数据"""
        # 添加示例将领
        self.add_general("韩信", "online", "统帅", "正在分析战场形势")
        self.add_general("白起", "busy", "主将", "率领先锋部队突击")
        self.add_general("项羽", "idle", "虎将", "待命准备冲锋")
        self.add_general("诸葛亮", "online", "军师", "夜观星象推演战局")

        # 添加示例军情
        self.add_report("侦察回报", "敌军粮草队已过乌江，预计明日午时抵达", "success")
        self.add_report("斥候急报", "发现敌军增援部队约三万人", "warning")
        self.add_report("后勤报告", "我军粮草尚可支撑七日", "info")

        # 更新战役态势
        self.update_battle_status(30000, 80000, "敌众我寡，宜用奇兵")

        # 添加战术建议
        self.clear_tactics()
        self.tactics_text.insert("1.0", "• 以逸待劳，后发制人\n")
        self.tactics_text.insert("end", "• 诱敌深入，设伏聚歼\n")
        self.tactics_text.insert("end", "• 断其粮道，围而不攻")

    def stop(self):
        """停止控制台"""
        self.is_running = False
        if self._root:
            self._root.quit()


# 快捷函数
def create_console(**kwargs) -> MilitaryCommandConsole:
    """创建并返回控制台实例"""
    return MilitaryCommandConsole(**kwargs)


def launch_demo():
    """启动演示模式"""
    console = MilitaryCommandConsole()
    console.run()
