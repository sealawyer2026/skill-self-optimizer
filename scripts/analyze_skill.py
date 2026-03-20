#!/usr/bin/env python3
"""
Skill Analyzer - Diagnose Skill quality and identify optimization opportunities
Usage: python analyze_skill.py /path/to/skill-folder [--strict]
"""

import os
import sys
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class SkillAnalyzer:
    def __init__(self, skill_path: str, strict: bool = False):
        self.skill_path = Path(skill_path)
        self.strict = strict
        self.issues = []
        self.scores = {}
        self.patterns = {}
        
    def analyze(self) -> Dict:
        """Run complete analysis and return report"""
        print(f"🔍 Analyzing Skill: {self.skill_path.name}\n")
        
        # Check basic structure
        self._check_structure()
        
        # Parse SKILL.md
        skill_md_path = self.skill_path / "SKILL.md"
        if not skill_md_path.exists():
            self._add_issue("CRITICAL", "SKILL.md not found", "Skill must have SKILL.md")
            return self._generate_report()
            
        frontmatter, body = self._parse_skill_md(skill_md_path)
        
        # Analyze metadata
        self._analyze_metadata(frontmatter)
        
        # Analyze content
        self._analyze_content(body)
        
        # Check design patterns
        self._detect_patterns(body)
        
        # Check resources
        self._check_resources()
        
        # Calculate scores
        self._calculate_scores()
        
        return self._generate_report()
    
    def _check_structure(self):
        """Verify skill directory structure"""
        required_files = ["SKILL.md"]
        for f in required_files:
            if not (self.skill_path / f).exists():
                self._add_issue("CRITICAL", f"Missing required file: {f}", "All skills must have SKILL.md")
        
        # Check for forbidden files
        forbidden = ["README.md", "CHANGELOG.md", "INSTALLATION.md", "QUICK_REFERENCE.md"]
        for f in forbidden:
            if (self.skill_path / f).exists():
                self._add_issue("WARNING", f"Forbidden file found: {f}", "Skills should not contain auxiliary documentation")
    
    def _parse_skill_md(self, path: Path) -> Tuple[Dict, str]:
        """Extract YAML frontmatter and body from SKILL.md"""
        content = path.read_text(encoding='utf-8')
        
        # Parse frontmatter
        frontmatter = {}
        body = content
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    body = parts[2]
                except yaml.YAMLError as e:
                    self._add_issue("ERROR", "Invalid YAML frontmatter", str(e))
        
        return frontmatter, body
    
    def _analyze_metadata(self, frontmatter: Dict):
        """Analyze YAML frontmatter quality"""
        # Check name
        name = frontmatter.get('name', '')
        if not name:
            self._add_issue("CRITICAL", "Missing 'name' in frontmatter", "Name is required")
        elif not re.match(r'^[a-z0-9-]+$', name):
            self._add_issue("ERROR", f"Invalid name format: '{name}'", "Use only lowercase, digits, and hyphens")
        
        # Check description
        description = frontmatter.get('description', '')
        if not description:
            self._add_issue("CRITICAL", "Missing 'description' in frontmatter", "Description is required for triggering")
        elif len(description) < 50:
            self._add_issue("WARNING", "Description too short", f"Only {len(description)} chars. Should be 100-300 chars with clear triggers")
        elif len(description) > 500:
            self._add_issue("WARNING", "Description too long", f"{len(description)} chars. May cause context bloat")
        
        # Check for trigger clarity
        trigger_words = ['when', 'use when', 'for', 'if', 'trigger']
        has_trigger = any(word in description.lower() for word in trigger_words)
        if not has_trigger:
            self._add_issue("WARNING", "Description lacks clear trigger conditions", "Add 'when to use' guidance")
        
        self.scores['metadata'] = 100 - len([i for i in self.issues if i['level'] in ['CRITICAL', 'ERROR']]) * 20
    
    def _analyze_content(self, body: str):
        """Analyze SKILL.md body content"""
        word_count = len(body.split())
        line_count = len(body.split('\n'))
        
        # Check length
        if word_count > 3000:
            self._add_issue("ERROR", f"SKILL.md too long: {word_count} words", "Target: <2500 words. Use progressive disclosure.")
        elif word_count > 2500:
            self._add_issue("WARNING", f"SKILL.md approaching limit: {word_count} words", "Consider moving content to references/")
        
        # Check conciseness (simplified heuristic)
        filler_patterns = [r'\b(very|really|quite|rather|basically|essentially)\b', 
                          r'\b(in order to|due to the fact that|at this point in time)\b']
        filler_count = sum(len(re.findall(p, body, re.I)) for p in filler_patterns)
        if filler_count > 10:
            self._add_issue("INFO", f"Potential filler words detected: {filler_count}", "Consider more concise phrasing")
        
        # Check for instructions vs explanations
        instruction_lines = len([l for l in body.split('\n') if l.strip().startswith('-') or l.strip().startswith('*')])
        if instruction_lines < 10 and word_count > 500:
            self._add_issue("WARNING", "Low instruction density", "More actionable items, fewer explanations")
        
        # Check progressive disclosure
        has_references = 'references/' in body or 'see [' in body.lower()
        has_scripts = 'scripts/' in body
        
        if word_count > 1500 and not has_references:
            self._add_issue("WARNING", "Large file without references", "Consider splitting into references/")
        
        self.scores['content'] = max(0, 100 - (word_count - 2000) / 20 if word_count > 2000 else 100)
        self.scores['conciseness'] = max(0, 100 - filler_count * 2)
    
    def _detect_patterns(self, body: str):
        """Detect which of the 5 design patterns are implemented"""
        body_lower = body.lower()
        
        # Pattern 1: Tool Wrapper
        tool_patterns = ['expert', 'specialized', 'professional', 'wrapper', 'api', 'integration']
        self.patterns['tool_wrapper'] = any(p in body_lower for p in tool_patterns)
        
        # Pattern 2: Generator
        generator_patterns = ['template', 'generate', 'output format', 'standardized', 'consistent output']
        self.patterns['generator'] = any(p in body_lower for p in generator_patterns)
        
        # Pattern 3: Reviewer
        reviewer_patterns = ['checklist', 'review', 'validate', 'verify', 'check', 'assessment']
        self.patterns['reviewer'] = any(p in body_lower for p in reviewer_patterns)
        
        # Pattern 4: Inversion
        inversion_patterns = ['ask before', 'clarify', 'question', 'confirm', 'understand', 'gather']
        self.patterns['inversion'] = any(p in body_lower for p in inversion_patterns)
        
        # Pattern 5: Orchestrator
        orchestrator_patterns = ['chain', 'sequence', 'next skill', 'recommend', 'coordinate', 'workflow']
        self.patterns['orchestrator'] = any(p in body_lower for p in orchestrator_patterns)
        
        pattern_count = sum(self.patterns.values())
        if pattern_count < 2:
            self._add_issue("WARNING", f"Only {pattern_count} design patterns detected", "Target: 2-5 patterns for optimal effectiveness")
        
        self.scores['patterns'] = pattern_count * 20
    
    def _check_resources(self):
        """Check scripts/, references/, assets/ organization"""
        scripts_dir = self.skill_path / "scripts"
        references_dir = self.skill_path / "references"
        assets_dir = self.skill_path / "assets"
        
        # Check scripts
        if scripts_dir.exists():
            scripts = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))
            if scripts:
                print(f"  ✓ Found {len(scripts)} script(s)")
                # Check if scripts are referenced in SKILL.md
                skill_md = (self.skill_path / "SKILL.md").read_text()
                for script in scripts:
                    if script.name not in skill_md:
                        self._add_issue("INFO", f"Script not referenced: {script.name}", "Add usage example in SKILL.md")
        
        # Check references
        if references_dir.exists():
            refs = list(references_dir.glob("*.md"))
            if refs:
                print(f"  ✓ Found {len(refs)} reference file(s)")
        
        # Check assets
        if assets_dir.exists():
            print(f"  ✓ Found assets/ directory")
    
    def _calculate_scores(self):
        """Calculate overall quality scores"""
        self.scores['overall'] = (
            self.scores.get('metadata', 0) * 0.3 +
            self.scores.get('content', 0) * 0.3 +
            self.scores.get('conciseness', 0) * 0.2 +
            self.scores.get('patterns', 0) * 0.2
        )
    
    def _add_issue(self, level: str, issue: str, suggestion: str):
        """Add an issue to the list"""
        self.issues.append({
            'level': level,
            'issue': issue,
            'suggestion': suggestion
        })
    
    def _generate_report(self) -> Dict:
        """Generate structured analysis report"""
        report = {
            'skill_name': self.skill_path.name,
            'summary': {
                'critical_issues': len([i for i in self.issues if i['level'] == 'CRITICAL']),
                'errors': len([i for i in self.issues if i['level'] == 'ERROR']),
                'warnings': len([i for i in self.issues if i['level'] == 'WARNING']),
                'info': len([i for i in self.issues if i['level'] == 'INFO']),
            },
            'scores': self.scores,
            'patterns_detected': self.patterns,
            'issues': self.issues,
            'recommendations': self._generate_recommendations()
        }
        
        # Print report
        self._print_report(report)
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Pattern recommendations
        if not self.patterns.get('generator'):
            recommendations.append("Apply Generator pattern: Add templates for standard outputs")
        if not self.patterns.get('reviewer'):
            recommendations.append("Apply Reviewer pattern: Add modular checklists")
        if not self.patterns.get('inversion'):
            recommendations.append("Apply Inversion pattern: Add clarification questions")
        if not self.patterns.get('orchestrator'):
            recommendations.append("Apply Orchestrator pattern: Add skill chain recommendations")
        
        # Content recommendations
        if self.scores.get('content', 100) < 80:
            recommendations.append("Reduce SKILL.md size: Move details to references/")
        
        return recommendations
    
    def _print_report(self, report: Dict):
        """Print formatted analysis report"""
        print("=" * 60)
        print("📊 ANALYSIS REPORT")
        print("=" * 60)
        
        # Summary
        s = report['summary']
        print(f"\nIssues Found:")
        print(f"  🔴 Critical: {s['critical_issues']}")
        print(f"  🟠 Errors: {s['errors']}")
        print(f"  🟡 Warnings: {s['warnings']}")
        print(f"  🔵 Info: {s['info']}")
        
        # Scores
        print(f"\nScores:")
        for key, score in report['scores'].items():
            if key != 'overall':
                status = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
                print(f"  {status} {key}: {score:.1f}/100")
        
        print(f"\n📈 Overall Score: {report['scores'].get('overall', 0):.1f}/100")
        
        # Patterns
        print(f"\nDesign Patterns Detected:")
        for pattern, detected in report['patterns_detected'].items():
            status = "✅" if detected else "❌"
            print(f"  {status} {pattern.replace('_', ' ').title()}")
        
        # Issues
        if report['issues']:
            print(f"\n📝 Detailed Issues:")
            for i, issue in enumerate(report['issues'], 1):
                emoji = {"CRITICAL": "🔴", "ERROR": "🟠", "WARNING": "🟡", "INFO": "🔵"}[issue['level']]
                print(f"\n  {emoji} [{issue['level']}] {issue['issue']}")
                print(f"     💡 Suggestion: {issue['suggestion']}")
        
        # Recommendations
        if report['recommendations']:
            print(f"\n🎯 Optimization Recommendations:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        print("\n" + "=" * 60)
        
        # Pass/Fail
        if self.strict and (s['critical_issues'] > 0 or s['errors'] > 0):
            print("❌ FAILED (strict mode)")
            sys.exit(1)
        elif report['scores'].get('overall', 0) >= 80:
            print("✅ PASSED - Ready for ClawHub")
        elif report['scores'].get('overall', 0) >= 60:
            print("⚠️ PASSED WITH WARNINGS - Consider improvements")
        else:
            print("❌ FAILED - Significant issues found")

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_skill.py /path/to/skill-folder [--strict]")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    strict = '--strict' in sys.argv
    
    analyzer = SkillAnalyzer(skill_path, strict)
    report = analyzer.analyze()
    
    # Save report to JSON
    output_path = Path(skill_path) / ".analysis_report.json"
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n💾 Report saved to: {output_path}")

if __name__ == "__main__":
    main()
