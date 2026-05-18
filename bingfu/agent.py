"""
Agent module (智能体模块)
Defines the Agent class with ancient Chinese warfare naming.
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class Agent(BaseModel):
    """
    Agent (智能体) — represents a single agent in the BingFu framework.
    Named after ancient Chinese warfare units.
    """
    
    name: str = Field(..., description="Agent name (e.g., 'Scout', 'General')")
    role: Optional[str] = Field(default=None, description="Agent role or title")
    description: Optional[str] = Field(default=None, description="Agent description")
    
    # Internal state (内部状态)
    is_active: bool = Field(default=False, description="Whether the agent is currently active")
    memory: Optional[Any] = Field(default=None, description="Agent memory (to be linked to Memory class)")
    tools: list[Any] = Field(default_factory=list, description="List of tools available to the agent")
    
    class Config:
        arbitrary_types_allowed = True
    
    def drum(self, task: str) -> str:
        """
        Drum signal (击鼓) — start the agent with a task.
        
        Args:
            task (str): The task description.
            
        Returns:
            str: Response message.
        """
        self.is_active = True
        return f"🥁 Drum! Agent '{self.name}' is now active. Task: {task}"
    
    def gong(self) -> str:
        """
        Gong signal (鸣金) — stop the agent.
        
        Returns:
            str: Response message.
        """
        self.is_active = False
        return f"🔔 Gong! Agent '{self.name}' has stopped."
    
    def add_tool(self, tool: Any) -> None:
        """
        Add a tool to the agent's toolkit.
        
        Args:
            tool (Any): The tool to add.
        """
        self.tools.append(tool)
    
    def remove_tool(self, tool: Any) -> None:
        """
        Remove a tool from the agent's toolkit.
        
        Args:
            tool (Any): The tool to remove.
        """
        if tool in self.tools:
            self.tools.remove(tool)
    
    def execute(self, task: str, tools: Optional[list[Any]] = None) -> str:
        """
        Execute a task (simplified version).
        
        Args:
            task (str): The task to execute.
            tools (Optional[list[Any]]): List of tools to use. If None, uses self.tools.
            
        Returns:
            str: Execution result.
        """
        tools_to_use = tools if tools is not None else self.tools
        
        # In a real implementation, this would call an LLM or execute logic.
        # For now, return a placeholder response.
        tool_names = [t.name if hasattr(t, 'name') else str(t) for t in tools_to_use]
        
        result = f"Agent '{self.name}' executing task: {task}\n"
        if tool_names:
            result += f"Using tools: {', '.join(tool_names)}\n"
        result += "✅ Task completed (placeholder)."
        
        return result
    
    def __str__(self) -> str:
        status = "🟢 Active" if self.is_active else "⚫ Inactive"
        return f"Agent(name='{self.name}', role='{self.role}', status={status})"
    
    def __repr__(self) -> str:
        return self.__str__()
