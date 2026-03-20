#!/usr/bin/env python3
"""
Performance Profiler - Analyze skill execution performance
Usage: python performance_profiler.py /path/to/skill [--iterations 10]
"""

import os
import sys
import time
import json
import argparse
import statistics
from pathlib import Path
from datetime import datetime

class PerformanceProfiler:
    """Profile skill performance"""
    
    def __init__(self, skill_path: str, iterations: int = 10):
        self.skill_path = Path(skill_path)
        self.iterations = iterations
        self.results = {
            "skill_name": self.skill_path.name,
            "timestamp": datetime.now().isoformat(),
            "iterations": iterations,
            "metrics": {}
        }
    
    def profile_file_operations(self):
        """Profile file read/write operations"""
        print("📁 Profiling file operations...")
        
        times = []
        skill_md = self.skill_path / "SKILL.md"
        
        if skill_md.exists():
            for _ in range(self.iterations):
                start = time.perf_counter()
                content = skill_md.read_text(encoding='utf-8')
                elapsed = time.perf_counter() - start
                times.append(elapsed)
            
            self.results["metrics"]["file_read"] = {
                "mean_ms": statistics.mean(times) * 1000,
                "median_ms": statistics.median(times) * 1000,
                "min_ms": min(times) * 1000,
                "max_ms": max(times) * 1000,
                "stdev_ms": statistics.stdev(times) * 1000 if len(times) > 1 else 0
            }
    
    def profile_memory_usage(self):
        """Profile memory usage"""
        print("🧠 Estimating memory usage...")
        
        try:
            import psutil
            process = psutil.Process()
            
            # Read skill files
            skill_md = self.skill_path / "SKILL.md"
            if skill_md.exists():
                mem_before = process.memory_info().rss / 1024 / 1024  # MB
                content = skill_md.read_text(encoding='utf-8')
                mem_after = process.memory_info().rss / 1024 / 1024  # MB
                
                self.results["metrics"]["memory"] = {
                    "base_mb": mem_before,
                    "after_load_mb": mem_after,
                    "skill_size_mb": len(content.encode('utf-8')) / 1024 / 1024
                }
        except ImportError:
            # Fallback without psutil
            skill_md = self.skill_path / "SKILL.md"
            if skill_md.exists():
                content = skill_md.read_text(encoding='utf-8')
                self.results["metrics"]["memory"] = {
                    "skill_size_mb": len(content.encode('utf-8')) / 1024 / 1024,
                    "note": "Install psutil for detailed memory profiling"
                }
    
    def profile_parsing(self):
        """Profile SKILL.md parsing"""
        print("📄 Profiling SKILL.md parsing...")
        
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return
        
        content = skill_md.read_text(encoding='utf-8')
        times = []
        
        for _ in range(self.iterations):
            start = time.perf_counter()
            # Simulate parsing operations
            lines = content.split('\n')
            headers = [line for line in lines if line.startswith('#')]
            code_blocks = content.count('```')
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        
        self.results["metrics"]["parsing"] = {
            "mean_ms": statistics.mean(times) * 1000,
            "median_ms": statistics.median(times) * 1000,
            "lines_count": len(lines),
            "headers_count": len(headers),
            "code_blocks_count": code_blocks
        }
    
    def analyze_complexity(self):
        """Analyze skill complexity"""
        print("📊 Analyzing complexity...")
        
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return
        
        content = skill_md.read_text(encoding='utf-8')
        
        # Complexity metrics
        metrics = {
            "total_chars": len(content),
            "total_lines": len(content.split('\n')),
            "word_count": len(content.split()),
            "heading_count": content.count('#'),
            "code_block_count": content.count('```'),
            "list_item_count": content.count('- ') + content.count('* '),
            "table_count": content.count('|'),
            "link_count": content.count('](')
        }
        
        # Calculate complexity score (0-100)
        # Lower is better for token efficiency
        complexity = min(100, (
            metrics["total_lines"] * 0.1 +
            metrics["heading_count"] * 0.5 +
            metrics["code_block_count"] * 2 +
            metrics["word_count"] * 0.01
        ))
        
        metrics["complexity_score"] = round(complexity, 2)
        
        # Token estimate (rough)
        metrics["estimated_tokens"] = metrics["word_count"] * 1.3
        
        self.results["metrics"]["complexity"] = metrics
    
    def generate_report(self) -> str:
        """Generate performance report"""
        report = f"""# Performance Report

## Skill: {self.results['skill_name']}
**Date**: {self.results['timestamp']}
**Iterations**: {self.results['iterations']}

---

## 📁 File Operations
"""
        if "file_read" in self.results["metrics"]:
            f = self.results["metrics"]["file_read"]
            report += f"""
| Metric | Value |
|--------|-------|
| Mean | {f['mean_ms']:.2f} ms |
| Median | {f['median_ms']:.2f} ms |
| Min | {f['min_ms']:.2f} ms |
| Max | {f['max_ms']:.2f} ms |
| Std Dev | {f['stdev_ms']:.2f} ms |
"""
        
        if "memory" in self.results["metrics"]:
            m = self.results["metrics"]["memory"]
            report += f"""
## 🧠 Memory Usage

| Metric | Value |
|--------|-------|
| Skill Size | {m.get('skill_size_mb', 'N/A'):.3f} MB |
"""
            if 'base_mb' in m:
                report += f"| Base Memory | {m['base_mb']:.2f} MB |\n"
                report += f"| After Load | {m['after_load_mb']:.2f} MB |\n"
        
        if "parsing" in self.results["metrics"]:
            p = self.results["metrics"]["parsing"]
            report += f"""
## 📄 Parsing Performance

| Metric | Value |
|--------|-------|
| Mean Time | {p['mean_ms']:.2f} ms |
| Lines | {p['lines_count']} |
| Headers | {p['headers_count']} |
| Code Blocks | {p['code_blocks_count']} |
"""
        
        if "complexity" in self.results["metrics"]:
            c = self.results["metrics"]["complexity"]
            report += f"""
## 📊 Complexity Analysis

| Metric | Value |
|--------|-------|
| Total Lines | {c['total_lines']} |
| Word Count | {c['word_count']} |
| Headings | {c['heading_count']} |
| Code Blocks | {c['code_block_count']} |
| Tables | {c['table_count']} |
| Links | {c['link_count']} |
| **Complexity Score** | **{c['complexity_score']}/100** |
| Est. Tokens | {int(c['estimated_tokens'])} |

### Complexity Rating
"""
            if c['complexity_score'] < 30:
                report += "✅ **Low Complexity** - Optimal for token efficiency\n"
            elif c['complexity_score'] < 60:
                report += "⚠️ **Medium Complexity** - Consider simplification\n"
            else:
                report += "❌ **High Complexity** - Recommend optimization\n"
        
        report += """
---

## 💡 Recommendations

"""
        recommendations = []
        
        if "complexity" in self.results["metrics"]:
            c = self.results["metrics"]["complexity"]
            if c['total_lines'] > 500:
                recommendations.append("- Consider splitting into multiple skills")
            if c['estimated_tokens'] > 2500:
                recommendations.append("- Move details to references/ directory")
            if c['code_block_count'] > 10:
                recommendations.append("- Extract scripts to separate files")
        
        if recommendations:
            report += "\n".join(recommendations)
        else:
            report += "✅ No major performance issues detected"
        
        return report
    
    def run(self):
        """Run full profiling"""
        print("="*60)
        print("⚡ Performance Profiler v3.3")
        print("="*60)
        print(f"\n📦 Skill: {self.skill_path.name}")
        print(f"🔄 Iterations: {self.iterations}")
        
        self.profile_file_operations()
        self.profile_memory_usage()
        self.profile_parsing()
        self.analyze_complexity()
        
        # Generate and save report
        report = self.generate_report()
        
        report_path = self.skill_path / ".performance_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Also save JSON
        json_path = self.skill_path / ".performance_profile.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Profiling complete!")
        print(f"📄 Report: {report_path}")
        print(f"📊 JSON: {json_path}")
        
        # Print summary
        if "complexity" in self.results["metrics"]:
            c = self.results["metrics"]["complexity"]
            print(f"\n📊 Summary:")
            print(f"   Complexity Score: {c['complexity_score']}/100")
            print(f"   Est. Tokens: {int(c['estimated_tokens'])}")
            print(f"   Lines: {c['total_lines']}")

def main():
    parser = argparse.ArgumentParser(description='Profile skill performance')
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('-i', '--iterations', type=int, default=10, help='Number of iterations')
    parser.add_argument('-o', '--output', help='Output report path')
    
    args = parser.parse_args()
    
    profiler = PerformanceProfiler(args.skill_path, args.iterations)
    profiler.run()

if __name__ == "__main__":
    main()
