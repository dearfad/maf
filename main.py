"""Microsoft Agent Framework 演示程序

支持自定义 OpenAI 兼容的 API 地址、API Key 和模型名称。

用法（设置环境变量）:
    set OPENAI_BASE_URL=https://api.openai.com/v1
    set OPENAI_API_KEY=your-api-key
    set OPENAI_CHAT_COMPLETION_MODEL=gpt-4o-mini
    python main.py

或使用短名称:
    set BASE_URL=https://api.openai.com/v1
    set API_KEY=your-api-key
    set MODEL=gpt-4o-mini
    python main.py
"""

import asyncio
import os

from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatCompletionClient

load_dotenv()


async def main() -> None:
    base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
    model = os.getenv("OPENAI_CHAT_COMPLETION_MODEL") or os.getenv("MODEL")

    if not all([base_url, api_key, model]):
        print("请设置以下环境变量:")
        print("  BASE_URL  - OpenAI 兼容的 API 地址 (如 https://api.openai.com/v1)")
        print("  API_KEY   - API 密钥")
        print("  MODEL     - 模型名称 (如 gpt-4o-mini)")
        print()
        print("示例:")
        print("  set BASE_URL=https://api.openai.com/v1")
        print("  set API_KEY=sk-xxx")
        print("  set MODEL=gpt-4o-mini")
        print("  python main.py")
        return

    client = OpenAIChatCompletionClient(
        model=model,
        api_key=api_key,
        base_url=base_url,
    )

    agent = client.as_agent(
        name="DemoAgent",
        instructions="You are a helpful assistant. Keep your answers concise.",
    )

    print(f"Agent 已启动 (模型: {model}, 地址: {base_url})")
    print("输入 exit 或 quit 退出\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit", "q"):
            break
        if not user_input:
            continue

        result = await agent.run(user_input)
        print(f"Agent: {result}")


if __name__ == "__main__":
    asyncio.run(main())
