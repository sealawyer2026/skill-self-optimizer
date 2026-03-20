# Google's 5 Design Patterns - Detailed Reference

This document provides in-depth guidance on implementing each of Google's 5 Skill design patterns.

## Pattern 1: Tool Wrapper

### Purpose
Transform complex tools or domains into accessible expertise for the Agent.

### When to Use
- Integrating external APIs or services
- Wrapping command-line tools
- Domain-specific operations (legal, medical, financial)
- Complex multi-step tool workflows

### Implementation Guide

```markdown
## Tool Expertise

This skill transforms complex [tool/domain] into simple, reliable operations.

### Wrapped Tools
| Tool | Raw Complexity | Skill Simplification |
|------|---------------|---------------------|
| `ffmpeg` | 100+ flags, codec knowledge | "Convert X to Y format" |
| `openssl` | Cryptographic parameters | "Generate secure key" |
| `pandas` | DataFrame operations | "Analyze CSV for insights" |

### Why This Skill?
- **No memorization needed**: Agent doesn't need to remember syntax
- **Best practices built-in**: Secure defaults, common patterns
- **Error handling**: Graceful fallbacks and explanations
- **Consistency**: Same output format every time

### Example Transformation

**Without Skill:**
```
User: "Analyze this data"
Agent: [spends 10 steps figuring out pandas syntax]
```

**With Tool Wrapper Skill:**
```
User: "Analyze this data"
Agent: [immediately uses skill, 2 steps, optimal output]
```
```

### Best Practices
1. **Abstract parameters**: Hide complexity behind intent-based interfaces
2. **Sensible defaults**: Provide good defaults for all optional parameters
3. **Error context**: When tools fail, explain why in domain terms
4. **Validation**: Pre-validate inputs before calling tools

---

## Pattern 2: Generator

### Purpose
Produce standardized, high-quality outputs using templates.

### When to Use
- Document creation (reports, contracts, emails)
- Code generation (boilerplate, scaffolding)
- Structured data outputs (JSON, YAML, CSV)
- Format conversion with structure preservation

### Implementation Guide

```markdown
## Output Templates

### Template A: [Use Case Name]
```
[Structured template with {placeholders}]

Section 1: {section_1_content}
- Point A: {point_a}
- Point B: {point_b}

Section 2: {section_2_content}
```

### Template Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `{section_1_content}` | [What goes here] | "Example content" |
| `{point_a}` | [What goes here] | "Example point" |

### Quality Checklist
Before finalizing output:
- [ ] All placeholders filled
- [ ] Formatting consistent
- [ ] Required sections present
- [ ] Style guidelines followed
```

### Template Design Principles

1. **Progressive Detail**: Start with outline, fill in details
2. **Conditional Sections**: Use [IF condition] for optional parts
3. **Example-Driven**: Include filled example alongside template
4. **Validation Rules**: Define what makes output "good"

### Example: Report Generator Skill

```markdown
## Report Template

```
# {report_title}

**Date**: {date}  
**Author**: {author}  
**Status**: {status}

## Executive Summary
{executive_summary}

## Key Findings
{findings}

[IF recommendations_exist]
## Recommendations
{recommendations}
[ENDIF]

## Appendix
{appendix}
```

### Pre-Generation Checklist
- [ ] Report scope defined
- [ ] Target audience identified
- [ ] Required data sources listed
```

---

## Pattern 3: Reviewer

### Purpose
Systematic quality assurance through modular checklists.

### When to Use
- Code review
- Document proofreading
- Compliance checking
- Output validation
- Security auditing

### Implementation Guide

```markdown
## Review Checklist

### Category 1: [Category Name]
- [ ] **Item 1**: [Specific check]
  - Pass criteria: [What constitutes passing]
  - Fail action: [What to do if failed]
  
- [ ] **Item 2**: [Specific check]
  - Pass criteria: [What constitutes passing]
  - Fail action: [What to do if failed]

### Category 2: [Category Name]
- [ ] **Item 3**: [Specific check]
- [ ] **Item 4**: [Specific check]

### Review Result
| Category | Status | Notes |
|----------|--------|-------|
| Category 1 | ✅/❌ | |
| Category 2 | ✅/❌ | |

### If Any Check Fails:
1. Pause execution
2. Report specific failure
3. Suggest remediation
4. Re-review after fix
```

