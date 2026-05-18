"""
Unit tests for Tool module.
测试工具模块
"""

import pytest
from bingfu.tool import Tool


class TestTool:
    """Test suite for Tool class."""

    def test_create_basic_tool(self):
        """Test creating a basic tool without function."""
        tool = Tool(name="Sword", description="A sharp blade")
        assert tool.name == "Sword"
        assert tool.description == "A sharp blade"
        assert tool.function is None

    def test_create_tool_with_function(self):
        """Test creating a tool with an attached function."""
        def multiply(a: int, b: int) -> int:
            return a * b

        tool = Tool.create(
            name="Calculator",
            func=multiply,
            description="Multiplies two numbers"
        )

        assert tool.name == "Calculator"
        assert tool.description == "Multiplies two numbers"
        assert tool.function is not None
        assert tool.function(3, 4) == 12

    def test_use_tool_without_function(self):
        """Test using a tool without function returns placeholder."""
        tool = Tool(name="EmptyTool")
        result = tool.use()
        assert "no function attached" in result
        assert "EmptyTool" in result

    def test_use_tool_with_function(self):
        """Test using a tool with function."""
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        tool = Tool.create(name="Greeter", func=greet)
        result = tool.use("Zhang San")
        assert result == "Hello, Zhang San!"

    def test_use_tool_with_kwargs(self):
        """Test using a tool with keyword arguments."""
        def power(base: int, exp: int = 2) -> int:
            return base ** exp

        tool = Tool.create(name="PowerTool", func=power)
        result = tool.use(base=3, exp=3)
        assert result == 27

    def test_use_tool_with_error(self):
        """Test tool handles function errors gracefully."""
        def failing_function(x):
            raise ValueError("Test error")

        tool = Tool.create(name="FailingTool", func=failing_function)
        result = tool.use("test")
        assert "Error" in result
        assert "Test error" in result

    def test_tool_str_representation(self):
        """Test Tool string representation."""
        tool = Tool(name="TestTool", description="A test")
        s = str(tool)
        assert "TestTool" in s
        assert "A test" in s
        assert "No function" in s

    def test_tool_str_with_function(self):
        """Test Tool string representation with function."""
        def dummy():
            pass

        tool = Tool.create(name="FuncTool", func=dummy)
        s = str(tool)
        assert "FuncTool" in s
        assert "Has function" in s

    def test_tool_repr(self):
        """Test Tool repr."""
        tool = Tool(name="ReprTool")
        assert repr(tool) == str(tool)

    def test_tool_without_description(self):
        """Test creating a tool without description."""
        tool = Tool(name="NoDesc")
        assert tool.name == "NoDesc"
        assert tool.description is None

    def test_tool_create_classmethod(self):
        """Test Tool.create classmethod returns Tool instance."""
        def add(a, b):
            return a + b

        tool = Tool.create(name="Adder", func=add)
        assert isinstance(tool, Tool)
        assert tool.name == "Adder"

    def test_multiple_tools_independent(self):
        """Test that multiple tools are independent."""
        def calc1(x):
            return x * 2

        def calc2(x):
            return x * 3

        tool1 = Tool.create(name="Calc1", func=calc1)
        tool2 = Tool.create(name="Calc2", func=calc2)

        assert tool1.use(5) == 10
        assert tool2.use(5) == 15


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
