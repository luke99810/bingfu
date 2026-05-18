"""
Visual Module Tests (可视化模块测试)
Tests for the MilitaryCommandConsole visualization module.
Note: These tests skip actual window creation (Tkinter).
"""

import pytest
from bingfu.visual.styles import (
    COLORS, FONTS, ICONS, BORDER_DOUBLE,
    CHINESE_NUMBERS, to_chinese_number
)


class TestStyles:
    """Test styles module"""

    def test_colors_exist(self):
        """Test all required colors are defined"""
        required_colors = [
            "bg_dark", "bg_medium", "bg_light",
            "gold", "gold_bright", "gold_dark",
            "text_primary", "text_secondary",
            "status_online", "status_busy", "status_offline"
        ]
        for color in required_colors:
            assert color in COLORS
            assert COLORS[color].startswith("#")

    def test_fonts_exist(self):
        """Test all required fonts are defined"""
        required_fonts = ["title", "subtitle", "body", "mono", "small"]
        for font in required_fonts:
            assert font in FONTS

    def test_icons_exist(self):
        """Test all required icons are defined"""
        required_icons = ["general", "battle", "report", "drum", "bell"]
        for icon in required_icons:
            assert icon in ICONS

    def test_chinese_numbers(self):
        """Test Chinese number conversion"""
        assert to_chinese_number(0) == "零"
        assert to_chinese_number(1) == "一"
        assert to_chinese_number(5) == "五"
        assert to_chinese_number(10) == "十"


class TestConsoleAPI:
    """Test MilitaryCommandConsole API without creating windows"""

    def test_console_import(self):
        """Test console can be imported"""
        from bingfu.visual import MilitaryCommandConsole
        assert MilitaryCommandConsole is not None

    def test_console_creation_api(self):
        """Test console API parameters"""
        from bingfu.visual import MilitaryCommandConsole

        # This should not create actual window
        console = MilitaryCommandConsole(
            title="测试控制台",
            width=1200,
            height=800
        )

        assert console.title == "测试控制台"
        assert console.width == 1200
        assert console.height == 800

        console.stop()

    def test_add_general_api(self):
        """Test add_general method exists"""
        from bingfu.visual import MilitaryCommandConsole

        console = MilitaryCommandConsole(title="测试")
        assert hasattr(console, "add_general")

        console.stop()

    def test_add_report_api(self):
        """Test add_report method exists"""
        from bingfu.visual import MilitaryCommandConsole

        console = MilitaryCommandConsole(title="测试")
        assert hasattr(console, "add_report")

        console.stop()

    def test_update_battle_status_api(self):
        """Test update_battle_status method exists"""
        from bingfu.visual import MilitaryCommandConsole

        console = MilitaryCommandConsole(title="测试")
        assert hasattr(console, "update_battle_status")

        console.stop()

    def test_add_tactics_api(self):
        """Test add_tactics method exists"""
        from bingfu.visual import MilitaryCommandConsole

        console = MilitaryCommandConsole(title="测试")
        assert hasattr(console, "add_tactics")

        console.stop()


class TestComponents:
    """Test UI component classes"""

    def test_general_card_import(self):
        """Test GeneralCard can be imported"""
        from bingfu.visual.components import GeneralCard
        assert GeneralCard is not None

    def test_battle_status_panel_import(self):
        """Test BattleStatusPanel can be imported"""
        from bingfu.visual.components import BattleStatusPanel
        assert BattleStatusPanel is not None

    def test_report_panel_import(self):
        """Test ReportPanel can be imported"""
        from bingfu.visual.components import ReportPanel
        assert ReportPanel is not None

    def test_stats_bar_import(self):
        """Test StatsBar can be imported"""
        from bingfu.visual.components import StatsBar
        assert StatsBar is not None

    def test_command_input_import(self):
        """Test CommandInput can be imported"""
        from bingfu.visual.components import CommandInput
        assert CommandInput is not None

    def test_styled_frame_import(self):
        """Test StyledFrame can be imported"""
        from bingfu.visual.components import StyledFrame
        assert StyledFrame is not None


class TestQuickFunctions:
    """Test quick utility functions"""

    def test_create_console_function(self):
        """Test create_console function"""
        from bingfu.visual.console import create_console

        console = create_console(title="测试")
        assert console is not None
        console.stop()

    def test_launch_demo_function_exists(self):
        """Test launch_demo function exists"""
        from bingfu.visual.console import launch_demo
        assert callable(launch_demo)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