### Checklist Design Principles

1. **Binary where possible**: Clear pass/fail criteria
2. **Actionable failures**: Every failure has a remediation step
3. **Prioritized**: Critical checks first
4. **Measurable**: Quantify when possible ("< 100ms", "> 95%")

### Example: Code Review Skill

```markdown
## Code Review Checklist

### Security
- [ ] **No hardcoded secrets**: No API keys, passwords in code
  - Check: grep -i "password\|secret\|key" 
  - Fail: Move to environment variables

- [ ] **Input validation**: All external inputs sanitized
  - Check: Trace all user inputs
  - Fail: Add validation layer

### Performance
- [ ] **No N+1 queries**: Database queries efficient
  - Check: Review query patterns
  - Fail: Add eager loading or caching

- [ ] **Memory efficiency**: No memory leaks
  - Check: Large object lifecycle
  - Fail: Add cleanup logic

### Maintainability
- [ ] **Function length**: Functions < 50 lines
- [ ] **Naming clarity**: Descriptive variable/function names
- [ ] **Documentation**: Complex logic explained

### Review Report
```
Security: 2/2 ✅
Performance: 1/2 ❌ (N+1 detected in line 45)
Maintainability: 3/3 ✅

**Action Required**: Fix N+1 query before merging.
```
```

---

## Pattern 4: Inversion

### Purpose
Gather necessary context through targeted questions before execution.

### When to Use
- Ambiguous requirements
- Complex multi-variable tasks
- High-stakes operations
- Context-dependent outcomes

### Implementation Guide

```markdown
## Information Gathering

Before proceeding, I need to understand:

### Question 1: [Topic]
**Question**: [Specific question]

**Why this matters**: [Explanation of how answer affects approach]

**Options**:
- A) [Option A] → [Implication]
- B) [Option B] → [Implication]
- C) [Option C] → [Implication]

### Question 2: [Topic]
**Question**: [Specific question]

**Why this matters**: [Explanation]

### Stop Condition
Do not proceed until:
- ✅ All questions answered
- ✅ Ambiguities resolved
- ✅ Approach confirmed

### After Gathering
Once clarified, I will:
1. [Step 1 based on answers]
2. [Step 2 based on answers]
3. [Step 3 based on answers]
```

### Question Design Principles

1. **Open first, narrow later**: Start broad, then drill down
2. **Explain relevance**: Why does this answer matter?
3. **Provide options**: When possible, give structured choices
4. **Show consequences**: "If A, then X; if B, then Y"

### Example: Requirements Gathering Skill

```markdown
## Project Clarification

To design the right solution, I need to understand:

### Q1: Primary Goal
**What is the main objective?**

- A) **Increase revenue** → I'll focus on conversion optimization
- B) **Reduce costs** → I'll focus on efficiency improvements
- C) **Improve experience** → I'll focus on UX enhancements
- D) **Other**: [please specify]

### Q2: Constraints
**What are the key constraints?**

| Constraint | Question | Why It Matters |
|------------|----------|----------------|
| Budget | What's the budget range? | Determines solution scope |
| Timeline | What's the deadline? | Affects complexity choices |
| Tech Stack | Any preferred technologies? | Influences architecture |
| Compliance | Any regulatory requirements? | May require specific features |

### Q3: Success Metrics
**How will we measure success?**

**Options** (select all that apply):
- [ ] Revenue increase of ___%
- [ ] Cost reduction of ___%
- [ ] User satisfaction score > ___
- [ ] Performance improvement: ___
- [ ] Other: ___

### Next Steps
Once you answer these, I'll provide:
1. Detailed approach
2. Resource requirements
3. Risk assessment
4. Timeline estimate
```

---

## Pattern 5: Orchestrator

### Purpose
Coordinate multiple skills into cohesive workflows.

### When to Use
- Multi-step complex tasks
- Skills that naturally sequence
- Workflow optimization
- Parallel execution opportunities

### Implementation Guide

