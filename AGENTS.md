# MAF — Agent Notes

## Setup
- Python 3.14, managed by `uv`
- Config in `.env`: `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_CHAT_COMPLETION_MODEL` (short aliases `BASE_URL`, `API_KEY`, `MODEL` also work)
- Entrypoints: `main.py` (single-agent chat), `discussion.py` (3-role group discussion)

## Commands
```powershell
uv run python main.py
uv run python discussion.py
uv add <package>        # add dependency
```

## Key facts
- Uses `agent-framework-openai` (v1.6) backed by `OpenAIChatCompletionClient` (Chat Completions API, not Responses)
- `discussion.py` passes conversation as a plain-text prompt string (not Message list) to avoid `author_name`/`name` field issues with third-party OpenAI-compatible APIs
- Discussion output auto-saves to `讨论_<slug>_<timestamp>.md`
- Agent instructions must include `"You must respond in Simplified Chinese only. 请用简体中文回复。"` for Chinese output
- `sys.stdout.reconfigure(encoding="utf-8")` required on Windows to avoid `UnicodeEncodeError`

## Gotchas
- `GroupChatBuilder` (agent-framework-orchestrations rc2) is buggy — avoid it, use manual round-robin loops instead
- `agent.run(stream=True)` → iterate chunks for display, then `await stream.get_final_response()` for the accumulated result
