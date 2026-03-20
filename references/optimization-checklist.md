# Skill Optimization Checklist

Pre-publication checklist for Skills going to ClawHub.

## Critical Checks (Must Pass)

### Structure
- [ ] SKILL.md exists in root directory
- [ ] No forbidden auxiliary files (README.md, CHANGELOG.md, etc.)
- [ ] Skill folder named exactly as skill name
- [ ] Name uses only lowercase letters, digits, and hyphens

### Metadata
- [ ] YAML frontmatter present at top of SKILL.md
- [ ] `name` field present and valid
- [ ] `description` field present (100-500 characters)
- [ ] Description includes clear "when to use" triggers
- [ ] Description includes "do NOT use when" negative examples

### Content Quality
- [ ] SKILL.md body < 2500 words
- [ ] No filler words (very, really, basically, etc.)
- [ ] Actionable instructions, not just explanations
- [ ] Progressive disclosure properly implemented

## Quality Checks (Should Pass)

### Design Patterns (Target: 2-5 patterns)
- [ ] At least one execution pattern (Tool Wrapper or Generator)
- [ ] At least one quality pattern (Reviewer or Inversion)
- [ ] Orchestrator pattern if skill fits into workflows

### Tool Wrapper Check (if applicable)
- [ ] Complex tools wrapped with simple interfaces
- [ ] Sensible defaults provided
- [ ] Error handling documented
- [ ] Validation rules specified

### Generator Check (if applicable)
- [ ] Output templates defined
- [ ] Template variables documented
- [ ] Example outputs provided
- [ ] Quality criteria specified

### Reviewer Check (if applicable)
- [ ] Modular checklists present
- [ ] Pass/fail criteria clear
- [ ] Remediation steps for failures
- [ ] Prioritized by criticality

### Inversion Check (if applicable)
- [ ] Clarification questions before execution
- [ ] Explanation of why each question matters
- [ ] Options provided where possible
- [ ] Stop conditions defined

### Orchestrator Check (if applicable)
- [ ] Skill chains documented
- [ ] Input/output handoffs clear
- [ ] Conditional routing logic
- [ ] Parallel execution opportunities identified

## Technical Checks

### Scripts
- [ ] Scripts in `scripts/` directory
- [ ] Scripts referenced in SKILL.md
- [ ] Scripts tested and working
- [ ] Scripts have help/usage documentation

### References
- [ ] Large content in `references/` (not inline)
- [ ] References linked from SKILL.md
- [ ] No deeply nested references (>1 level deep)
- [ ] Reference files have table of contents if >100 lines

### Assets
- [ ] Assets in `assets/` directory
- [ ] Assets not loaded into context (used in output only)
- [ ] Templates, images, fonts properly organized

## Testing Requirements

### Functional Testing
- [ ] Tested on 3+ real tasks
- [ ] Triggering accuracy >95%
- [ ] Task completion rate >90%
- [ ] No critical errors or crashes

### Edge Cases
- [ ] Tested with minimal input
- [ ] Tested with maximal input
- [ ] Tested with ambiguous input
- [ ] Error messages are helpful

### Integration Testing
- [ ] Works with other related skills
- [ ] Doesn't break when other skills present
- [ ] Skill chains work correctly

## Documentation Requirements

### SKILL.md Sections (Recommended)
- [ ] Quick Start
- [ ] When to Use This Skill
- [ ] Core functionality documentation
- [ ] Examples (3+ if possible)
- [ ] Resources/references section

### Code Documentation
- [ ] Scripts have comments
- [ ] Complex logic explained
- [ ] Usage examples in comments

## Version Management

### Versioning
- [ ] Version number in frontmatter
- [ ] Follows semantic versioning
- [ ] Changelog tracked

### Iteration Records
- [ ] Previous versions documented
- [ ] Optimization history tracked
- [ ] Lessons learned recorded

## Final Review

### Before Packaging
- [ ] Run `analyze_skill.py --strict` (must pass)
- [ ] Review all changes since last version
- [ ] Check for breaking changes
- [ ] Verify all references resolve

### Packaging
- [ ] Run `package_skill.py` successfully
- [ ] No validation errors
- [ ] .skill file created
- [ ] File size reasonable (<10MB)

### Pre-Submission
- [ ] Test installation from .skill file
- [ ] Verify skill triggers correctly
- [ ] Check that resources load properly
- [ ] Final manual review

## Post-Publication

### Monitoring
- [ ] Track usage metrics
- [ ] Collect user feedback
- [ ] Monitor error rates
- [ ] Watch for triggering issues

### Iteration Triggers
Consider optimization when:
- [ ] Trigger accuracy < 90%
- [ ] User complaints > 3 in one week
- [ ] Task completion < 85%
- [ ] New pattern available that could help
- [ ] 30+ days since last optimization

## Scoring Guide

Calculate quality score:

| Category | Weight | Score |
|----------|--------|-------|
| Critical Checks | 30% | ___/100 |
| Quality Checks | 25% | ___/100 |
| Technical Checks | 20% | ___/100 |
| Testing | 15% | ___/100 |
| Documentation | 10% | ___/100 |

**Total Score**: ___/100

### Score Interpretation
- **90-100**: Excellent - Ready for ClawHub
- **80-89**: Good - Minor improvements needed
- **70-79**: Acceptable - Address warnings
- **60-69**: Needs work - Fix issues before publishing
- **<60**: Not ready - Major revision required

## Quick Fixes Reference

### If description is unclear
```yaml
# Before
description: "PDF processing skill"

# After
description: "PDF processing for document manipulation. Use when: (1) Converting PDFs to other formats, (2) Merging/splitting PDFs, (3) Extracting text/images. Do NOT use for: creating PDFs from scratch (use docx skill), password cracking."
```

### If SKILL.md is too long
```markdown
# Before: 3000 words inline

# After: Move sections to references/
## Advanced Usage
See [references/advanced.md](references/advanced.md) for:
- Detailed configuration
- Edge cases
- Performance tuning
```

### If missing patterns
```markdown
# Add Generator pattern
## Output Template
```
[Template with {placeholders}]
```

# Add Reviewer pattern
## Quality Checklist
- [ ] Check 1
- [ ] Check 2

# Add Inversion pattern
## Before Starting
I need to clarify:
1. Question 1...
2. Question 2...
```

## Sign-Off

I certify that this Skill:
- [ ] Passes all critical checks
- [ ] Meets quality standards
- [ ] Has been tested thoroughly
- [ ] Is ready for ClawHub publication

**Reviewer**: _______________  
**Date**: _______________  
**Version**: _______________
