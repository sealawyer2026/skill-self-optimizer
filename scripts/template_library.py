#!/usr/bin/env python3
"""
Template Library - Community skill templates
Usage: python template_library.py [--list] [--search keyword] [--install template-name]
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from typing import List, Dict

# Built-in templates
BUILTIN_TEMPLATES = {
    "minimal": {
        "name": "Minimal Skill",
        "description": "Bare minimum skill structure",
        "category": "starter",
        "files": {
            "SKILL.md": """---
name: {skill_name}
description: "A minimal skill template"
---

# {skill_name}

Brief description of what this skill does.

## When to Use

- Condition 1
- Condition 2

## Usage

Instructions here.
"""
        }
    },
    "tool-wrapper": {
        "name": "Tool Wrapper Pattern",
        "description": "Skill wrapping external tools with expert knowledge",
        "category": "pattern",
        "files": {
            "SKILL.md": """---
name: {skill_name}
description: "Expert wrapper for [TOOL]. Use when: user needs [OPERATION] with [DATA]"
---

# {skill_name}

Makes you an instant expert in [TOOL].

## When to Use

- DO NOT assume user knows [TOOL] options - ask first
- User mentions [OPERATION] with [DATA]

## Expert Knowledge

### Common Options
```
--option1: Description
--option2: Description
```

### Common Errors
| Error | Cause | Fix |
|-------|-------|-----|
| error1 | cause1 | fix1 |

## Usage Flow

1. **Ask** about [REQUIRED_INFO]
2. **Execute** with proper flags
3. **Validate** output
""",
            "references/common-errors.md": "# Common Errors\n\nList common errors and solutions here.\n",
            "references/examples.md": "# Examples\n\n## Example 1\n\n```bash\n# Command here\n```\n"
        }
    },
    "generator": {
        "name": "Generator Pattern",
        "description": "Template-driven output generation",
        "category": "pattern",
        "files": {
            "SKILL.md": """---
name: {skill_name}
description: "Generate [OUTPUT_TYPE] from [INPUT]. Use when: user needs consistent [OUTPUT]"
---

# {skill_name}

Template-driven [OUTPUT_TYPE] generation.

## When to Use

- User requests [OUTPUT_TYPE]
- Consistency is important

## Template Structure

```
[TITLE]

[SECTION_1]
- Point 1
- Point 2

[SECTION_2]
- Detail 1
- Detail 2
```

## Output Rules

1. Always use template
2. Fill all placeholders
3. Never add extra sections
""",
            "assets/template.txt": """TITLE: {{title}}

SECTION 1:
{{section1_content}}

SECTION 2:
{{section2_content}}
"""
        }
    },
    "reviewer": {
        "name": "Reviewer Pattern", 
        "description": "Checklist-based quality review",
        "category": "pattern",
        "files": {
            "SKILL.md": """---
name: {skill_name}
description: "Review [ITEM_TYPE] against standards. Use when: quality check needed"
---

# {skill_name}

Modular checklist-based review.

## When to Use

- User asks for review of [ITEM_TYPE]
- Before finalizing [DELIVERABLE]

## Review Checklist

### Category 1
- [ ] Criterion 1
- [ ] Criterion 2

### Category 2
- [ ] Criterion 3
- [ ] Criterion 4

## Scoring

| Score | Meaning |
|-------|---------|
| 100% | Perfect |
| 80%+ | Good |
| 60%+ | Acceptable |
| <60% | Needs work |

## Output Format

```
## Review Results

**Score**: X/100

### Passed
- Item 1

### Issues
- [SEVERITY] Issue 1 → Fix: Solution

### Recommendations
1. Rec 1
```
""",
            "references/checklist.md": "# Full Checklist\n\nComplete checklist here\n"
        }
    },
    "pipeline": {
        "name": "Pipeline Pattern",
        "description": "Multi-step workflow with gating",
        "category": "pattern", 
        "files": {
            "SKILL.md": """---
name: {skill_name}
description: "Multi-step [WORKFLOW]. Use when: [COMPLEX_TASK] requiring phased approach"
---

# {skill_name}

Multi-phase [WORKFLOW] with gating.

## When to Use

- Complex [TASK] requiring multiple steps
- Each step needs validation

## Pipeline Overview

```
[INPUT] → Phase 1 → Gate → Phase 2 → Gate → Phase 3 → [OUTPUT]
```

