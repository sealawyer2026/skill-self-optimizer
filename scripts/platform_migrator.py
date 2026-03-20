#!/usr/bin/env python3
"""
Platform Migrator - Migrate skills between OpenClaw, Claude, and GPT platforms
Usage: python platform_migrator.py ./my-skill --target claude
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

class PlatformMigrator:
    """Migrate skills between different AI platforms"""
    
    PLATFORM_CONFIGS = {
        "openclaw": {
            "name": "OpenClaw",
            "file_extension": ".skill",
            "config_format": "yaml_frontmatter",
            "supports_scripts": True,
            "supports_references": True,
            "max_skill_size": 500000,  # bytes
            "special_files": ["SKILL.md"]
        },
        "claude": {
            "name": "Claude (Anthropic)",
            "file_extension": ".md",
            "config_format": "xml_tags",
            "supports_scripts": False,
            "supports_references": False,
            "max_skill_size": 100000,
            "special_files": []
        },
        "gpt": {
            "name": "ChatGPT (OpenAI)",
            "file_extension": ".json",
            "config_format": "json",
            "supports_scripts": False,
            "supports_references": False,
            "max_skill_size": 80000,
            "special_files": []
        },
        "openai": {
            "name": "OpenAI Assistants API",
            "file_extension": ".json",
            "config_format": "json_api",
            "supports_scripts": True,
            "supports_references": True,
            "max_skill_size": 200000,
            "special_files": []
        }
    }
    
    def __init__(self, skill_path: str, source: str = None, target: str = None):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.source = source or self._detect_platform()
        self.target = target
        self.output_dir = Path.cwd() / f"{self.skill_name}-{target}-migrated"
    
    def _detect_platform(self) -> str:
        """Auto-detect source platform"""
        if (self.skill_path / "SKILL.md").exists():
            return "openclaw"
        elif list(self.skill_path.glob("*.json")):
            return "gpt"
        elif list(self.skill_path.glob("*.md")):
            return "claude"
        return "openclaw"  # default
    
    def _parse_skill(self) -> dict:
        """Parse skill from source format"""
        skill_data = {
            "name": self.skill_name,
            "description": "",
            "content": "",
            "version": "1.0.0",
            "scripts": [],
            "references": {}
        }
        
        if self.source == "openclaw":
            skill_md = self.skill_path / "SKILL.md"
            if skill_md.exists():
                content = skill_md.read_text(encoding='utf-8')
                
                # Parse frontmatter
                frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
                if frontmatter_match:
                    import yaml
                    try:
                        metadata = yaml.safe_load(frontmatter_match.group(1))
                        skill_data.update(metadata)
                    except:
                        pass
                    skill_data["content"] = frontmatter_match.group(2)
                else:
                    skill_data["content"] = content
                
                # Collect scripts
                scripts_dir = self.skill_path / "scripts"
                if scripts_dir.exists():
                    for script in scripts_dir.glob("*.py"):
                        skill_data["scripts"].append({
                            "name": script.name,
                            "content": script.read_text(encoding='utf-8')
                        })
                
                # Collect references
                refs_dir = self.skill_path / "references"
                if refs_dir.exists():
                    for ref in refs_dir.glob("*.md"):
                        skill_data["references"][ref.name] = ref.read_text(encoding='utf-8')
        
        elif self.source == "claude":
            # Claude format: single markdown file
            md_files = list(self.skill_path.glob("*.md"))
            if md_files:
                content = md_files[0].read_text(encoding='utf-8')
                
                # Try to extract name from first heading
                name_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                if name_match:
                    skill_data["name"] = name_match.group(1).lower().replace(' ', '-')
                
                skill_data["content"] = content
        
        elif self.source in ["gpt", "openai"]:
            # GPT/OpenAI format: JSON
            json_files = list(self.skill_path.glob("*.json"))
            if json_files:
                with open(json_files[0], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    skill_data.update(data)
        
        return skill_data
    
    def _convert_to_openclaw(self, skill_data: dict) -> dict:
        """Convert to OpenClaw format"""
        converted = {
            "files": {}
        }
        
        # Create SKILL.md
        skill_md = f"""---
