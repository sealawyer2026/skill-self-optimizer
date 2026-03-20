#!/usr/bin/env python3
"""
AI Code Generator - Generate complete skills from natural language
Usage: python ai_code_generator.py "create a skill for processing PDF files"
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

class AICodeGenerator:
    """Generate complete skills from natural language descriptions"""
    
    def __init__(self, description: str, output_dir: str = None):
        self.description = description
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.skill_name = self._extract_skill_name()
        self.skill_path = self.output_dir / self.skill_name
        
    def _extract_skill_name(self) -> str:
        """Extract skill name from description"""
        # Remove common prefixes
        desc = re.sub(r'^(create|make|build|generate)\s+(a\s+)?(skill\s+)?(for\s+)?', '', self.description, flags=re.I)
        # Convert to kebab-case
        words = re.findall(r'[a-zA-Z]+', desc.lower())
        return '-'.join(words[:4])  # Max 4 words
    
    def _analyze_requirements(self) -> dict:
        """Analyze user requirements from description"""
        requirements = {
            "task_type": "general",
            "input_format": "text",
            "output_format": "text",
            "complexity": "medium",
            "patterns": ["tool-wrapper"],
            "tools": [],
            "files_needed": []
        }
        
        # Detect task type
        task_keywords = {
            "pdf": ("document-processing", ["pypdf", "pdfplumber"]),
            "image": ("image-processing", ["pillow", "opencv"]),
            "data": ("data-processing", ["pandas", "numpy"]),
            "api": ("api-integration", ["requests", "httpx"]),
            "web": ("web-scraping", ["requests", "beautifulsoup4"]),
            "scrape": ("web-scraping", ["requests", "beautifulsoup4"]),
            "database": ("database", ["sqlite3", "sqlalchemy"]),
            "sql": ("database", ["sqlite3", "sqlalchemy"]),
            "test": ("testing", ["pytest"]),
            "convert": ("conversion", []),
            "transform": ("transformation", ["pandas"]),
            "analyze": ("analysis", ["pandas", "numpy"]),
            "generate": ("generation", []),
            "validate": ("validation", []),
            "check": ("validation", [])
        }
        
        desc_lower = self.description.lower()
        for keyword, (task_type, tools) in task_keywords.items():
            if keyword in desc_lower:
                requirements["task_type"] = task_type
                requirements["tools"].extend(tools)
                break
        
        # Detect complexity
        if any(w in desc_lower for w in ['simple', 'basic', 'minimal']):
            requirements["complexity"] = "low"
        elif any(w in desc_lower for w in ['complex', 'advanced', 'sophisticated', 'ai', 'ml']):
            requirements["complexity"] = "high"
        
        # Detect patterns
        if 'check' in desc_lower or 'validate' in desc_lower or 'review' in desc_lower:
            requirements["patterns"].append("reviewer")
        if 'ask' in desc_lower or 'confirm' in desc_lower or 'before' in desc_lower:
            requirements["patterns"].append("inversion")
        if 'template' in desc_lower or 'generate' in desc_lower:
            requirements["patterns"].append("generator")
        if 'chain' in desc_lower or 'sequence' in desc_lower or 'pipeline' in desc_lower:
            requirements["patterns"].append("orchestrator")
        
        # Detect file needs
        if 'template' in desc_lower:
            requirements["files_needed"].append("assets/template.txt")
        if 'example' in desc_lower or 'sample' in desc_lower:
            requirements["files_needed"].append("references/examples.md")
        
        return requirements
    
    def _generate_skill_md(self, requirements: dict) -> str:
        """Generate SKILL.md content"""
        task_desc = self.description.replace('create a skill for ', '').replace('create a skill to ', '')
        
        skill_md = f"""---
name: {self.skill_name}
description: "{task_desc.capitalize()}. Use when: user needs {requirements['task_type'].replace('-', ' ')}"
version: "1.0.0"
---

# {self.skill_name.replace('-', ' ').title()}

{task_desc.capitalize()}.

## When to Use

- User needs to {task_desc}
- Input is {requirements['input_format']}
- Output should be {requirements['output_format']}

## When NOT to Use

- DO NOT use for unrelated tasks
- DO NOT use when [SPECIFIC_EXCLUSION]

## Usage Flow

1. **Ask** for required information
2. **Validate** inputs
3. **Process** according to requirements
4. **Verify** outputs

## Examples

### Example 1: Basic usage
```
User: [INPUT]
Agent: [PROCESS]
Output: [RESULT]
```

### Example 2: Advanced usage
```
User: [COMPLEX_INPUT]
Agent: [PROCESS_WITH_OPTIONS]
Output: [RESULT]
```

## Output Format

```
[STRUCTURED_OUTPUT]
```

## Validation Checklist

- [ ] Input validated
- [ ] Processing complete
- [ ] Output verified
"""
        return skill_md
    
    def _generate_script(self, requirements: dict) -> str:
        """Generate processing script"""
        script_content = f"""#!/usr/bin/env python3
