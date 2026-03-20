#!/usr/bin/env python3
"""
Dependency Analyzer - Analyze skill dependencies
Usage: python dependency_analyzer.py /path/to/skill [--visualize]
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict

class DependencyAnalyzer:
    """Analyze dependencies between skills"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.dependencies = {
            "skill_name": self.skill_path.name,
            "internal_deps": [],
            "external_deps": [],
            "skill_refs": [],
            "tool_refs": [],
            "file_refs": []
        }
    
    def analyze_skill_references(self, content: str):
        """Find references to other skills"""
        # Pattern: [skill-name] or skill-name (in descriptions)
        skill_patterns = [
            r'\[([a-z0-9-]+)\]',  # [skill-name]
            r'skill[s]?\s*:\s*([a-z0-9-]+)',  # skill: name
            r'chain.*:\s*([a-z0-9-]+)',  # chain: name
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if match not in self.dependencies["skill_refs"]:
                    self.dependencies["skill_refs"].append(match)
    
    def analyze_tool_references(self, content: str):
        """Find tool/system dependencies"""
        tools = {
            "python": r'python\d?|\.py',
            "node": r'node|npm|\.js',
            "curl": r'curl',
            "git": r'git',
            "docker": r'docker',
            "kubectl": r'kubectl|k8s',
            "aws": r'aws',
            "gcp": r'gcloud|gsutil',
            "azure": r'az\s',
        }
        
        for tool, pattern in tools.items():
            if re.search(pattern, content, re.IGNORECASE):
                if tool not in self.dependencies["tool_refs"]:
                    self.dependencies["tool_refs"].append(tool)
    
    def analyze_file_references(self, content: str):
        """Find file path references"""
        # Find references to files/directories
        file_patterns = [
            r'`([^`]+\.(?:md|py|js|sh|yaml|yml|json))`',
            r'references/([a-z0-9-]+)',
            r'assets/([a-z0-9-]+)',
            r'scripts/([a-z0-9-]+)',
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if match not in self.dependencies["file_refs"]:
                    self.dependencies["file_refs"].append(match)
    
    def check_actual_files(self):
        """Check which referenced files actually exist"""
        existing = []
        missing = []
        
        for ref in self.dependencies["file_refs"]:
            # Try different paths
            paths_to_check = [
                self.skill_path / ref,
                self.skill_path / "references" / ref,
                self.skill_path / "assets" / ref,
                self.skill_path / "scripts" / ref,
            ]
            
            found = False
            for path in paths_to_check:
                if path.exists():
                    existing.append({"ref": ref, "path": str(path)})
                    found = True
                    break
            
            if not found:
                missing.append(ref)
        
        self.dependencies["existing_files"] = existing
        self.dependencies["missing_files"] = missing
    
    def generate_dependency_graph(self) -> dict:
        """Generate dependency graph data"""
        nodes = [{"id": self.skill_path.name, "type": "main", "label": "This Skill"}]
        edges = []
        
        # Add skill references as nodes
        for i, skill in enumerate(self.dependencies["skill_refs"]):
            nodes.append({
                "id": skill,
                "type": "skill",
                "label": skill
            })
            edges.append({
                "from": self.skill_path.name,
                "to": skill,
                "label": "uses"
            })
        
        # Add tool references
        for tool in self.dependencies["tool_refs"]:
            nodes.append({
                "id": tool,
                "type": "tool",
                "label": tool
            })
            edges.append({
                "from": self.skill_path.name,
                "to": tool,
                "label": "requires"
            })
        
        # Add file references
        for file_ref in self.dependencies["existing_files"]:
            nodes.append({
                "id": file_ref["ref"],
                "type": "file",
                "label": file_ref["ref"]
            })
            edges.append({
                "from": self.skill_path.name,
                "to": file_ref["ref"],
                "label": "includes"
            })
        
        return {"nodes": nodes, "edges": edges}
    
    def generate_mermaid_diagram(self) -> str:
        """Generate Mermaid diagram"""
        diagram = "graph TD\n"
        
        main_node = self.skill_path.name.replace('-', '_')
        diagram += f"    {main_node}[{self.skill_path.name}]\n"
        
        # Add skills
        for skill in self.dependencies["skill_refs"]:
            skill_id = skill.replace('-', '_')
            diagram += f"    {skill_id}[{skill}]\n"
            diagram += f"    {main_node} -->|uses| {skill_id}\n"
        
        # Add tools
        for tool in self.dependencies["tool_refs"]:
            tool_id = tool.replace('-', '_')
            diagram += f"    {tool_id}(({tool}))\n"
            diagram += f"    {main_node} -.->|requires| {tool_id}\n"
        
        # Add files
        for file_ref in self.dependencies["existing_files"]:
            file_id = file_ref["ref"].replace('.', '_').replace('-', '_')
            diagram += f"    {file_id}[{file_ref['ref']}]\n"
            diagram += f"    {main_node} -->|includes| {file_id}\n"
        
        return diagram
    
    def generate_html_visualization(self) -> str:
        """Generate HTML visualization"""
        graph_data = self.generate_dependency_graph()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dependency Graph - {self.skill_path.name}</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
        #graph {{ width: 100vw; height: 100vh; }}
        .info {{ position: absolute; top: 20px; left: 20px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h2 {{ margin-top: 0; color: #667eea; }}
        .legend {{ margin-top: 10px; }}
        .legend-item {{ display: flex; align-items: center; margin: 5px 0; }}
        .dot {{ width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }}
    </style>
</head>
<body>
    <div id="graph"></div>
    <div class="info">
        <h2>🔗 Dependency Graph</h2>
        <p>Skill: <strong>{self.skill_path.name}</strong></p>
        <div class="legend">
            <div class="legend-item"><div class="dot" style="background:#667eea"></div>Main Skill</div>
            <div class="legend-item"><div class="dot" style="background:#48bb78"></div>Other Skill</div>
            <div class="legend-item"><div class="dot" style="background:#ed8936"></div>Tool</div>
            <div class="legend-item"><div class="dot" style="background:#a0aec0"></div>File</div>
        </div>
    </div>
    <script>
        const nodes = new vis.DataSet({json.dumps(graph_data['nodes'])});
        const edges = new vis.DataSet({json.dumps(graph_data['edges'])});
        
        const container = document.getElementById('graph');
        const data = {{ nodes: nodes, edges: edges }};
        
        const options = {{
            nodes: {{
                shape: 'box',
                font: {{ size: 14 }},
                borderWidth: 2,
                shadow: true
            }},
            edges: {{
                width: 2,
                shadow: true,
                smooth: {{ type: 'continuous' }},
                arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }}
            }},
            physics: {{
                stabilization: false,
                barnesHut: {{
                    gravitationalConstant: -2000,
                    springConstant: 0.04,
                    springLength: 200
                }}
            }},
            groups: {{
                main: {{ color: {{ background: '#667eea', border: '#5a67d8' }}, font: {{ color: 'white' }} }},
                skill: {{ color: {{ background: '#48bb78', border: '#38a169' }} }},
                tool: {{ color: {{ background: '#ed8936', border: '#dd6b20' }} }},
                file: {{ color: {{ background: '#a0aec0', border: '#718096' }} }}
            }}
        }};
        
        new vis.Network(container, data, options);
    </script>
</body>
</html>"""
        
        return html
    
    def run(self):
        """Run full analysis"""
        print("="*60)
        print("🔗 Dependency Analyzer v3.3")
        print("="*60)
        print(f"\n📦 Skill: {self.skill_path.name}")
        
        skill_md = self.skill_path / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8')
            
            print("\n🔍 Analyzing...")
            self.analyze_skill_references(content)
            self.analyze_tool_references(content)
            self.analyze_file_references(content)
            self.check_actual_files()
        
        # Generate reports
        self._save_reports()
        
        # Print summary
        self._print_summary()
    
    def _save_reports(self):
        """Save analysis reports"""
        # JSON report
        json_path = self.skill_path / ".dependency_analysis.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.dependencies, f, indent=2)
        
        # Mermaid diagram
        mermaid_path = self.skill_path / ".dependency_graph.mmd"
        with open(mermaid_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_mermaid_diagram())
        
        # HTML visualization
        html_path = self.skill_path / ".dependency_graph.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_html_visualization())
        
        print(f"\n📄 Reports saved:")
        print(f"   • JSON: {json_path}")
        print(f"   • Mermaid: {mermaid_path}")
        print(f"   • HTML: {html_path}")
    
    def _print_summary(self):
        """Print analysis summary"""
        print("\n📊 Summary:")
        print(f"   Skill References: {len(self.dependencies['skill_refs'])}")
        print(f"   Tool Dependencies: {len(self.dependencies['tool_refs'])}")
        print(f"   File References: {len(self.dependencies['file_refs'])}")
        print(f"   Missing Files: {len(self.dependencies.get('missing_files', []))}")
        
        if self.dependencies['skill_refs']:
            print(f"\n🔗 Referenced Skills:")
            for skill in self.dependencies['skill_refs']:
                print(f"   • {skill}")
        
        if self.dependencies['tool_refs']:
            print(f"\n🛠️  Required Tools:")
            for tool in self.dependencies['tool_refs']:
                print(f"   • {tool}")
        
        if self.dependencies.get('missing_files'):
            print(f"\n⚠️  Missing Files:")
            for file in self.dependencies['missing_files']:
                print(f"   • {file}")

def main():
    parser = argparse.ArgumentParser(description='Analyze skill dependencies')
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('--visualize', '-v', action='store_true', help='Open HTML visualization')
    
    args = parser.parse_args()
    
    analyzer = DependencyAnalyzer(args.skill_path)
    analyzer.run()
    
    if args.visualize:
        html_path = Path(args.skill_path) / ".dependency_graph.html"
        import webbrowser
        webbrowser.open(f"file://{html_path.absolute()}")
        print(f"\n🌐 Opened: {html_path}")

if __name__ == "__main__":
    main()
