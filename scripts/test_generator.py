#!/usr/bin/env python3
"""
Test Generator - Automatically generate test cases for skills
Usage: python test_generator.py /path/to/skill [--output ./tests]
"""

import os
import sys
import json
import argparse
from pathlib import Path
import re

class TestGenerator:
    def __init__(self, skill_path: str, output_path: str):
        self.skill_path = Path(skill_path)
        self.output_path = Path(output_path)
        self.skill_md = self.skill_path / "SKILL.md"
        
    def read_skill(self):
        """Read and parse skill content"""
        if not self.skill_md.exists():
            return None
        return self.skill_md.read_text(encoding='utf-8')
    
    def extract_triggers(self, content: str):
        """Extract trigger conditions from skill"""
        triggers = []
        
        # Look for "Use when" patterns
        use_when_match = re.search(r'[Uu]se when[:：](.+?)(?=\n\n|\n##|$)', content, re.DOTALL)
        if use_when_match:
            trigger_text = use_when_match.group(1)
            # Extract numbered items
            items = re.findall(r'\((\d+)\)\s*([^\n]+)', trigger_text)
            for num, desc in items:
                triggers.append({
                    "id": f"trigger_{num}",
                    "description": desc.strip(),
                    "test_input": self.generate_test_input(desc.strip())
                })
        
        return triggers
    
    def generate_test_input(self, trigger_desc: str):
        """Generate appropriate test input based on trigger description"""
        # Simple rule-based generation
        desc_lower = trigger_desc.lower()
        
        if 'pdf' in desc_lower:
            return "请处理这个PDF文件：document.pdf"
        elif 'analyze' in desc_lower or '分析' in desc_lower:
            return "分析一下当前的数据情况"
        elif 'convert' in desc_lower or '转换' in desc_lower:
            return "把这份文档转换成PDF格式"
        elif 'review' in desc_lower or '检查' in desc_lower:
            return "帮我检查一下这段代码"
        elif 'generate' in desc_lower or '生成' in desc_lower:
            return "生成一份项目报告"
        else:
            return f"测试输入：{trigger_desc[:20]}..."
    
    def extract_examples(self, content: str):
        """Extract usage examples from skill"""
        examples = []
        
        # Look for example sections
        example_sections = re.findall(r'### Example \d+[:：](.+?)(?=### Example|\n##|$)', content, re.DOTALL)
        
        for i, section in enumerate(example_sections, 1):
            input_match = re.search(r'[Ii]nput[：:](.+?)(?=[Oo]utput|$)', section, re.DOTALL)
            output_match = re.search(r'[Oo]utput[：:](.+?)(?=###|$)', section, re.DOTALL)
            
            if input_match:
                examples.append({
                    "id": f"example_{i}",
                    "input": input_match.group(1).strip(),
                    "expected_output": output_match.group(1).strip() if output_match else "See skill output"
                })
        
        return examples
    
    def generate_test_cases(self, content: str):
        """Generate comprehensive test cases"""
        triggers = self.extract_triggers(content)
        examples = self.extract_examples(content)
        
        test_cases = {
            "skill_name": self.skill_path.name,
            "test_suites": []
        }
        
        # Suite 1: Trigger accuracy tests
        trigger_tests = {
            "suite_name": "Trigger Accuracy",
            "description": "Test if skill triggers correctly for intended use cases",
            "tests": []
        }
        
        for trigger in triggers:
            trigger_tests["tests"].append({
                "id": trigger["id"],
                "name": f"Should trigger for: {trigger['description'][:30]}...",
                "input": trigger["test_input"],
                "expected_behavior": "Skill should trigger and execute",
                "validation": "Check if skill is selected by agent"
            })
        
        # Add negative test cases
        trigger_tests["tests"].append({
            "id": "trigger_negative_1",
            "name": "Should NOT trigger for unrelated input",
            "input": "今天天气怎么样？",
            "expected_behavior": "Skill should NOT trigger",
            "validation": "Check skill is not selected"
        })
        
        test_cases["test_suites"].append(trigger_tests)
        
        # Suite 2: Functionality tests
        if examples:
            func_tests = {
                "suite_name": "Functionality",
                "description": "Test core functionality with example inputs",
                "tests": []
            }
            
            for example in examples:
                func_tests["tests"].append({
                    "id": example["id"],
                    "name": f"Test: {example['input'][:40]}...",
                    "input": example["input"],
                    "expected_output": example["expected_output"],
                    "validation": "Compare actual output with expected"
                })
            
            test_cases["test_suites"].append(func_tests)
        
        # Suite 3: Edge cases
        edge_tests = {
            "suite_name": "Edge Cases",
            "description": "Test edge cases and error handling",
            "tests": [
                {
                    "id": "edge_empty",
                    "name": "Handle empty input",
                    "input": "",
                    "expected_behavior": "Graceful error handling",
                    "validation": "No crash, helpful error message"
                },
                {
                    "id": "edge_large",
                    "name": "Handle large input",
                    "input": "[Very large input - 10000 characters]",
                    "expected_behavior": "Process or reject appropriately",
                    "validation": "Performance or clear limitation message"
                },
                {
                    "id": "edge_unicode",
                    "name": "Handle unicode/special characters",
                    "input": "测试 🎉 émojis ñoño",
                    "expected_behavior": "Process without errors",
                    "validation": "Output preserved or properly escaped"
                }
            ]
        }
        test_cases["test_suites"].append(edge_tests)
        
        return test_cases
    
    def generate_test_runner(self, test_cases: dict):
        """Generate test runner script"""
        runner_script = f'''#!/usr/bin/env python3
"""
Auto-generated test runner for {test_cases['skill_name']}
Generated by Test Generator v3.0
"""

import json
import sys
from pathlib import Path

class SkillTestRunner:
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.results = []
    
    def run_test(self, test: dict):
        """Run a single test"""
        print(f"Running: {{test['name']}}")
        
        # TODO: Implement actual skill execution
        # For now, simulate test
        
        result = {{
            "id": test["id"],
            "name": test["name"],
            "status": "pending",  # pass/fail/pending
            "input": test.get("input", ""),
            "actual_output": None,
            "expected_output": test.get("expected_output") or test.get("expected_behavior"),
            "notes": "Manual verification required"
        }}
        
        return result
    
    def run_all(self, test_cases: dict):
        """Run all test suites"""
        print("="*60)
        print(f"🧪 Testing: {{test_cases['skill_name']}}")
        print("="*60)
        
        for suite in test_cases["test_suites"]:
            print(f"\\n📋 Suite: {{suite['suite_name']}}")
            print(f"   {{suite['description']}}")
            print("-"*40)
            
            for test in suite["tests"]:
                result = self.run_test(test)
                self.results.append(result)
                print(f"   {{result['status'].upper()}}: {{test['name'][:50]}}")
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate test report"""
        passed = sum(1 for r in self.results if r["status"] == "pass")
        failed = sum(1 for r in self.results if r["status"] == "fail")
        pending = sum(1 for r in self.results if r["status"] == "pending")
        
        report = {{
            "skill": "{test_cases['skill_name']}",
            "total_tests": len(self.results),
            "passed": passed,
            "failed": failed,
            "pending": pending,
            "results": self.results
        }}
        
        # Save report
        report_path = Path("test_report.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\\n📊 Summary: {{passed}} passed, {{failed}} failed, {{pending}} pending")
        print(f"💾 Report saved: {{report_path}}")
        
        return report

if __name__ == "__main__":
    # Load test cases
    with open("test_cases.json") as f:
        test_cases = json.load(f)
    
    runner = SkillTestRunner("{self.skill_path}")
    runner.run_all(test_cases)
'''
        return runner_script
    
    def run(self):
        """Run test generator"""
        print(f"🧪 Generating tests for: {self.skill_path.name}")
        
        content = self.read_skill()
        if not content:
            print("❌ SKILL.md not found!")
            return
        
        # Generate test cases
        test_cases = self.generate_test_cases(content)
        
        # Create output directory
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Save test cases
        test_cases_path = self.output_path / "test_cases.json"
        with open(test_cases_path, 'w', encoding='utf-8') as f:
            json.dump(test_cases, f, indent=2, ensure_ascii=False)
        
        # Generate and save test runner
        runner_script = self.generate_test_runner(test_cases)
        runner_path = self.output_path / "test_runner.py"
        with open(runner_path, 'w', encoding='utf-8') as f:
            f.write(runner_script)
        
        # Make executable
        os.chmod(runner_path, 0o755)
        
        print(f"✅ Generated {sum(len(s['tests']) for s in test_cases['test_suites'])} test cases")
        print(f"📁 Test cases: {test_cases_path}")
        print(f"🚀 Test runner: {runner_path}")
        print(f"\\n💡 To run tests:")
        print(f"   cd {self.output_path}")
        print(f"   python test_runner.py")

def main():
    parser = argparse.ArgumentParser(description='Generate test cases for skills')
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('--output', '-o', default='./tests', help='Output folder for tests')
    
    args = parser.parse_args()
    
    generator = TestGenerator(args.skill_path, args.output)
    generator.run()

if __name__ == "__main__":
    main()
