---
name: skill-self-optimizer
description: "Meta-skill for fully automated skill optimization with real LLM integration. Use when: (1) Skill triggers incorrectly, (2) User reports issues, (3) Pre-ClawHub review, (4) Version iteration, (5) Applying Google's 5 design patterns, (6) Want fully automatic optimization pipeline, (7) Need pattern combination suggestions, (8) Choosing right design pattern, (9) Need real AI optimization, (10) Compare skill versions, (11) Need AI code generation, (12) Collect user feedback, (13) Migrate between platforms, (14) Run automated tests, (15) Monitor in production, (16) Analyze market trends. Implements all 5 patterns with Web UI, Config, Templates, Performance, Dependencies, AI Generation, Feedback Learning, Platform Migration, Auto Testing, Real-time Monitoring, and Market Analysis."
version: "3.4.0"
changelog:
  - "3.4.0": Added AI Code Generator, Feedback Learner, Platform Migrator, Auto Tester, Real-time Monitor, Market Analyzer
  - "3.3.0": Added Web UI, Config Manager, Template Library, Performance Profiler, Dependency Analyzer
  - "3.2.0": Added real LLM optimizer, version diff comparison, HTML reports
  - "3.1.0": Added pattern combiner, decision tree, constraint analysis
  - "3.0.0": Fully automatic mode with AI advisor, test generation, and auto-deployment
  - "2.0.0": Added auto-monitoring, batch optimization, CI/CD integration
  - "1.0.0": Initial release with 5 design patterns support
---

# Skill Self-Optimizer

A meta-skill that analyzes, diagnoses, and optimizes other Agent Skills. Based on Google's 5 design patterns and progressive disclosure principles.

## Quick Start

### One-Click Optimization (Recommended)
```bash
# Analyze + Optimize in one command
python scripts/auto_optimize.py /path/to/skill-folder --output ./optimized
```

### Batch Optimization (v2.0)
```bash
# Optimize multiple skills at once
python scripts/batch_optimize.py /path/to/skills-folder --parallel --output ./optimized-batch
```

### Auto-Monitoring (v2.0)
```bash
# Continuous monitoring with auto-upgrade
python scripts/monitor.py /path/to/skills-folder --schedule weekly

# Or run as daemon
python scripts/monitor.py /path/to/skills-folder --schedule daily --daemon
```

### Manual Process
```bash
# Step 1: Analyze
python scripts/analyze_skill.py /path/to/skill-folder

# Step 2: Optimize
python scripts/optimize_skill.py /path/to/skill-folder --output ./optimized
```

## When to Use This Skill

1. **Skill underperformance**: Triggering incorrectly, missing context, or producing poor results
2. **Usage feedback**: Users report issues or inefficiencies after real-world use
3. **Pre-publication review**: Before submitting to ClawHub
4. **Version iteration**: Creating v2, v3... based on accumulated learnings
5. **Pattern application**: Applying Google's 5 design patterns systematically

## Google's 5 Design Patterns (Core Framework)

This optimizer implements and enforces all 5 patterns:

### Pattern 1: Tool Wrapper
- **Purpose**: Make Agent an instant expert
- **Optimization**: Check if Skill wraps complex tools effectively
- **Metric**: Reduction in repeated tool explanations

### Pattern 2: Generator
- **Purpose**: Template-driven generation
- **Optimization**: Standardize output formats, ensure consistency
- **Metric**: Output quality consistency score

### Pattern 3: Reviewer
- **Purpose**: Modular checklist-based review
- **Optimization**: Structured validation steps
- **Metric**: Checklist coverage and effectiveness

### Pattern 4: Inversion
- **Purpose**: Ask before doing
- **Optimization**: Clarification questions before execution
- **Metric**: Reduction in misinterpretation errors

### Pattern 5: Orchestrator
- **Purpose**: Multi-skill coordination
- **Optimization**: Chain recommendations, skill composition
- **Metric**: Task completion efficiency with skill chains

## Optimization Process

### Phase 1: Analysis (Automatic)