\"\"\"
{self.skill_name.replace('-', ' ').title()}
Auto-generated on {datetime.now().strftime('%Y-%m-%d')}
\"\"\"

import argparse
from pathlib import Path

def process(input_path: str, output_path: str = None):
    \"\"\"Main processing function\"\"\"
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Error: File not found: {{input_path}}")
        return False
    
    # TODO: Implement {requirements['task_type']} logic
    print(f"Processing: {{input_path}}")
    
    # Add your processing logic here
    
    if output_path:
        print(f"Output saved to: {{output_path}}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='{self.skill_name.replace('-', ' ').title()}')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('--output', '-o', help='Output file path')
    
    args = parser.parse_args()
    process(args.input, args.output)

if __name__ == "__main__":
    main()
"""
        return script_content
    
    def _generate_template(self, requirements: dict) -> str:
        """Generate template file"""
        return """# Template for {{task}}

## Input
{{input_data}}

## Processing
{{processing_steps}}

## Output
{{output_format}}

## Notes
{{additional_notes}}
"""
    
    def _generate_examples(self, requirements: dict) -> str:
        """Generate examples file"""
        return f"""# Examples for {self.skill_name.replace('-', ' ').title()}

## Example 1: Basic

**Input:**
```
[Your input here]
```

**Processing:**
1. Step 1
2. Step 2

**Output:**
```
[Expected output]
```

## Example 2: Advanced

[Add more examples as needed]
"""
    
    def generate(self):
        """Generate complete skill"""
        print("="*60)
        print("🤖 AI Code Generator v3.4")
        print("="*60)
        print(f"\n📝 Description: {self.description}")
        print(f"📦 Skill name: {self.skill_name}")
        print(f"📁 Output: {self.skill_path}")
        
        # Analyze requirements
        requirements = self._analyze_requirements()
        print(f"\n🔍 Analysis:")
        print(f"   Task type: {requirements['task_type']}")
        print(f"   Complexity: {requirements['complexity']}")
        print(f"   Patterns: {', '.join(requirements['patterns'])}")
        if requirements['tools']:
            print(f"   Tools: {', '.join(requirements['tools'])}")
        
        # Create directory structure
        self.skill_path.mkdir(parents=True, exist_ok=True)
        
        # Generate files
        files_created = []
        
        # SKILL.md
        skill_md = self._generate_skill_md(requirements)
        (self.skill_path / "SKILL.md").write_text(skill_md, encoding='utf-8')
        files_created.append("SKILL.md")
        
        # Processing script
        scripts_dir = self.skill_path / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        script = self._generate_script(requirements)
        (scripts_dir / "process.py").write_text(script, encoding='utf-8')
        files_created.append("scripts/process.py")
        
        # Template file (if needed)
        if "assets/template.txt" in requirements["files_needed"]:
            assets_dir = self.skill_path / "assets"
            assets_dir.mkdir(exist_ok=True)
            template = self._generate_template(requirements)
            (assets_dir / "template.txt").write_text(template, encoding='utf-8')
            files_created.append("assets/template.txt")
        
        # Examples file (if needed)
        if "references/examples.md" in requirements["files_needed"]:
            refs_dir = self.skill_path / "references"
            refs_dir.mkdir(exist_ok=True)
            examples = self._generate_examples(requirements)
            (refs_dir / "examples.md").write_text(examples, encoding='utf-8')
            files_created.append("references/examples.md")
        
        # README.md
        readme = f"""# {self.skill_name.replace('-', ' ').title()}

Auto-generated skill for: {self.description}

## Files

{chr(10).join([f'- {f}' for f in files_created])}

## Usage

```bash
python scripts/process.py input.txt --output output.txt
```

## TODO

- [ ] Implement core processing logic
- [ ] Add error handling
- [ ] Write tests
- [ ] Add more examples
"""
        (self.skill_path / "README.md").write_text(readme, encoding='utf-8')
        files_created.append("README.md")
        
        # Print summary
        print(f"\n✅ Generated {len(files_created)} files:")
        for f in files_created:
            print(f"   • {f}")
        
        print(f"\n📂 Skill location: {self.skill_path.absolute()}")
        print(f"\n🚀 Next steps:")
        print(f"   1. Review and customize SKILL.md")
        print(f"   2. Implement logic in scripts/process.py")
        print(f"   3. Test the skill")
        print(f"   4. Remove README.md before publishing")

def main():
    parser = argparse.ArgumentParser(description='AI Code Generator')
    parser.add_argument('description', help='Natural language description of the skill')
    parser.add_argument('--output', '-o', help='Output directory', default='.')
    parser.add_argument('--name', '-n', help='Override skill name')
    
    args = parser.parse_args()
    
    generator = AICodeGenerator(args.description, args.output)
    if args.name:
        generator.skill_name = args.name
        generator.skill_path = generator.output_dir / args.name
    
    generator.generate()

if __name__ == "__main__":
    main()