```markdown
## Skill Orchestration

### Workflow Overview
```
[Input] → [Skill A] → [Skill B] → [Skill C] → [Output]
              ↓           ↓           ↓
         [Output A]  [Output B]  [Output C]
```

### Skill Chain Options

#### Chain 1: [Name/Use Case]
**Sequence**:
1. **[skill-1-name]** → [What it produces]
2. **[skill-2-name]** → [What it produces]
3. **[skill-3-name]** → [Final output]

**When to use**: [Specific scenario]

#### Chain 2: [Name/Use Case]
**Sequence**:
1. **[skill-4-name]** → [What it produces]
2. **[skill-5-name]** → [What it produces]

**When to use**: [Specific scenario]

### Dynamic Routing
Based on input, route to:

| Condition | Next Skill | Reason |
|-----------|-----------|--------|
| If [condition A] | [skill-X] | [Why] |
| If [condition B] | [skill-Y] | [Why] |
| Otherwise | [skill-Z] | [Default] |

### Recommended Next Steps
After this skill completes:
- **For [scenario 1]**: Use [skill-name]
- **For [scenario 2]**: Use [skill-name]
- **For [scenario 3]**: Use [skill-name]

### Parallel Execution
When possible, these skills can run in parallel:
- [Skill A] + [Skill B] → Combine results
- [Skill C] + [Skill D] → Combine results
```

### Orchestration Principles

1. **Clear handoffs**: Define outputs of each skill clearly
2. **Conditional routing**: Different paths for different inputs
3. **Parallel when possible**: Identify independent operations
4. **Fallback options**: What to do if a skill fails

### Example: Project Management Orchestrator

```markdown
## Project Workflow

### Standard Project Flow
```
[Requirements] 
      ↓
[requirements-gathering] → Clear specs
      ↓
[architecture-design] → Technical design
      ↓
[implementation-plan] → Task breakdown
      ↓
[code-generation] → Implementation
      ↓
[code-review] → Quality check
      ↓
[testing] → Validation
      ↓
[deployment] → Release
```

### Quick Paths

**For small changes**:
```
[change-request] → [code-generation] → [code-review] → Done
```

**For urgent fixes**:
```
[bug-report] → [hotfix-generation] → [minimal-review] → Deploy
```

### Parallel Workstreams

**Frontend Track**: [ui-design] → [frontend-code] → [ui-testing]
**Backend Track**: [api-design] → [backend-code] → [api-testing]
**Combined**: Merge → [integration-testing] → Deploy

### Skill Recommendations by Phase

| Phase | Recommended Skills | Optional Skills |
|-------|-------------------|-----------------|
| Discovery | requirements-gathering, stakeholder-analysis | market-research |
| Design | architecture-design, ui-design | security-review |
| Build | code-generation, component-library | performance-optimization |
| Validate | code-review, testing, security-scan | accessibility-check |
| Deploy | deployment, monitoring-setup | rollback-planning |
```

---

## Combining Patterns

The most effective Skills combine multiple patterns:

### Example: Document Review Skill

Combines **Tool Wrapper** + **Reviewer** + **Generator**:

```markdown
## Document Review

### Wrapped Tools
- Grammar checking API
- Style guide validation
- Plagiarism detection

### Review Checklist (Reviewer Pattern)
- [ ] Grammar: No errors
- [ ] Style: Follows brand guide
- [ ] Structure: Proper sections
- [ ] Clarity: Readable score > 80

### Output Template (Generator Pattern)
```
## Review Report: {document_name}

**Overall Score**: {score}/100

### Issues Found
{issues_list}

### Suggested Edits
{edits}

### Approved Sections
{approved}
```
```

### Pattern Selection Matrix

| Task Type | Primary Pattern | Secondary Pattern |
|-----------|----------------|-------------------|
| API integration | Tool Wrapper | Reviewer (validation) |
| Report creation | Generator | Reviewer (quality check) |
| Requirements gathering | Inversion | Generator (output format) |
| Complex workflow | Orchestrator | All others as needed |
| Code review | Reviewer | Tool Wrapper (linters) |
| Multi-step process | Orchestrator | Inversion (clarification) |

Remember: Patterns are composable. The best Skills layer patterns for maximum effectiveness.
