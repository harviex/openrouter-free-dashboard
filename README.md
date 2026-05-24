# OpenRouter Free Models Dashboard 🤖

一个类似 [CanIRun.ai](https://www.canirun.ai) 风格的 OpenRouter 免费模型仪表板，每日自动更新，支持卡片式浏览、筛选、排序和一键复制模型 ID。

## 在线访问

**https://harviex.github.io/openrouter-free-dashboard/**

## 功能特性

- 🎨 **卡片式布局**：参考 CanIRun.ai 的深色主题设计
- 📊 **实时数据**：每日自动从 OpenRouter API 获取最新免费模型
- 🔍 **智能筛选**：按提供商、功能（Tools / Vision / Reasoning）筛选
- 📏 **灵活排序**：按上下文长度、名称、创建时间、参数数量排序
- 📋 **一键复制**：点击卡片或按钮快速复制模型 ID
- 📱 **响应式设计**：支持桌面和移动设备
- 🔄 **自动更新**：GitHub Actions 每日自动更新数据并部署
- 🌐 **多语言支持**：EN / 中文切换

## 数据说明

### 来源
- **API**：[OpenRouter Models API](https://openrouter.ai/docs/api-reference/models/get-models)
- **频率**：每日 UTC 00:00 自动更新（GitHub Actions）
- **数据文件**：`data/models.json`

### 数据格式

```json
{
  "last_updated": "2026-04-28 12:00:00 UTC",
  "total_models": 30,
  "total_providers": 10,
  "providers": ["Google", "Meta", "NVIDIA", ...],
  "models": [
    {
      "id": "google/gemma-4-31b-it:free",
      "name": "Google Gemma 4 31B",
      "provider": "Google",
      "context_length": 262000,
      "has_tools": true,
      "has_vision": true,
      "has_reasoning": false,
      "pricing_prompt": 0,
      "pricing_completion": 0,
      "created": 1777300000
    }
  ]
}
```

## 本地运行

### 1. 克隆仓库

```bash
git clone https://github.com/harviex/openrouter-free-dashboard.git
cd openrouter-free-dashboard
```

### 2. 获取数据

```bash
mkdir -p data
python fetch_models.py
```

### 3. 启动本地服务器

```bash
python -m http.server 8000
```

然后访问 `http://localhost:8000`

## 项目结构

```
├── .github/workflows/    # GitHub Actions 自动更新工作流
├── data/
│   ├── models.json       # 模型数据（自动生成）
│   └── models/           # 详细模型参数数据
├── docs/                 # 额外文档
├── index.html            # 主页面
├── script.js             # 前端逻辑
├── style.css             # 主样式
├── additions.css         # 补充样式
├── fetch_models.py       # 数据抓取脚本
├── add_parameters.py     # 模型参数补充脚本
├── scripts_update.py     # 脚本更新工具
├── DOCUMENTATION.md      # 详细文档
└── README.md             # 本文件
```

## GitHub Actions 工作流程

- **定时任务**：每日 UTC 00:00 自动运行 `fetch_models.py`
- **手动触发**：支持通过 GitHub Actions 页面手动运行
- **自动部署**：数据更新后自动部署到 GitHub Pages

## 技术栈

- **前端**：纯 HTML/CSS/JavaScript（无框架依赖）
- **数据**：Python 脚本从 OpenRouter API 获取
- **部署**：GitHub Pages
- **自动化**：GitHub Actions（`.github/workflows/update.yml`）

## 设计灵感

本项目的设计风格参考了 [CanIRun.ai](https://www.canirun.ai) 的：
- 深色主题配色
- 卡片式布局
- 简洁的信息展示
- 流畅的交互动画

## 更新日志

- **2026-05**：多语言支持（EN/中文）、参数排序、Grid/List 视图切换
- **2026-04**：初版上线，卡片式布局、筛选、一键复制

## License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

- GitHub Issues：[提交问题](https://github.com/harviex/openrouter-free-dashboard/issues)
- OpenRouter：[官网](https://openrouter.ai)

---

**⚡ 由 [Hermes Agent (小爱玛)](https://hermes-agent.nousresearch.com) 创建并维护**