Run `scripts/analyze_skill.py` to generate diagnostic report:

```
Analysis Report: skill-name
├── Metadata Quality
│   ├── name: [OK/ISSUE]
│   ├── description: [OK/ISSUE] - Trigger clarity, coverage
│   └── triggering accuracy: [SCORE]
├── Structure Analysis
│   ├── SKILL.md length: [WORDS] (target: <2500)
│   ├── progressive disclosure: [OK/ISSUE]
│   └── resource organization: [OK/ISSUE]
├── Content Quality
│   ├── conciseness: [SCORE]
│   ├── degrees of freedom: [APPROPRIATE/TOO_HIGH/TOO_LOW]
│   └── example quality: [SCORE]
├── Pattern Compliance
│   ├── Tool Wrapper: [YES/NO/PARTIAL]
│   ├── Generator: [YES/NO/PARTIAL]
│   ├── Reviewer: [YES/NO/PARTIAL]
│   ├── Inversion: [YES/NO/PARTIAL]
│   └── Orchestrator: [YES/NO/PARTIAL]
└── Issues Found
    ├── [ISSUE-1]: Description + severity
    ├── [ISSUE-2]: Description + severity
    └── ...
```

### Phase 2: Diagnosis (Manual Review)

Review the analysis report and identify:
1. **Critical issues**: Breaking functionality or major inefficiency
2. **Improvement opportunities**: Pattern application, structure optimization
3. **Missing patterns**: Which of the 5 patterns could enhance this Skill

### Phase 3: Optimization (Semi-Automatic)

Run `scripts/optimize_skill.py` with diagnosed issues:

```bash
python scripts/optimize_skill.py /path/to/skill \
  --issues issue1,issue2,issue3 \
  --patterns generator,reviewer \
  --output ./skill-v2
```

The script generates optimized version with:
- Fixed critical issues
- Applied design patterns
- Improved structure
- Version bump (v1 → v2)

### Phase 4: Validation

1. Test optimized Skill on real tasks
2. Compare before/after metrics
3. Document learnings in CHANGELOG

## Optimization Rules

### Rule 1: Conciseness Check
- SKILL.md body should be <2500 words (<500 lines)
- Every sentence must justify its token cost
- Move details to references/ when approaching limit

### Rule 2: Trigger Precision
- Description must include ALL trigger conditions
- Test: "Would Codex know when to use this?"
- Add negative examples (when NOT to use)

### Rule 3: Progressive Disclosure
- Level 1: Metadata only (always loaded)
- Level 2: SKILL.md body (when triggered)
- Level 3: References (as needed)
- No deeply nested references (>1 level)

### Rule 4: Appropriate Freedom
- **High freedom**: Text instructions for context-dependent tasks
- **Medium freedom**: Pseudocode/scripts with parameters
- **Low freedom**: Specific scripts for fragile operations

### Rule 5: Pattern Application
Every Skill should leverage at least 2 patterns:
- Minimum: One execution pattern (Wrapper/Generator) + one quality pattern (Reviewer/Inversion)
- Ideal: All 5 patterns in harmony

## v3.4 - AI Generation, Feedback, Migration, Testing, Monitoring & Market Analysis (NEW)

全面增强版本，新增 6 大功能模块。

### 🤖 AI Code Generator - AI 代码生成

**根据自然语言描述自动生成完整 Skill：**

```bash
# 生成 Skill
python scripts/ai_code_generator.py "create a skill for processing PDF files"

# 指定输出目录和名称
python scripts/ai_code_generator.py "处理 Excel 数据" --output ./my-skills --name excel-processor
```

**功能：**
- 智能任务类型识别
- 自动设计模式建议
- 生成完整文件结构
- 提供 TODO 清单

### 🧠 Feedback Learner - 智能反馈学习

**收集和分析用户反馈，持续改进 Skill：**

```bash
# 收集反馈
python scripts/feedback_learner.py ./my-skill --collect --rating 4 --comment "Works well but slow"

# 分析反馈
python scripts/feedback_learner.py ./my-skill --analyze

# 获取改进建议
python scripts/feedback_learner.py ./my-skill --suggest
```

