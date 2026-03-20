#!/usr/bin/env python3
"""
Fully Auto Mode - Complete automation: monitor → analyze → optimize → test → deploy
Usage: python fully_auto.py /path/to/skills-folder [--deploy-clawhub] [--deploy-github]
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

class FullyAutoOptimizer:
    def __init__(self, skills_folder: str, deploy_clawhub: bool = False, deploy_github: bool = False):
        self.skills_folder = Path(skills_folder)
        self.deploy_clawhub = deploy_clawhub
        self.deploy_github = deploy_github
        self.scripts_dir = Path(__file__).parent
        self.results = []
        
    def log(self, message: str):
        """Log with timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def run_monitor(self):
        """Step 1: Monitor and identify skills needing optimization"""
        self.log("🔍 Step 1: Monitoring skills...")
        
        monitor_script = self.scripts_dir / 'monitor.py'
        result = subprocess.run(
            [sys.executable, str(monitor_script), str(self.skills_folder), '--schedule', 'weekly'],
            capture_output=True,
            text=True
        )
        
        # Parse monitoring results
        db_path = self.skills_folder / '.skill_monitoring_db.json'
        if db_path.exists():
            with open(db_path) as f:
                db = json.load(f)
                needs_attention = [k for k, v in db.items() if 'last_optimized' in v]
                return needs_attention
        
        return []
    
    def run_ai_advisor(self, skill_name: str):
        """Step 2: AI analysis"""
        self.log(f"🤖 Step 2: AI analysis for {skill_name}...")
        
        skill_path = self.skills_folder / skill_name
        advisor_script = self.scripts_dir / 'ai_advisor.py'
        
        subprocess.run(
            [sys.executable, str(advisor_script), str(skill_path)],
            capture_output=True,
            text=True
        )
        
        # Check if AI report generated
        report_path = skill_path / '.ai_advisor_report.md'
        return report_path.exists()
    
    def run_optimize(self, skill_name: str):
        """Step 3: Auto-optimize"""
        self.log(f"🚀 Step 3: Optimizing {skill_name}...")
        
        skill_path = self.skills_folder / skill_name
        output_path = self.skills_folder / 'optimized' / f'{skill_name}-v2'
        
        auto_optimize_script = self.scripts_dir / 'auto_optimize.py'
        result = subprocess.run(
            [sys.executable, str(auto_optimize_script), str(skill_path), '--output', str(output_path)],
            capture_output=True,
            text=True
        )
        
        return result.returncode == 0, output_path
    
    def run_test_generation(self, skill_name: str, optimized_path: Path):
        """Step 4: Generate tests"""
        self.log(f"🧪 Step 4: Generating tests for {skill_name}...")
        
        test_gen_script = self.scripts_dir / 'test_generator.py'
        test_output = optimized_path / 'tests'
        
        subprocess.run(
            [sys.executable, str(test_gen_script), str(optimized_path), '--output', str(test_output)],
            capture_output=True,
            text=True
        )
        
        return test_output.exists()
    
    def run_validation(self, skill_name: str, optimized_path: Path):
        """Step 5: Validate optimization"""
        self.log(f"✅ Step 5: Validating {skill_name}...")
        
        analyze_script = self.scripts_dir / 'analyze_skill.py'
        result = subprocess.run(
            [sys.executable, str(analyze_script), str(optimized_path)],
            capture_output=True,
            text=True
        )
        
        # Check new score
        report_path = optimized_path / '.analysis_report.json'
        if report_path.exists():
            with open(report_path) as f:
                report = json.load(f)
                return report.get('scores', {}).get('overall', 0)
        
        return 0
    
    def deploy_github(self, skill_name: str, optimized_path: Path):
        """Step 6a: Deploy to GitHub"""
        if not self.deploy_github:
            return True
        
        self.log(f"📤 Step 6a: Deploying {skill_name} to GitHub...")
        
        # This would require git operations
        # For now, just create a ready-to-push folder
        deploy_ready = self.skills_folder / 'deploy-ready' / skill_name
        
        # Copy optimized skill
        import shutil
        if deploy_ready.exists():
            shutil.rmtree(deploy_ready)
        shutil.copytree(optimized_path, deploy_ready)
        
        self.log(f"   Ready for GitHub push: {deploy_ready}")
        return True
    
    def deploy_clawhub(self, skill_name: str, optimized_path: Path):
        """Step 6b: Deploy to ClawHub"""
        if not self.deploy_clawhub:
            return True
        
        self.log(f"📤 Step 6b: Preparing {skill_name} for ClawHub...")
        
        # Create .skill package
        import shutil
        skill_package = self.skills_folder / 'clawhub-ready' / f'{skill_name}.skill'
        skill_package.parent.mkdir(parents=True, exist_ok=True)
        
        # Create zip
        shutil.make_archive(str(skill_package).replace('.skill', ''), 'zip', optimized_path)
        os.rename(str(skill_package).replace('.skill', '') + '.zip', skill_package)
        
        self.log(f"   Ready for ClawHub: {skill_package}")
        return True
    
    def process_single_skill(self, skill_name: str):
        """Process a single skill through full pipeline"""
        self.log(f"\n{'='*60}")
        self.log(f"🔄 Processing: {skill_name}")
        self.log('='*60)
        
        result = {
            "skill": skill_name,
            "timestamp": datetime.now().isoformat(),
            "steps": {}
        }
        
        try:
            # Step 2: AI Advisor
            ai_ok = self.run_ai_advisor(skill_name)
            result["steps"]["ai_advisor"] = "success" if ai_ok else "failed"
            
            # Step 3: Optimize
            opt_ok, optimized_path = self.run_optimize(skill_name)
            result["steps"]["optimize"] = "success" if opt_ok else "failed"
            
            if not opt_ok:
                result["status"] = "failed"
                return result
            
            # Step 4: Generate Tests
            test_ok = self.run_test_generation(skill_name, optimized_path)
            result["steps"]["test_generation"] = "success" if test_ok else "failed"
            
            # Step 5: Validate
            new_score = self.run_validation(skill_name, optimized_path)
            result["steps"]["validation"] = f"score_{new_score}"
            result["new_score"] = new_score
            
            # Step 6: Deploy
            if self.deploy_github:
                gh_ok = self.deploy_github(skill_name, optimized_path)
                result["steps"]["deploy_github"] = "success" if gh_ok else "failed"
            
            if self.deploy_clawhub:
                ch_ok = self.deploy_clawhub(skill_name, optimized_path)
                result["steps"]["deploy_clawhub"] = "success" if ch_ok else "failed"
            
            result["status"] = "success"
            result["optimized_path"] = str(optimized_path)
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def run(self):
        """Run fully automated optimization pipeline"""
        self.log("🎯 FULLY AUTO OPTIMIZER v3.0")
        self.log("="*60)
        self.log(f"Target: {self.skills_folder}")
        self.log(f"Deploy GitHub: {self.deploy_github}")
        self.log(f"Deploy ClawHub: {self.deploy_clawhub}")
        self.log("="*60 + "\n")
        
        # Step 1: Monitor
        skills_to_optimize = self.run_monitor()
        
        if not skills_to_optimize:
            self.log("✅ All skills healthy! Nothing to optimize.")
            return
        
        self.log(f"Found {len(skills_to_optimize)} skill(s) needing optimization\n")
        
        # Process each skill
        for skill_name in skills_to_optimize:
            result = self.process_single_skill(skill_name)
            self.results.append(result)
        
        # Generate final report
        self.generate_report()
    
    def generate_report(self):
        """Generate final automation report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total": len(self.results),
            "successful": sum(1 for r in self.results if r.get("status") == "success"),
            "failed": sum(1 for r in self.results if r.get("status") == "failed"),
            "details": self.results
        }
        
        # Save report
        report_path = self.skills_folder / '.fully_auto_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Print summary
        self.log("\n" + "="*60)
        self.log("📊 FULLY AUTO COMPLETE")
        self.log("="*60)
        self.log(f"Total: {report['total']}")
        self.log(f"Successful: {report['successful']}")
        self.log(f"Failed: {report['failed']}")
        self.log(f"\\n💾 Report: {report_path}")
        
        # Print next steps
        self.log("\n📋 Next Steps:")
        if self.deploy_github:
            self.log("   1. Review deploy-ready/ folder")
            self.log("   2. Push to GitHub: git push origin main")
        if self.deploy_clawhub:
            self.log("   3. Upload clawhub-ready/*.skill to ClawHub")

def main():
    parser = argparse.ArgumentParser(description='Fully automated skill optimization pipeline')
    parser.add_argument('skills_folder', help='Path to skills folder')
    parser.add_argument('--deploy-github', action='store_true', help='Deploy to GitHub')
    parser.add_argument('--deploy-clawhub', action='store_true', help='Prepare for ClawHub')
    parser.add_argument('--daemon', action='store_true', help='Run continuously')
    
    args = parser.parse_args()
    
    auto = FullyAutoOptimizer(args.skills_folder, args.deploy_clawhub, args.deploy_github)
    
    if args.daemon:
        import time
        print("👻 Running in daemon mode... (Press Ctrl+C to stop)")
        while True:
            auto.run()
            print("\n⏰ Sleeping for 24 hours...\n")
            time.sleep(86400)
    else:
        auto.run()

if __name__ == "__main__":
    main()
