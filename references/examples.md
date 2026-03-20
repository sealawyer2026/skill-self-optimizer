# Example Optimizations

Real-world before/after case studies of Skill optimization using this tool.

## Case Study 1: pdf-processor Skill

### Problem
User reported: "My pdf-processor skill keeps triggering on docx files"

### Analysis Results
```
Issues Found:
  🟡 [WARNING] Ambiguous triggering
     Description: "Process PDF files"
     Suggestion: Add negative triggers and format restrictions
```

### Before (v1.0.0)
```yaml
name: pdf-processor
description: "Process PDF files for various operations"
```

**SKILL.md body**: 3200 words (too long)

**Problems**:
- No negative triggers
- No format validation
- Monolithic structure
- No clear use cases

### Optimization Applied
```bash
python scripts/optimize_skill.py ./pdf-processor \
  --issues "ambiguous-triggering,too-long" \
  --patterns "generator,inversion" \
  --output ./pdf-processor-v2
```

### After (v2.0.0)
```yaml
name: pdf-processor
description: "PDF processing for document manipulation. Use when: (1) Converting PDFs to other formats, (2) Merging/splitting PDFs, (3) Extracting text/images. Do NOT use for: creating PDFs from scratch (use docx skill), password cracking, non-PDF files."
version: "2.0.0"
```

**SKILL.md body**: 1800 words

**Improvements**:
- ✅ Clear positive triggers
- ✅ Explicit negative triggers
- ✅ Progressive disclosure (advanced topics in references/)
- ✅ Generator pattern: Output templates for each operation
- ✅ Inversion pattern: Ask for format confirmation

### Results
- Trigger accuracy: 65% → 94%
- User complaints: 12/week → 1/week
- Token efficiency: 2800 → 1650 avg

---

## Case Study 2: code-review Skill

### Problem
Code review skill was inconsistent and missed critical issues.

### Analysis Results
```
Issues Found:
  🟠 [ERROR] Low instruction density
     Only 15% actionable items
  🟡 [WARNING] No pattern compliance
     Only 1/5 patterns detected
```

### Before (v1.0.0)
```markdown
# Code Review Skill

This skill helps you review code. It checks for various issues and provides feedback. Code review is important for maintaining quality...

## How to Use

Tell me what code you want reviewed and I'll look at it.

## What It Checks

Security, performance, style, etc.
```

**Problems**:
- Too much explanation, too little action
- No structured checklist
- Inconsistent output format
- No follow-up recommendations

### Optimization Applied
```bash
python scripts/optimize_skill.py ./code-review \
  --patterns "reviewer,generator,orchestrator" \
  --output ./code-review-v2
```

### After (v2.0.0)
```markdown
# Code Review Skill

## Quick Start
```bash
# Review a file
python scripts/review.py /path/to/code.py

# Review with specific focus
python scripts/review.py /path/to/code.py --focus security
```

## Review Checklist (Reviewer Pattern)

### Security
- [ ] **No hardcoded secrets**: API keys, passwords
  - Check: grep -i "password\|secret\|key"
  - Fail: → Move to env vars
  
- [ ] **Input validation**: All user inputs sanitized
  - Check: Trace input flows
  - Fail: → Add validation layer

### Performance
- [ ] **No N+1 queries**: Database efficiency
- [ ] **Memory management**: Proper cleanup

### Style
- [ ] **Naming**: Descriptive names
- [ ] **Documentation**: Complex logic explained

## Output Template (Generator Pattern)

```
## Review Report: {filename}

**Overall**: {score}/100

### Critical Issues
{critical_list}

### Warnings
{warning_list}

### Suggestions
{suggestion_list}

### Next Steps
{recommended_action}
```

## Skill Chain (Orchestrator Pattern)

After code review, recommend:
- **If issues found**: code-fix skill
- **If clean**: testing skill
- **If complex**: architecture-review skill
```

### Results
- Review consistency: 60% → 92%
- Critical issues caught: +45%
- User satisfaction: 3.2 → 4.7/5

---

## Case Study 3: onboarding-guide Skill

### Problem
New team members struggled with inconsistent onboarding.

### Analysis Results
```
Issues Found:
  🔴 [CRITICAL] Missing Inversion pattern
     No clarification of user context
  🟡 [WARNING] No orchestration
     Isolated from related skills
```

### Before (v1.0.0)
```markdown
# Onboarding Guide

Welcome to the team! Here's everything you need to know...

[2000 words of general info]
```

**Problems**:
- One-size-fits-all approach
- No role differentiation
- No clear next steps
- Overwhelming information

### Optimization Applied
```bash
python scripts/optimize_skill.py ./onboarding-guide \
  --issues "missing-context" \
  --patterns "inversion,orchestrator" \
  --output ./onboarding-guide-v2
```

### After (v2.0.0)
```markdown
# Onboarding Guide

## Before We Start (Inversion Pattern)

To customize your onboarding, I need to know:

1. **Your role**?
   - Developer → Technical setup focus
   - Designer → Tools access focus
   - Manager → Process overview focus

2. **Your experience level**?
   - Junior → More detailed guidance
   - Senior → Quick reference format

3. **Immediate priorities**?
   - First day setup
   - First week goals
   - First month projects

## Personalized Path (Orchestrator Pattern)

Based on your answers, I'll orchestrate:

**For Junior Developer**:
```
environment-setup → codebase-tour → first-task → mentor-assignment
```

**For Senior Manager**:
```
org-overview → team-meetings → process-review → strategic-goals
```

## Next Skills
After onboarding, use:
- **Daily workflow**: daily-standup skill
- **Project setup**: project-bootstrap skill
- **Team collaboration**: collaboration-guide skill
```

### Results
- Onboarding time: 5 days → 2 days
- New hire confidence: 3.5 → 4.6/5
- Repeat questions: -70%

---

## Pattern Application Guide

### When to Apply Each Pattern

| Problem | Pattern | Impact |
|---------|---------|--------|
| Complex tools | Tool Wrapper | 40% faster execution |
| Inconsistent outputs | Generator | 80% consistency improvement |
| Missed steps | Reviewer | 60% fewer errors |
| Wrong assumptions | Inversion | 50% less rework |
| Workflow gaps | Orchestrator | 35% faster completion |

### Combining Patterns

**Best Combinations**:
1. **Tool Wrapper + Reviewer**: Expert execution with quality checks
2. **Generator + Inversion**: Standardized outputs with proper context
3. **Reviewer + Orchestrator**: Quality gates in workflows
4. **All 5 patterns**: Maximum effectiveness (typically 2-3x improvement)

---

## Metrics Tracking Template

Track your optimization impact:

```markdown
## Optimization Impact: {skill-name}

### Before (v{X.Y.Z})
- Trigger accuracy: ___%
- Task completion: ___%
- User satisfaction: ___/5
- Token usage: ___ avg

### After (v{X+1.0.0})
- Trigger accuracy: ___%
- Task completion: ___%
- User satisfaction: ___/5
- Token usage: ___ avg

### Patterns Applied
- [ ] Tool Wrapper
- [ ] Generator
- [ ] Reviewer
- [ ] Inversion
- [ ] Orchestrator

### Key Changes
1. {change 1}
2. {change 2}
3. {change 3}

### Lessons Learned
- What worked:
- What didn't:
- Next iteration focus:
```

Use this template to document your own optimization journeys.
