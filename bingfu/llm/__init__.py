"""
BingFu LLM 模块 (兵符 · 军师谋略层)

提供多模型 LLM 适配器，让将领（Agent）真正能听懂军令、运筹帷幄。

支持:
  - DeepSeek (默认推荐，性价比高)
  - OpenAI (GPT 系列)
  - 任意 OpenAI 兼容 API (如：通义千问、智谱、Ollama 本地模型等)

使用示例:
```python
from bingfu.llm import LLMFactory, LLMConfig

# 创建 DeepSeek provider
config = LLMConfig(
    provider="deepseek",
    api_key="sk-xxx",
    model="deepseek-chat"
)
llm = LLMFactory.create(config)

# 生成回复
response = llm.generate("帮我分析一下当前的战场形势")
print(response.content)
```
"""

from bingfu.llm.base import LLMProvider, LLMResponse, LLMMessage, ToolCall
from bingfu.llm.config import LLMConfig, LLMManager
from bingfu.llm.factory import LLMFactory

__all__ = [
    "LLMProvider",
    "LLMResponse",
    "LLMMessage",
    "ToolCall",
    "LLMConfig",
    "LLMManager",
    "LLMFactory",
]
