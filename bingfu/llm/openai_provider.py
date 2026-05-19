"""
OpenAI LLM Provider (兵符 · 正规军师)

支持 OpenAI GPT 系列及所有 OpenAI 兼容 API。

兵法云：以正合，以奇胜 —— OpenAI 乃正规军，DeepSeek 乃奇兵。
两者皆可为我所用，灵活调度方为上策。
"""

from typing import List, Optional
import json

from bingfu.llm.base import (
    LLMProvider, LLMResponse, LLMMessage,
    ToolCall, ToolDefinition
)
from bingfu.llm.config import LLMConfig


# OpenAI API 默认地址
OPENAI_BASE_URL = "https://api.openai.com/v1"


class OpenAIProvider(LLMProvider):
    """
    OpenAI 适配器 (正规军师)

    支持 GPT-4o、GPT-4、GPT-3.5 等。
    也兼容所有 OpenAI 接口格式的第三方服务（通义千问、智谱、Ollama 等）。
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client = None

    def _get_client(self):
        """懒加载 OpenAI 客户端"""
        if self._client is None:
            try:
                from openai import OpenAI
            except ImportError:
                raise ImportError(
                    "使用 OpenAI 需要安装 openai 库：pip install openai\n"
                    "兵法云：兵马未动，粮草先行——依赖先装好才能上阵！"
                )

            api_key = self.config.resolve_api_key()
            if not api_key:
                raise ValueError(
                    "OpenAI API Key 未配置！\n"
                    "请通过以下任一方式设置：\n"
                    "  1. 配置文件中设置 api_key\n"
                    "  2. 环境变量 OPENAI_API_KEY"
                )

            base_url = self.config.base_url or OPENAI_BASE_URL
            self._client = OpenAI(
                api_key=api_key,
                base_url=base_url,
            )
        return self._client

    def generate(
        self,
        messages: List[LLMMessage],
        tools: Optional[List[ToolDefinition]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """
        调用 OpenAI API 生成回复

        Args:
            messages: 对话历史
            tools: 可用工具定义
            temperature: 生成温度
            max_tokens: 最大 token 数

        Returns:
            LLMResponse: 统一格式响应
        """
        client = self._get_client()

        # 构建请求参数
        kwargs = {
            "model": self.config.model or "gpt-4o",
            "messages": [m.to_dict() for m in messages],
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
        }

        # 添加工具定义
        if tools:
            kwargs["tools"] = [t.to_dict() for t in tools]
            kwargs["tool_choice"] = "auto"

        # 调用 API
        try:
            completion = client.chat.completions.create(**kwargs)
        except Exception as e:
            return LLMResponse(
                content=f"❌ OpenAI 调用失败：{e}",
                model=self.config.model,
                finish_reason="error"
            )

        # 解析响应
        choice = completion.choices[0]
        message = choice.message

        # 解析工具调用
        tool_calls = None
        if message.tool_calls:
            tool_calls = []
            for tc in message.tool_calls:
                try:
                    args = json.loads(tc.function.arguments)
                except (json.JSONDecodeError, TypeError):
                    args = {"raw": tc.function.arguments}
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=args
                ))

        return LLMResponse(
            content=message.content,
            tool_calls=tool_calls,
            usage={
                "prompt_tokens": completion.usage.prompt_tokens if completion.usage else 0,
                "completion_tokens": completion.usage.completion_tokens if completion.usage else 0,
                "total_tokens": completion.usage.total_tokens if completion.usage else 0,
            },
            model=completion.model,
            finish_reason=choice.finish_reason or "",
            raw=completion
        )

    def __str__(self) -> str:
        model = self.config.model or "gpt-4o"
        base = self.config.base_url or "openai"
        return f"OpenAI军师(model={model}, base={base})"


class OpenAICompatibleProvider(OpenAIProvider):
    """
    OpenAI 兼容适配器 (万用军师)

    适用于所有兼容 OpenAI 接口的服务：
    - 通义千问 (Qwen): base_url=https://dashscope.aliyuncs.com/compatible-mode/v1
    - 智谱 (GLM): base_url=https://open.bigmodel.cn/api/paas/v4
    - Ollama 本地: base_url=http://localhost:11434/v1
    - 其他任何 OpenAI 兼容 API
    """

    def __init__(self, config: LLMConfig):
        # 必须提供 base_url
        if not config.base_url:
            raise ValueError(
                "OpenAI 兼容模式必须指定 base_url！\n"
                "兵法云：知己知彼——不知道敌营在哪，如何进攻？\n"
                "示例：\n"
                "  通义千问: base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'\n"
                "  智谱GLM:  base_url='https://open.bigmodel.cn/api/paas/v4'\n"
                "  Ollama:   base_url='http://localhost:11434/v1'"
            )
        super().__init__(config)

    def __str__(self) -> str:
        return f"兼容军师(model={self.config.model}, base={self.config.base_url})"