## Phase 1: [NAME]

**DO NOT proceed to Phase 2 until:**
- Gate condition 1
- Gate condition 2

### Steps
1. Step 1
2. Step 2

## Phase 2: [NAME]

**DO NOT proceed to Phase 3 until:**
- Gate condition 3

### Steps
1. Step 1
2. Step 2

## Phase 3: [NAME]

### Steps
1. Step 1
2. Final validation
"""
        }
    },
    "inversion": {
        "name": "Inversion Pattern",
        "description": "Ask before doing",
        "category": "pattern",
        "files": {
            "SKILL.md": """---
name: {skill_name}
description: "[TASK] with user clarification. Use when: ambiguity likely"
---

# {skill_name}

Ask before doing.

## When to Use

- [TASK] with multiple interpretations
- Context is unclear

## DO NOT Proceed Until

You have asked ALL clarification questions:

### Required Information
1. **Question 1**: [what to ask]
2. **Question 2**: [what to ask]
3. **Question 3**: [what to ask]

## After Clarification

Once user provides answers:
1. Confirm understanding
2. Execute with confirmed parameters
3. Validate output matches intent
"""
        }
    },
    "api-integration": {
        "name": "API Integration",
        "description": "Skill for REST API integration",
        "category": "integration",
        "files": {
            "SKILL.md": """---
name: {skill_name}
description: "Interact with [API_NAME]. Use when: user needs [API_OPERATION]"
---

# {skill_name}

[API_NAME] integration.

## Prerequisites

Set environment variable:
```bash
export {API_NAME}_API_KEY="your-key"
```

## API Reference

### Authentication
Header: `Authorization: Bearer ${API_KEY}`

### Common Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /endpoint1 | GET | Description |
| /endpoint2 | POST | Description |

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Unauthorized | Check API key |
| 429 | Rate limited | Wait and retry |
""",
            "references/api-reference.md": "# API Reference\n\nFull API documentation\n"
        }
    },
    "data-processor": {
        "name": "Data Processor",
        "description": "Process and transform data files",
        "category": "utility",
        "files": {
            "SKILL.md": """---
name: {skill_name}
description: "Process [DATA_TYPE] files. Use when: user needs [OPERATION] on [DATA]"
---

# {skill_name}

[DATA_TYPE] processing and transformation.

## Supported Formats

- Format 1 (.ext1)
- Format 2 (.ext2)

## Operations

### Operation 1
```python
# Example code
```

### Operation 2
```python
# Example code
```

## Validation

