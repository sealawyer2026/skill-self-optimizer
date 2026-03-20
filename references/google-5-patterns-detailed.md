# Google 5种Agent Skill设计模式详解

> 来源: Google Cloud Tech - 5 Agent Skill design patterns every ADK developer should know
> 整理: 2026-03-20

---

## 概述

超过30个Agent工具（Claude Code、Gemini CLI、Cursor等）已统一SKILL.md格式规范，但**格式只是皮囊，内容设计才是灵魂**。

这5种模式帮你从"会用格式"进阶到"设计得好"。

---

## 模式一：Tool Wrapper —— 让Agent秒变专家

### 核心理念
与其把某个库的最佳实践硬编码到系统提示词里，不如包装成一个Skill，让Agent在需要时才加载。

### 好处
- 系统提示词保持精简
- 上下文按需加载，省token
- 团队的编码规范可以"即插即用"

### 实现要点
- `references/` 目录存放详细的规范文档
- SKILL.md里告诉Agent"什么时候加载"以及"加载后怎么用"

### 示例
```yaml
---
name: api-expert
description: FastAPI development best practices and conventions.
  Use when building, reviewing, or debugging FastAPI applications.
---

You are an expert in FastAPI development.

## Core Conventions
Load 'references/conventions.md' for the complete list of best practices.

## When Reviewing Code
1. Load the conventions reference
2. Check code against each convention
3. For violations, cite the rule and suggest the fix
```

### 适用场景
- 团队内部编码规范分发
- 特定库/框架的专业知识封装
- 最佳实践标准化

---

## 模式二：Generator —— 模板驱动生成

### 核心思路
解决"每次输出结构都不一样"的问题。把"内容"和"结构"分离，模板管结构，Agent管内容填充。

### 实现结构
- `assets/` 目录放输出模板
- `references/` 目录放风格指南
- SKILL.md充当"项目经理"，指挥Agent按步骤填空

### 示例
```yaml
---
name: report-generator
description: Generates structured technical reports in Markdown.
---

You are a technical report generator. Follow these steps exactly:

Step 1: Load 'references/style-guide.md' for tone and formatting rules.

Step 2: Load 'assets/report-template.md' for the required structure.

Step 3: Ask the user for missing information:
- Topic or subject
- Key findings or data points
- Target audience

Step 4: Fill the template following the style guide.

Step 5: Return the completed report.
```

### 适用场景
- 技术报告生成
- 文档标准化输出
- 任何需要固定格式的内容生成

---

## 模式三：Reviewer —— 模块化检查清单

### 精髓
把"查什么"和"怎么查"分开。将检查规则放到 `references/review-checklist.md` 里，让Agent动态加载。

### 实现示例
```yaml
---
name: code-reviewer
description: Reviews Python code for quality, style, and bugs.
---

You are a Python code reviewer. Follow this protocol exactly:

Step 1: Load 'references/review-checklist.md' for review criteria.

Step 2: Read the user's code carefully.

Step 3: Apply each rule. For every violation:
- Note the line number
- Classify severity: error / warning / info
- Explain WHY it's a problem
- Suggest a specific fix

Step 4: Produce structured output:
- **Summary**: What the code does, overall assessment
- **Findings**: Grouped by severity
- **Score**: Rate 1-10 with justification
- **Top 3 Recommendations**
```

### 妙处
把Python风格检查清单换成OWASP安全清单，同一个Skill瞬间变成安全审计工具——基础设施完全不变，只是换了个参考文档。

### 适用场景
- 代码审查
- 安全检查
- 质量保证
- 合规性审查

---

## 模式四：Inversion —— 先问再做

### 核心问题
Agent天生爱"猜"。用户说一句，它就想给出答案。但在复杂场景下，**猜错了比不回答更可怕**。

### 核心理念
把"用户驱动Agent"变成"Agent面试用户"。

### 关键设计
- 明确的"门禁"指令："DO NOT start building until all phases are complete"
- 分阶段提问，每个阶段必须等用户回答完才能进入下一阶段
- 最后才输出结果

