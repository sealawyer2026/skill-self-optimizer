#!/usr/bin/env python3
"""
Skill Monitor - Automatic monitoring and auto-upgrade trigger
Usage: python monitor.py /path/to/skills-folder [--schedule daily|weekly|monthly]
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class SkillMonitor:
    def __init__(self, skills_folder: str, schedule: str = 'weekly'):
        self.skills_folder = Path(skills_folder)
        self.schedule = schedule
        self.monitoring_db = self.skills_folder / '.skill_monitoring_db.json'
        self.thresholds = {
            'min_score': 90,
            'max_complaints': 3,
            'min_completion_rate': 85,
            'max_days_since_optimization': 30
        }
        
    def load_db(self):
        """Load monitoring database"""
        if self.monitoring_db.exists():
            with open(self.monitoring_db) as f:
                return json.load(f)
        return {}
    
    def save_db(self, db):
        """Save monitoring database"""
        with open(self.monitoring_db, 'w') as f:
            json.dump(db, f, indent=2, default=str)
    
    def scan_skills(self):
        """Scan all skills in folder"""
        skills = []
        for item in self.skills_folder.iterdir():
            if item.is_dir() and (item / 'SKILL.md').exists():
                skills.append(item)
        return skills
    
    def analyze_skill(self, skill_path: Path):
        """Analyze a single skill"""
        analyze_script = Path(__file__).parent / 'analyze_skill.py'
        result = subprocess.run(
            [sys.executable, str(analyze_script), str(skill_path)],
            capture_output=True,
            text=True
        )
        
        report_path = skill_path / '.analysis_report.json'
        if report_path.exists():
            with open(report_path) as f:
                return json.load(f)
        return None
    
    def check_needs_optimization(self, skill_name: str, report: dict, db: dict):
        """Check if skill needs optimization"""
        reasons = []
        
        # Check score
        score = report.get('scores', {}).get('overall', 0)
        if score < self.thresholds['min_score']:
            reasons.append(f"Score {score} < {self.thresholds['min_score']}")
        
        # Check critical issues
        critical = report.get('summary', {}).get('critical_issues', 0)
        if critical > 0:
            reasons.append(f"{critical} critical issues")
        
        # Check last optimization time
        last_opt = db.get(skill_name, {}).get('last_optimized')
        if last_opt:
            last_date = datetime.fromisoformat(last_opt)
            days_since = (datetime.now() - last_date).days
            if days_since > self.thresholds['max_days_since_optimization']:
                reasons.append(f"{days_since} days since last optimization")
        
        return reasons
    
    def auto_optimize(self, skill_path: Path, output_path: Path):
        """Auto-optimize a skill"""
        auto_optimize_script = Path(__file__).parent / 'auto_optimize.py'
        result = subprocess.run(
            [sys.executable, str(auto_optimize_script), str(skill_path), '--output', str(output_path)],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def run(self):
        """Run monitoring cycle"""
        print(f"🔍 Skill Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"📁 Monitoring: {self.skills_folder}")
        print(f"⏰ Schedule: {self.schedule}\n")
        
        db = self.load_db()
        skills = self.scan_skills()
        
        print(f"Found {len(skills)} skill(s) to monitor\n")
        
        needs_attention = []
        
        for skill in skills:
            skill_name = skill.name
            print(f"📊 Analyzing: {skill_name}")
            
            report = self.analyze_skill(skill)
            if not report:
                print(f"   ❌ Failed to analyze")
                continue
            
            score = report.get('scores', {}).get('overall', 0)
            print(f"   Score: {score}/100")
            
            reasons = self.check_needs_optimization(skill_name, report, db)
            
            if reasons:
                print(f"   ⚠️ Needs optimization:")
                for r in reasons:
                    print(f"      - {r}")
                needs_attention.append({
                    'skill': skill_name,
                    'path': str(skill),
                    'score': score,
                    'reasons': reasons
                })
            else:
                print(f"   ✅ Healthy")
            
            print()
        
        # Summary
        print(f"\n📈 Summary:")
        print(f"   Total skills: {len(skills)}")
        print(f"   Need attention: {len(needs_attention)}")
        
        if needs_attention:
            print(f"\n🚀 Auto-optimization starting for {len(needs_attention)} skill(s)...\n")
            
            optimized_dir = self.skills_folder / 'optimized'
            optimized_dir.mkdir(exist_ok=True)
            
            for item in needs_attention:
                skill_path = Path(item['path'])
                output_path = optimized_dir / f"{item['skill']}-v2"
                
                print(f"Optimizing: {item['skill']}")
                success = self.auto_optimize(skill_path, output_path)
                
                if success:
                    print(f"   ✅ Optimized -> {output_path}")
                    db[item['skill']] = {
                        'last_optimized': datetime.now().isoformat(),
                        'previous_score': item['score'],
                        'optimized_path': str(output_path)
                    }
                else:
                    print(f"   ❌ Failed")
            
            self.save_db(db)
            
            print(f"\n💾 Results saved to: {optimized_dir}/")
            print(f"📝 Database updated: {self.monitoring_db}")
        else:
            print(f"\n✅ All skills healthy! No optimization needed.")
        
        # Schedule next run
        if self.schedule == 'daily':
            next_run = datetime.now() + timedelta(days=1)
        elif self.schedule == 'weekly':
            next_run = datetime.now() + timedelta(weeks=1)
        else:
            next_run = datetime.now() + timedelta(days=30)
        
        print(f"\n⏰ Next run: {next_run.strftime('%Y-%m-%d %H:%M')}")

def main():
    parser = argparse.ArgumentParser(description='Monitor and auto-optimize Skills')
    parser.add_argument('skills_folder', help='Path to skills folder')
    parser.add_argument('--schedule', choices=['daily', 'weekly', 'monthly'], 
                        default='weekly', help='Monitoring schedule')
    parser.add_argument('--daemon', action='store_true', 
                        help='Run as daemon (continuous monitoring)')
    
    args = parser.parse_args()
    
    monitor = SkillMonitor(args.skills_folder, args.schedule)
    
    if args.daemon:
        print("👻 Running as daemon... (Press Ctrl+C to stop)")
        while True:
            monitor.run()
            if args.schedule == 'daily':
                time.sleep(86400)
            elif args.schedule == 'weekly':
                time.sleep(604800)
            else:
                time.sleep(2592000)
    else:
        monitor.run()

if __name__ == "__main__":
    main()