**输出：**
- `.improvement_report.md` - 改进报告
- `.feedback_analysis.json` - 分析数据
- 自动识别常见问题类型

### 🔄 Platform Migrator - 跨平台迁移

**在 OpenClaw、Claude、GPT 之间迁移 Skill：**

```bash
# 迁移到 Claude
python scripts/platform_migrator.py ./my-skill --target claude

# 从 Claude 迁移到 OpenClaw
python scripts/platform_migrator.py ./my-skill --source claude --target openclaw

# 自动检测源平台
python scripts/platform_migrator.py ./my-skill --target gpt
```

**支持平台：**
- OpenClaw (SKILL.md + 脚本)
- Claude (Markdown + XML 标签)
- ChatGPT (JSON 格式)
- OpenAI Assistants API

### 🧪 Auto Tester - 自动化测试

**自动生成和运行测试：**

```bash
# 生成测试
python scripts/auto_tester.py ./my-skill --generate

# 运行测试
python scripts/auto_tester.py ./my-skill --run

# 覆盖率报告
python scripts/auto_tester.py ./my-skill --coverage
```

**测试类型：**
- 触发条件测试
- 示例验证测试
- 校验规则测试
- 结构完整性测试

### 📊 Realtime Monitor - 实时监控

**监控 Skill 在生产环境的表现：**

```bash
# 启动实时监控
python scripts/realtime_monitor.py ./my-skill --start

# 生成监控报告
python scripts/realtime_monitor.py ./my-skill --report

# 检查告警
python scripts/realtime_monitor.py ./my-skill --alert
```

**监控指标：**
- 调用成功率
- 错误率
- 平均延迟
- 自动告警

**告警阈值：**
- 错误率 > 10%
- 成功率 < 90%
- 延迟 > 5000ms

### 📈 Market Analyzer - 市场分析

**分析 ClawHub 市场趋势：**

```bash
# 查看市场趋势
python scripts/market_analyzer.py --trends

# 与市场对标
python scripts/market_analyzer.py --skill ./my-skill --compare

# 生成完整报告
python scripts/market_analyzer.py --report
```

**分析内容：**
- 热门 Skill 类别
- 设计模式趋势
- 成功因素分析
- 竞品对标建议

## v3.3 - Web UI, Config, Templates, Performance & Dependencies
## v3.3 - Web UI, Config, Templates, Performance & Dependencies (NEW)

全新的 Web 界面和 5 大增强功能。

### 🌐 Web UI - 可视化操作界面

**启动 Web 界面：**
```bash
python scripts/web_ui.py --port 8080
```

**功能：**
- 📤 拖拽上传 Skill 文件夹
- 📊 实时显示分析结果
- 🎨 美观的可视化界面
- 📱 响应式设计，支持移动端

**访问：** http://localhost:8080

### ⚙️ Config Manager - 配置文件管理

**创建默认配置：**
```bash
python scripts/config_manager.py --init
```

**生成的 `.skill-optimizer.yaml`：**
```yaml
version: "3.3.0"
optimization:
  auto_apply_fixes: false
  strict_mode: false
  patterns:
    tool_wrapper: { enabled: true, weight: 1.0 }
    generator: { enabled: true, weight: 1.0 }
    # ...
llm:
  enabled: true
  provider: kimi
  model: moonshot-v1-8k
```

**常用命令：**
```bash
# 查看配置
python scripts/config_manager.py --show

# 获取配置项
python scripts/config_manager.py --get optimization.strict_mode

# 设置配置项
python scripts/config_manager.py --set llm.temperature 0.5

# 验证配置
python scripts/config_manager.py --validate
```

### 📚 Template Library - 社区模板库

**查看所有模板：**
```bash
python scripts/template_library.py --list
```

**内置模板：**
| 模板 | 说明 |
|-----|------|
| `minimal` | 最小化 Skill 结构 |
| `tool-wrapper` | Tool Wrapper 设计模式 |
| `generator` | Generator 设计模式 |
| `reviewer` | Reviewer 设计模式 |
| `pipeline` | Pipeline 设计模式 |
| `inversion` | Inversion 设计模式 |
| `api-integration` | API 集成模板 |
| `data-processor` | 数据处理模板 |