name: {skill_data['name']}
description: "{skill_data.get('description', 'Migrated from ' + self.PLATFORM_CONFIGS[self.source]['name'])}"
version: "{skill_data.get('version', '1.0.0')}"
migrated_from: {self.source}
migrated_at: {datetime.now().isoformat()}
---

{skill_data['content']}
"""
        converted["files"]["SKILL.md"] = skill_md
        
        # Add scripts
        if skill_data.get("scripts"):
            for script in skill_data["scripts"]:
                converted["files"][f"scripts/{script['name']}"] = script["content"]
        
        # Add references
        if skill_data.get("references"):
            for name, content in skill_data["references"].items():
                converted["files"][f"references/{name}"] = content
        
        return converted
    
    def _convert_to_claude(self, skill_data: dict) -> dict:
        """Convert to Claude format"""
        converted = {
            "files": {}
        }
        
        # Claude uses XML-style tags in markdown
        content = f"""# {skill_data['name'].replace('-', ' ').title()}

<instructions>
{skill_data.get('description', '')}
</instructions>

{skill_data['content']}

---

*Migrated from {self.PLATFORM_CONFIGS[self.source]['name']} on {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        # Inline scripts as code blocks since Claude doesn't support external scripts
        if skill_data.get("scripts"):
            content += "\n\n## Reference Scripts\n\n"
            for script in skill_data["scripts"]:
                content += f"\n### {script['name']}\n\n```python\n{script['content']}\n```\n"
        
        converted["files"][f"{skill_data['name']}.md"] = content
        
        return converted
    
    def _convert_to_gpt(self, skill_data: dict) -> dict:
        """Convert to GPT format"""
        converted = {
            "files": {}
        }
        
        # GPT uses JSON format
        gpt_data = {
            "name": skill_data['name'].replace('-', ' ').title(),
            "description": skill_data.get('description', ''),
            "instructions": skill_data['content'],
            "model": "gpt-4",
            "tools": [],
            "file_ids": []
        }
        
        # Add code interpreter if scripts exist
        if skill_data.get("scripts"):
            gpt_data["tools"].append({"type": "code_interpreter"})
            # Scripts become files to upload
            for script in skill_data["scripts"]:
                converted["files"][f"files/{script['name']}"] = script["content"]
        
        converted["files"][f"{skill_data['name']}.json"] = json.dumps(gpt_data, indent=2)
        
        return converted
    
    def _convert_to_openai(self, skill_data: dict) -> dict:
        """Convert to OpenAI Assistants API format"""
        converted = {
            "files": {}
        }
        
        assistant_data = {
            "name": skill_data['name'].replace('-', ' ').title(),
            "description": skill_data.get('description', ''),
            "instructions": skill_data['content'],
            "model": "gpt-4-turbo-preview",
            "tools": [{"type": "code_interpreter"}],
            "metadata": {
                "migrated_from": self.source,
                "migrated_at": datetime.now().isoformat()
            }
        }
        
        converted["files"]["assistant.json"] = json.dumps(assistant_data, indent=2)
        
        # Add scripts
        if skill_data.get("scripts"):
            for script in skill_data["scripts"]:
                converted["files"][f"scripts/{script['name']}"] = script["content"]
        
        return converted
    
    def migrate(self):
        """Run migration"""
        print("="*60)
        print(f"🔄 Platform Migrator v3.4")
        print("="*60)
        print(f"\n📦 Source: {self.PLATFORM_CONFIGS[self.source]['name']}")
        print(f"🎯 Target: {self.PLATFORM_CONFIGS[self.target]['name']}")
        print(f"📂 Skill: {self.skill_name}")
        
        # Parse source
        print(f"\n📖 Parsing {self.source} format...")
        skill_data = self._parse_skill()
        
        # Convert
        print(f"🔄 Converting to {self.target} format...")
        converters = {
            "openclaw": self._convert_to_openclaw,
            "claude": self._convert_to_claude,
            "gpt": self._convert_to_gpt,
            "openai": self._convert_to_openai
        }
        
        converted = converters[self.target](skill_data)
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write files
        print(f"\n💾 Writing files to {self.output_dir}...")
        for file_path, content in converted["files"].items():
            full_path = self.output_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
            print(f"   ✓ {file_path}")
        
        # Generate migration report
        self._generate_report(skill_data, converted)
        
        print(f"\n✅ Migration complete!")
        print(f"📂 Output: {self.output_dir.absolute()}")
        
        # Show warnings
        self._show_warnings(skill_data)
    
    def _generate_report(self, skill_data: dict, converted: dict):
        """Generate migration report"""
        report = f"""# Migration Report

**Source:** {self.PLATFORM_CONFIGS[self.source]['name']}  
**Target:** {self.PLATFORM_CONFIGS[self.target]['name']}  
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Skill:** {self.skill_name}

---

## 📊 Conversion Summary

| Aspect | Source | Target | Status |
|--------|--------|--------|--------|
| Scripts | {len(skill_data.get('scripts', []))} files | {'Supported' if self.PLATFORM_CONFIGS[self.target]['supports_scripts'] else 'Inlined/Removed'} | ⚠️ Check |
| References | {len(skill_data.get('references', {}))} files | {'Supported' if self.PLATFORM_CONFIGS[self.target]['supports_references'] else 'Inlined/Removed'} | ⚠️ Check |
| Format | {self.PLATFORM_CONFIGS[self.source]['config_format']} | {self.PLATFORM_CONFIGS[self.target]['config_format']} | ✅ Converted |

## 📁 Files Generated

{chr(10).join([f'- {path}' for path in converted['files'].keys()])}

## ⚠️ Important Notes

"""
        
        if not self.PLATFORM_CONFIGS[self.target]['supports_scripts'] and skill_data.get('scripts'):
            report += "- **Scripts:** Target platform doesn't support external scripts. Scripts have been inlined as code blocks.\n"
        
        if not self.PLATFORM_CONFIGS[self.target]['supports_references'] and skill_data.get('references'):
            report += "- **References:** Target platform doesn't support reference files. Consider inlining critical content.\n"
        
        report += f"""
- **Size Limit:** Target platform max size is {self.PLATFORM_CONFIGS[self.target]['max_skill_size'] // 1024}KB. Verify your skill fits.
- **Testing:** Always test the migrated skill thoroughly on the target platform.

## 🚀 Next Steps

1. Review converted files
2. Test on {self.PLATFORM_CONFIGS[self.target]['name']}
3. Adjust for platform-specific features
4. Publish/deploy
"""
        
        report_path = self.output_dir / "MIGRATION_REPORT.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path}")
    
    def _show_warnings(self, skill_data: dict):
        """Show migration warnings"""
        warnings = []
        
        if not self.PLATFORM_CONFIGS[self.target]['supports_scripts'] and skill_data.get('scripts'):
            warnings.append("⚠️ Scripts inlined - functionality may be limited")
        
        if not self.PLATFORM_CONFIGS[self.target]['supports_references'] and skill_data.get('references'):
            warnings.append("⚠️ References removed - consider inlining important content")
        
        # Check size
        total_size = len(skill_data.get('content', ''))
        if skill_data.get('scripts'):
            for script in skill_data['scripts']:
                total_size += len(script['content'])
        
        if total_size > self.PLATFORM_CONFIGS[self.target]['max_skill_size']:
            warnings.append(f"⚠️ Skill size ({total_size // 1024}KB) exceeds target limit ({self.PLATFORM_CONFIGS[self.target]['max_skill_size'] // 1024}KB)")
        
        if warnings:
            print(f"\n⚠️ Warnings:")
            for w in warnings:
                print(f"   {w}")

def main():
    parser = argparse.ArgumentParser(description='Platform Migrator')
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('--source', '-s', choices=['openclaw', 'claude', 'gpt', 'openai'],
                        help='Source platform (auto-detected if not specified)')
    parser.add_argument('--target', '-t', required=True, choices=['openclaw', 'claude', 'gpt', 'openai'],
                        help='Target platform')
    parser.add_argument('--output', '-o', help='Output directory')
    
    args = parser.parse_args()
    
    migrator = PlatformMigrator(args.skill_path, args.source, args.target)
    if args.output:
        migrator.output_dir = Path(args.output)
    
    migrator.migrate()

if __name__ == "__main__":
    main()
