# MAF Demo — Microsoft Agent Framework 演示程序

基于 Microsoft Agent Framework 的演示项目，展示单 Agent 对话和多角色自由讨论。

## 快速开始

编辑项目根目录下的 `.env` 文件，填入你的 API 信息：

```env
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_CHAT_COMPLETION_MODEL=gpt-4o-mini
```

## 演示程序

### 1. 单 Agent 对话 (`main.py`)

简单的交互式聊天机器人：

```powershell
uv run python main.py
```

### 2. 多角色自由讨论 (`discussion.py`)

三个角色（教师/学生/管理者）就指定议题进行多轮自由讨论：
- **Teacher** — 知识渊博的教师，清晰解释概念
- **Student** — 好奇的学生，提问并深入思考
- **Admin** — 讨论管理者，确保讨论有序进行

启动后输入讨论议题即可开始：

```powershell
uv run python discussion.py
```

## 依赖

- Python >= 3.14
- agent-framework-openai
- agent-framework-orchestrations

由 `uv` 自动管理。
