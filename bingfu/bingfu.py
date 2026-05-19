"""
BingFu main module (兵符主模块)
Implements the main BingFu class — the entry point of the framework.
Combines Agent, Tool, Memory, Signal, Commander, and LLM.
"""

from typing import Any, Dict, List, Optional
import yaml
from pydantic import BaseModel, Field

from bingfu.agent import Agent
from bingfu.tool import Tool
from bingfu.memory import Memory
from bingfu.signal import Drum, Gong, drum, gong
from bingfu.commander import Commander


class BingFu(BaseModel):
    """
    BingFu (兵符) — main class of the framework.
    Represents the "tally" (兵符) used in ancient China to command troops.
    """
    
    name: str = Field(default="BingFu", description="Framework name")
    version: str = Field(default="0.4.0", description="Framework version")
    
    # Core components (核心组件)
    agents: Dict[str, Agent] = Field(
        default_factory=dict,
        description="Registered agents: {name: Agent}"
    )
    tools: Dict[str, Tool] = Field(
        default_factory=dict,
        description="Registered tools: {name: Tool}"
    )
    memories: Dict[str, Memory] = Field(
        default_factory=dict,
        description="Registered memories: {name: Memory}"
    )
    
    # Commander (指挥系统)
    commander: Optional[Commander] = Field(
        default=None,
        description="Commander for multi‑agent coordination"
    )
    
    # Configuration (配置)
    config: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Loaded configuration dictionary"
    )

    # LLM Manager (军师调度府)
    llm_manager: Optional[Any] = Field(
        default=None,
        description="LLM configuration manager"
    )
    default_llm: Optional[Any] = Field(
        default=None,
        description="Default LLM Provider instance"
    )
    
    class Config:
        arbitrary_types_allowed = True
    
    # ========== Agent Management (智能体管理) ==========
    
    def add_agent(self, agent: Agent) -> None:
        """
        Add an agent to BingFu.
        Automatically binds the default LLM if the agent doesn't have one.

        Args:
            agent (Agent): The agent to add.
        """
        self.agents[agent.name] = agent

        # 自动绑定默认 LLM
        if self.default_llm and not agent.llm:
            agent.llm = self.default_llm

        # If commander exists, also add to commander
        if self.commander:
            self.commander.add_agent(agent)
    
    def remove_agent(self, agent_name: str) -> bool:
        """
        Remove an agent from BingFu.
        
        Args:
            agent_name (str): Name of the agent to remove.
            
        Returns:
            bool: True if removed, False if not found.
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            
            # Also remove from commander if exists
            if self.commander:
                self.commander.remove_agent(agent_name)
            return True
        return False
    
    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """
        Get an agent by name.
        
        Args:
            agent_name (str): Agent name.
            
        Returns:
            Optional[Agent]: The agent, or None if not found.
        """
        return self.agents.get(agent_name)
    
    # ========== Tool Management (工具管理) ==========
    
    def add_tool(self, tool: Tool) -> None:
        """
        Add a tool to BingFu.
        
        Args:
            tool (Tool): The tool to add.
        """
        self.tools[tool.name] = tool
    
    def remove_tool(self, tool_name: str) -> bool:
        """
        Remove a tool from BingFu.
        
        Args:
            tool_name (str): Name of the tool to remove.
            
        Returns:
            bool: True if removed, False if not found.
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            return True
        return False
    
    # ========== Memory Management (记忆管理) ==========
    
    def add_memory(self, memory: Memory) -> None:
        """
        Add a memory to BingFu.
        
        Args:
            memory (Memory): The memory to add.
        """
        self.memories[memory.name] = memory
    
    def remove_memory(self, memory_name: str) -> bool:
        """
        Remove a memory from BingFu.
        
        Args:
            memory_name (str): Name of the memory to remove.
            
        Returns:
            bool: True if removed, False if not found.
        """
        if memory_name in self.memories:
            del self.memories[memory_name]
            return True
        return False
    
    # ========== Signal Operations (信号操作) ==========
    
    def drum(self, agent_name: str, task: str) -> str:
        """
        Send drum signal (击鼓) to an agent.
        
        Args:
            agent_name (str): Target agent name.
            task (str): Task description.
            
        Returns:
            str: Result message.
        """
        agent = self.get_agent(agent_name)
        if not agent:
            return f"❌ Agent '{agent_name}' not found."
        
        # In real implementation, this would call agent.drum(task)
        return f"🥁 BingFu drums '{agent_name}': {task}"
    
    def gong(self, agent_name: str) -> str:
        """
        Send gong signal (鸣金) to an agent.
        
        Args:
            agent_name (str): Target agent name.
            
        Returns:
            str: Result message.
        """
        agent = self.get_agent(agent_name)
        if not agent:
            return f"❌ Agent '{agent_name}' not found."
        
        # In real implementation, this would call agent.gong()
        return f"🔔 BingFu gongs '{agent_name}'"
    
    def drum_all(self, task: str) -> Dict[str, str]:
        """
        Send drum signal (击鼓) to all agents.
        
        Args:
            task (str): Task description.
            
        Returns:
            Dict[str, str]: Results from each agent.
        """
        results = {}
        for name in self.agents:
            results[name] = self.drum(name, task)
        return results
    
    def gong_all(self) -> Dict[str, str]:
        """
        Send gong signal (鸣金) to all agents.
        
        Returns:
            Dict[str, str]: Results from each agent.
        """
        results = {}
        for name in self.agents:
            results[name] = self.gong(name)
        return results
    
    # ========== Commander Operations (指挥操作) ==========
    
    def enable_commander(self, name: str = "Marshal") -> None:
        """
        Enable the commander (启用指挥系统).
        
        Args:
            name (str): Commander name.
        """
        self.commander = Commander(name=name)
        
        # Add existing agents to commander
        for agent in self.agents.values():
            self.commander.add_agent(agent)
    
    def disable_commander(self) -> None:
        """Disable the commander (禁用指挥系统)."""
        self.commander = None
    
    # ========== Config Operations (配置操作) ==========
    
    def load_config(self, config_file: str) -> None:
        """
        Load configuration from YAML file.
        Automatically initializes LLM providers if configured.

        Args:
            config_file (str): Path to config YAML file.
        """
        with open(config_file, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        # 自动初始化 LLM
        if self.config and "llm" in self.config:
            self._init_llm_from_config()

    def _init_llm_from_config(self) -> None:
        """从配置初始化 LLM Manager 和默认 Provider"""
        try:
            from bingfu.llm.config import LLMManager
            from bingfu.llm.factory import LLMFactory

            self.llm_manager = LLMManager.from_yaml_dict(self.config)

            if self.llm_manager.providers:
                self.default_llm = LLMFactory.from_manager(self.llm_manager)
                if self.default_llm:
                    # 将 LLM 绑定到所有已注册的 Agent
                    for agent in self.agents.values():
                        if not agent.llm:
                            agent.llm = self.default_llm
        except Exception as e:
            # LLM 初始化失败不影响框架其他功能
            import sys
            print(f"⚠️ LLM 初始化失败: {e}（框架仍可使用，但将领无智能执行能力）")

    def set_llm(self, provider: Any, set_as_default: bool = True) -> None:
        """
        手动设置 LLM Provider

        Args:
            provider: LLM Provider 实例
            set_as_default: 是否设为默认（对所有 Agent 生效）
        """
        if set_as_default:
            self.default_llm = provider
            for agent in self.agents.values():
                if not agent.llm:
                    agent.llm = provider
    
    def save_config(self, config_file: str) -> None:
        """
        Save configuration to YAML file.
        
        Args:
            config_file (str): Path to config YAML file.
        """
        if self.config:
            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
    
    # ========== Status & Info (状态与信息) ==========
    
    def status(self) -> Dict[str, Any]:
        """
        Get BingFu status.

        Returns:
            Dict[str, Any]: Status information.
        """
        result = {
            "name": self.name,
            "version": self.version,
            "agent_count": len(self.agents),
            "tool_count": len(self.tools),
            "memory_count": len(self.memories),
            "commander_enabled": self.commander is not None,
            "llm_enabled": self.default_llm is not None,
        }

        if self.commander:
            result["commander"] = str(self.commander)

        if self.default_llm:
            result["llm"] = str(self.default_llm)

        if self.llm_manager:
            result["llm_providers"] = list(self.llm_manager.providers.keys())

        return result
    
    def __str__(self) -> str:
        commander_status = "✅ Enabled" if self.commander else "⚫ Disabled"
        return (
            f"BingFu(name='{self.name}', version='{self.version}', "
            f"agents={len(self.agents)}, tools={len(self.tools)}, "
            f"memories={len(self.memories)}, commander={commander_status})"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