### 示例
```yaml
---
name: project-planner
description: Plans software projects by gathering requirements through
  structured questions before producing a plan.
---

You are conducting a requirements interview.
DO NOT start building until all phases are complete.

## Phase 1 — Problem Discovery (ask one question at a time)
Ask in order. Do not skip any.
- Q1: "What problem does this project solve for its users?"
- Q2: "Who are the primary users? What is their technical level?"
- Q3: "What is the expected scale?"

## Phase 2 — Technical Constraints (only after Phase 1 is complete)
- Q4: "What deployment environment will you use?"
- Q5: "Do you have technology stack preferences?"
- Q6: "What are the non-negotiable requirements?"

## Phase 3 — Synthesis (only after all questions answered)
1. Load 'assets/plan-template.md'
2. Fill in every section using gathered requirements
3. Present the plan
4. Ask: "Does this capture your requirements?"
5. Iterate until user confirms
```

### 适用场景
- 需求收集
- 项目规划
- 复杂任务拆解
- 任何容易理解错的场景

---

## 模式五：Pipeline —— 严格流水线

### 核心问题
有些任务，一步都不能少。跳过任何一步，结果都可能出问题。

### 核心理念
用"硬检查点"确保流程完整。

### 实现示例
```yaml
---
name: doc-pipeline
description: Generates API documentation from Python source code.
---

You are running a documentation pipeline.
Execute each step in order. Do NOT skip steps.

## Step 1 — Parse & Inventory
Analyze the code to extract all public classes and functions.
Ask: "Is this the complete public API you want documented?"

## Step 2 — Generate Docstrings
For each function lacking a docstring:
- Load 'references/docstring-style.md' for format
- Generate docstrings following the style guide
- Present each for user approval

**Do NOT proceed to Step 3 until user confirms.**

## Step 3 — Assemble Documentation
Load 'assets/api-doc-template.md' for output structure.
Compile all symbols into a single API reference document.

## Step 4 — Quality Check
Review against 'references/quality-checklist.md':
- Every public symbol documented
- Every parameter has type and description
- At least one usage example per function

Report results. Fix issues before final delivery.
```

### 设计亮点
"Do NOT proceed to Step 3 until user confirms"——这就是**钻石门禁**。Agent不能自己跳过，必须等人工确认。

### 适用场景
- 多步骤文档生成
- 严格流程控制
- 质量保证流程
- 合规性流程

---

## 模式选择决策树

```
只需要让Agent懂某个库？
├── 是 → Tool Wrapper
└── 否 → 需要输出固定格式？
    ├── 是 → Generator
    └── 否 → 需要检查、评审？
        ├── 是 → Reviewer
        └── 否 → 需求复杂、容易理解错？
            ├── 是 → Inversion
            └── 否 → 任务多步骤、不能跳步？
                └── 是 → Pipeline
```

**简单说：**
- **Tool Wrapper**: 只需要让Agent懂某个库
- **Generator**: 需要输出固定格式
- **Reviewer**: 需要检查、评审
- **Inversion**: 需求复杂、容易理解错
- **Pipeline**: 任务多步骤、不能跳步

---

## 模式组合使用

这五种模式**不是互斥的**，而是可以组合使用。

### 组合示例

**Pipeline + Reviewer**: 一个Pipeline可以在最后加一个Reviewer步骤，自己检查自己的工作

**Generator + Inversion**: 一个Generator可以先用Inversion模式收集必要信息，再填充模板

**完整组合**: Pipeline → Inversion → Generator → Reviewer

### 渐进式上下文加载
ADK的SkillToolset机制让Agent只在需要的时候才加载对应的Skill，组合使用不会炸token。

---

## 核心感悟

### 1. 格式已死，设计永生
SKILL.md的YAML、目录结构已标准化，真正的竞争力在于：**你能不能把业务逻辑抽象成合适的设计模式**。

### 2. 每种模式都在对抗Agent的"本能"
Agent天生爱猜、爱跳步、爱一次性输出。这五种模式本质上都是"约束"——约束Agent按规矩办事。

### 3. 组合才是王道
单一模式能解决的问题有限。真正复杂的生产场景，往往是Pipeline + Reviewer + Tool Wrapper的组合拳。

### 4. 写Skill就像写代码
抽象对了，事半功倍。

---

## 参考

- 5 Agent Skill design patterns every ADK developer should know - Google Cloud Tech
- Agent Development Kit (ADK) - Google