**安装模板：**
```bash
python scripts/template_library.py --install tool-wrapper --output ./my-api-skill --name my-api
```

**搜索模板：**
```bash
python scripts/template_library.py --search api
```

**保存自定义模板：**
```bash
python scripts/template_library.py --save my-template --skill-path ./my-skill --name "My Template"
```

### ⚡ Performance Profiler - 性能分析

**运行性能分析：**
```bash
python scripts/performance_profiler.py ./my-skill --iterations 10
```

**分析维度：**
- 📁 文件操作性能 (读取速度)
- 🧠 内存使用分析
- 📄 SKILL.md 解析性能
- 📊 复杂度分析 (Token 估算)

**输出报告：**
- `.performance_report.md` - 可读报告
- `.performance_profile.json` - 详细数据

**复杂度评分：**
- 0-30: ✅ 低复杂度 - Token 效率最优
- 30-60: ⚠️ 中复杂度 - 建议简化
- 60-100: ❌ 高复杂度 - 需要优化

### 🔗 Dependency Analyzer - 依赖分析

**分析依赖关系：**
```bash
python scripts/dependency_analyzer.py ./my-skill --visualize
```

**分析内容：**
- 🔗 Skill 间引用关系
- 🛠️ 工具依赖 (Python, Node, curl 等)
- 📄 文件引用 (检查缺失文件)
- 📊 依赖图谱可视化

**输出：**
- `.dependency_analysis.json` - 分析数据
- `.dependency_graph.mmd` - Mermaid 图表
- `.dependency_graph.html` - 交互式可视化

## v3.2 - LLM Integration & Version Diff
## v3.2 - LLM Integration & Version Diff (NEW)

真正的 AI 优化和智能版本对比。

### 🤖 LLM Optimizer - 真正的 AI 优化

**调用 Kimi API 进行深度优化：**
```bash
# 使用环境变量中的 API Key
export KIMI_API_KEY="your-key"
python scripts/llm_optimizer.py ./my-skill

# 或直接在命令行指定
python scripts/llm_optimizer.py ./my-skill --api-key YOUR_KEY
```

**功能：**
- 🧠 调用真实 LLM 进行优化建议
- 📊 预测优化后的评分
- 💡 生成具体的改进方案
- 🔄 自动应用 Google 5 种设计模式

**优化维度：**
- 设计模式应用
- 约束设计完善
- 触发条件精确化
- 步骤流程优化

### 🔄 Version Diff - 智能版本对比

**对比两个版本的 Skill：**
```bash
python scripts/version_diff.py ./skill-v1 ./skill-v2
```

**输出：**
- 📊 设计模式变化分析
- 📈 指标变化统计
- 🎉 改进亮点提取
- 📄 详细 diff 报告
- 🌐 HTML 可视化报告

**示例输出：**
```
✅ 新增模式: Pipeline, Reviewer
📈 约束语句: +5
📈 步骤流程: +3  
🎉 改进亮点:
   - ✅ 约束设计 (更多 DO NOT/MUST NOT)
   - ✅ 流程控制 (更多步骤/阶段)
```

## v3.1 - Pattern Combiner & Decision Tree
 (NEW)

基于 Google Cloud Tech 最新文章深度优化，支持模式组合和约束分析。

### Pattern Combiner - 模式组合分析

**分析 Skill 的模式组合机会：**
```bash
python scripts/pattern_combiner.py ./my-skill
```

**功能：**
- 🔍 检测当前使用的模式
- 💡 推荐模式组合（Pipeline+Reviewer, Generator+Inversion等）
- ⛓️ 分析约束设计（对抗Agent本能）
- 📊 生成详细改进报告

