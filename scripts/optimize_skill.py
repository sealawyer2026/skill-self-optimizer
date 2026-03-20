#!/usr/bin/env python3
"""
Skill Optimizer - Generate optimized version of a Skill
Usage: python optimize_skill.py /path/to/skill --issues issue1,issue2 --patterns generator,reviewer --output ./skill-v2
"""

import os
import sys
import re
import yaml
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional

class SkillOptimizer:
    def __init__(self, skill_path: str, output_path: str, issues: List[str] = None, patterns: List[str] = None):
        self.skill_path = Path(skill_path)
        self.output_path = Path(output_path)
        self.issues = issues or []
        self.patterns = patterns or []
        self.changes = []
        
    def optimize(self):
        """Run optimization and generate new skill version"""
        print(f"🚀 Optimizing Skill: {self.skill_path.name}")
        print(f"📁 Output: {self.output_path}\n")
        
        # Create output directory
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Copy existing skill
        self._copy_skill()
        
        # Parse original
        skill_md_path = self.output_path / "SKILL.md"
        frontmatter, body = self._parse_skill_md(skill_md_path)
        
        # Apply optimizations
        new_frontmatter = self._optimize_frontmatter(frontmatter)
        new_body = self._optimize_body(body)
        
        # Apply pattern enhancements
        if self.patterns:
            new_body = self._apply_patterns(new_body)
        
        # Fix identified issues
        if self.issues:
            new_body = self._fix_issues(new_body)
        
        # Version bump
        new_frontmatter = self._bump_version(new_frontmatter)
        
        # Write optimized SKILL.md
        self._write_skill_md(skill_md_path, new_frontmatter, new_body)
        
        # Create optimization log
        self._create_optimization_log()
        
        print(f"\n✅ Optimization complete!")
        print(f"📊 Changes made: {len(self.changes)}")
        for change in self.changes:
            print(f"   • {change}")
        
        print(f"\n💾 Optimized skill saved to: {self.output_path}")
        print(f"📝 Next steps:")
        print(f"   1. Review optimized SKILL.md")
        print(f"   2. Test on real tasks")
        print(f"   3. Run: python analyze_skill.py {self.output_path}")
    
    def _copy_skill(self):
        """Copy original skill to output directory"""
        if self.output_path.exists():
            shutil.rmtree(self.output_path)
        shutil.copytree(self.skill_path, self.output_path)
        self.changes.append("Copied original skill structure")
    
    def _parse_skill_md(self, path: Path) -> tuple:
        """Parse SKILL.md into frontmatter and body"""
        content = path.read_text(encoding='utf-8')
        
        frontmatter = {}
        body = content
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    body = parts[2]
                except yaml.YAMLError:
                    pass
        
        return frontmatter, body
    
    def _optimize_frontmatter(self, frontmatter: Dict) -> Dict:
        """Optimize YAML frontmatter"""
        new_fm = frontmatter.copy()
        
        # Ensure description has trigger conditions
        description = new_fm.get('description', '')
        if 'when' not in description.lower() and 'use when' not in description.lower():
            new_fm['description'] = self._enhance_description(description)
            self.changes.append("Enhanced description with trigger conditions")
        
        # Add version if missing
        if 'version' not in new_fm:
            new_fm['version'] = '1.0.0'
        
        return new_fm
    
    def _enhance_description(self, description: str) -> str:
        """Add trigger conditions to description"""
        # Extract skill purpose
        sentences = description.split('.')
        if sentences:
            purpose = sentences[0]
            enhanced = f"{purpose}. Use when: (1) [specific trigger 1], (2) [specific trigger 2], (3) [specific trigger 3]."
            return enhanced
        return description
    
    def _optimize_body(self, body: str) -> str:
        """Optimize body content"""
        # Remove filler words
        fillers = {
            r'\bvery\b': '',
            r'\breally\b': '',
            r'\bin order to\b': 'to',
            r'\bdue to the fact that\b': 'because',
            r'\bat this point in time\b': 'now',
        }
        
        new_body = body
        for pattern, replacement in fillers.items():
            new_body = re.sub(pattern, replacement, new_body, flags=re.I)
        
        if new_body != body:
            self.changes.append("Removed filler words for conciseness")
        
        # Add Quick Start section if missing
        if '## Quick Start' not in new_body:
            quick_start = self._generate_quick_start()
            # Insert after first heading
            lines = new_body.split('\n')
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith('# ') and i > 0:
                    insert_idx = i + 1
                    break
            lines.insert(insert_idx, '\n' + quick_start)
            new_body = '\n'.join(lines)
            self.changes.append("Added Quick Start section")
        
        return new_body
    
    def _generate_quick_start(self) -> str:
        """Generate Quick Start section"""
        return """## Quick Start

```bash
# Basic usage
python scripts/main.py [arguments]

# Example
python scripts/main.py --input file.txt --output result.txt
```

## When to Use This Skill

Use this skill when you need to: [specific use case 1], [specific use case 2], [specific use case 3].

Do NOT use when: [negative example 1], [negative example 2].
"""
    
    def _apply_patterns(self, body: str) -> str:
        """Apply selected design patterns"""
        new_body = body
        
        for pattern in self.patterns:
            if pattern.lower() == 'generator':
                new_body = self._apply_generator_pattern(new_body)
            elif pattern.lower() == 'reviewer':
                new_body = self._apply_reviewer_pattern(new_body)
            elif pattern.lower() == 'inversion':
                new_body = self._apply_inversion_pattern(new_body)
            elif pattern.lower() == 'orchestrator':
                new_body = self._apply_orchestrator_pattern(new_body)
            elif pattern.lower() == 'tool_wrapper':
                new_body = self._apply_tool_wrapper_pattern(new_body)
        
        return new_body
    
    def _apply_generator_pattern(self, body: str) -> str:
        """Add Generator pattern - template-driven outputs"""
        if '## Output Template' in body:
            return body
        
        template_section = """
## Output Template

This skill produces standardized output using the following template:

```
[Template structure with placeholders]
```

### Template Variables
- `{variable1}`: Description of variable 1
- `{variable2}`: Description of variable 2
"""
        
        body += template_section
        self.changes.append("Applied Generator pattern: Added output templates")
        return body
    
    def _apply_reviewer_pattern(self, body: str) -> str:
        """Add Reviewer pattern - modular checklists"""
        if '## Checklist' in body:
            return body
        
        checklist_section = """
## Checklist

Before completing, verify:

- [ ] Item 1: [Specific check]
- [ ] Item 2: [Specific check]
- [ ] Item 3: [Specific check]
- [ ] Item 4: [Quality criteria]

If any item fails, pause and address before continuing.
"""
        
        body += checklist_section
        self.changes.append("Applied Reviewer pattern: Added modular checklists")
        return body
    
    def _apply_inversion_pattern(self, body: str) -> str:
        """Add Inversion pattern - clarification questions"""
        if '## Clarification Questions' in body:
            return body
        
        inversion_section = """
## Clarification Questions

Before executing, gather necessary context:

1. **Question 1**: [Specific question to understand need]
   - Why: [Explanation of why this matters]

2. **Question 2**: [Specific question to scope work]
   - Why: [Explanation of why this matters]

3. **Question 3**: [Specific question about constraints]
   - Why: [Explanation of why this matters]

Do not proceed until these are answered.
"""
        
        body += inversion_section
        self.changes.append("Applied Inversion pattern: Added clarification questions")
        return body
    
    def _apply_orchestrator_pattern(self, body: str) -> str:
        """Add Orchestrator pattern - skill chains"""
        if '## Skill Chain' in body:
            return body
        
        orchestrator_section = """
## Skill Chain

This skill works best as part of a workflow:

```
[Previous Skill] → This Skill → [Next Skill]
     ↓                ↓              ↓
[Output A]      [Output B]     [Output C]
```

### Recommended Sequences

**Sequence 1: [Name]**
1. [skill-name-1] - [What it does]
2. **This Skill** - [What it adds]
3. [skill-name-2] - [What it finishes]

**Sequence 2: [Name]**
1. [skill-name-3] - [What it does]
2. **This Skill** - [What it adds]

### Next Skill Recommendation
After this skill completes, consider: [recommended-next-skill]
"""
        
        body += orchestrator_section
        self.changes.append("Applied Orchestrator pattern: Added skill chain recommendations")
        return body
    
    def _apply_tool_wrapper_pattern(self, body: str) -> str:
        """Add Tool Wrapper pattern - expert tool usage"""
        if '## Tool Expertise' in body:
            return body
        
        wrapper_section = """
## Tool Expertise

This skill transforms complex [tool/domain] operations into simple instructions.

### Tools Wrapped
- **[Tool Name]**: [What it does] → [How this skill makes it easy]
- **[Tool Name]**: [What it does] → [How this skill makes it easy]

### Why Use This Skill Instead of Raw Tools?
- ✅ **Consistency**: Standardized outputs every time
- ✅ **Safety**: Built-in validation and error handling
- ✅ **Efficiency**: No need to remember complex syntax
- ✅ **Expertise**: Embeds best practices automatically
"""
        
        body += wrapper_section
        self.changes.append("Applied Tool Wrapper pattern: Added tool expertise documentation")
        return body
    
    def _fix_issues(self, body: str) -> str:
        """Fix identified issues"""
        new_body = body
        
        for issue in self.issues:
            if issue == 'too-long':
                new_body = self._split_to_references(new_body)
            elif issue == 'ambiguous-triggering':
                new_body = self._clarify_triggers(new_body)
            elif issue == 'missing-examples':
                new_body = self._add_examples(new_body)
            elif issue == 'no-progressive-disclosure':
                new_body = self._add_progressive_disclosure(new_body)
        
        return new_body
    
    def _split_to_references(self, body: str) -> str:
        """Move large sections to references/"""
        # This is a simplified version - in practice, would need more sophisticated parsing
        refs_dir = self.output_path / "references"
        refs_dir.mkdir(exist_ok=True)
        
        # Extract large sections (simplified)
        advanced_section = """
# Advanced Usage

See [references/advanced.md](references/advanced.md) for:
- Detailed configuration options
- Edge case handling
- Performance optimization
"""
        
        self.changes.append("Split large sections to references/ for progressive disclosure")
        return body + "\n" + advanced_section
    
    def _clarify_triggers(self, body: str) -> str:
        """Make triggers more explicit"""
        trigger_section = """
## Trigger Conditions

**USE when:**
- ✅ [Specific condition 1]
- ✅ [Specific condition 2]
- ✅ [Specific condition 3]

**DO NOT use when:**
- ❌ [Negative condition 1]
- ❌ [Negative condition 2]
- ❌ [Negative condition 3]
"""
        
        self.changes.append("Clarified trigger conditions")
        return body + "\n" + trigger_section
    
    def _add_examples(self, body: str) -> str:
        """Add usage examples"""
        examples_section = """
## Examples

### Example 1: [Scenario Name]
**Input**: [What user says]
**Process**: [What the skill does]
**Output**: [What user gets]

### Example 2: [Scenario Name]
**Input**: [What user says]
**Process**: [What the skill does]
**Output**: [What user gets]
"""
        
        self.changes.append("Added usage examples")
        return body + "\n" + examples_section
    
    def _add_progressive_disclosure(self, body: str) -> str:
        """Add references for progressive disclosure"""
        disclosure_note = """
## Resources

- [Quick Reference](references/quick-ref.md) - Common commands and shortcuts
- [Advanced Topics](references/advanced.md) - Detailed configuration
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions
"""
        
        self.changes.append("Added progressive disclosure with references")
        return body + "\n" + disclosure_note
    
    def _bump_version(self, frontmatter: Dict) -> Dict:
        """Increment version number"""
        version = frontmatter.get('version', '1.0.0')
        parts = version.split('.')
        
        if len(parts) == 3:
            # Bump minor version
            parts[1] = str(int(parts[1]) + 1)
            parts[2] = '0'
            new_version = '.'.join(parts)
        else:
            new_version = '2.0.0'
        
        frontmatter['version'] = new_version
        self.changes.append(f"Version bumped: {version} → {new_version}")
        
        # Add changelog entry
        if 'changelog' not in frontmatter:
            frontmatter['changelog'] = []
        
        frontmatter['changelog'].append({
            'version': new_version,
            'changes': [c for c in self.changes if 'Version' not in c][:5]  # Top 5 changes
        })
        
        return frontmatter
    
    def _write_skill_md(self, path: Path, frontmatter: Dict, body: str):
        """Write optimized SKILL.md"""
        # Format frontmatter
        fm_yaml = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
        
        content = f"---\n{fm_yaml}---\n{body}"
        
        path.write_text(content, encoding='utf-8')
    
    def _create_optimization_log(self):
        """Create optimization log file"""
        log_content = f"""# Optimization Log

## Original Skill
- Path: {self.skill_path}
- Name: {self.skill_path.name}

## Optimization Parameters
- Issues addressed: {', '.join(self.issues) if self.issues else 'None specified'}
- Patterns applied: {', '.join(self.patterns) if self.patterns else 'None specified'}

## Changes Made
"""
        for change in self.changes:
            log_content += f"- {change}\n"
        
        log_content += """
## Validation Checklist
- [ ] Review optimized SKILL.md
- [ ] Test on 3+ real tasks
- [ ] Verify all patterns work correctly
- [ ] Check references/ organization
- [ ] Run analyze_skill.py for final check

## Metrics to Track
- Trigger accuracy: ___%
- Task completion rate: ___%
- User satisfaction: ___/5
"""
        
        log_path = self.output_path / ".optimization_log.md"
        log_path.write_text(log_content, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description='Optimize an Agent Skill')
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('--output', '-o', required=True, help='Output path for optimized skill')
    parser.add_argument('--issues', help='Comma-separated list of issues to fix')
    parser.add_argument('--patterns', '-p', help='Comma-separated list of patterns to apply')
    
    args = parser.parse_args()
    
    issues = args.issues.split(',') if args.issues else []
    patterns = args.patterns.split(',') if args.patterns else []
    
    optimizer = SkillOptimizer(args.skill_path, args.output, issues, patterns)
    optimizer.optimize()

if __name__ == "__main__":
    main()
