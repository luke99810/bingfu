"""
Tests for Agent module (Agent 模块测试)
"""

import pytest
from bingfu.agent import Agent


class TestAgent:
    """Test cases for Agent class (Agent 类测试用例)."""
    
    def test_create_agent(self):
        """Test creating an agent."""
        agent = Agent(name="TestAgent")
        assert agent.name == "TestAgent"
        assert agent.is_active is False
    
    def test_create_agent_with_role(self):
        """Test creating an agent with a role."""
        agent = Agent(name="Scout", role="Scout")
        assert agent.name == "Scout"
        assert agent.role == "Scout"
    
    def test_drum_signal(self):
        """Test drum signal activates agent."""
        agent = Agent(name="TestAgent")
        result = agent.drum("Test task")
        assert "🥁" in result
        assert agent.is_active is True
    
    def test_gong_signal(self):
        """Test gong signal deactivates agent."""
        agent = Agent(name="TestAgent", is_active=True)
        result = agent.gong()
        assert "🔔" in result
        assert agent.is_active is False
    
    def test_add_tool(self):
        """Test adding a tool to agent."""
        from bingfu.tool import Tool
        
        agent = Agent(name="TestAgent")
        tool = Tool(name="TestTool")
        agent.add_tool(tool)
        
        assert len(agent.tools) == 1
        assert agent.tools[0].name == "TestTool"
    
    def test_remove_tool(self):
        """Test removing a tool from agent."""
        from bingfu.tool import Tool
        
        agent = Agent(name="TestAgent")
        tool = Tool(name="TestTool")
        agent.add_tool(tool)
        agent.remove_tool(tool)
        
        assert len(agent.tools) == 0
    
    def test_execute_task(self):
        """Test executing a task."""
        agent = Agent(name="TestAgent")
        result = agent.execute("Test task")
        
        assert "TestAgent" in result
        assert "Test task" in result
    
    def test_str_representation(self):
        """Test string representation of agent."""
        agent = Agent(name="TestAgent", role="Tester")
        str_repr = str(agent)
        
        assert "TestAgent" in str_repr
        assert "Tester" in str_repr
