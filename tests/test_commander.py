"""
Tests for Commander module (Commander 模块测试)
"""

import pytest
from bingfu.commander import Commander
from bingfu.agent import Agent


class TestCommander:
    """Test cases for Commander class (Commander 类测试用例)."""
    
    def test_create_commander(self):
        """Test creating a commander."""
        commander = Commander(name="TestCommander")
        assert commander.name == "TestCommander"
        assert len(commander.agents) == 0
        assert commander.strategy == "round_robin"
    
    def test_add_agent(self):
        """Test adding an agent to commander."""
        commander = Commander(name="TestCommander")
        agent = Agent(name="TestAgent")
        
        commander.add_agent(agent)
        
        assert len(commander.agents) == 1
        assert "TestAgent" in commander.agents
    
    def test_remove_agent(self):
        """Test removing an agent from commander."""
        commander = Commander(name="TestCommander")
        agent = Agent(name="TestAgent")
        
        commander.add_agent(agent)
        result = commander.remove_agent("TestAgent")
        
        assert result is True
        assert len(commander.agents) == 0
    
    def test_remove_nonexistent_agent(self):
        """Test removing a non-existent agent."""
        commander = Commander(name="TestCommander")
        result = commander.remove_agent("NonExistent")
        
        assert result is False
    
    def test_drum_all(self):
        """Test sending drum signal to all agents."""
        commander = Commander(name="TestCommander")
        agent1 = Agent(name="Agent1")
        agent2 = Agent(name="Agent2")
        
        commander.add_agent(agent1)
        commander.add_agent(agent2)
        
        results = commander.drum_all("Attack!")
        
        assert len(results) == 2
        assert "Agent1" in results
        assert "Agent2" in results
    
    def test_gong_all(self):
        """Test sending gong signal to all agents."""
        commander = Commander(name="TestCommander")
        agent1 = Agent(name="Agent1")
        agent2 = Agent(name="Agent2")
        
        commander.add_agent(agent1)
        commander.add_agent(agent2)
        
        results = commander.gong_all()
        
        assert len(results) == 2
        assert "Agent1" in results
        assert "Agent2" in results
    
    def test_drum_one(self):
        """Test sending drum signal to specific agent."""
        commander = Commander(name="TestCommander")
        agent = Agent(name="TestAgent")
        commander.add_agent(agent)
        
        result = commander.drum_one("TestAgent", "Specific task")
        
        assert "🥁" in result
        assert "TestAgent" in result
        assert "Specific task" in result
    
    def test_drum_nonexistent_agent(self):
        """Test sending drum to non-existent agent."""
        commander = Commander(name="TestCommander")
        
        result = commander.drum_one("NonExistent", "Task")
        
        assert "❌" in result
    
    def test_gong_one(self):
        """Test sending gong signal to specific agent."""
        commander = Commander(name="TestCommander")
        agent = Agent(name="TestAgent")
        commander.add_agent(agent)
        
        result = commander.gong_one("TestAgent")
        
        assert "🔔" in result
        assert "TestAgent" in result
    
    def test_coordinate(self):
        """Test coordinating agents."""
        commander = Commander(name="TestCommander")
        agent1 = Agent(name="Agent1")
        agent2 = Agent(name="Agent2")
        
        commander.add_agent(agent1)
        commander.add_agent(agent2)
        
        results = commander.coordinate("Battle plan", strategy="round_robin")
        
        assert len(results) == 2
    
    def test_status(self):
        """Test getting commander status."""
        commander = Commander(name="TestCommander")
        agent = Agent(name="TestAgent", is_active=True)
        commander.add_agent(agent)
        
        status = commander.status()
        
        assert status["commander"] == "TestCommander"
        assert status["agent_count"] == 1
        assert "TestAgent" in status["agents"]
    
    def test_str_representation(self):
        """Test string representation of commander."""
        commander = Commander(name="TestCommander")
        str_repr = str(commander)
        
        assert "TestCommander" in str_repr
        assert "round_robin" in str_repr
