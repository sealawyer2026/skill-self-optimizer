#!/usr/bin/env python3
"""
Auto Tester - Generate and run automated tests for skills
Usage: python auto_tester.py ./my-skill [--generate|--run|--coverage]
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class AutoTester:
    """Generate and run automated tests for skills"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.tests_dir = self.skill_path / "tests"
        self.test_results_dir = self.skill_path / ".test_results"
        
    def _parse_skill_md(self) -> dict:
        """Parse SKILL.md to understand skill functionality"""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return {}
        
        content = skill_md.read_text(encoding='utf-8')
        
        # Extract key sections
        data = {
            "name": self.skill_name,
            "description": "",
            "trigger_conditions": [],
            "examples": [],
            "validation_rules": []
        }
        
        # Extract description
        desc_match = re.search(r'description:\s*"([^"]+)"', content)
        if desc_match:
            data["description"] = desc_match.group(1)
        
        # Extract "When to Use" section
        when_match = re.search(r'##?\s*When to Use\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if when_match:
            triggers = re.findall(r'[-*]\s*(.+)', when_match.group(1))
            data["trigger_conditions"] = [t.strip() for t in triggers if t.strip()]
        
        # Extract examples
        example_matches = re.findall(r'##?\s*Example.*?\n(.*?)(?=##|```\n\n|$)', content, re.DOTALL)
        for ex in example_matches:
            data["examples"].append(ex.strip())
        
        # Extract validation checklist
        checklist_match = re.search(r'##?\s*.*?(?:Checklist|Validation).*?\n(.*?)(?=##|$)', content, re.DOTALL)
        if checklist_match:
            rules = re.findall(r'- \[.\]\s*(.+)', checklist_match.group(1))
            data["validation_rules"] = [r.strip() for r in rules]
        
        return data
    
    def generate_tests(self):
        """Generate test cases from skill content"""
        print("="*60)
        print("🧪 Auto Tester v3.4")
        print("="*60)
        print(f"\n📦 Skill: {self.skill_name}")
        
        skill_data = self._parse_skill_md()
        if not skill_data:
            print("❌ Could not parse SKILL.md")
            return
        
        print(f"📝 Description: {skill_data.get('description', 'N/A')[:60]}...")
        
        # Create tests directory
        self.tests_dir.mkdir(exist_ok=True)
        
        # Generate test files
        tests_generated = []
        
        # 1. Trigger tests
        trigger_tests = self._generate_trigger_tests(skill_data)
        if trigger_tests:
            trigger_file = self.tests_dir / "test_triggers.py"
            trigger_file.write_text(trigger_tests, encoding='utf-8')
            tests_generated.append("test_triggers.py")
        
        # 2. Example tests
        example_tests = self._generate_example_tests(skill_data)
        if example_tests:
            example_file = self.tests_dir / "test_examples.py"
            example_file.write_text(example_tests, encoding='utf-8')
            tests_generated.append("test_examples.py")
        
        # 3. Validation tests
        validation_tests = self._generate_validation_tests(skill_data)
        if validation_tests:
            validation_file = self.tests_dir / "test_validation.py"
            validation_file.write_text(validation_tests, encoding='utf-8')
            tests_generated.append("test_validation.py")
        
        # 4. Structure tests
        structure_tests = self._generate_structure_tests()
        structure_file = self.tests_dir / "test_structure.py"
        structure_file.write_text(structure_tests, encoding='utf-8')
        tests_generated.append("test_structure.py")
        
        # Generate conftest.py
        conftest = self._generate_conftest()
        (self.tests_dir / "conftest.py").write_text(conftest, encoding='utf-8')
        
        # Generate pytest.ini
        pytest_ini = """[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
"""
        (self.skill_path / "pytest.ini").write_text(pytest_ini, encoding='utf-8')
        
        print(f"\n✅ Generated {len(tests_generated)} test files:")
        for f in tests_generated:
            print(f"   • {f}")
        
        print(f"\n🚀 To run tests:")
        print(f"   cd {self.skill_path}")
        print(f"   pip install pytest")
        print(f"   pytest")
    
    def _generate_trigger_tests(self, skill_data: dict) -> str:
        """Generate trigger condition tests"""
        test_cases = []
        
        for i, trigger in enumerate(skill_data.get("trigger_conditions", [])[:5], 1):
            test_cases.append(f"""
    def test_trigger_condition_{i}(self):
        \"\"\"Test: {trigger}\"\"\"
        # TODO: Implement test for trigger condition
        # trigger_input = "{trigger}"
        # result = self.skill.should_trigger(trigger_input)
        # assert result is True
        pass
""")
        
        if not test_cases:
            return None
        
        return f"""#!/usr/bin/env python3
\"\"\"
Trigger Tests for {self.skill_name}
Auto-generated on {datetime.now().strftime('%Y-%m-%d')}
\"\"\"

import pytest

class TestTriggers:
    \"\"\"Test trigger conditions\"\"\"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        \"\"\"Setup test fixtures\"\"\"
        # TODO: Initialize skill
        self.skill = None
    {''.join(test_cases)}
    
    def test_no_false_positives(self):
        \"\"\"Test that skill doesn't trigger on unrelated input\"\"\"
        # TODO: Test negative cases
        # unrelated_input = "completely unrelated query"
        # result = self.skill.should_trigger(unrelated_input)
        # assert result is False
        pass
"""
    
    def _generate_example_tests(self, skill_data: dict) -> str:
        """Generate example-based tests"""
        test_cases = []
        
        for i, example in enumerate(skill_data.get("examples", [])[:3], 1):
            # Extract input/output from example
            test_cases.append(f"""
    def test_example_{i}(self):
        \"\"\"Test example {i}\"\"\"
        # Example content:
        # {example[:100].replace(chr(10), chr(10)+'        # ')}
        
        # TODO: Extract input/output and test
        pass
""")
        
        if not test_cases:
            return None
        
        return f"""#!/usr/bin/env python3
\"\"\"
Example Tests for {self.skill_name}
Auto-generated on {datetime.now().strftime('%Y-%m-%d')}
\"\"\"

import pytest

class TestExamples:
    \"\"\"Test documented examples\"\"\"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        \"\"\"Setup test fixtures\"\"\"
        self.skill = None
    {''.join(test_cases)}
"""
    
    def _generate_validation_tests(self, skill_data: dict) -> str:
        """Generate validation rule tests"""
        test_cases = []
        
        for i, rule in enumerate(skill_data.get("validation_rules", [])[:5], 1):
            test_cases.append(f"""
    def test_validation_rule_{i}(self):
        \"\"\"Test: {rule}\"\"\"
        # TODO: Implement validation test
        pass
""")
        
        return f"""#!/usr/bin/env python3
\"\"\"
Validation Tests for {self.skill_name}
Auto-generated on {datetime.now().strftime('%Y-%m-%d')}
\"\"\"

import pytest

class TestValidation:
    \"\"\"Test validation rules\"\"\"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        \"\"\"Setup test fixtures\"\"\"
        self.skill = None
    {''.join(test_cases) if test_cases else '''
    def test_placeholder(self):
        \"\"\"Placeholder test - add validation tests here\"\"\"
        pass
'''}
"""
    
    def _generate_structure_tests(self) -> str:
        """Generate structure validation tests"""
        return f"""#!/usr/bin/env python3
\"\"\"
Structure Tests for {self.skill_name}
Auto-generated on {datetime.now().strftime('%Y-%m-%d')}
\"\"\"

import pytest
from pathlib import Path

class TestStructure:
    \"\"\"Test skill structure and files\"\"\"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        \"\"\"Setup test fixtures\"\"\"
        self.skill_path = Path(__file__).parent.parent
    
    def test_skill_md_exists(self):
        \"\"\"SKILL.md must exist\"\"\"
        assert (self.skill_path / "SKILL.md").exists()
    
    def test_skill_md_not_empty(self):
        \"\"\"SKILL.md must not be empty\"\"\"
        skill_md = self.skill_path / "SKILL.md"
        assert skill_md.exists()
        content = skill_md.read_text()
        assert len(content) > 100
    
    def test_skill_md_has_frontmatter(self):
        \"\"\"SKILL.md should have YAML frontmatter\"\"\"
        skill_md = self.skill_path / "SKILL.md"
        content = skill_md.read_text()
        assert content.startswith("---")
    
    def test_skill_md_has_name(self):
        \"\"\"SKILL.md should have name field\"\"\"
        skill_md = self.skill_path / "SKILL.md"
        content = skill_md.read_text()
        assert "name:" in content
    
    def test_skill_md_has_description(self):
        \"\"\"SKILL.md should have description\"\"\"
        skill_md = self.skill_path / "SKILL.md"
        content = skill_md.read_text()
        assert "description:" in content
    
    def test_skill_size_reasonable(self):
        \"\"\"SKILL.md should be under 500KB\"\"\"
        skill_md = self.skill_path / "SKILL.md"
        if skill_md.exists():
            size = skill_md.stat().st_size
            assert size < 500 * 1024, f"SKILL.md is {{size / 1024:.1f}}KB, should be <500KB"
    
    def test_no_auxiliary_files_in_root(self):
        \"\"\"Root should only contain SKILL.md and allowed files\"\"\"
        allowed = {{"SKILL.md", "tests", "scripts", "assets", "references", ".git", 
                    "pytest.ini", "README.md", ".feedback", ".test_results"}}
        for item in self.skill_path.iterdir():
            if item.is_file():
                assert item.name in allowed or item.name.startswith("."), f"Unexpected file: {{item.name}}"
"""
    
    def _generate_conftest(self) -> str:
        """Generate conftest.py"""
        return """# pytest configuration
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Add scripts directory if exists
scripts_dir = Path(__file__).parent.parent / "scripts"
if scripts_dir.exists():
    sys.path.insert(0, str(scripts_dir))
"""
    
    def run_tests(self):
        """Run the test suite"""
        import subprocess
        
        print("="*60)
        print("🧪 Running Tests")
        print("="*60)
        
        # Check if pytest is installed
        result = subprocess.run(["python", "-m", "pytest", "--version"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ pytest not installed. Installing...")
            subprocess.run(["pip", "install", "pytest", "-q"])
        
        # Run tests
        print(f"\n📂 Running tests in {self.skill_path}...")
        result = subprocess.run(
            ["python", "-m", "pytest", str(self.tests_dir), "-v", "--tb=short"],
            cwd=self.skill_path,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        # Save results
        self.test_results_dir.mkdir(exist_ok=True)
        results_file = self.test_results_dir / f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        results_file.write_text(result.stdout + "\n" + result.stderr, encoding='utf-8')
        
        print(f"\n📄 Results saved: {results_file}")
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Tests failed (exit code: {result.returncode})")
    
    def generate_coverage_report(self):
        """Generate test coverage report"""
        print("="*60)
        print("📊 Coverage Report")
        print("="*60)
        
        skill_data = self._parse_skill_md()
        
        # Calculate coverage metrics
        metrics = {
            "trigger_conditions": len(skill_data.get("trigger_conditions", [])),
            "examples": len(skill_data.get("examples", [])),
            "validation_rules": len(skill_data.get("validation_rules", [])),
            "has_tests": self.tests_dir.exists() and any(self.tests_dir.glob("test_*.py")),
            "test_files": len(list(self.tests_dir.glob("test_*.py"))) if self.tests_dir.exists() else 0
        }
        
        report = f"""# Test Coverage Report

**Skill:** {self.skill_name}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Coverage Metrics

| Aspect | Count | Has Tests | Coverage |
|--------|-------|-----------|----------|
| Trigger Conditions | {metrics['trigger_conditions']} | {'✅' if metrics['has_tests'] else '❌'} | {'Partial' if metrics['has_tests'] else 'None'} |
| Examples | {metrics['examples']} | {'✅' if metrics['has_tests'] else '❌'} | {'Partial' if metrics['has_tests'] else 'None'} |
| Validation Rules | {metrics['validation_rules']} | {'✅' if metrics['has_tests'] else '❌'} | {'Partial' if metrics['has_tests'] else 'None'} |
| Structure | N/A | {'✅' if metrics['test_files'] >= 1 else '❌'} | {'Yes' if metrics['test_files'] >= 1 else 'No'} |

## Test Files

{metrics['test_files']} test file(s) generated

## Recommendations

"""
        
        if not metrics['has_tests']:
            report += "- 🚨 **Critical:** No tests found. Run `python auto_tester.py --generate` first.\n"
        else:
            report += "- ✅ Tests exist. Run `pytest` to execute.\n"
        
        if metrics['trigger_conditions'] == 0:
            report += "- ⚠️ No trigger conditions documented in SKILL.md\n"
        
        if metrics['examples'] == 0:
            report += "- ⚠️ No examples documented in SKILL.md\n"
        
        report_path = self.skill_path / ".test_coverage.md"
        report_path.write_text(report, encoding='utf-8')
        
        print(f"📄 Coverage report: {report_path}")
        print(f"\n📊 Summary:")
        print(f"   Trigger conditions: {metrics['trigger_conditions']}")
        print(f"   Examples: {metrics['examples']}")
        print(f"   Validation rules: {metrics['validation_rules']}")
        print(f"   Test files: {metrics['test_files']}")

def main():
    parser = argparse.ArgumentParser(description='Auto Tester')
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('--generate', '-g', action='store_true', help='Generate tests')
    parser.add_argument('--run', '-r', action='store_true', help='Run tests')
    parser.add_argument('--coverage', '-c', action='store_true', help='Generate coverage report')
    
    args = parser.parse_args()
    
    tester = AutoTester(args.skill_path)
    
    if args.generate:
        tester.generate_tests()
    elif args.run:
        tester.run_tests()
    elif args.coverage:
        tester.generate_coverage_report()
    else:
        # Default: generate tests
        tester.generate_tests()

if __name__ == "__main__":
    main()
