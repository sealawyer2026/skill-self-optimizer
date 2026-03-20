#!/usr/bin/env python3
"""
Pattern Decision Tree - Interactive tool to choose the right design pattern
Usage: python pattern_decision_tree.py [--skill /path/to/skill]
"""

import argparse
from pathlib import Path

class PatternDecisionTree:
    """Interactive decision tree for pattern selection"""
    
    PATTERNS = {
        "tool_wrapper": {
            "name": "Tool Wrapper",
            "description": "让Agent秒变专家",
            "best_for": "封装特定领域知识、编码规范、最佳实践",
            "example": "FastAPI专家、Python代码规范检查器"
        },
        "generator": {
            "name": "Generator",
            "description": "模板驱动生成",
            "best_for": "需要固定格式输出的场景",
            "example": "技术报告生成器、API文档生成"
        },
        "reviewer": {
            "name": "Reviewer",
            "description": "模块化检查清单",
            "best_for": "代码审查、安全检查、质量保证",
            "example": "Python代码审查、OWASP安全检查"
        },
        "inversion": {
            "name": "Inversion",
            "description": "先问再做",
            "best_for": "需求复杂、容易理解错的场景",
            "example": "项目规划器、需求收集助手"
        },
        "pipeline": {
            "name": "Pipeline",
            "description": "严格流水线",
            "best_for": "多步骤任务、不能跳步的场景",
            "example": "API文档生成流水线、部署流程"
        }
    }
    
    COMBINATIONS = {
        "pipeline_reviewer": {
            "name": "Pipeline + Reviewer",
            "description": "多步骤工作流 + 质量门禁",
            "best_for": "复杂多步骤任务，每步需要验证"
        },
        "generator_inversion": {
            "name": "Generator + Inversion", 
            "description": "模板生成 + 需求收集",
            "best_for": "输出格式固定但需求不清晰"
        },
        "tool_wrapper_reviewer": {
            "name": "Tool Wrapper + Reviewer",
            "description": "专家知识 + 质量验证",
            "best_for": "专业领域知识需要验证"
        },
        "full_stack": {
            "name": "完整组合",
            "description": "Pipeline + Inversion + Generator + Reviewer",
            "best_for": "复杂项目，需要全流程控制"
        }
    }
    
    def __init__(self, skill_path: str = None):
        self.skill_path = Path(skill_path) if skill_path else None
        self.answers = {}
    
    def ask(self, question: str, options: list) -> str:
        """Ask a question and get answer"""
        print(f"\n❓ {question}")
        for i, opt in enumerate(options, 1):
            print(f"   {i}. {opt}")
        
        while True:
            try:
                choice = input("\n选择 (1-{}): ".format(len(options)))
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return options[idx]
            except (ValueError, IndexError):
                pass
            print("请输入有效的选项数字")
    
    def yes_no(self, question: str) -> bool:
        """Yes/No question"""
        print(f"\n❓ {question} (y/n)")
        while True:
            answer = input().lower().strip()
            if answer in ['y', 'yes', '是']:
                return True
            elif answer in ['n', 'no', '否']:
                return False
            print("请输入 y 或 n")
    
    def run_interactive(self):
        """Run interactive decision tree"""
        print("=" * 60)
        print("🎯 Google 5种设计模式 - 决策树")
        print("=" * 60)
        print("\n回答几个问题，帮你选择最合适的设计模式...")
        
        # Question 1
        if self.yes_no("你的Skill主要是让Agent掌握某个特定库/工具的知识吗？"):
            pattern = "tool_wrapper"
            if self.yes_no("需要验证输出是否符合最佳实践吗？"):
                return self.recommend_combination("tool_wrapper_reviewer")
            return self.recommend_pattern(pattern)
        
        # Question 2
        if self.yes_no("你的Skill需要输出固定格式的内容吗？（如报告、文档）"):
            pattern = "generator"
            if self.yes_no("用户可能不清楚需要提供什么信息吗？"):
                return self.recommend_combination("generator_inversion")
            return self.recommend_pattern(pattern)
        
        # Question 3
        if self.yes_no("你的Skill主要是检查、审查、验证吗？"):
            return self.recommend_pattern("reviewer")
        
        # Question 4
        if self.yes_no("任务需求复杂，Agent容易理解错吗？"):
            pattern = "inversion"
            if self.yes_no("需要多步骤执行吗？"):
                return self.recommend_combination("full_stack")
            return self.recommend_pattern(pattern)
        
        # Question 5
        if self.yes_no("任务是分步骤的，不能跳过任何一步吗？"):
            pattern = "pipeline"
            if self.yes_no("每个步骤后需要质量检查吗？"):
                return self.recommend_combination("pipeline_reviewer")
            return self.recommend_pattern(pattern)
        
        # Default
        print("\n🤔 根据你的回答，建议使用组合模式...")
        return self.recommend_combination("full_stack")
    
    def recommend_pattern(self, pattern_key: str):
        """Recommend a single pattern"""
        p = self.PATTERNS[pattern_key]
        print("\n" + "=" * 60)
        print(f"🎯 推荐模式: {p['name']}")
        print("=" * 60)
        print(f"\n📌 {p['description']}")
        print(f"\n✨ 最适合: {p['best_for']}")
        print(f"\n💡 示例: {p['example']}")
        print(f"\n📖 详细文档: references/design-patterns.md")
        
        print("\n🚀 快速开始:")
        print(f"   python scripts/optimize_skill.py ./your-skill \\")
        print(f"     --patterns {pattern_key} \\")
        print(f"     --output ./your-skill-optimized")
        
        return pattern_key
    
    def recommend_combination(self, combo_key: str):
        """Recommend a pattern combination"""
        c = self.COMBINATIONS[combo_key]
        print("\n" + "=" * 60)
        print(f"🎯 推荐组合: {c['name']}")
        print("=" * 60)
        print(f"\n📌 {c['description']}")
        print(f"\n✨ 最适合: {c['best_for']}")
        
        print("\n🚀 快速开始:")
        print(f"   python scripts/pattern_combiner.py ./your-skill")
        print(f"   # 查看详细的组合建议报告")
        
        return combo_key
    
    def analyze_skill(self, skill_path: Path):
        """Analyze existing skill and suggest improvements"""
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            print("❌ SKILL.md not found!")
            return
        
        content = skill_md.read_text(encoding='utf-8').lower()
        
        print("\n" + "=" * 60)
        print(f"🔍 分析Skill: {skill_path.name}")
        print("=" * 60)
        
        # Detect current characteristics
        characteristics = []
        
        if 'expert' in content or 'convention' in content or 'best practice' in content:
            characteristics.append("包含专业知识/规范")
        if 'template' in content or 'generate' in content:
            characteristics.append("涉及内容生成")
        if 'check' in content or 'review' in content or 'verify' in content:
            characteristics.append("包含检查/验证逻辑")
        if 'step' in content:
            characteristics.append("有多步骤流程")
        if 'ask' in content or 'question' in content:
            characteristics.append("需要询问用户")
        
        print("\n📊 检测到的特征:")
        for c in characteristics:
            print(f"   • {c}")
        
        # Suggest patterns
        print("\n💡 建议:")
        if 'expert' in content and 'check' not in content:
            print("   • 建议添加 Reviewer 模式进行质量验证")
        if 'step' in content and 'verify' not in content:
            print("   • 建议添加 Reviewer 模式作为步骤间质量门禁")
        if 'generate' in content and 'ask' not in content:
            print("   • 建议添加 Inversion 模式先收集需求")
        
        print(f"\n🚀 运行完整分析:")
        print(f"   python scripts/pattern_combiner.py {skill_path}")

def main():
    parser = argparse.ArgumentParser(description='Pattern selection decision tree')
    parser.add_argument('--skill', '-s', help='Path to skill folder to analyze')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run interactive mode')
    
    args = parser.parse_args()
    
    tree = PatternDecisionTree(args.skill)
    
    if args.interactive or not args.skill:
        tree.run_interactive()
    else:
        tree.analyze_skill(Path(args.skill))

if __name__ == "__main__":
    main()
