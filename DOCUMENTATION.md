# OpenRouter Free Models Dashboard - 制作文档

> 创建时间：2026-04-30  
> 最后更新：2026-05-02  
> 作者：小爱玛 (Hermes Agent) for Harvie Tse  
> 网站地址：https://harviex.github.io/openrouter-free-dashboard/

---

## 📋 项目概述

**OpenRouter Free Models Dashboard** 是一个静态网站，用于展示 OpenRouter 平台上的免费 AI 模型信息。

### 核心功能
- 📊 展示所有免费模型（`:free` 后缀）
- 🔍 搜索、过滤、排序功能
- 🌓 深色/浅色主题切换
- 🌍 三语支持（中文/英文/日文）
- 📅 显示模型创建日期、到期日
- 🔄 每日自动更新模型数据（GitHub Action）

---

## 🏗️ 技术架构

```
openrouter-free-dashboard/
├── index.html          # 主页面
├── style.css           # 主样式
├── additions.css       # 额外样式（三语、卡片优化）
├── script.js           # 核心逻辑（加载、渲染、交互）
├── fetch_models.py     # Python脚本：抓取OpenRouter API数据
├── data/
│   └── models.json     # 模型数据（自动生成）
└── .github/
    └── workflows/
        └── update-models.yml  # GitHub Action自动更新
```

### 技术栈
- **前端**：纯 HTML/CSS/JavaScript（无框架依赖）
- **数据源**：OpenRouter API (`https://openrouter.ai/api/v1/models`)
- **部署**：GitHub Pages
- **自动化**：GitHub Actions

---

## 🚀 快速开始

### 本地运行

1. **克隆仓库**
   ```bash
   git clone https://github.com/harviex/openrouter-free-dashboard.git
   cd openrouter-free-dashboard
   ```

2. **启动本地服务器**
   ```bash
   python3 -m http.server 8000
   ```
   然后访问 `http://localhost:8000`

### 更新模型数据

**方法1：手动运行**
```bash
cd ~/openrouter-free-dashboard
python3 fetch_models.py
git add data/models.json
git commit -m "Update models data"
git push origin main
```

**方法2：让 GitHub Action 自动更新**
- 每天北京时间 08:00 自动运行
- 或手动触发：仓库 → Actions → Update Models Data → Run workflow

---

## 📊 数据抓取逻辑

### fetch_models.py 工作流程

1. **调用 OpenRouter API**
   ```python
   https://openrouter.ai/api/v1/models
   ```
   获取所有模型数据（约100+个）

2. **过滤免费模型**
   - 只保留 `id` 包含 `:free` 的模型
   - 当前约 29 个免费模型

3. **提取关键信息**
   - 基本信息：name, id, provider, created
   - 技术参数：parameters, context_length
   - 功能标记：has_tools, has_vision, has_reasoning
   - 定价信息：paid_pricing（付费版价格，仅供参考）
   - 到期信息：expiration_date

4. **生成 JSON 数据**
   - 输出到 `data/models.json`
   - 包含 `last_updated` 时间戳

### 注意事项
- **费用显示已移除**：因为免费模型费用都是 $0，显示付费版价格容易引起混淆
- **请求数抓取暂未实现**：OpenRouter 页面使用动态加载，`__NEXT_DATA__` 提取暂不可用
- **HuggingFace 评分**：原计划从 HuggingFace 获取模型评分，但因 API 限制暂未实现

---

## 🎨 前端功能说明

### 排序方式
1. **最新发布**（默认）：按 `created` 时间戳降序
2. 参数量（高到低）
3. 参数量（低到高）
4. 上下文长度（高到低）
5. 上下文长度（低到高）
6. 名称（A-Z）

### 过滤功能
- **提供商过滤**：下拉菜单选择特定提供商
- **功能过滤**：工具调用、视觉、推理
- **搜索**：支持模型名称、ID、提供商搜索

### 视图切换
- **网格视图**（默认）：卡片式展示
- **列表视图**：紧凑列表展示

### 主题切换
- 自动检测系统主题
- 手动切换：🌓 按钮
- 三主题：自动/深色/浅色

---

## 🔄 GitHub Action 自动更新

### 配置文件
`.github/workflows/update-models.yml`

### 运行时间
- **北京时间每日 08:00**（UTC 00:00）
- Cron 表达式：`0 0 * * *`

### 工作流程
1. 检出仓库代码
2. 设置 Python 3.11 环境
3. 安装依赖（urllib3, requests）
4. 运行 `fetch_models.py`
5. 检测 `data/models.json` 是否有变化
6. 如有变化，自动提交并推送

### 手动触发
仓库页面 → Actions → Update Models Data → Run workflow

---

## 🛠️ 常见修改场景

### 添加新的排序方式
1. 在 `index.html` 的 `#sortBy` 下拉菜单添加选项
2. 在 `script.js` 的 `applyFilters()` 函数中添加 `case`

### 修改卡片显示内容
编辑 `script.js` 中的 `createModelCard()` 函数

### 添加新的过滤条件
1. 在 `index.html` 添加过滤控件
2. 在 `script.js` 的 `applyFilters()` 函数中添加过滤逻辑

### 修改样式
- 主样式：`style.css`
- 额外样式：`additions.css`（建议在此文件修改，避免冲突）

---

## ❓ 常见问题

### Q: 为什么费用信息不显示？
A: 免费模型费用都是 $0，显示付费版价格（$.../$.../1M）容易引起混淆，故移除。

### Q: 请求数（requests_per_day）为什么不显示？
A: OpenRouter 页面使用 Next.js 动态加载，`__NEXT_DATA__` 提取暂不可用。需要进一步研究其 API。

### Q: 如何手动更新模型数据？
A: 运行 `python3 fetch_models.py`，然后提交推送即可。

### Q: GitHub Action 失败了怎么办？
A: 
1. 检查 Actions 页面的错误日志
2. 常见原因：网络超时、API 限流
3. 可手动触发重新运行

### Q: 如何修改自动更新时间？
A: 编辑 `.github/workflows/update-models.yml` 中的 cron 表达式：
- 北京时间 08:00 = UTC 00:00 → `0 0 * * *`
- 北京时间 20:00 = UTC 12:00 → `0 12 * * *`

---

## 📝 版本历史

### v3 (2026-05-02)
- ✅ 移除费用显示
- ✅ 移除请求数显示（暂不可用）
- ✅ "最新发布" 设为默认排序
- ✅ 设置 GitHub Action 自动更新（北京时间每日8点）
- ✅ 添加三语支持（中文/英文/日文）

### v2 (2026-04-30)
- ✅ 添加排序功能
- ✅ 添加过滤功能
- ✅ 添加主题切换
- ✅ 添加到期日显示

### v1 (2026-04-28)
- ✅ 初始版本
- ✅ 基础卡片展示
- ✅ 搜索功能
- ✅ GitHub Pages 部署

---

## 📚 参考资料

- [OpenRouter API 文档](https://openrouter.ai/docs)
- [GitHub Pages 文档](https://pages.github.com/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [CanIRun.ai](https://www.canirun.ai) - 灵感来源

---

**制作人员**  
🤖 小爱玛 (Hermes Agent) - AI 开发助手  
👤 Harvie Tse - 项目发起人和需求方  

**联系方式**  
- GitHub: [@harviex](https://github.com/harviex)
- Twitter: [@TseHarvie](https://twitter.com/TseHarvie)
