#!/usr/bin/env python3
"""
One-Click Skill Optimizer - Analyze and optimize in one command
Usage: python auto_optimize.py /path/to/skill [--output ./optimized]
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

def print_header(text):
    print("\n" + "="*60)
    print(f"🚀 {text}")
    print("="*60)

def print_step(step_num, total, text):
    print(f"\n📍 Step {step_num}/{total}: {text}")

def run_analysis(skill_path):
    """Run analysis script"""
    script_dir = Path(__file__).parent
    analyze_script = script_dir / "analyze_skill.py"
    
    result = subprocess.run(
        [sys.executable, str(analyze_script), skill_path],
        capture_output=True,
        text=True
    )
    
    # Parse report
    report_path = Path(skill_path) / ".analysis_report.json"
    if report_path.exists():
        with open(report_path) as f:
            return json.load(f)
    return None

def run_optimization(skill_path, output_path, issues, patterns):
    """Run optimization script"""
    script_dir = Path(__file__).parent
    optimize_script = script_dir / "optimize_skill.py"
    
    cmd = [
        sys.executable, str(optimize_script),
        skill_path,
        "--output", output_path
    ]
    
    if issues:
        cmd.extend(["--issues", ",".join(issues)])
    if patterns:
        cmd.extend(["--patterns", ",".join(patterns)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def suggest_patterns(report):
    """Suggest patterns based on analysis"""
    suggestions = []
    patterns = report.get('patterns_detected', {})
    
    if not patterns.get('generator'):
        suggestions.append('generator')
    if not patterns.get('reviewer'):
        suggestions.append('reviewer')
    if not patterns.get('inversion'):
        suggestions.append('inversion')
    if not patterns.get('orchestrator'):
        suggestions.append('orchestrator')
    
    return suggestions[:3]  # Top 3

def suggest_issues(report):
    """Suggest issues to fix based on analysis"""
    issues = []
    for issue in report.get('issues', []):
        issue_type = issue['issue'].lower()
        if 'too long' in issue_type:
            issues.append('too-long')
        elif 'trigger' in issue_type:
            issues.append('ambiguous-triggering')
        elif 'example' in issue_type:
            issues.append('missing-examples')
        elif 'disclosure' in issue_type:
            issues.append('no-progressive-disclosure')
    return issues

def generate_comparison(original_path, optimized_path):
    """Generate before/after comparison"""
    print("\n📊 Before/After Comparison:")
    print("-" * 50)
    
    # File sizes
    original_size = sum(f.stat().st_size for f in Path(original_path).rglob('*') if f.is_file())
    optimized_size = sum(f.stat().st_size for f in Path(optimized_path).rglob('*') if f.is_file())
    
    print(f"\n📁 Size:")
    print(f"   Original:  {original_size/1024:.1f} KB")
    print(f"   Optimized: {optimized_size/1024:.1f} KB")
    print(f"   Change:    {(optimized_size-original_size)/1024:+.1f} KB")
    
    # Line counts
    original_md = Path(original_path) / "SKILL.md"
    optimized_md = Path(optimized_path) / "SKILL.md"
    
    if original_md.exists() and optimized_md.exists():
        original_lines = len(original_md.read_text().split('\n'))
        optimized_lines = len(optimized_md.read_text().split('\n'))
        
        print(f"\n📝 SKILL.md Lines:")
        print(f"   Original:  {original_lines}")
        print(f"   Optimized: {optimized_lines}")
        print(f"   Change:    {optimized_lines-original_lines:+d}")
    
    print("-" * 50)

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_optimize.py /path/to/skill [--output ./optimized]")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    output_path = sys.argv[sys.argv.index('--output') + 1] if '--output' in sys.argv else f"{skill_path}-optimized"
    
    print_header("AUTO SKILL OPTIMIZER")
    print(f"\n🎯 Target: {skill_path}")
    print(f"📁 Output: {output_path}")
    
    # Step 1: Analysis
    print_step(1, 4, "Analyzing Skill...")
    report = run_analysis(skill_path)
    
    if not report:
        print("❌ Analysis failed")
        sys.exit(1)
    
    score = report.get('scores', {}).get('overall', 0)
    print(f"   Initial Score: {score:.0f}/100")
    
    # Check if already optimal
    if score >= 90:
        print(f"\n✅ Skill already optimal ({score:.0f}/100). No optimization needed.")
        sys.exit(0)
    
    # Step 2: Diagnosis
    print_step(2, 4, "Diagnosing Issues...")
    
    issues = suggest_issues(report)
    patterns = suggest_patterns(report)
    
    if issues:
        print(f"   Issues to fix: {', '.join(issues)}")
    else:
        print("   No critical issues found")
    
    if patterns:
        print(f"   Patterns to add: {', '.join(patterns)}")
    else:
        print("   All patterns already present ✓")
    
    # Step 3: Optimization
    print_step(3, 4, "Running Optimization...")
    
    if not issues and not patterns:
        print("   Nothing to optimize. Exiting.")
        sys.exit(0)
    
    success = run_optimization(skill_path, output_path, issues, patterns)
    
    if not success:
        print("❌ Optimization failed")
        sys.exit(1)
    
    print("   ✓ Optimization complete")
    
    # Step 4: Validation
    print_step(4, 4, "Validating Results...")
    
    new_report = run_analysis(output_path)
    new_score = new_report.get('scores', {}).get('overall', 0) if new_report else 0
    
    print(f"   New Score: {new_score:.0f}/100")
    print(f"   Improvement: {new_score - score:+.0f} points")
    
    # Generate comparison
    generate_comparison(skill_path, output_path)
    
    # Summary
    print_header("OPTIMIZATION COMPLETE")
    
    print(f"""
📈 Results Summary:
   • Original Score:  {score:.0f}/100
   • Optimized Score: {new_score:.0f}/100
   • Improvement:     {new_score - score:+.0f} points

📁 Output Location:
   {output_path}

📝 Next Steps:
   1. Review optimized SKILL.md
   2. Test on real tasks
   3. Compare before/after performance
   4. Iterate if needed

💾 Optimization Log:
   {output_path}/.optimization_log.md
""")
    
    # Create summary file
    summary = {
        "timestamp": datetime.now().isoformat(),
        "original_path": skill_path,
        "optimized_path": output_path,
        "original_score": score,
        "optimized_score": new_score,
        "improvement": new_score - score,
        "issues_fixed": issues,
        "patterns_added": patterns
    }
    
    summary_path = Path(output_path) / ".optimization_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"   Summary saved: {summary_path}")

if __name__ == "__main__":
    main()
