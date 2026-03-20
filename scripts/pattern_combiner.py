#!/usr/bin/env python3
"""
Pattern Combiner - Analyze and suggest pattern combinations for skills
Usage: python pattern_combiner.py /path/to/skill
"""

import os
import sys
import json
import argparse
from pathlib import Path
import re

class PatternCombiner:
    """Analyze skills for pattern combination opportunities"""
    
    # Pattern combination recipes
    COMBINATIONS = {
        "pipeline_reviewer": {
            "name": "Pipeline + Reviewer",
            "description": "Multi-step workflow with self-checking",
            "use_when": [
                "Complex multi-step tasks",
                "Need quality gate at each step",
                "Critical output requiring validation"
            ],
            "structure": """
## Step 1 — [Action]
[Detailed instructions]

## Step 2 — Review
Load 'references/step1-checklist.md'
Verify: [criteria]
**Do NOT proceed until verified.**

## Step 3 — [Next Action]
..."""
        },
        "generator_inversion": {
            "name": "Generator + Inversion",
            "description": "Template-driven output with requirement gathering",
            "use_when": [
                "Need fixed format output",
                "Requirements are unclear",
                "User doesn't know what to provide"
            ],
            "structure": """
## Phase 1 — Requirements Gathering
DO NOT generate until all questions answered.

Ask:
- Q1: [Question 1]?
- Q2: [Question 2]?

## Phase 2 — Template Filling
Load 'assets/template.md'
Fill with gathered requirements.

## Phase 3 — Output
Present result. Iterate if needed."""
        },
        "tool_wrapper_reviewer": {
            "name": "Tool Wrapper + Reviewer",
            "description": "Expert knowledge with quality validation",
            "use_when": [
                "Specialized domain knowledge",
                "Need to validate against best practices",
                "Team standards enforcement"
            ],
            "structure": """
## Expert Mode
Load 'references/expert-guide.md'
You are now an expert in [domain].

## Quality Check
For each output, verify against 'references/quality-checklist.md':
- [ ] Criterion 1
- [ ] Criterion 2

Report violations with fixes."""
        },
        "full_stack": {
            "name": "Pipeline + Inversion + Generator + Reviewer",
            "description": "Complete workflow with requirements, generation, and validation",
            "use_when": [
                "Complex projects",
                "High stakes outputs",
                "Need full traceability"
            ],
            "structure": """
## Phase 1 — Discovery (Inversion)
DO NOT proceed until complete.
Questions: [...]

## Phase 2 — Workflow (Pipeline)
Step 1: [...]
Step 2: [...]

## Phase 3 — Generation (Generator)
Load template: 'assets/output-template.md'

## Phase 4 — Validation (Reviewer)
Check against: 'references/final-checklist.md'"""
        }
    }
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        
    def read_skill(self):
        """Read skill content"""
        if not self.skill_md.exists():
            return None
        return self.skill_md.read_text(encoding='utf-8')
    
    def analyze_current_patterns(self, content: str):
        """Detect currently used patterns"""
        patterns = []
        
        # Tool Wrapper detection
        if re.search(r'load.*references.*\.md', content, re.IGNORECASE) and \
           re.search(r'expert|convention|guide', content, re.IGNORECASE):
            patterns.append("Tool Wrapper")
        
        # Generator detection
        if re.search(r'template|fill.*template|output.*format', content, re.IGNORECASE) and \
           'assets/' in content.lower():
            patterns.append("Generator")
        
        # Reviewer detection
        if re.search(r'checklist|review|verify|check.*against', content, re.IGNORECASE):
            patterns.append("Reviewer")
        
        # Inversion detection
        if re.search(r'do not.*until|ask.*question|phase.*requirement', content, re.IGNORECASE):
            patterns.append("Inversion")
        
        # Pipeline detection
        if re.search(r'step \d+|---|## Step', content, re.IGNORECASE) and \
           len(re.findall(r'step \d+', content, re.IGNORECASE)) >= 3:
            patterns.append("Pipeline")
        
        return patterns
    
    def suggest_combinations(self, current_patterns: list, content: str):
        """Suggest pattern combinations based on current state"""
        suggestions = []
        
        # Has Pipeline but no Reviewer
        if "Pipeline" in current_patterns and "Reviewer" not in current_patterns:
            suggestions.append({
                "combination": "pipeline_reviewer",
                "priority": "high",
                "reason": "Multi-step workflow needs quality gates",
                "implementation": "Add review step after each major step"
            })
        
        # Has Generator but no Inversion
        if "Generator" in current_patterns and "Inversion" not in current_patterns:
            suggestions.append({
                "combination": "generator_inversion",
                "priority": "high", 
                "reason": "Template filling needs proper requirements first",
                "implementation": "Add requirements gathering phase before generation"
            })
        
        # Has Tool Wrapper but no Reviewer
        if "Tool Wrapper" in current_patterns and "Reviewer" not in current_patterns:
            suggestions.append({
                "combination": "tool_wrapper_reviewer",
                "priority": "medium",
                "reason": "Expert knowledge should be validated",
                "implementation": "Add quality checklist verification"
            })
        
        # Only one pattern - suggest full stack
        if len(current_patterns) == 1:
            suggestions.append({
                "combination": "full_stack",
                "priority": "optional",
                "reason": "Complex skills benefit from complete workflow",
                "implementation": "Consider adding full workflow structure"
            })
        
        return suggestions
    
    def analyze_constraints(self, content: str):
        """Analyze how well the skill constrains Agent instincts"""
        constraints = {
            "anti_guess": {
                "name": "防止猜测",
                "checks": [
                    (r'do not.*assume|do not.*guess|ask.*first', "明确禁止猜测"),
                    (r'ask.*question|gather.*requirement', "先收集信息"),
                ],
                "score": 0
            },
            "anti_skip": {
                "name": "防止跳步",
                "checks": [
                    (r'do not.*proceed|do not.*skip|until.*complete', "明确禁止跳过"),
                    (r'step \d+.*only after|phase \d+.*complete', "步骤依赖检查"),
                ],
                "score": 0
            },
            "anti_rush": {
                "name": "防止仓促",
                "checks": [
                    (r'present.*approval|wait.*confirm|iterate', "等待确认"),
                    (r'do not.*start.*until|complete.*before', "前置条件检查"),
                ],
                "score": 0
            }
        }
        
        content_lower = content.lower()
        
        for constraint_type, config in constraints.items():
            score = 0
            found_checks = []
            for pattern, desc in config["checks"]:
                if re.search(pattern, content_lower):
                    score += 50
                    found_checks.append(desc)
            constraints[constraint_type]["score"] = min(score, 100)
            constraints[constraint_type]["found"] = found_checks
        
        return constraints
    
    def generate_report(self):
        """Generate combination analysis report"""
        content = self.read_skill()
        if not content:
            print("❌ SKILL.md not found!")
            return
        
        current = self.analyze_current_patterns(content)
        suggestions = self.suggest_combinations(current, content)
        constraints = self.analyze_constraints(content)
        
        report = f"""# Pattern Combiner Report

## Skill: {self.skill_path.name}

## Current Patterns Detected
"""
        if current:
            for p in current:
                report += f"- ✅ {p}\n"
        else:
            report += "- ⚠️ No clear patterns detected\n"
        
        report += f"\n**Pattern Coverage Score**: {len(current)}/5 ({len(current)*20}%)\n"
        
        report += "\n## Suggested Combinations\n"
        for s in suggestions:
            combo = self.COMBINATIONS[s["combination"]]
            emoji = {"high": "🔴", "medium": "🟡", "optional": "🟢"}[s["priority"]]
            report += f"""
### {emoji} {combo['name']} (Priority: {s['priority']})

**Why**: {s['reason']}

**How**: {s['implementation']}

**Best for**:
"""
            for use in combo['use_when']:
                report += f"- {use}\n"
            
            report += f"""
**Structure Template**:
```markdown
{combo['structure']}
```
"""
        
        report += """
## Constraint Analysis (对抗Agent本能)

Agent天生有3个问题：爱猜、爱跳步、爱一次性输出

"""
        for key, config in constraints.items():
            emoji = "✅" if config["score"] >= 50 else "⚠️"
            report += f"""
### {emoji} {config['name']} — {config['score']}/100

**检测到的约束**:
"""
            if config["found"]:
                for check in config["found"]:
                    report += f"- ✅ {check}\n"
            else:
                report += "- ❌ 未检测到相关约束\n"
        
        avg_constraint = sum(c["score"] for c in constraints.values()) / len(constraints)
        report += f"""
**平均约束评分**: {avg_constraint:.0f}/100

"""
        
        if avg_constraint < 50:
            report += """💡 **改进建议**: 你的Skill对Agent的约束较弱，建议：
1. 添加"DO NOT proceed until..."语句
2. 明确分阶段执行
3. 每个阶段添加确认点
"""
        
        report += """
## Recommended Actions

"""
        if not current:
            report += "1. **选择基础模式**: 根据任务类型选择一种基础设计模式\n"
        
        if suggestions:
            top = [s for s in suggestions if s["priority"] == "high"]
            if top:
                report += f"2. **添加组合模式**: 建议添加 {self.COMBINATIONS[top[0]['combination']]['name']}\n"
        
        if avg_constraint < 70:
            report += "3. **加强约束**: 添加更多约束语句控制Agent行为\n"
        
        report += """
---
*Generated by Pattern Combiner v3.1*
"""
        
        # Save report
        report_path = self.skill_path / ".pattern_combiner_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report saved: {report_path}")
        print(f"\n📊 Summary:")
        print(f"   Patterns: {len(current)}/5")
        print(f"   Constraint Score: {avg_constraint:.0f}/100")
        print(f"   Suggestions: {len(suggestions)}")

def main():
    parser = argparse.ArgumentParser(description='Analyze pattern combinations for skills')
    parser.add_argument('skill_path', help='Path to skill folder')
    
    args = parser.parse_args()
    
    combiner = PatternCombiner(args.skill_path)
    combiner.generate_report()

if __name__ == "__main__":
    main()