Always validate:
1. File format
2. Data integrity
3. Output correctness
""",
            "scripts/processor.py": "#!/usr/bin/env python3\n# Processing script\n\ndef process(data):\n    pass\n"
        }
    }
}

class TemplateLibrary:
    """Manage skill templates"""
    
    def __init__(self):
        self.templates_dir = Path.home() / ".skill-optimizer" / "templates"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self._load_templates()
    
    def _load_templates(self):
        """Load all available templates"""
        self.templates = BUILTIN_TEMPLATES.copy()
        
        # Load custom templates from directory
        if self.templates_dir.exists():
            for template_file in self.templates_dir.glob("*.json"):
                try:
                    with open(template_file, 'r') as f:
                        template = json.load(f)
                        self.templates[template_file.stem] = template
                except:
                    pass
    
    def list_templates(self, category: str = None) -> List[Dict]:
        """List available templates"""
        results = []
        
        for key, template in self.templates.items():
            if category and template.get("category") != category:
                continue
            
            results.append({
                "id": key,
                "name": template["name"],
                "description": template["description"],
                "category": template.get("category", "general")
            })
        
        return results
    
    def search_templates(self, keyword: str) -> List[Dict]:
        """Search templates by keyword"""
        results = []
        keyword = keyword.lower()
        
        for key, template in self.templates.items():
            if (keyword in template["name"].lower() or 
                keyword in template["description"].lower()):
                results.append({
                    "id": key,
                    "name": template["name"],
                    "description": template["description"],
                    "category": template.get("category", "general")
                })
        
        return results
    
    def install_template(self, template_id: str, output_dir: str, skill_name: str = None):
        """Install template to directory"""
        if template_id not in self.templates:
            print(f"❌ Template not found: {template_id}")
            return False
        
        template = self.templates[template_id]
        output_path = Path(output_dir)
        
        # Use provided name or template default
        if skill_name is None:
            skill_name = output_path.name
        
        print(f"📦 Installing template: {template['name']}")
        print(f"📁 Target: {output_path}")
        
        # Create directory structure
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create files
        for file_path, content in template["files"].items():
            full_path = output_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Replace placeholders
            content = content.replace("{skill_name}", skill_name)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✓ Created: {file_path}")
        
        print(f"\n✅ Template installed successfully!")
        print(f"   Location: {output_path.absolute()}")
        print(f"   Files: {len(template['files'])}")
        
        return True
    
    def save_custom_template(self, template_id: str, skill_path: str, name: str, description: str):
        """Save current skill as template"""
        skill_path = Path(skill_path)
        
        if not skill_path.exists():
            print(f"❌ Skill not found: {skill_path}")
            return False
        
        template = {
            "name": name,
            "description": description,
            "category": "custom",
            "files": {}
        }
        
        # Collect all files
        for file_path in skill_path.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(skill_path)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Replace skill name with placeholder
                    content = content.replace(skill_path.name, "{skill_name}")
                    template["files"][str(rel_path)] = content
                except:
                    pass  # Skip binary files
        
        # Save template
        template_file = self.templates_dir / f"{template_id}.json"
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2)
        
        print(f"✅ Template saved: {template_id}")
        print(f"   Location: {template_file}")
        print(f"   Files: {len(template['files'])}")
        
        return True
    
    def show_template_info(self, template_id: str):
        """Show detailed template information"""
        if template_id not in self.templates:
            print(f"❌ Template not found: {template_id}")
            return
        
        template = self.templates[template_id]
        
        print("="*60)
        print(f"📦 {template['name']}")
        print("="*60)
        print(f"\n📝 Description:")
        print(f"   {template['description']}")
        print(f"\n📂 Category: {template.get('category', 'general')}")
        print(f"\n📄 Files included:")
        for file_path in template["files"].keys():
            print(f"   • {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Template Library')
    parser.add_argument('--list', '-l', action='store_true', help='List all templates')
    parser.add_argument('--search', '-s', help='Search templates by keyword')
    parser.add_argument('--install', '-i', help='Install template by ID')
    parser.add_argument('--output', '-o', help='Output directory for install')
    parser.add_argument('--name', '-n', help='Skill name for template')
    parser.add_argument('--info', help='Show template info')
    parser.add_argument('--save', help='Save current skill as template (provide ID)')
    parser.add_argument('--skill-path', help='Path to skill for --save')
    parser.add_argument('--category', '-c', help='Filter by category')
    
    args = parser.parse_args()
    
    library = TemplateLibrary()
    
    if args.list:
        templates = library.list_templates(args.category)
        print("="*60)
        print("📚 Available Templates")
        print("="*60)
        
        current_category = None
        for t in templates:
            if t['category'] != current_category:
                current_category = t['category']
                print(f"\n【{current_category.upper()}】")
            print(f"\n  {t['id']:20} - {t['name']}")
            print(f"  {'':20}   {t['description']}")
    
    elif args.search:
        templates = library.search_templates(args.search)
        print(f"🔍 Search results for '{args.search}':")
        for t in templates:
            print(f"  • {t['id']}: {t['name']}")
    
    elif args.install:
        if not args.output:
            print("❌ Please specify --output directory")
            sys.exit(1)
        library.install_template(args.install, args.output, args.name)
    
    elif args.info:
        library.show_template_info(args.info)
    
    elif args.save:
        if not args.skill_path:
            print("❌ Please specify --skill-path")
            sys.exit(1)
        library.save_custom_template(
            args.save, 
            args.skill_path,
            args.name or args.save,
            f"Custom template based on {args.skill_path}"
        )
    
    else:
        # Default: list templates
        templates = library.list_templates()
        print("="*60)
        print("📚 Skill Templates")
        print("="*60)
        print("\nUsage:")
        print("  python template_library.py --list")
        print("  python template_library.py --install template-id --output ./my-skill")
        print("  python template_library.py --info template-id")
        print("\n" + "-"*60)
        
        current_category = None
        for t in templates:
            if t['category'] != current_category:
                current_category = t['category']
                print(f"\n【{current_category.upper()}】")
            print(f"  {t['id']:20} - {t['name']}")

if __name__ == "__main__":
    main()
