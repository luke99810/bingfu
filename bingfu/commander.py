"""
Commander module (指挥系统模块)
Implements multi‑agent coordination, inspired by ancient Chinese warfare command.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from bingfu.agent import Agent
from bingfu.signal import Drum, Gong


class Commander(BaseModel):
    """
    Commander (指挥系统) — coordinates multiple agents.
    Inspired by ancient Chinese warfare command structures.
    """
    
    name: str = Field(default="Marshal", description="Commander name (e.g., 'Marshal', 'General')")
    agents: Dict[str, Agent] = Field(
        default_factory=dict,
        description="Dictionary of agents under command: {agent_name: Agent}"
    )
    strategy: str = Field(
        default="round_robin",
        description="Coordination strategy: 'round_robin', 'priority', 'custom'"
    )
    
    class Config:
        arbitrary_types_allowed = True
    
    def add_agent(self, agent: Agent) -> None:
        """
        Add an agent to the command.
        
        Args:
            agent (Agent): The agent to add.
        """
        self.agents[agent.name] = agent
    
    def remove_agent(self, agent_name: str) -> bool:
        """
        Remove an agent from the command.
        
        Args:
            agent_name (str): Name of the agent to remove.
            
        Returns:
            bool: True if removed, False if not found.
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            return True
        return False
    
    def drum_all(self, task: str) -> Dict[str, str]:
        """
        Send drum signal (击鼓) to all agents.
        
        Args:
            task (str): The task to assign.
            
        Returns:
            Dict[str, str]: Results from each agent.
        """
        results = {}
        for name, agent in self.agents.items():
            # In real implementation, this would call agent.drum(task)
            results[name] = f"🥁 Drum sent to '{name}': {task}"
        return results
    
    def gong_all(self) -> Dict[str, str]:
        """
        Send gong signal (鸣金) to all agents.
        
        Returns:
            Dict[str, str]: Results from each agent.
        """
        results = {}
        for name, agent in self.agents.items():
            # In real implementation, this would call agent.gong()
            results[name] = f"🔔 Gong sent to '{name}'"
        return results
    
    def drum_one(self, agent_name: str, task: str) -> str:
        """
        Send drum signal (击鼓) to a specific agent.
        
        Args:
            agent_name (str): Name of the target agent.
            task (str): The task to assign.
            
        Returns:
            str: Result message.
            
        Raises:
            KeyError: If agent not found.
        """
        if agent_name not in self.agents:
            return f"❌ Agent '{agent_name}' not found in command."
        
        # In real implementation, this would call agent.drum(task)
        return f"🥁 Drum sent to '{agent_name}': {task}"
    
    def gong_one(self, agent_name: str) -> str:
        """
        Send gong signal (鸣金) to a specific agent.
        
        Args:
            agent_name (str): Name of the target agent.
            
        Returns:
            str: Result message.
        """
        if agent_name not in self.agents:
            return f"❌ Agent '{agent_name}' not found in command."
        
        # In real implementation, this would call agent.gong()
        return f"🔔 Gong sent to '{agent_name}'"
    
    def coordinate(self, task: str, strategy: Optional[str] = None) -> Dict[str, str]:
        """
        Coordinate agents to complete a task (simplified version).
        
        Args:
            task (str): The task to coordinate.
            strategy (Optional[str]): Override default strategy.
            
        Returns:
            Dict[str, str]: Coordination results.
        """
        use_strategy = strategy if strategy else self.strategy
        results = {}
        
        if use_strategy == "round_robin":
            # Simple round-robin coordination
            for name in self.agents:
                results[name] = f"Coordinating '{name}' (round-robin)"
        
        elif use_strategy == "priority":
            # Priority-based (simplified: just use order in dict)
            priority_list = list(self.agents.keys())
            for i, name in enumerate(priority_list):
                results[name] = f"Coordinating '{name}' (priority {i+1})"
        
        else:  # custom or unknown
            results["info"] = f"Using strategy: {use_strategy} (custom)"
        
        return results
    
    def status(self) -> Dict[str, Any]:
        """
        Get status of all agents.
        
        Returns:
            Dict[str, Any]: Status information.
        """
        return {
            "commander": self.name,
            "strategy": self.strategy,
            "agent_count": len(self.agents),
            "agents": {
                name: "🟢 Active" if a.is_active else "⚫ Inactive"
                for name, a in self.agents.items()
            }
        }
    
    def __str__(self) -> str:
        return f"Commander(name='{self.name}', agents={len(self.agents)}, strategy='{self.strategy}')"
    
    def __repr__(self) -> str:
        return self.__str__()
