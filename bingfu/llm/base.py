"""
LLM Provider 基类与数据结构

定义所有 LLM 适配器必须遵守的统一接口。
新增模型只需继承 LLMProvider 并实现 generate() 方法即可。
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from pydantic import BaseModel, Field
from enum import Enum


class RoleType(str, Enum):
    """消息角色类型"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class LLMMessage(BaseModel):
    """
    LLM 消息（军令格式）

    统一的消息结构，跨模型通用。
    """
    role: RoleType = Field(..., description="消息角色")
    content: Optional[str] = Field(default=None, description="消息内容")
    tool_calls: Optional[List["ToolCall"]] = Field(default=None, description="工具调用请求")
    tool_call_id: Optional[str] = Field(default=None, description="工具调用结果对应的ID")
    name: Optional[str] = Field(default=None, description="工具名称（role=tool时使用）")

    class Config:
        arbitrary_types_allowed = True

    def to_dict(self) -> Dict[str, Any]:
        """转换为 API 请求格式的字典"""
        d: Dict[str, Any] = {"role": self.role.value}
        if self.content is not None:
            d["content"] = self.content
        if self.tool_calls:
            d["tool_calls"] = [tc.to_dict() for tc in self.tool_calls]
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        if self.name:
            d["name"] = self.name
        return d


class ToolCall(BaseModel):
    """
    工具调用请求（军令调度）

    LLM 决定调用某个工具时的结构化请求。
    """
    id: str = Field(..., description="工具调用ID")
    name: str = Field(..., description="工具名称（兵器名）")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="调用参数")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": "function",
            "function": {
                "name": self.name,
                "arguments": str(self.arguments) if isinstance(self.arguments, str) else __import__("json").dumps(self.arguments, ensure_ascii=False)
            }
        }


class ToolDefinition(BaseModel):
    """
    工具定义（兵器谱）

    向 LLM 声明可用工具的结构。
    """
    name: str = Field(..., description="工具名称")
    description: str = Field(..., description="工具描述")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="参数 JSON Schema"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }


class LLMResponse(BaseModel):
    """
    LLM 响应（军师献策）

    统一的响应结构，无论底层是 DeepSeek、OpenAI 还是其他模型。
    """
    content: Optional[str] = Field(default=None, description="文本回复")
    tool_calls: Optional[List[ToolCall]] = Field(default=None, description="工具调用请求")
    usage: Dict[str, int] = Field(default_factory=dict, description="token 用量")
    model: str = Field(default="", description="实际使用的模型名")
    finish_reason: str = Field(default="", description="结束原因")
    raw: Optional[Any] = Field(default=None, description="原始API响应（调试用）")

    @property
    def has_tool_calls(self) -> bool:
        """是否有工具调用"""
        return bool(self.tool_calls)

    class Config:
        arbitrary_types_allowed = True


class LLMProvider(ABC):
    """
    LLM 适配器基类（军师之基）

    所有 LLM 适配器必须继承此类并实现 generate() 方法。
    这保证了框架可以无缝切换不同的大模型。

    兵法云：知己知彼，百战不殆。
    不同模型如同不同兵种，各有长短，统一接口方能灵活调度。
    """

    def __init__(self, config: "LLMConfig"):
        self.config = config

    @abstractmethod
    def generate(
        self,
        messages: List[LLMMessage],
        tools: Optional[List[ToolDefinition]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """
        生成回复（军师献策）

        Args:
            messages: 对话消息列表
            tools: 可用工具定义列表
            temperature: 生成温度（越高越随机）
            max_tokens: 最大生成 token 数

        Returns:
            LLMResponse: 统一格式的响应
        """
        ...

    def simple_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        简单生成（快速献策）

        便捷方法：一条 prompt 直接拿到文本回复。
        适合不需要工具调用的简单场景。

        Args:
            prompt: 用户输入
            system_prompt: 系统提示
            temperature: 生成温度

        Returns:
            str: 生成的文本
        """
        messages = []
        if system_prompt:
            messages.append(LLMMessage(role=RoleType.SYSTEM, content=system_prompt))
        messages.append(LLMMessage(role=RoleType.USER, content=prompt))

        response = self.generate(messages, temperature=temperature)
        return response.content or ""

    @property
    def name(self) -> str:
        """Provider 名称"""
        return self.config.provider

    def __str__(self) -> str:
        return f"LLMProvider({self.config.provider}/{self.config.model})"
