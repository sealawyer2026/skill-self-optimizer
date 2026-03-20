#!/usr/bin/env python3
"""
Version Diff - Smart comparison between skill versions
Usage: python version_diff.py /path/to/skill-v1 /path/to/skill-v2
"""

import os
import sys
import difflib
import argparse
from pathlib import Path
import re

class VersionDiff:
    """Compare two versions of a skill"""
    
    def __init__(self, v1_path: str, v2_path: str):
        self.v1_path = Path(v1_path)
        self.v2_path = Path(v2_path)
        self.v1_skill = self.v1_path / "SKILL.md"
        self.v2_skill = self.v2_path / "SKILL.md"
        
    def read_files(self):
        """Read both skill files"""
        v1_content = self.v1_skill.read_text(encoding='utf-8') if self.v1_skill.exists() else ""
        v2_content = self.v2_skill.read_text(encoding='utf-8') if self.v2_skill.exists() else ""
        return v1_content, v2_content
    
    def extract_version(self, content: str) -> str:
        """Extract version from skill"""
        match = re.search(r'version[:\s]*["\']?([\d.]+)', content, re.IGNORECASE)
        return match.group(1) if match else "unknown"
    
    def extract_patterns(self, content: str) -> list:
        """Extract design patterns used"""
        patterns = []
        content_lower = content.lower()
        
        checks = [
            ('tool wrapper', r'load.*references.*expert|convention'),
            ('generator', r'template|fill.*template|output.*format'),
            ('reviewer', r'checklist|review|verify'),
            ('inversion', r'do not.*until|ask.*question|phase'),
            ('pipeline', r'step \d+|## step|phase \d+'),
        ]
        
        for name, pattern in checks:
            if re.search(pattern, content_lower):
                patterns.append(name)
        
        return patterns
    
    def extract_metrics(self, content: str) -> dict:
        """Extract key metrics"""
        return {
            "lines": len(content.splitlines()),
            "chars": len(content),
            "headers": len(re.findall(r'^##', content, re.MULTILINE)),
            "examples": len(re.findall(r'### example|## example', content, re.IGNORECASE)),
            "constraints": len(re.findall(r'do not|must not|never', content, re.IGNORECASE)),
            "steps": len(re.findall(r'step \d+|phase \d+', content, re.IGNORECASE))
        }
    
    def generate_diff(self, v1_content: str, v2_content: str) -> str:
        """Generate unified diff"""
        v1_lines = v1_content.splitlines()
        v2_lines = v2_content.splitlines()
        
        diff = difflib.unified_diff(
            v1_lines, v2_lines,
            fromfile=f"{self.v1_path.name}/SKILL.md",
            tofile=f"{self.v2_path.name}/SKILL.md",
            lineterm=''
        )
        
        return '\n'.join(diff)
    
    def analyze_changes(self, v1_content: str, v2_content: str) -> dict:
        """Analyze meaningful changes"""
        changes = {
            "added_patterns": [],
            "removed_patterns": [],
            "improved_areas": [],
            "size_change": {}
        }
        
        v1_patterns = set(self.extract_patterns(v1_content))
        v2_patterns = set(self.extract_patterns(v2_content))
        
        changes["added_patterns"] = list(v2_patterns - v1_patterns)
        changes["removed_patterns"] = list(v1_patterns - v2_patterns)
        
        v1_metrics = self.extract_metrics(v1_content)
        v2_metrics = self.extract_metrics(v2_content)
        
        changes["size_change"] = {
            key: v2_metrics[key] - v1_metrics[key]
            for key in v1_metrics
        }
        
        # Detect improvements
        if v2_metrics["constraints"] > v1_metrics["constraints"]:
            changes["improved_areas"].append("约束设计 (更多 DO NOT/MUST NOT)")
        
        if v2_metrics["steps"] > v1_metrics["steps"]:
            changes["improved_areas"].append("流程控制 (更多步骤/阶段)")
        
        if v2_metrics["examples"] > v1_metrics["examples"]:
            changes["improved_areas"].append("示例丰富度")
        
        return changes
    
    def generate_smart_summary(self, changes: dict, v1_ver: str, v2_ver: str) -> str:
        """Generate human-readable summary"""
        summary = f"""
## 版本对比摘要

### 版本信息
- 旧版本: {v1_ver}
- 新版本: {v2_ver}

### 设计模式变化
"""
        
        if changes["added_patterns"]:
            summary += f"\n✅ **新增模式**: {', '.join(changes['added_patterns'])}\n"
        
        if changes["removed_patterns"]:
            summary += f"\n❌ **移除模式**: {', '.join(changes['removed_patterns'])}\n"
        
        if not changes["added_patterns"] and not changes["removed_patterns"]:
            summary += "\n📊 设计模式保持不变\n"
        
        summary += "\n### 指标变化\n"
        size = changes["size_change"]
        for key, value in size.items():
            emoji = "📈" if value > 0 else "📉" if value < 0 else "➡️"
            sign = "+" if value > 0 else ""
            summary += f"- {emoji} {key}: {sign}{value}\n"
        
        if changes["improved_areas"]:
            summary += "\n### 🎉 改进亮点\n"
            for area in changes["improved_areas"]:
                summary += f"- ✅ {area}\n"
        
        return summary
    
    def generate_html_report(self, diff: str, summary: str, changes: dict) -> str:
        """Generate HTML report"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Skill Version Diff</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .summary {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .diff {{ background: white; padding: 20px; border-radius: 10px; overflow-x: auto; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .diff-add {{ background: #d4edda; color: #155724; }}
        .diff-del {{ background: #f8d7da; color: #721c24; }}
        .diff-info {{ background: #e7f3ff; color: #004085; }}
        pre {{ margin: 0; font-family: 'Monaco', 'Consolas', monospace; font-size: 13px; line-height: 1.5; }}
        h1, h2 {{ margin-top: 0; }}
        .metric {{ display: inline-block; background: #f0f0f0; padding: 10px 15px; border-radius: 20px; margin: 5px; }}
        .metric.positive {{ background: #d4edda; color: #155724; }}
        .metric.negative {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔄 Skill 版本对比</h1>
        <p>{self.v1_path.name} → {self.v2_path.name}</p>
    </div>
    
    <div class="summary">
        {summary.replace(chr(10), '<br>')}
    </div>
    
    <div class="diff">
        <h2>📊 详细差异</h2>
        <pre>{diff.replace('<', '&lt;').replace('>', '&gt;')}</pre>
    </div>
    
    <div style="text-align: center; margin-top: 20px; color: #666;">
        Generated by Version Diff v3.2
    </div>
</body>
</html>"""
        return html
    
    def run(self):
        """Run version comparison"""
        print("="*60)
        print("🔄 Version Diff v3.2")
        print("="*60)
        print(f"\n📁 V1: {self.v1_path.name}")
        print(f"📁 V2: {self.v2_path.name}")
        
        v1_content, v2_content = self.read_files()
        
        if not v1_content or not v2_content:
            print("❌ SKILL.md not found in one or both paths!")
            return
        
        v1_ver = self.extract_version(v1_content)
        v2_ver = self.extract_version(v2_content)
        
        print(f"\n📌 V1 Version: {v1_ver}")
        print(f"📌 V2 Version: {v2_ver}")
        
        # Analyze changes
        changes = self.analyze_changes(v1_content, v2_content)
        
        # Generate summary
        summary = self.generate_smart_summary(changes, v1_ver, v2_ver)
        print(summary)
        
        # Generate diff
        diff = self.generate_diff(v1_content, v2_content)
        
        # Save reports
        diff_path = Path("version_diff.txt")
        with open(diff_path, 'w', encoding='utf-8') as f:
            f.write(f"# Version Diff Report\n\n")
            f.write(f"V1: {self.v1_path.name} ({v1_ver})\n")
            f.write(f"V2: {self.v2_path.name} ({v2_ver})\n\n")
            f.write(summary)
            f.write(f"\n\n## Unified Diff\n\n```diff\n{diff}\n```\n")
        
        # HTML report
        html = self.generate_html_report(diff, summary, changes)
        html_path = Path("version_diff.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n✅ 对比完成!")
        print(f"📄 文本报告: {diff_path}")
        print(f"🌐 HTML报告: {html_path}")
        
        # Quick summary
        print(f"\n📊 快速概览:")
        print(f"   新增模式: {len(changes['added_patterns'])} 个")
        print(f"   移除模式: {len(changes['removed_patterns'])} 个")
        print(f"   改进领域: {len(changes['improved_areas'])} 个")

def main():
    parser = argparse.ArgumentParser(description='Compare skill versions')
    parser.add_argument('v1_path', help='Path to version 1')
    parser.add_argument('v2_path', help='Path to version 2')
    
    args = parser.parse_args()
    
    differ = VersionDiff(args.v1_path, args.v2_path)
    differ.run()

if __name__ == "__main__":
    main()
