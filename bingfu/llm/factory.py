"""
LLM Factory (兵符 · 军师点将台)

工厂模式创建 LLM Provider 实例。
根据配置自动选择正确的适配器，无需关心底层实现。

兵法云：将听吾计，用之必胜——选对军师，胜算在握。
"""

from typing import Optional

from bingfu.llm.base import LLMProvider
from bingfu.llm.config import LLMConfig, LLMManager


# Provider 注册表（军师名册）
_PROVIDER_REGISTRY: dict[str, type[LLMProvider]] = {}


def _init_registry():
    """初始化 provider 注册表"""
    if _PROVIDER_REGISTRY:
        return

    try:
        from bingfu.llm.deepseek import DeepSeekProvider
        _PROVIDER_REGISTRY["deepseek"] = DeepSeekProvider
    except ImportError:
        pass

    try:
        from bingfu.llm.openai_provider import OpenAIProvider, OpenAICompatibleProvider
        _PROVIDER_REGISTRY["openai"] = OpenAIProvider
        _PROVIDER_REGISTRY["openai_compatible"] = OpenAICompatibleProvider
    except ImportError:
        pass


class LLMFactory:
    """
    LLM 工厂 (军师点将台)

    根据配置创建对应的 LLM Provider 实例。

    使用示例:
    ```python
    # 方式1：从配置创建
    config = LLMConfig(provider="deepseek", api_key="sk-xxx", model="deepseek-chat")
    llm = LLMFactory.create(config)

    # 方式2：从 LLMManager 创建默认 provider
    manager = LLMManager.from_yaml_dict(config_data)
    llm = LLMFactory.from_manager(manager)

    # 方式3：指定名称创建
    llm = LLMFactory.from_manager(manager, name="openai")
    ```
    """

    @staticmethod
    def create(config: LLMConfig) -> LLMProvider:
        """
        根据配置创建 LLM Provider

        Args:
            config: LLM 配置

        Returns:
            LLMProvider: 对应的 provider 实例

        Raises:
            ValueError: 不支持的 provider 类型
        """
        _init_registry()

        provider_type = config.provider.lower()

        # 精确匹配
        if provider_type in _PROVIDER_REGISTRY:
            return _PROVIDER_REGISTRY[provider_type](config)

        # 如果 base_url 存在但 provider 不是已知的，自动降级为 openai_compatible
        if config.base_url:
            if "openai_compatible" in _PROVIDER_REGISTRY:
                from bingfu.llm.openai_provider import OpenAICompatibleProvider
                return OpenAICompatibleProvider(config)

        available = ", ".join(_PROVIDER_REGISTRY.keys()) or "（无，请安装 openai 库）"
        raise ValueError(
            f"不支持的 LLM provider: '{config.provider}'\n"
            f"可用 provider: {available}\n"
            f"兵法云：知己知彼——选对军师才能百战不殆！"
        )

    @staticmethod
    def from_manager(manager: LLMManager, name: Optional[str] = None) -> Optional[LLMProvider]:
        """
        从 LLMManager 创建 Provider

        Args:
            manager: LLM 配置管理器
            name: provider 名称，为 None 时使用默认

        Returns:
            LLMProvider 实例，如果配置不存在则返回 None
        """
        config = manager.get_provider_config(name)
        if not config:
            return None
        return LLMFactory.create(config)

    @staticmethod
    def register_provider(name: str, provider_class: type[LLMProvider]) -> None:
        """
        注册自定义 Provider

        允许用户扩展框架，添加新的 LLM 适配器。

        Args:
            name: provider 名称
            provider_class: provider 类（必须继承 LLMProvider）

        兵法云：兵无常势，水无常形——框架可扩展，方能应万变。
        """
        if not issubclass(provider_class, LLMProvider):
            raise TypeError(f"{provider_class} 必须继承 LLMProvider")
        _PROVIDER_REGISTRY[name.lower()] = provider_class

    @staticmethod
    def list_providers() -> list[str]:
        """列出所有已注册的 provider"""
        _init_registry()
        return list(_PROVIDER_REGISTRY.keys())
