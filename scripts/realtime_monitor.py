#!/usr/bin/env python3
"""
Realtime Monitor - Monitor skill performance in production
Usage: python realtime_monitor.py ./my-skill [--start|--report|--alert]
"""

import os
import json
import time
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import threading

class RealtimeMonitor:
    """Monitor skill performance in real-time"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.monitor_dir = self.skill_path / ".monitor"
        self.metrics_file = self.monitor_dir / "metrics.jsonl"
        self.config_file = self.monitor_dir / "config.json"
        self.alert_file = self.monitor_dir / "alerts.jsonl"
        self.running = False
        
    def _ensure_monitor_dir(self):
        """Create monitor directory"""
        self.monitor_dir.mkdir(exist_ok=True)
    
    def _load_config(self) -> dict:
        """Load monitoring configuration"""
        default_config = {
            "enabled": True,
            "sample_rate": 1.0,  # Log every invocation
            "alert_thresholds": {
                "error_rate": 0.1,  # 10% error rate
                "avg_latency_ms": 5000,  # 5 seconds
                "success_rate": 0.9  # 90% success rate
            },
            "retention_days": 30
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
            except:
                pass
        
        return default_config
    
    def _save_config(self, config: dict):
        """Save monitoring configuration"""
        self._ensure_monitor_dir()
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def log_invocation(self, success: bool, latency_ms: float, 
                       input_preview: str = None, error: str = None):
        """Log a single skill invocation"""
        self._ensure_monitor_dir()
        
        config = self._load_config()
        if not config["enabled"]:
            return
        
        # Sample if needed
        if config["sample_rate"] < 1.0:
            import random
            if random.random() > config["sample_rate"]:
                return
        
        metric = {
            "timestamp": datetime.now().isoformat(),
            "skill": self.skill_name,
            "success": success,
            "latency_ms": latency_ms,
            "input_preview": input_preview[:100] if input_preview else None,
            "error": error
        }
        
        with open(self.metrics_file, 'a') as f:
            f.write(json.dumps(metric) + '\n')
    
    def get_metrics(self, hours: int = 24) -> dict:
        """Get metrics for the specified time period"""
        if not self.metrics_file.exists():
            return {}
        
        cutoff = datetime.now() - timedelta(hours=hours)
        
        metrics = []
        with open(self.metrics_file, 'r') as f:
            for line in f:
                try:
                    metric = json.loads(line)
                    metric_time = datetime.fromisoformat(metric["timestamp"])
                    if metric_time >= cutoff:
                        metrics.append(metric)
                except:
                    pass
        
        if not metrics:
            return {}
        
        # Calculate aggregates
        total = len(metrics)
        successful = sum(1 for m in metrics if m["success"])
        failed = total - successful
        
        latencies = [m["latency_ms"] for m in metrics if m.get("latency_ms")]
        
        return {
            "period_hours": hours,
            "total_invocations": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "error_rate": failed / total if total > 0 else 0,
            "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
            "max_latency_ms": max(latencies) if latencies else 0,
            "min_latency_ms": min(latencies) if latencies else 0
        }
    
    def check_alerts(self) -> list:
        """Check if any alerts should be triggered"""
        config = self._load_config()
        thresholds = config.get("alert_thresholds", {})
        
        metrics = self.get_metrics(hours=1)  # Check last hour
        if not metrics:
            return []
        
        alerts = []
        
        # Check error rate
        if metrics["error_rate"] > thresholds.get("error_rate", 0.1):
            alerts.append({
                "severity": "critical",
                "type": "error_rate",
                "message": f"Error rate {metrics['error_rate']:.1%} exceeds threshold {thresholds['error_rate']:.1%}",
                "timestamp": datetime.now().isoformat()
            })
        
        # Check success rate
        if metrics["success_rate"] < thresholds.get("success_rate", 0.9):
            alerts.append({
                "severity": "warning",
                "type": "success_rate",
                "message": f"Success rate {metrics['success_rate']:.1%} below threshold {thresholds['success_rate']:.1%}",
                "timestamp": datetime.now().isoformat()
            })
        
        # Check latency
        if metrics["avg_latency_ms"] > thresholds.get("avg_latency_ms", 5000):
            alerts.append({
                "severity": "warning",
                "type": "latency",
                "message": f"Average latency {metrics['avg_latency_ms']:.0f}ms exceeds threshold {thresholds['avg_latency_ms']:.0f}ms",
                "timestamp": datetime.now().isoformat()
            })
        
        # Log alerts
        if alerts:
            self._ensure_monitor_dir()
            with open(self.alert_file, 'a') as f:
                for alert in alerts:
                    f.write(json.dumps(alert) + '\n')
        
        return alerts
    
    def generate_dashboard(self):
        """Generate monitoring dashboard"""
        print("="*60)
        print("📊 Realtime Monitor v3.4")
        print("="*60)
        print(f"\n📦 Skill: {self.skill_name}")
        
        # Get metrics for different periods
        metrics_1h = self.get_metrics(hours=1)
        metrics_24h = self.get_metrics(hours=24)
        metrics_7d = self.get_metrics(hours=168)
        
        print(f"\n📈 Performance (Last Hour):")
        if metrics_1h:
            print(f"   Invocations: {metrics_1h['total_invocations']}")
            print(f"   Success Rate: {metrics_1h['success_rate']:.1%}")
            print(f"   Error Rate: {metrics_1h['error_rate']:.1%}")
            print(f"   Avg Latency: {metrics_1h['avg_latency_ms']:.0f}ms")
        else:
            print("   No data available")
        
        print(f"\n📈 Performance (Last 24 Hours):")
        if metrics_24h:
            print(f"   Invocations: {metrics_24h['total_invocations']}")
            print(f"   Success Rate: {metrics_24h['success_rate']:.1%}")
            print(f"   Error Rate: {metrics_24h['error_rate']:.1%}")
            print(f"   Avg Latency: {metrics_24h['avg_latency_ms']:.0f}ms")
        else:
            print("   No data available")
        
        # Check alerts
        alerts = self.check_alerts()
        if alerts:
            print(f"\n🚨 Active Alerts ({len(alerts)}):")
            for alert in alerts:
                icon = "🔴" if alert["severity"] == "critical" else "🟡"
                print(f"   {icon} [{alert['type']}] {alert['message']}")
        else:
            print(f"\n✅ No active alerts")
        
        # Generate HTML dashboard
        self._generate_html_dashboard(metrics_24h, alerts)
    
    def _generate_html_dashboard(self, metrics: dict, alerts: list):
        """Generate HTML dashboard"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Monitor - {self.skill_name}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }}
        .metric-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .metric-value {{ font-size: 32px; font-weight: bold; color: #667eea; }}
        .metric-label {{ color: #666; margin-top: 5px; }}
        .alerts {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .alert {{ padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .alert-critical {{ background: #fee; border-left: 4px solid #e53e3e; }}
        .alert-warning {{ background: #fffbeb; border-left: 4px solid #d69e2e; }}
        .no-alerts {{ color: #48bb78; font-size: 18px; }}
        .refresh {{ text-align: center; margin-top: 20px; color: #666; }}
    </style>
    <meta http-equiv="refresh" content="30">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 {self.skill_name}</h1>
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{metrics.get('total_invocations', 0)}</div>
                <div class="metric-label">Invocations (24h)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics.get('success_rate', 0)*100:.1f}%</div>
                <div class="metric-label">Success Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics.get('error_rate', 0)*100:.1f}%</div>
                <div class="metric-label">Error Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics.get('avg_latency_ms', 0):.0f}ms</div>
                <div class="metric-label">Avg Latency</div>
            </div>
        </div>
        
        <div class="alerts">
            <h2>🚨 Alerts</h2>
"""
        
        if alerts:
            for alert in alerts:
                css_class = f"alert-{alert['severity']}"
                html += f'            <div class="alert {css_class}"><strong>[{alert["type"].upper()}]</strong> {alert["message"]}</div>\n'
        else:
            html += '            <div class="no-alerts">✅ No active alerts</div>\n'
        
        html += """        
        </div>
        
        <div class="refresh">Auto-refresh every 30 seconds</div>
    </div>
</body>
</html>"""
        
        dashboard_path = self.monitor_dir / "dashboard.html"
        dashboard_path.write_text(html, encoding='utf-8')
        print(f"\n🌐 Dashboard: {dashboard_path}")
    
    def start_monitoring(self, interval: int = 60):
        """Start continuous monitoring"""
        print("="*60)
        print("📊 Starting Real-time Monitor")
        print("="*60)
        print(f"\n📦 Skill: {self.skill_name}")
        print(f"⏱️  Check interval: {interval}s")
        print(f"\nPress Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                # Check alerts
                alerts = self.check_alerts()
                
                if alerts:
                    print(f"\n🚨 {datetime.now().strftime('%H:%M:%S')} - {len(alerts)} alert(s):")
                    for alert in alerts:
                        print(f"   [{alert['type']}] {alert['message']}")
                else:
                    print(f"{datetime.now().strftime('%H:%M:%S')} - ✅ Healthy")
                
                # Generate dashboard
                self.generate_dashboard()
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped")
            self.running = False
    
    def configure(self, sample_rate: float = None, error_threshold: float = None):
        """Configure monitoring settings"""
        config = self._load_config()
        
        if sample_rate is not None:
            config["sample_rate"] = sample_rate
        
        if error_threshold is not None:
            config["alert_thresholds"]["error_rate"] = error_threshold
        
        self._save_config(config)
        print("✅ Configuration updated")
        print(f"   Sample rate: {config['sample_rate']}")
        print(f"   Error threshold: {config['alert_thresholds']['error_rate']:.1%}")

def main():
    parser = argparse.ArgumentParser(description='Realtime Monitor')
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('--start', '-s', action='store_true', help='Start monitoring')
    parser.add_argument('--report', '-r', action='store_true', help='Generate report')
    parser.add_argument('--alert', '-a', action='store_true', help='Check alerts only')
    parser.add_argument('--interval', '-i', type=int, default=60, help='Check interval in seconds')
    parser.add_argument('--configure', '-c', action='store_true', help='Configure monitoring')
    parser.add_argument('--sample-rate', type=float, help='Sample rate (0.0-1.0)')
    parser.add_argument('--error-threshold', type=float, help='Error rate threshold')
    
    args = parser.parse_args()
    
    monitor = RealtimeMonitor(args.skill_path)
    
    if args.start:
        monitor.start_monitoring(args.interval)
    elif args.report:
        monitor.generate_dashboard()
    elif args.alert:
        alerts = monitor.check_alerts()
        if alerts:
            print(f"🚨 {len(alerts)} alert(s):")
            for alert in alerts:
                print(f"   [{alert['type']}] {alert['message']}")
        else:
            print("✅ No active alerts")
    elif args.configure:
        monitor.configure(args.sample_rate, args.error_threshold)
    else:
        # Default: show dashboard
        monitor.generate_dashboard()

if __name__ == "__main__":
    main()
