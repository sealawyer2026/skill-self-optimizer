---
name: skill-self-optimizer
description: "Meta-skill for analyzing and optimizing other Agent Skills. Use when: (1) Skill triggers incorrectly, (2) User reports issues, (3) Pre-ClawHub review, (4) Version iteration, (5) Applying Google's 5 design patterns. Implements Tool Wrapper, Generator, Reviewer, Inversion, and Orchestrator patterns."
version: "2.0.0"
changelog:
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
