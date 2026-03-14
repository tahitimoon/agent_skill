# Agent Skill 实践项目

这是一个基于 [Strands Agents](https://strandsagents.com/) 框架的 Agent Skills 实践项目，展示如何创建和使用可复用的 AI 技能模块。

## 项目简介

Agent Skills 是一种让 AI Agent 具备特定领域能力的机制。通过将技能封装成独立的 SKILL.md 文件，可以让 Agent 在需要时自动加载和使用这些技能，实现能力的模块化和复用。

本项目包含三个示例技能，展示了从简单到复杂的不同应用场景。

## 目录结构

```
agent_skill/
├── main.py                           # 基础示例：hello-skill
├── explain-code.py                   # 代码解释示例
├── pdf-processing.py                 # PDF 处理示例
├── pyproject.toml                    # 项目依赖配置
├── .env.example                      # 环境变量模板
├── skills/                           # 技能目录
│   ├── hello-skill/                  # 简单测试技能
│   │   └── SKILL.md
│   ├── explain-code/                 # 代码解释技能
│   │   └── SKILL.md
│   └── pdf-processing/               # PDF 处理技能
│       ├── SKILL.md
│       └── scripts/
│           └── extract.py            # PDF 提取脚本
└── README.md
```

**重要规则**: 
- `SKILL.md` 必须放在以技能名称命名的子目录中
- 子目录名称必须与 SKILL.md 中的 `name` 字段一致
- 不能直接将 SKILL.md 放在 `skills/` 根目录下

## 快速开始

### 1. 安装依赖

本项目使用 [uv](https://github.com/astral-sh/uv) 作为包管理器（推荐），也可以使用 pip：

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -r pyproject.toml
```

### 2. 配置环境变量

复制环境变量模板并填入你的 API Key：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
OPENAI_API_KEY="your-openai-api-key"
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_API_KEY="your-deepseek-api-key"  # 可选
```

### 3. 运行示例

```bash
# 示例 1: 测试 hello-skill
python main.py

# 示例 2: 代码解释技能
python explain-code.py

# 示例 3: PDF 处理技能
python pdf-processing.py
```

## 技能说明

### 1. hello-skill - 简单测试技能

**用途**: 验证 Agent Skills 功能是否正常工作

**触发条件**: 用户说 "hello" 或要求测试技能

**功能**: 返回友好的问候消息和技能状态信息

**示例代码**: `main.py`

### 2. explain-code - 代码解释技能

**用途**: 以可视化和类比的方式解释代码

**触发条件**: 用户询问 "这段代码怎么工作的？" 或要求解释代码

**功能特点**:
- 使用日常生活类比帮助理解
- 绘制 ASCII 流程图
- 逐步讲解代码执行过程
- 指出常见陷阱和误区

**示例代码**: `explain-code.py`

### 3. pdf-processing - PDF 处理技能

**用途**: 从 PDF 文件中提取文本和表格内容

**触发条件**: 用户要求提取 PDF 内容

**功能特点**:
- 使用 PyMuPDF 库进行 PDF 解析
- 逐页提取文本内容
- 返回结构化的 JSON 数据
- 支持中文内容

**技术实现**:
- 使用 `allowed-tools: shell` 限制技能只能使用 shell 工具
- 通过 Python 脚本 `skills/pdf-processing/scripts/extract.py` 执行实际提取
- Agent 自动调用脚本并处理返回结果

**示例代码**: `pdf-processing.py`

## 模型配置

项目默认使用 OpenAI 模型，你也可以切换到其他模型：

### 使用 OpenAI (默认)

```python
from strands.models.openai import OpenAIModel

model = OpenAIModel(
    client_args={"api_key": os.getenv("OPENAI_API_KEY")},
    model_id="gpt-5-mini",
)
```

### 使用 Anthropic

```python
from strands.models import Anthropic

model = Anthropic(model="claude-3-5-sonnet-20241022")
```

环境变量：

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### 使用 AWS Bedrock

```python
from strands.models import Bedrock

model = Bedrock(model="anthropic.claude-3-5-sonnet-20241022-v2:0")
```

环境变量：

```bash
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_DEFAULT_REGION="us-east-1"
```

### 使用 DeepSeek

```python
from strands.models.openai import OpenAIModel

model = OpenAIModel(
    client_args={
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "base_url": os.getenv("DEEPSEEK_BASE_URL")
    },
    model_id="deepseek-chat",
)
```

## 创建自定义技能

### 步骤 1: 创建技能目录

```bash
mkdir -p skills/your-skill-name
```

### 步骤 2: 创建 SKILL.md 文件

在 `skills/your-skill-name/SKILL.md` 中定义技能：

```markdown
---
name: your-skill-name
description: 简短描述技能的用途和触发条件
allowed-tools: shell,file_read  # 可选，限制技能可用的工具
---

# 技能名称

详细说明技能的功能、使用方法和注意事项。

## 使用场景

描述什么时候应该使用这个技能。

## 执行步骤

1. 第一步做什么
2. 第二步做什么
3. ...
```

### 步骤 3: 在代码中使用

```python
from strands import Agent, AgentSkills
from strands.models.openai import OpenAIModel

# 加载技能目录
plugin = AgentSkills(skills="./skills/")

# 创建 Agent
agent = Agent(model=model, plugins=[plugin])

# Agent 会根据用户输入自动选择合适的技能
agent("用户的问题或请求")
```

## 技能设计最佳实践

### 1. 清晰的描述字段

`description` 字段是 Agent 判断何时使用技能的关键：

```yaml
# ❌ 不好：太模糊
description: 处理文件

# ✅ 好：明确触发条件
description: Extract text and tables from PDF files. Use when user asks to read, parse, or extract content from PDF documents.
```

### 2. 使用 allowed-tools 限制权限

通过 `allowed-tools` 字段限制技能可以使用的工具，提高安全性：

```yaml
allowed-tools: shell,file_read  # 只允许使用 shell 和 file_read 工具
```

### 3. 提供详细的执行指令

在 SKILL.md 正文中提供清晰的步骤说明：

```markdown
## 执行步骤

1. 使用 `file_read` 工具读取目标文件
2. 调用 `shell` 工具运行处理脚本
3. 解析返回的 JSON 结果
4. 向用户总结提取的内容
```

### 4. 包含辅助脚本

对于复杂任务，可以在技能目录下创建 `scripts/` 子目录存放辅助脚本：

```
skills/
└── pdf-processing/
    ├── SKILL.md
    └── scripts/
        └── extract.py
```

## SKILL.md 文件格式详解

每个 `SKILL.md` 文件由两部分组成：

### 1. YAML Frontmatter（必需）

```yaml
---
name: skill-name              # 必需：必须与父目录名称完全一致
description: 技能描述          # 必需：Agent 用此判断何时使用该技能
allowed-tools: tool1,tool2    # 可选：限制技能可用的工具
---
```

### 2. Markdown 正文（必需）

Frontmatter 之后是 Markdown 格式的详细说明和指令：

```markdown
# 技能标题

技能的详细说明、使用方法、执行步骤等。

Agent 会读取这部分内容来理解如何执行该技能。
```

### 完整示例

```markdown
---
name: pdf-processing
description: Extract text and tables from PDF files
allowed-tools: shell
---

# PDF Processing

当用户要求提取 PDF 内容时：

1. 使用 shell 工具运行 `skills/pdf-processing/scripts/extract.py`
2. 解析返回的 JSON 结果
3. 向用户总结提取的内容
```

## 工作原理

### Agent Skills 的执行流程

```
用户输入
    ↓
Agent 分析意图
    ↓
匹配技能描述 (description)
    ↓
加载对应的 SKILL.md
    ↓
按照技能指令执行
    ↓
返回结果给用户
```

### 技能匹配机制

Agent 通过以下方式判断使用哪个技能：

1. **语义匹配**: 分析用户输入与技能 `description` 的相关性
2. **关键词触发**: description 中的关键短语（如 "Use when..."）
3. **上下文理解**: 结合对话历史判断用户意图

### 工具限制机制

通过 `allowed-tools` 字段可以限制技能的权限：

```yaml
allowed-tools: shell,file_read  # 只能使用这两个工具
```

如果不设置 `allowed-tools`，技能可以使用 Agent 的所有可用工具。

## 实际应用场景

### 场景 1: 企业知识库

创建针对公司内部文档、API、流程的专用技能，让 Agent 成为企业知识助手。

### 场景 2: 代码审查

创建代码审查技能，自动检查代码规范、安全问题、性能优化点。

### 场景 3: 数据处理

创建数据清洗、转换、分析的技能，处理 CSV、Excel、JSON 等格式。

### 场景 4: 自动化运维

创建部署、监控、日志分析等运维技能，提高运维效率。

## 常见问题

### Q1: 技能没有被触发怎么办？

**原因**: description 描述不够清晰或与用户输入不匹配

**解决方案**:
- 在 description 中添加明确的触发条件，如 "Use when..."
- 包含关键词和同义词，如 "extract, parse, read PDF"
- 测试不同的用户输入表述

### Q2: 报错 `skill name does not match parent directory name`

**原因**: SKILL.md 文件位置不正确或 name 字段不匹配

**解决方案**:

```bash
# ❌ 错误结构
skills/SKILL.md
skills/my-skill.md

# ✅ 正确结构
skills/hello-skill/SKILL.md  # 目录名和 name 字段都是 hello-skill
```

### Q3: 如何调试技能是否被加载？

在代码中添加日志：

```python
plugin = AgentSkills(skills="./skills/")
print(f"已加载的技能: {plugin.skills}")  # 查看加载的技能列表
```

### Q4: 技能可以调用外部 API 吗？

可以，有两种方式：

1. **使用 shell 工具**: 调用 Python/Node.js 脚本来访问 API
2. **使用 strands_tools**: 如果 Strands 提供了相关工具（如 `web_search`）

### Q5: 多个技能之间可以协作吗？

可以。Agent 可以在一次对话中使用多个技能。例如：
- 先用 `pdf-processing` 提取内容
- 再用 `explain-code` 解释提取出的代码片段

## 项目依赖

本项目使用以下主要依赖：

```toml
[project]
requires-python = ">=3.12"
dependencies = [
    "strands-agents[openai]>=1.30.0",  # Strands Agent 框架
    "strands-agents-tools>=0.2.22",     # Agent 工具集
    "pymupdf>=1.27.2",                  # PDF 处理库
]
```

## 进阶技巧

### 1. 技能组合使用

可以在一个 Agent 中加载多个技能，让 Agent 具备多种能力：

```python
plugin = AgentSkills(skills="./skills/")
agent = Agent(
    model=model, 
    plugins=[plugin],
    tools=[shell, file_read, web_search]  # 提供额外工具
)
```

### 2. 动态技能加载

根据不同场景加载不同的技能集：

```python
# 场景 1: 代码助手
code_plugin = AgentSkills(skills="./skills/code/")

# 场景 2: 数据分析
data_plugin = AgentSkills(skills="./skills/data/")

# 根据用户选择创建不同的 Agent
agent = Agent(model=model, plugins=[code_plugin])
```

### 3. 技能版本管理

为技能创建版本，便于维护和回滚：

```
skills/
├── pdf-processing-v1/
│   └── SKILL.md
└── pdf-processing-v2/
    └── SKILL.md
```

### 4. 技能测试

为每个技能编写测试脚本，确保功能正常：

```python
# test_skills.py
def test_hello_skill():
    agent = Agent(model=model, plugins=[plugin])
    response = agent("hello")
    assert "Hello" in response

def test_pdf_processing():
    agent = Agent(model=model, plugins=[plugin])
    response = agent("从 test.pdf 提取内容")
    assert "success" in response
```

## 性能优化

### 1. 技能描述优化

- 保持 description 简洁（1-2 句话）
- 使用明确的触发词
- 避免模糊或重叠的描述

### 2. 减少技能数量

- 不要加载过多技能（建议 < 20 个）
- 技能过多会增加 Agent 的决策时间
- 考虑按场景分组加载

### 3. 缓存常用结果

对于耗时操作，在技能脚本中实现缓存：

```python
# skills/your-skill/scripts/process.py
import json
from pathlib import Path

cache_file = Path(".cache/results.json")

def process_with_cache(input_data):
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    
    result = expensive_operation(input_data)
    cache_file.write_text(json.dumps(result))
    return result
```

## 参考资源

### 官方文档

- [Strands Agents 官网](https://strandsagents.com/)
- [AgentSkills API 文档](https://strandsagents.com/docs/api/python/strands.vended_plugins.skills.agent_skills/)
- [Skill 数据模型](https://strandsagents.com/docs/api/python/strands.vended_plugins.skills.skill/)

### 相关项目

- [PyMuPDF 文档](https://pymupdf.readthedocs.io/) - PDF 处理库
- [python-dotenv](https://github.com/theskumar/python-dotenv) - 环境变量管理

### 社区资源

- [Strands GitHub](https://github.com/strandsagents/strands)
- [示例技能库](https://github.com/strandsagents/strands-examples)

## 许可证

本项目仅供学习和测试使用。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v0.1.0 (2026-03-15)

- ✅ 实现 hello-skill 基础测试技能
- ✅ 实现 explain-code 代码解释技能
- ✅ 实现 pdf-processing PDF 处理技能
- ✅ 支持 OpenAI、Anthropic、Bedrock、DeepSeek 模型
- ✅ 完善项目文档和示例代码