**支持组合：**
| 组合 | 说明 | 适用场景 |
|-----|------|---------|
| Pipeline + Reviewer | 多步骤+质量门禁 | 复杂工作流 |
| Generator + Inversion | 生成+需求收集 | 格式固定但需求不清 |
| Tool Wrapper + Reviewer | 专家+验证 | 专业领域标准 |
| Full Stack | 完整组合 | 关键项目 |

### Pattern Decision Tree - 交互式决策树

**不知道选什么模式？让决策树帮你：**
```bash
# 交互式问答
python scripts/pattern_decision_tree.py --interactive

# 或分析现有Skill
python scripts/pattern_decision_tree.py --skill ./my-skill
```

**决策流程：**
```
是让Agent掌握特定知识? → Tool Wrapper
  ↓ 否
需要固定格式输出? → Generator (+Inversion?)
  ↓ 否
主要是检查/审查? → Reviewer
  ↓ 否
需求复杂易理解错? → Inversion (+Pipeline?)
  ↓ 否
任务分步骤不能跳? → Pipeline (+Reviewer?)
  ↓ 否
→ 推荐 Full Stack 组合
```

### 约束设计分析

基于 Google 文章的核心观点：**好的设计就是好的约束**

**评估维度：**
- 🚫 **防止猜测** - 是否有"DO NOT assume"
- 🚫 **防止跳步** - 是否有"DO NOT proceed until"
- 🚫 **防止仓促** - 是否有"wait for confirmation"

**Agent 3大问题：**
1. 爱猜 - 用 Inversion 模式约束
2. 爱跳步 - 用 Pipeline 模式约束
3. 爱一次性输出 - 用 Phase/Step 分段约束

## v3.0 - Fully Automatic Mode
 (NEW)

### Complete Automation Pipeline

```
Monitor → AI Analysis → Optimize → Test → Deploy
   ↑                                         ↓
   └──────────── Feedback Loop ←─────────────┘
```

### Fully Auto Mode

**One command for complete automation:**
```bash
python scripts/fully_auto.py ./skills --deploy-github --deploy-clawhub
```

**What it does:**
1. 🔍 **Monitor** - Scan all skills for issues
2. 🤖 **AI Advisor** - Get intelligent optimization suggestions
3. 🚀 **Auto-Optimize** - Apply design patterns
4. 🧪 **Test Generation** - Create test cases automatically
5. ✅ **Validation** - Verify improvement
6. 📤 **Auto-Deploy** - Push to GitHub/ClawHub

**Daemon Mode (24/7 automation):**
```bash
python scripts/fully_auto.py ./skills --daemon
```

### AI Advisor

Get AI-powered optimization suggestions:

```bash
python scripts/ai_advisor.py ./my-skill
```

**Features:**
- Automatic issue detection
- Pattern recommendations
- Improvement examples
- Prompt for Kimi/GPT-4 deep analysis

### Test Generator

Automatically generate comprehensive test cases:

```bash
python scripts/test_generator.py ./my-skill --output ./tests
```

**Generated Tests:**
- Trigger accuracy tests
- Functionality tests
- Edge case tests
- Auto-generated test runner

### Auto-Deployment

**Deploy to GitHub:**
```bash
python scripts/fully_auto.py ./skills --deploy-github
```

**Prepare for ClawHub:**
```bash
python scripts/fully_auto.py ./skills --deploy-clawhub
```

**Both:**
```bash
python scripts/fully_auto.py ./skills --deploy-github --deploy-clawhub
```

## Advanced Features (v2.0)


### Auto-Monitoring & Auto-Upgrade
Continuously monitor skills and automatically trigger optimization when needed.

**Trigger Conditions:**
- Score < 90/100
- Critical issues detected
- >30 days since last optimization
- User complaints > 3/week

**Usage:**
```bash
# Weekly monitoring
python scripts/monitor.py ./skills --schedule weekly

# Daily monitoring as daemon
python scripts/monitor.py ./skills --schedule daily --daemon
```

**Features:**
- Automatic database tracking
- Email/notification alerts
- Batch auto-optimization
- Historical trend analysis

### Batch Optimization
Optimize multiple skills in parallel.

