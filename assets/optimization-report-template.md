# Skill Optimization Report Template

Use this template to document your optimization results.

---

## Optimization Report: {{skill_name}}

**Date**: {{date}}  
**Optimizer**: {{optimizer_name}}  
**Original Version**: {{original_version}}  
**Optimized Version**: {{optimized_version}}

---

## Executive Summary

### Scores
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Overall Score | {{before_score}} | {{after_score}} | {{score_change}} |
| Metadata Quality | {{before_metadata}} | {{after_metadata}} | {{metadata_change}} |
| Content Quality | {{before_content}} | {{after_content}} | {{content_change}} |
| Pattern Coverage | {{before_patterns}} | {{after_patterns}} | {{patterns_change}} |

### Design Patterns
| Pattern | Before | After |
|---------|--------|-------|
| Tool Wrapper | {{before_tool_wrapper}} | {{after_tool_wrapper}} |
| Generator | {{before_generator}} | {{after_generator}} |
| Reviewer | {{before_reviewer}} | {{after_reviewer}} |
| Inversion | {{before_inversion}} | {{after_inversion}} |
| Orchestrator | {{before_orchestrator}} | {{after_orchestrator}} |

---

## Issues Addressed

### Fixed
{{#fixed_issues}}
- [x] **{{level}}**: {{description}}
  - Solution: {{solution}}
{{/fixed_issues}}

### Remaining
{{#remaining_issues}}
- [ ] **{{level}}**: {{description}}
  - Recommendation: {{recommendation}}
{{/remaining_issues}}

---

## Changes Made

### Structure
{{#structure_changes}}
- {{change}}
{{/structure_changes}}

### Content
{{#content_changes}}
- {{change}}
{{/content_changes}}

### Patterns Applied
{{#patterns_applied}}
- **{{pattern_name}}**: {{pattern_description}}
{{/patterns_applied}}

---

## Before/After Comparison

### SKILL.md Size
- **Original**: {{original_lines}} lines, {{original_words}} words
- **Optimized**: {{optimized_lines}} lines, {{optimized_words}} words
- **Change**: {{lines_change}} lines, {{words_change}} words

### Key Improvements
{{#improvements}}
1. {{improvement}}
{{/improvements}}

---

## Testing Results

### Test Cases
{{#test_cases}}
#### Test {{number}}: {{name}}
**Input**: {{input}}
**Expected**: {{expected}}
**Actual**: {{actual}}
**Status**: {{status}}
{{/test_cases}}

### Performance Metrics
- **Trigger Accuracy**: {{trigger_accuracy}}%
- **Task Completion**: {{task_completion}}%
- **Average Token Usage**: {{token_usage}}
- **User Satisfaction**: {{satisfaction}}/5

---

## Recommendations

### Immediate Actions
{{#immediate_actions}}
- [ ] {{action}}
{{/immediate_actions}}

### Future Improvements
{{#future_improvements}}
- [ ] {{improvement}}
{{/future_improvements}}

---

## Lessons Learned

### What Worked Well
{{#what_worked}}
- {{item}}
{{/what_worked}}

### What Could Be Improved
{{#what_could_improve}}
- {{item}}
{{/what_could_improve}}

### Patterns to Consider Next
{{#next_patterns}}
- [ ] {{pattern}}
{{/next_patterns}}

---

## Sign-off

- [ ] Optimization reviewed
- [ ] Testing completed
- [ ] Documentation updated
- [ ] Ready for deployment

**Reviewed by**: _______________  
**Date**: _______________

---

## Appendix

### Full Analysis Report
See `.analysis_report.json` in optimized skill folder.

### Optimization Log
See `.optimization_log.md` in optimized skill folder.

### Before State
Location: {{original_path}}

### After State
Location: {{optimized_path}}
