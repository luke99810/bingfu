"""
LLM 配置管理 (兵符 · 军师调度配置)

管理多个 LLM provider 的配置，支持热切换默认模型。
配置来源：YAML 文件 / 代码创建 / 环境变量
"""

import os
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """
    单个 LLM Provider 的配置 (一员军师的委任状)

    Attributes:
        provider: 提供商名称 (deepseek/openai/openai_compatible)
        api_key: API 密钥
        base_url: API 基础 URL（OpenAI 兼容接口可自定义）
        model: 模型名称
        temperature: 默认生成温度
        max_tokens: 默认最大 token 数
        extra: 额外参数（各 provider 特有的配置）
    """
    provider: str = Field(..., description="提供商: deepseek/openai/openai_compatible")
    api_key: str = Field(default="", description="API 密钥")
    base_url: Optional[str] = Field(default=None, description="API 基础 URL")
    model: str = Field(default="", description="模型名称")
    temperature: float = Field(default=0.7, description="生成温度")
    max_tokens: int = Field(default=2048, description="最大生成 token 数")
    extra: Dict[str, Any] = Field(default_factory=dict, description="额外参数")

    def resolve_api_key(self) -> str:
        """
        解析 API 密钥

        优先级：直接配置 > 环境变量

        环境变量命名规则：
          - DeepSeek: DEEPSEEK_API_KEY
          - OpenAI: OPENAI_API_KEY
          - 自定义: LLM_API_KEY_{provider大写}
        """
        if self.api_key:
            return self.api_key

        # 环境变量回退
        env_map = {
            "deepseek": "DEEPSEEK_API_KEY",
            "openai": "OPENAI_API_KEY",
        }
        env_key = env_map.get(self.provider, f"LLM_API_KEY_{self.provider.upper()}")
        return os.environ.get(env_key, "")


class LLMManager(BaseModel):
    """
    LLM 配置管理器 (军师调度府)

    管理多个 LLM provider 配置，支持默认 provider 切换。
    """
    default_provider: str = Field(default="deepseek", description="默认使用的 provider")
    providers: Dict[str, LLMConfig] = Field(
        default_factory=dict,
        description="所有 provider 配置: {name: LLMConfig}"
    )

    class Config:
        arbitrary_types_allowed = True

    def add_provider(self, name: str, config: LLMConfig) -> None:
        """添加一个 provider 配置"""
        self.providers[name] = config

    def remove_provider(self, name: str) -> bool:
        """移除一个 provider 配置"""
        if name in self.providers:
            del self.providers[name]
            if self.default_provider == name:
                # 如果删除的是默认的，切换到第一个可用的
                if self.providers:
                    self.default_provider = next(iter(self.providers.keys()))
                else:
                    self.default_provider = ""
            return True
        return False

    def get_provider_config(self, name: Optional[str] = None) -> Optional[LLMConfig]:
        """
        获取指定 provider 的配置

        Args:
            name: provider 名称，为 None 时使用默认

        Returns:
            LLMConfig 或 None
        """
        key = name or self.default_provider
        return self.providers.get(key)

    def set_default(self, name: str) -> bool:
        """设置默认 provider"""
        if name in self.providers:
            self.default_provider = name
            return True
        return False

    @classmethod
    def from_yaml_dict(cls, data: Dict[str, Any]) -> "LLMManager":
        """
        从 YAML 配置字典创建 LLMManager

        期望格式:
        ```yaml
        llm:
          default_provider: deepseek
          providers:
            deepseek:
              provider: deepseek
              api_key: sk-xxx
              model: deepseek-chat
            openai:
              provider: openai
              api_key: sk-xxx
              model: gpt-4o
        ```
        """
        llm_data = data.get("llm", {})
        manager = cls(
            default_provider=llm_data.get("default_provider", "deepseek")
        )

        for name, cfg in llm_data.get("providers", {}).items():
            manager.add_provider(name, LLMConfig(**cfg))

        return manager

    def to_yaml_dict(self) -> Dict[str, Any]:
        """导出为 YAML 配置字典"""
        providers_dict = {}
        for name, cfg in self.providers.items():
            providers_dict[name] = cfg.model_dump(exclude_none=True)

        return {
            "llm": {
                "default_provider": self.default_provider,
                "providers": providers_dict
            }
        }

    def __str__(self) -> str:
        names = ", ".join(self.providers.keys())
        return f"LLMManager(default={self.default_provider}, providers=[{names}])"
