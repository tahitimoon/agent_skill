# Agent Skill 实践项目

基于 [Strands Agents](https://strandsagents.com/) 的 AI 技能模块化实践项目。

## 项目简介

Agent Skills 让 AI Agent 具备可复用的特定能力。本项目包含 3 个示例技能：
- **hello-skill**: 简单测试
- **explain-code**: 代码解释（带类比和图表）
- **pdf-processing**: PDF 文本提取

## 快速开始

### 1. 安装依赖

```bash
uv sync
# 或 pip install strands-agents[openai] strands-agents-tools pymupdf
```

### 2. 配置环境

```bash
cp .env.example .env
# 编辑 .env 填入 OPENAI_API_KEY
```

### 3. 运行示例

```bash
python main.py              # hello-skill 测试
python explain-code.py      # 代码解释
python pdf-processing.py    # PDF 提取
```

## 目录结构

```
agent_skill/
├── main.py                    # 示例 1
├── explain-code.py            # 示例 2
├── pdf-processing.py          # 示例 3
└── skills/                    # 技能目录
    ├── hello-skill/
    │   └── SKILL.md
    ├── explain-code/
    │   └── SKILL.md
    └── pdf-processing/
        ├── SKILL.md
        └── scripts/
            └── extract.py
```

**核心规则**: `SKILL.md` 必须放在与技能同名的子目录中。

## 创建自定义技能

### 1. 创建目录和文件

```bash
mkdir -p skills/your-skill-name
```

### 2. 编写 SKILL.md

```markdown
---
name: your-skill-name
description: 简短描述用途和触发条件
allowed-tools: shell,file_read  # 可选
---

# 技能说明

详细说明技能的功能和执行步骤。
```

### 3. 在代码中使用

```python
from strands import Agent, AgentSkills

plugin = AgentSkills(skills="./skills/")
agent = Agent(model=model, plugins=[plugin])
agent("用户输入")
```

## SKILL.md 格式

### YAML Frontmatter（必需）

```yaml
---
name: skill-name              # 必须与目录名一致
description: 技能描述          # Agent 用此判断何时触发
allowed-tools: tool1,tool2    # 可选，限制可用工具
---
```

### Markdown 正文（必需）

说明技能的功能、执行步骤等，Agent 会读取此内容来执行任务。

## 切换模型

### OpenAI (默认)

```python
from strands.models.openai import OpenAIModel

model = OpenAIModel(
    client_args={"api_key": os.getenv("OPENAI_API_KEY")},
    model_id="gpt-5-mini",
)
```

### Anthropic

```python
from strands.models import Anthropic

model = Anthropic(model="claude-3-5-sonnet-20241022")
# 需要 ANTHROPIC_API_KEY
```

## 常见问题

**Q: 技能没被触发？**
- 检查 description 是否清晰明确
- 添加 "Use when..." 说明触发条件

**Q: 报错 `skill name does not match parent directory name`？**
- 确保目录名与 SKILL.md 中的 name 字段一致
- 正确结构: `skills/hello-skill/SKILL.md`

**Q: 如何调试？**
```python
plugin = AgentSkills(skills="./skills/")
print(f"已加载: {plugin.skills}")
```

## 参考资源

- [Strands Agents 文档](https://strandsagents.com/)
- [AgentSkills API](https://strandsagents.com/docs/api/python/strands.vended_plugins.skills.agent_skills/)
- [PyMuPDF 文档](https://pymupdf.readthedocs.io/)
