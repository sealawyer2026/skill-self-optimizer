# Skill Optimizer Hub

**全球首个 Skill 自优化与迭代升级平台**

基于 Google 5 种设计模式的 Agent Skill 自动分析、诊断、优化工具。

---

## 🎯 核心功能

### 1. 自动分析 (Auto-Analysis)
```bash
python scripts/analyze_skill.py /path/to/your/skill
```
- 100分制质量评分
- 检测设计模式覆盖
- 识别触发条件问题
- 检查内容质量

### 2. 智能优化 (Smart Optimization)
```bash
python scripts/optimize_skill.py /path/to/your/skill --output ./optimized
```
- 自动应用 Google 5 种设计模式
- 修复识别的问题
- 版本号自动升级
- 生成优化日志

### 3. 一键升级 (One-Click Upgrade)
```bash
python scripts/auto_optimize.py /path/to/your/skill --output ./optimized
```
分析 + 优化一步完成，自动生成对比报告。

---

## 🎨 Google 5 种设计模式

| 模式 | 用途 | 优化效果 |
|-----|------|---------|
| **Tool Wrapper** | 工具包装 | Agent 秒变专家 |
| **Generator** | 模板生成 | 输出标准化 |
| **Reviewer** | 检查清单 | 质量保证 |
| **Inversion** | 需求澄清 | 减少误解 |
| **Orchestrator** | 技能编排 | 工作流优化 |

---

## 📊 评分标准

| 指标 | 权重 | 说明 |
|-----|------|------|
| 元数据质量 | 25% | 名称、描述、触发条件 |
| 内容质量 | 25% | 可操作性、清晰度 |
| 简洁度 | 25% | SKILL.md < 2500 词 |
| 模式覆盖 | 25% | 5 种模式覆盖数 |

**评分等级：**
- 90-100：优秀，适合发布
- 80-89：良好，小幅改进
- 70-79：及格，需要优化
- <70：不合格，需重写

---

## 🚀 快速开始

### 安装
```bash
git clone https://github.com/你的用户名/skill-optimizer-hub.git
cd skill-optimizer-hub
```

### 优化你的第一个 Skill
```bash
# 一键优化
python scripts/auto_optimize.py /path/to/your/skill --output ./optimized

# 查看优化报告
cat ./optimized/.optimization_summary.json
```

---

## 📁 项目结构

```
skill-optimizer-hub/
├── scripts/
│   ├── analyze_skill.py          # 分析诊断
│   ├── optimize_skill.py         # 自动优化
│   └── auto_optimize.py          # 一键优化
├── references/
│   ├── design-patterns.md        # 5种模式详解
│   ├── optimization-checklist.md # 发布前检查清单
│   └── examples.md               # 真实案例
├── assets/
│   └── optimization-report-template.md  # 报告模板
├── SKILL.md                      # 本Skill定义
└── README.md                     # 本文件
```

---

## 📖 使用案例

### 案例1：修复触发问题
```bash
# 用户反馈："我的pdf-processor经常在错误场景触发"
python scripts/auto_optimize.py ./pdf-processor --output ./pdf-processor-v2

# 结果：触发准确率 65% → 94%
```

### 案例2：应用设计模式
```bash
# 当前Skill缺少结构，需要优化
python scripts/optimize_skill.py ./my-skill \
  --patterns "generator,reviewer" \
  --output ./my-skill-v2
```

### 案例3：预发布检查
```bash
# 发布前最终检查
python scripts/analyze_skill.py ./my-skill --strict
# 必须通过所有检查才能发布
```

---

## 🔧 高级用法

### 批量优化
```bash
# 优化目录下所有技能
for skill in ./skills/*/; do
  python scripts/auto_optimize.py "$skill" --output "${skill}-optimized"
done
```

### 持续集成
```yaml
# .github/workflows/optimize.yml
name: Skill Optimization
on: [push]
jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Analyze Skills
        run: python scripts/analyze_skill.py ./skills --strict
```

---

## 📈 迭代升级工作流

```
使用Skill → 收集反馈 → 运行分析 → 发现问题
                                    ↓
发布v2 ← 测试验证 ← 生成优化版 ← 应用模式
```

**定期优化触发条件：**
- 评分 < 90 分
- 用户投诉 > 3 次/周
- 任务完成率 < 85%
- 30 天未优化

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- 基于 [Google Agent Skill Design Patterns](https://example.com)
- 灵感来自 OpenClaw 社区

---

**作者：** 张海洋  
**版本：** 1.0.0  
**更新日期：** 2026-03-20
