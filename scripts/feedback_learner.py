#!/usr/bin/env python3
"""
Feedback Learner - Collect and analyze user feedback for skill improvement
Usage: python feedback_learner.py ./my-skill [--collect|--analyze|--suggest]
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class FeedbackLearner:
    """Collect and learn from user feedback"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.feedback_dir = self.skill_path / ".feedback"
        self.feedback_file = self.feedback_dir / "feedback.jsonl"
        self.analysis_file = self.skill_path / ".feedback_analysis.json"
        
    def _ensure_feedback_dir(self):
        """Create feedback directory if needed"""
        self.feedback_dir.mkdir(exist_ok=True)
    
    def collect_feedback(self, rating: int, comment: str = None, issue_type: str = None):
        """Collect a single feedback entry"""
        self._ensure_feedback_dir()
        
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "skill": self.skill_name,
            "rating": rating,  # 1-5
            "comment": comment,
            "issue_type": issue_type,  # trigger, output, performance, other
            "version": self._get_skill_version()
        }
        
        # Append to file
        with open(self.feedback_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback) + '\n')
        
        print(f"✅ Feedback recorded: {rating}/5")
        if comment:
            print(f"   Comment: {comment}")
    
    def _get_skill_version(self) -> str:
        """Extract version from SKILL.md"""
        skill_md = self.skill_path / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8')
            match = re.search(r'version:\s*["\']?([\d.]+)', content, re.I)
            if match:
                return match.group(1)
        return "unknown"
    
    def analyze_feedback(self) -> dict:
        """Analyze all collected feedback"""
        if not self.feedback_file.exists():
            print("❌ No feedback data found")
            return None
        
        feedbacks = []
        with open(self.feedback_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        feedbacks.append(json.loads(line))
                    except:
                        pass
        
        if not feedbacks:
            print("❌ No valid feedback entries")
            return None
        
        # Calculate metrics
        total = len(feedbacks)
        avg_rating = sum(f['rating'] for f in feedbacks) / total
        
        # Issue type breakdown
        issue_types = defaultdict(int)
        for f in feedbacks:
            if f.get('issue_type'):
                issue_types[f['issue_type']] += 1
        
        # Rating distribution
        rating_dist = defaultdict(int)
        for f in feedbacks:
            rating_dist[f['rating']] += 1
        
        # Common keywords in comments
        keywords = self._extract_keywords([f.get('comment', '') for f in feedbacks if f.get('comment')])
        
        analysis = {
            "total_feedback": total,
            "average_rating": round(avg_rating, 2),
            "rating_distribution": dict(rating_dist),
            "issue_types": dict(issue_types),
            "common_keywords": keywords,
            "recommendations": self._generate_recommendations(feedbacks, avg_rating, issue_types)
        }
        
        # Save analysis
        with open(self.analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2)
        
        return analysis
    
    def _extract_keywords(self, comments: list) -> list:
        """Extract common keywords from comments"""
        word_freq = defaultdict(int)
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                      'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                      'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                      'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
                      'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
                      'through', 'during', 'before', 'after', 'above', 'below',
                      'between', 'under', 'and', 'but', 'or', 'yet', 'so', 'if',
                      'because', 'although', 'though', 'while', 'where', 'when',
                      'that', 'which', 'who', 'whom', 'whose', 'what', 'this',
                      'these', 'those', 'i', 'me', 'my', 'mine', 'myself', 'you',
                      'your', 'yours', 'yourself', 'he', 'him', 'his', 'himself',
                      'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                      'we', 'us', 'our', 'ours', 'ourselves', 'they', 'them',
                      'their', 'theirs', 'themselves', 'not', 'no', 'yes', 'it'}
        
        for comment in comments:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', comment.lower())
            for word in words:
                if word not in stop_words:
                    word_freq[word] += 1
        
        # Return top 10 keywords
        return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    def _generate_recommendations(self, feedbacks: list, avg_rating: float, issue_types: dict) -> list:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Rating-based recommendations
        if avg_rating < 3.0:
            recommendations.append({
                "priority": "high",
                "category": "overall",
                "issue": "Low average rating",
                "suggestion": "Major revision needed. Consider redesigning the skill approach.",
                "confidence": "high"
            })
        elif avg_rating < 4.0:
            recommendations.append({
                "priority": "medium",
                "category": "overall",
                "issue": "Average rating below target",
                "suggestion": "Identify and fix specific pain points from user comments.",
                "confidence": "medium"
            })
        
        # Issue-type based recommendations
        if issue_types.get('trigger', 0) > 2:
            recommendations.append({
                "priority": "high",
                "category": "triggering",
                "issue": f"{issue_types['trigger']} users reported triggering issues",
                "suggestion": "Review SKILL.md description. Make trigger conditions more explicit. Add negative examples.",
                "confidence": "high"
            })
        
        if issue_types.get('output', 0) > 2:
            recommendations.append({
                "priority": "high",
                "category": "output",
                "issue": f"{issue_types['output']} users reported output quality issues",
                "suggestion": "Add more examples, improve templates, or add validation steps.",
                "confidence": "high"
            })
        
        if issue_types.get('performance', 0) > 1:
            recommendations.append({
                "priority": "medium",
                "category": "performance",
                "issue": f"{issue_types['performance']} users reported performance issues",
                "suggestion": "Review skill size and complexity. Move content to references/ if too large.",
                "confidence": "medium"
            })
        
        return recommendations
    
    def generate_improvement_report(self):
        """Generate a comprehensive improvement report"""
        analysis = self.analyze_feedback()
        if not analysis:
            return
        
        report_path = self.skill_path / ".improvement_report.md"
        
        report = f"""# Feedback Analysis Report

**Skill:** {self.skill_name}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Total Feedback:** {analysis['total_feedback']} entries

---

## 📊 Overall Metrics

| Metric | Value |
|--------|-------|
| Average Rating | {analysis['average_rating']}/5 |
| Total Feedback | {analysis['total_feedback']} |

### Rating Distribution

| Rating | Count | Percentage |
|--------|-------|------------|
"""
        
        for rating in [5, 4, 3, 2, 1]:
            count = analysis['rating_distribution'].get(rating, 0)
            pct = (count / analysis['total_feedback'] * 100) if analysis['total_feedback'] else 0
            report += f"| {rating} | {count} | {pct:.1f}% |\n"
        
        if analysis['issue_types']:
            report += f"\n### Issue Types\n\n| Type | Count |\n|------|-------|\n"
            for issue_type, count in sorted(analysis['issue_types'].items(), key=lambda x: x[1], reverse=True):
                report += f"| {issue_type} | {count} |\n"
        
        if analysis['common_keywords']:
            report += f"\n### Common Keywords\n\n"
            for keyword, count in analysis['common_keywords']:
                report += f"- {keyword} ({count})\n"
        
        if analysis['recommendations']:
            report += f"\n---\n\n## 🎯 Recommendations\n\n"
            for i, rec in enumerate(analysis['recommendations'], 1):
                report += f"""### {i}. {rec['issue']}

- **Priority:** {rec['priority'].upper()}
- **Category:** {rec['category']}
- **Suggestion:** {rec['suggestion']}
- **Confidence:** {rec['confidence']}

"""
        
        report += f"""---

## 🛠️ Action Items

- [ ] Review all {analysis['total_feedback']} feedback entries
- [ ] Address high-priority recommendations
- [ ] Update SKILL.md based on insights
- [ ] Test improvements with real users
- [ ] Collect more feedback
"""
        
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path}")
        
        # Print summary
        print(f"\n📊 Summary:")
        print(f"   Average Rating: {analysis['average_rating']}/5")
        print(f"   Total Feedback: {analysis['total_feedback']}")
        print(f"   Recommendations: {len(analysis['recommendations'])}")
        
        if analysis['recommendations']:
            print(f"\n🎯 Top Recommendations:")
            for rec in analysis['recommendations'][:3]:
                print(f"   [{rec['priority'].upper()}] {rec['issue']}")
    
    def suggest_improvements(self):
        """Suggest specific improvements based on feedback"""
        analysis = self.analyze_feedback()
        if not analysis:
            return
        
        print("="*60)
        print(f"💡 Suggested Improvements for {self.skill_name}")
        print("="*60)
        
        for rec in analysis['recommendations']:
            icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            print(f"\n{icon} {rec['issue']}")
            print(f"   Action: {rec['suggestion']}")

def main():
    parser = argparse.ArgumentParser(description='Feedback Learner')
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('--collect', '-c', action='store_true', help='Collect new feedback')
    parser.add_argument('--analyze', '-a', action='store_true', help='Analyze feedback')
    parser.add_argument('--suggest', '-s', action='store_true', help='Suggest improvements')
    parser.add_argument('--rating', '-r', type=int, help='Rating (1-5) for --collect')
    parser.add_argument('--comment', help='Comment for --collect')
    parser.add_argument('--issue-type', choices=['trigger', 'output', 'performance', 'other'], 
                        help='Issue type for --collect')
    
    args = parser.parse_args()
    
    learner = FeedbackLearner(args.skill_path)
    
    if args.collect:
        if not args.rating:
            print("❌ Please provide --rating (1-5)")
            return
        learner.collect_feedback(args.rating, args.comment, args.issue_type)
    elif args.analyze:
        learner.generate_improvement_report()
    elif args.suggest:
        learner.suggest_improvements()
    else:
        # Default: show suggestions
        learner.suggest_improvements()

if __name__ == "__main__":
    import re
    main()