**Usage:**
```bash
# Parallel processing (4 workers)
python scripts/batch_optimize.py ./skills --parallel --output ./optimized-batch

# Sequential processing
python scripts/batch_optimize.py ./skills --sequential
```

**Output:**
- `batch_optimization_report.json` - Detailed metrics
- `batch_optimization_report.html` - Visual dashboard
- Individual optimized skills

### CI/CD Integration
GitHub Actions template for automated skill optimization.

**Features:**
- Auto-analyze on push/PR
- Weekly scheduled optimization
- Auto-create optimization PRs
- Artifact uploads

**Setup:**
1. Copy `templates/github-actions.yml` to `.github/workflows/skill-optimization.yml`
2. Push to GitHub
3. Automated optimization on every skill change

### Chain Optimization
Optimize skill chains using Orchestrator pattern:

```markdown
## Skill Chain
This skill works best in sequence:
1. [skill-a] - Do X
2. [skill-b] - Review X  
3. [skill-c] - Generate final output

Next skill recommendation: [skill-b]
```

### Version Management
Track iterations:

```yaml
# In SKILL.md frontmatter
version: "2.1.3"
changelog:
  - "2.1.3": Fixed triggering ambiguity
  - "2.1.2": Added Generator pattern
  - "2.1.0": Initial release
```

### Self-Improvement Loop
After optimization, the Skill learns:

```markdown
## Optimization History
- v1 → v2: Added Reviewer pattern, reduced SKILL.md by 40%
- v2 → v3: Implemented Inversion, reduced misinterpretation by 60%
- Learnings: [Document what worked]
```

## Checklist: Before Publishing to ClawHub

Run through [optimization-checklist.md](references/optimization-checklist.md):

- [ ] Analysis report generated and reviewed
- [ ] All critical issues resolved
- [ ] At least 2 design patterns applied
- [ ] SKILL.md <2500 words
- [ ] Description includes all trigger conditions
- [ ] Progressive disclosure properly implemented
- [ ] Tested on 3+ real tasks
- [ ] Version bumped and documented
- [ ] No auxiliary files (README, CHANGELOG, etc.)

## Resources

- [Design Patterns Reference](references/design-patterns.md) - Detailed pattern implementations
- [Optimization Checklist](references/optimization-checklist.md) - Pre-publication checklist
- [Example Optimizations](references/examples.md) - Before/after case studies with metrics
- [Report Template](assets/optimization-report-template.md) - Template for documenting results
- [CI/CD Template](templates/github-actions.yml) - GitHub Actions workflow

## Usage Examples

### Example 1: Fix Underperforming Skill

```bash
# User reports: "My pdf-processor skill keeps triggering on docx files"

# Step 1: Analyze
python scripts/analyze_skill.py ./pdf-processor
# → Issue: Description lacks negative triggers

# Step 2: Optimize  
python scripts/optimize_skill.py ./pdf-processor \
  --issues "ambiguous-triggering" \
  --output ./pdf-processor-v2

# Step 3: Test and validate
```

### Example 2: Apply Design Patterns

```bash
# Current skill is too verbose, needs structure

python scripts/optimize_skill.py ./my-skill \
  --patterns "generator,reviewer" \
  --output ./my-skill-v2

# Applies Generator: Creates templates for common outputs
# Applies Reviewer: Adds modular checklists
```

### Example 3: Pre-ClawHub Review

```bash
# Final check before publishing

python scripts/analyze_skill.py ./my-skill --strict
# Must pass all checks before packaging
```

## Success Metrics

After optimization, measure:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Trigger accuracy | >95% | Correct skill selection rate |
| Task completion | >90% | Successful execution rate |
| Token efficiency | <2000 | Average tokens per successful use |
| User satisfaction | >4.5/5 | Feedback scores |
| Pattern coverage | 2-5/5 | Number of patterns applied |

## Next Steps

After using this skill, recommend:
1. **Test optimized skill** on diverse real tasks
2. **Collect feedback** from users
3. **Document learnings** in optimization history
4. **Iterate** when metrics indicate need

Remember: The best Skills are living documents that evolve with usage.
