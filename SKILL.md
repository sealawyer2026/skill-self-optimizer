---
name: skill-self-optimizer
description: "Meta-skill for fully automated skill optimization. Use when: (1) Skill triggers incorrectly, (2) User reports issues, (3) Pre-ClawHub review, (4) Version iteration, (5) Applying Google's 5 design patterns, (6) Want fully automatic optimization pipeline, (7) Need pattern combination suggestions, (8) Choosing right design pattern. Implements Tool Wrapper, Generator, Reviewer, Inversion, Pipeline patterns with combination support."
version: "3.1.0"
changelog:
  - "3.1.0": Added pattern combiner, decision tree, constraint analysis based on Google best practices
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

## v3.1 - Pattern Combiner & Decision Tree (NEW)

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
