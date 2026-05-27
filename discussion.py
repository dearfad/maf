"""多角色自由讨论 - Microsoft Agent Framework 演示

三个角色: 教师、学生、管理者 就指定议题进行多轮自由讨论。
"""

import asyncio
import os
import re
import sys
from datetime import datetime

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

ROUNDS = 3


def _get_client() -> OpenAIChatCompletionClient:
    base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
    model = os.getenv("OPENAI_CHAT_COMPLETION_MODEL") or os.getenv("MODEL")
    if not all([base_url, api_key, model]):
        print("请先在 .env 文件中设置 OPENAI_BASE_URL / OPENAI_API_KEY / OPENAI_CHAT_COMPLETION_MODEL")
        raise SystemExit(1)
    return OpenAIChatCompletionClient(model=model, api_key=api_key, base_url=base_url)


async def main() -> None:
    client = _get_client()

    LANG = "You must respond in Simplified Chinese only. 请用简体中文回复。"

    agents = {
        "Teacher": Agent(
            name="Teacher",
            instructions=f"{LANG} You are a knowledgeable teacher. "
            "Explain concepts clearly with examples and ask guiding questions.",
            client=client,
        ),
        "Student": Agent(
            name="Student",
            instructions=f"{LANG} You are a curious student. "
            "Ask thoughtful questions, share your perspective, and engage with others.",
            client=client,
        ),
        "Admin": Agent(
            name="Admin",
            instructions=f"{LANG} You are the discussion administrator. "
            "Summarize key points, keep the discussion productive, and pose follow-up questions.",
            client=client,
        ),
    }

    topic = input("请输入讨论议题: ").strip()
    if not topic:
        topic = "人工智能对人类未来会有什么影响？"

    print(f"\n讨论议题: {topic}")
    print("=" * 60)

    turns: list[tuple[str, str]] = []  # (speaker_name, text)

    for _round in range(1, ROUNDS + 1):
        for name, agent in agents.items():
            lines = [f"Discussion topic: {topic}"]
            for speaker, text in turns:
                lines.append(f"{speaker}: {text}")
            lines.append(f"Now {name}, please contribute to this discussion.")
            prompt = "\n\n".join(lines)

            response = await agent.run(prompt)
            text = (response.text or "").strip()
            if text:
                print(f"\n[{name}] {text}\n")
                turns.append((name, text))
            else:
                print(f"\n[{name}] (未回应)")

    print("=" * 60)
    print("讨论结束。\n")

    slug = re.sub(r"[^\w\u4e00-\u9fff]", "_", topic)[:40].strip("_")
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"讨论_{slug}_{now}.md"

    lines = [
        f"# 讨论记录：{topic}",
        "",
        f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
    ]
    for i, (speaker, text) in enumerate(turns, 1):
        lines.append(f"### {i}. {speaker}")
        lines.append("")
        lines.append(text)
        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"讨论内容已保存至: {filename}")


if __name__ == "__main__":
    asyncio.run(main())
