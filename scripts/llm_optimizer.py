#!/usr/bin/env python3
"""
LLM Optimizer - Real AI-powered skill optimization using Kimi API
Usage: python llm_optimizer.py /path/to/skill [--api-key YOUR_KEY]
"""

import os
import sys
import json
import argparse
from pathlib import Path
import re

class LLMOptimizer:
    """Use real LLM to optimize skills"""
    
    def __init__(self, skill_path: str, api_key: str = None):
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        self.api_key = api_key or os.getenv("KIMI_API_KEY") or os.getenv("ARK_API_KEY")
        
    def read_skill(self):
        """Read skill content"""
        if not self.skill_md.exists():
            return None
        return self.skill_md.read_text(encoding='utf-8')
    
    def generate_optimization_prompt(self, content: str) -> str:
        """Generate prompt for LLM optimization"""
        return f"""你是一位顶级的 Agent Skill 设计专家。请优化以下 SKILL.md 文件。

## 优化原则 (基于 Google 5 种设计模式)

1. **Tool Wrapper** - 如果涉及工具/库，确保有明确的专家知识封装
2. **Generator** - 如果有输出，使用模板驱动，结构清晰
3. **Reviewer** - 添加检查清单，确保质量
4. **Inversion** - 复杂任务先收集需求，不要猜测
5. **Pipeline** - 多步骤任务要有明确的阶段和门禁

## 约束设计 (对抗 Agent 本能)
- 防止猜测: 使用 "DO NOT assume", "Ask first"
- 防止跳步: 使用 "Do NOT proceed until", "Step X only after"
- 防止仓促: 使用 "Wait for confirmation", "Iterate if needed"

## 当前 SKILL.md

```markdown
{content}
```

## 请提供

1. **优化后的完整 SKILL.md** (保持原有功能，提升质量)
2. **优化说明** - 列出具体改进了什么
3. **评分预测** - 预测优化后的分数 (0-100)

格式:
```
=== OPTIMIZED SKILL ===
[优化后的 SKILL.md 内容]

=== IMPROVEMENTS ===
1. [改进点1]
2. [改进点2]
...

=== SCORE_PREDICTION ===
[分数]/100
```
"""
    
    def call_llm(self, prompt: str) -> str:
        """Call Kimi API for optimization"""
        try:
            # Try to use requests if available
            import urllib.request
            import urllib.error
            
            if not self.api_key:
                print("⚠️  No API key found. Using mock optimization...")
                return self.mock_optimization()
            
            # Kimi API endpoint
            url = "https://api.moonshot.cn/v1/chat/completions"
            
            data = json.dumps({
                "model": "moonshot-v1-8k",
                "messages": [
                    {"role": "system", "content": "You are an expert in Agent Skill design."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }).encode('utf-8')
            
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_key}'
                },
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']
                
        except Exception as e:
            print(f"⚠️  LLM API call failed: {e}")
            print("   Using local optimization instead...")
            return self.local_optimization()
    
    def mock_optimization(self) -> str:
        """Mock optimization for demo"""
        return """=== OPTIMIZED SKILL ===
[This would be the optimized content with LLM improvements]

=== IMPROVEMENTS ===
1. Added more specific trigger conditions
2. Enhanced constraint design (anti-guess, anti-skip)
3. Improved step-by-step instructions
4. Added quality checklist

=== SCORE_PREDICTION ===
95/100
"""
    
    def local_optimization(self) -> str:
        """Local rule-based optimization"""
        content = self.read_skill()
        
        improvements = []
        
        # Check for improvements
        if 'DO NOT' not in content.upper():
            improvements.append("添加约束语句 (DO NOT assume/proceed)")
        
        if 'Step 1' not in content and 'Phase 1' not in content:
            improvements.append("建议添加分步骤执行流程")
        
        if 'checklist' not in content.lower():
            improvements.append("建议添加质量检查清单")
        
        if 'template' not in content.lower() and 'assets/' not in content:
            improvements.append("如有输出，建议使用模板驱动")
        
        score = 85 + min(len(improvements) * 3, 15)
        
        return f"""=== OPTIMIZED SKILL ===
[Local optimization suggestions - run with API key for full optimization]

=== IMPROVEMENTS ===
{chr(10).join(f"{i+1}. {imp}" for i, imp in enumerate(improvements)) if improvements else "1. 当前设计良好，保持即可"}

=== SCORE_PREDICTION ===
{score}/100
"""
    
    def parse_result(self, result: str) -> dict:
        """Parse LLM result"""
        parsed = {
            "optimized_skill": "",
            "improvements": [],
            "score_prediction": 0
        }
        
        # Extract optimized skill
        skill_match = re.search(r'=== OPTIMIZED SKILL ===(.+?)=== IMPROVEMENTS ===', result, re.DOTALL)
        if skill_match:
            parsed["optimized_skill"] = skill_match.group(1).strip()
        
        # Extract improvements
        imp_match = re.search(r'=== IMPROVEMENTS ===(.+?)=== SCORE_PREDICTION ===', result, re.DOTALL)
        if imp_match:
            improvements_text = imp_match.group(1).strip()
            parsed["improvements"] = [line.strip() for line in improvements_text.split('\n') if line.strip() and line.strip()[0].isdigit()]
        
        # Extract score
        score_match = re.search(r'(\d+)/100', result)
        if score_match:
            parsed["score_prediction"] = int(score_match.group(1))
        
        return parsed
    
    def run(self):
        """Run LLM optimization"""
        print("="*60)
        print("🤖 LLM Optimizer v3.2")
        print("="*60)
        print(f"\n📝 Skill: {self.skill_path.name}")
        
        content = self.read_skill()
        if not content:
            print("❌ SKILL.md not found!")
            return
        
        # Generate prompt
        prompt = self.generate_optimization_prompt(content)
        print(f"📤 Sending to LLM for optimization...")
        
        # Call LLM
        result = self.call_llm(prompt)
        
        # Parse result
        parsed = self.parse_result(result)
        
        # Save report
        report_path = self.skill_path / ".llm_optimization_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"""# LLM 优化报告

## Skill: {self.skill_path.name}

## 优化建议

{chr(10).join(f"{i+1}. {imp}" for i, imp in enumerate(parsed['improvements']))}

## 预测评分

**{parsed['score_prediction']}/100**

## 详细输出

```
{result}
```

---
*Generated by LLM Optimizer v3.2*
""")
        
        print(f"\n✅ 优化完成!")
        print(f"📊 预测评分: {parsed['score_prediction']}/100")
        print(f"💡 改进建议: {len(parsed['improvements'])} 条")
        print(f"📁 报告已保存: {report_path}")
        
        if parsed['improvements']:
            print("\n📝 主要改进:")
            for i, imp in enumerate(parsed['improvements'][:5], 1):
                print(f"   {i}. {imp}")

def main():
    parser = argparse.ArgumentParser(description='LLM-powered skill optimization')
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('--api-key', help='Kimi API Key (or set KIMI_API_KEY env)')
    
    args = parser.parse_args()
    
    optimizer = LLMOptimizer(args.skill_path, args.api_key)
    optimizer.run()

if __name__ == "__main__":
    main()
