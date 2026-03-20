#!/usr/bin/env python3
"""
Batch Optimizer - Optimize multiple skills at once
Usage: python batch_optimize.py /path/to/skills-folder [--parallel] [--output ./optimized]
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

class BatchOptimizer:
    def __init__(self, skills_folder: str, output_folder: str, parallel: bool = True):
        self.skills_folder = Path(skills_folder)
        self.output_folder = Path(output_folder)
        self.parallel = parallel
        self.results = []
        
    def scan_skills(self):
        """Scan all skills in folder"""
        skills = []
        for item in self.skills_folder.iterdir():
            if item.is_dir() and (item / 'SKILL.md').exists():
                skills.append(item)
        return skills
    
    def optimize_single(self, skill_path: Path):
        """Optimize a single skill"""
        skill_name = skill_path.name
        output_path = self.output_folder / f"{skill_name}-optimized"
        
        print(f"🚀 Optimizing: {skill_name}")
        
        auto_optimize_script = Path(__file__).parent / 'auto_optimize.py'
        result = subprocess.run(
            [sys.executable, str(auto_optimize_script), str(skill_path), '--output', str(output_path)],
            capture_output=True,
            text=True
        )
        
        success = result.returncode == 0
        
        # Parse summary if available
        summary_path = output_path / '.optimization_summary.json'
        improvement = 0
        if summary_path.exists():
            with open(summary_path) as f:
                summary = json.load(f)
                improvement = summary.get('improvement', 0)
        
        return {
            'skill': skill_name,
            'success': success,
            'improvement': improvement,
            'output': str(output_path)
        }
    
    def run_sequential(self, skills):
        """Run optimizations sequentially"""
        results = []
        for skill in skills:
            result = self.optimize_single(skill)
            results.append(result)
        return results
    
    def run_parallel(self, skills):
        """Run optimizations in parallel"""
        results = []
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(self.optimize_single, skill): skill for skill in skills}
            
            for future in as_completed(futures):
                skill = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        'skill': skill.name,
                        'success': False,
                        'error': str(e)
                    })
        return results
    
    def generate_report(self):
        """Generate batch optimization report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total': len(self.results),
            'successful': sum(1 for r in self.results if r.get('success')),
            'failed': sum(1 for r in self.results if not r.get('success')),
            'average_improvement': sum(r.get('improvement', 0) for r in self.results) / len(self.results) if self.results else 0,
            'details': self.results
        }
        
        report_path = self.output_folder / 'batch_optimization_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate HTML report
        self.generate_html_report(report)
        
        return report
    
    def generate_html_report(self, report):
        """Generate HTML report"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Batch Optimization Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .metric {{ display: inline-block; margin: 10px 20px; }}
        .metric-value {{ font-size: 32px; font-weight: bold; color: #2ecc71; }}
        .metric-label {{ font-size: 14px; color: #666; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #333; color: white; }}
        .success {{ color: #2ecc71; }}
        .failed {{ color: #e74c3c; }}
    </style>
</head>
<body>
    <h1>📊 Batch Optimization Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="summary">
        <div class="metric">
            <div class="metric-value">{report['total']}</div>
            <div class="metric-label">Total Skills</div>
        </div>
        <div class="metric">
            <div class="metric-value">{report['successful']}</div>
            <div class="metric-label">Successful</div>
        </div>
        <div class="metric">
            <div class="metric-value">{report['failed']}</div>
            <div class="metric-label">Failed</div>
        </div>
        <div class="metric">
            <div class="metric-value">{report['average_improvement']:.1f}</div>
            <div class="metric-label">Avg Improvement</div>
        </div>
    </div>
    
    <table>
        <tr>
            <th>Skill</th>
            <th>Status</th>
            <th>Improvement</th>
            <th>Output Path</th>
        </tr>
"""
        
        for detail in report['details']:
            status_class = 'success' if detail['success'] else 'failed'
            status_text = '✅ Success' if detail['success'] else '❌ Failed'
            html += f"""
        <tr>
            <td>{detail['skill']}</td>
            <td class="{status_class}">{status_text}</td>
            <td>{detail.get('improvement', 'N/A'):+.1f}</td>
            <td>{detail.get('output', 'N/A')}</td>
        </tr>
"""
        
        html += """
    </table>
</body>
</html>
"""
        
        html_path = self.output_folder / 'batch_optimization_report.html'
        with open(html_path, 'w') as f:
            f.write(html)
    
    def run(self):
        """Run batch optimization"""
        print("="*60)
        print("🚀 BATCH SKILL OPTIMIZER")
        print("="*60)
        print(f"\n📁 Source: {self.skills_folder}")
        print(f"📁 Output: {self.output_folder}")
        print(f"⚡ Mode: {'Parallel' if self.parallel else 'Sequential'}\n")
        
        # Create output folder
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # Scan skills
        skills = self.scan_skills()
        print(f"Found {len(skills)} skill(s) to optimize\n")
        
        if not skills:
            print("❌ No skills found!")
            return
        
        # Run optimization
        if self.parallel and len(skills) > 1:
            print("Running in parallel mode (4 workers)...\n")
            self.results = self.run_parallel(skills)
        else:
            print("Running in sequential mode...\n")
            self.results = self.run_sequential(skills)
        
        # Generate report
        print("\n" + "="*60)
        print("📊 Generating Report...")
        report = self.generate_report()
        
        print("\n✅ Batch Optimization Complete!")
        print(f"   Total: {report['total']}")
        print(f"   Successful: {report['successful']}")
        print(f"   Failed: {report['failed']}")
        print(f"   Avg Improvement: {report['average_improvement']:.1f} points")
        print(f"\n📄 Reports saved:")
        print(f"   JSON: {self.output_folder}/batch_optimization_report.json")
        print(f"   HTML: {self.output_folder}/batch_optimization_report.html")

def main():
    parser = argparse.ArgumentParser(description='Batch optimize multiple Skills')
    parser.add_argument('skills_folder', help='Path to skills folder')
    parser.add_argument('--output', '-o', default='./optimized-batch', 
                        help='Output folder')
    parser.add_argument('--parallel', '-p', action='store_true', 
                        help='Run optimizations in parallel')
    parser.add_argument('--sequential', '-s', action='store_true', 
                        help='Run optimizations sequentially')
    
    args = parser.parse_args()
    
    parallel = args.parallel and not args.sequential
    
    optimizer = BatchOptimizer(args.skills_folder, args.output, parallel)
    optimizer.run()

if __name__ == "__main__":
    main()
