#!/usr/bin/env python3
"""
Config Manager - Handle .skill-optimizer.yaml configuration
Usage: python config_manager.py [--init] [--show]
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG = {
    "version": "3.3.0",
    "optimization": {
        "auto_apply_fixes": False,
        "strict_mode": False,
        "max_iterations": 5,
        "patterns": {
            "tool_wrapper": {"enabled": True, "weight": 1.0},
            "generator": {"enabled": True, "weight": 1.0},
            "reviewer": {"enabled": True, "weight": 1.0},
            "inversion": {"enabled": True, "weight": 1.0},
            "pipeline": {"enabled": True, "weight": 1.0}
        }
    },
    "analysis": {
        "check_conciseness": True,
        "check_triggers": True,
        "check_patterns": True,
        "check_constraints": True,
        "min_score_threshold": 70
    },
    "llm": {
        "enabled": True,
        "provider": "kimi",
        "model": "moonshot-v1-8k",
        "temperature": 0.3,
        "max_tokens": 4000
    },
    "output": {
        "format": "markdown",
        "save_reports": True,
        "report_dir": "./optimization-reports",
        "verbose": True
    },
    "web": {
        "enabled": True,
        "port": 8080,
        "host": "0.0.0.0",
        "auto_open": False
    },
    "templates": {
        "auto_update": True,
        "repository": "https://github.com/openclaw/skill-templates",
        "local_path": "~/.skill-optimizer/templates"
    }
}

class ConfigManager:
    """Manage skill optimizer configuration"""
    
    def __init__(self, config_path: str = None):
        self.config_path = Path(config_path or self._find_config())
        self.config = self._load_config()
    
    def _find_config(self) -> str:
        """Find config file in standard locations"""
        locations = [
            ".skill-optimizer.yaml",
            ".skill-optimizer.yml",
            "~/.skill-optimizer/config.yaml",
            "~/.config/skill-optimizer/config.yaml"
        ]
        
        for loc in locations:
            path = Path(loc).expanduser()
            if path.exists():
                return str(path)
        
        return ".skill-optimizer.yaml"
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_path.exists():
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f) or {}
            
            # Merge with defaults
            config = DEFAULT_CONFIG.copy()
            self._deep_merge(config, user_config)
            return config
            
        except Exception as e:
            print(f"⚠️  Failed to load config: {e}")
            return DEFAULT_CONFIG.copy()
    
    def _deep_merge(self, base: Dict, override: Dict):
        """Deep merge dictionaries"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def init_config(self):
        """Initialize default config file"""
        if self.config_path.exists():
            print(f"⚠️  Config already exists: {self.config_path}")
            response = input("Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("Cancelled")
                return
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✅ Created config: {self.config_path}")
    
    def get(self, key: str, default=None):
        """Get config value by key (dot notation)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set config value by key (dot notation)"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✅ Saved config: {self.config_path}")
    
    def show(self):
        """Display current configuration"""
        print("="*60)
        print("📋 Skill Optimizer Configuration")
        print("="*60)
        print(f"\nConfig file: {self.config_path}")
        print("\nCurrent settings:")
        print(yaml.dump(self.config, default_flow_style=False, allow_unicode=True))
    
    def validate(self) -> bool:
        """Validate configuration"""
        errors = []
        
        # Check required fields
        required = ["version", "optimization", "analysis"]
        for field in required:
            if field not in self.config:
                errors.append(f"Missing required field: {field}")
        
        # Check pattern weights
        patterns = self.config.get("optimization", {}).get("patterns", {})
        for pattern, settings in patterns.items():
            if not isinstance(settings.get("weight"), (int, float)):
                errors.append(f"Invalid weight for pattern: {pattern}")
            if settings.get("weight", 0) < 0 or settings.get("weight", 0) > 2:
                errors.append(f"Weight should be 0-2 for pattern: {pattern}")
        
        if errors:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"   • {error}")
            return False
        
        print("✅ Configuration valid")
        return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Config Manager')
    parser.add_argument('--init', action='store_true', help='Initialize default config')
    parser.add_argument('--show', action='store_true', help='Show current config')
    parser.add_argument('--validate', action='store_true', help='Validate config')
    parser.add_argument('--get', help='Get config value (dot notation)')
    parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'), help='Set config value')
    parser.add_argument('--config', '-c', help='Config file path')
    
    args = parser.parse_args()
    
    manager = ConfigManager(args.config)
    
    if args.init:
        manager.init_config()
    elif args.show:
        manager.show()
    elif args.validate:
        manager.validate()
    elif args.get:
        value = manager.get(args.get)
        print(f"{args.get}: {value}")
    elif args.set:
        key, value = args.set
        # Try to parse as JSON
        try:
            import json
            value = json.loads(value)
        except:
            pass
        manager.set(key, value)
        manager.save()
        print(f"✅ Set {key} = {value}")
    else:
        manager.show()

if __name__ == "__main__":
    try:
        import yaml
    except ImportError:
        print("Installing PyYAML...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml", "-q"])
        import yaml
    
    main()
