# 🧮 数模智能体 Web 版

> 数学建模竞赛全流程辅助工具 — FastAPI + React 全栈应用

Gradio 版的升级版本。后端 FastAPI 提供 REST API + SSE 流式聊天，前端 React + Vite 构建的双栏交互界面。

---

## 🚀 快速开始

### 前置条件

- Python 3.10+
- Node.js 18+
- OpenRouter API Key（或 DeepSeek / GLM 等）

### 1. 启动后端

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 编辑 .env，配置 API Key
cp .env.example .env
# 填入 OPENROUTER_API_KEY=sk-or-...

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

### 3. 访问

浏览器打开 `http://localhost:5173`

---

## ✨ 功能

### 💬 对话解题
- SSE 流式聊天，逐 token 显示
- 支持 Tool Calling：LLM 可调用代码沙箱执行 Python
- 一键 EDA / 异常值检测 / 缺失值分析
- 中断控制（AbortController）
- 多模型切换（DeepSeek / GLM / Qwen / GPT-4o Mini）

### 🎯 选题决策
从历年赛题库中筛选候选题目，填入团队优势，系统自动打分排序。

评分维度：
- 类别匹配（30分）— 题目类别是否匹配团队偏好
- 能力匹配（30分）— 团队优势能否覆盖题目所需能力
- 数据可得性（20分）— 有现成数据加分
- 时间可行性（20分）— 难度与可用时间匹配度

支持预设配置一键切换：数据分析型 / 理论推导型 / 编程实现型 / 综合型

### 📚 历年赛题库
内置 23 道 CUMCM / MCM / ICM 真题（2020-2024）。

支持按竞赛、年份、类别、难度、关键词筛选。点击题目查看详情和推荐模型。

### 📖 题目速读模板
点击任意赛题生成结构化分析卡，包含：
核心问题 → 已知条件 → 问题类型判断 → 数据特征分析 → 推荐模型 → 任务分解 → 难点风险评估 → 时间规划建议

也支持自定义题目生成模板。

### 🔍 选题分析 / 🎯 模型推荐 / 💻 代码生成 / 📄 论文排版
保留的独立功能模块，通过侧边栏切换。

---

## 🏗 项目结构

```
math-model-agent-web/
├── backend/
│   ├── main.py               # FastAPI 入口
│   ├── .env.example          # 环境变量模板
│   ├── routers/
│   │   ├── chat.py           # SSE 流式聊天
│   │   ├── analysis.py       # 选题分析
│   │   ├── recommend.py      # 模型推荐
│   │   ├── code_gen.py       # 代码生成
│   │   ├── paper.py          # 论文排版
│   │   ├── system.py         # 会话管理 / 文件上传 / 模型列表
│   │   ├── data_analysis.py  # 一键 EDA / 异常值检测
│   │   └── problem_bank.py   # 赛题库 / 选题决策 / 速读模板
│   ├── services/
│   │   ├── ai_service.py     # LLM 路由 + Streaming + Tool Calling
│   │   ├── sandbox.py        # 代码沙箱（subprocess 隔离）
│   │   ├── file_handler.py   # 文件上传与数据分析
│   │   ├── data_tools.py     # EDA / 异常值 / 缺失值代码生成
│   │   ├── session_manager.py # 会话持久化
│   │   ├── problem_bank.py   # 历年赛题数据库
│   │   ├── topic_selector.py # 选题决策引擎
│   │   └── latex_service.py  # LaTeX 论文模板
│   └── models/
│       └── schemas.py        # Pydantic 数据模型
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # 应用主入口 + 侧边栏导航
│   │   ├── main.tsx          # React 挂载
│   │   ├── pages/
│   │   │   ├── ChatPage.tsx      # 对话页面
│   │   │   ├── TopicSelection.tsx # 选题决策页面
│   │   │   └── ProblemBank.tsx   # 赛题库 + 速读模板页面
│   │   ├── api/
│   │   │   └── client.ts     # 所有 API 调用
│   │   └── styles.css        # 全局样式
│   ├── package.json
│   └── vite.config.ts
└── docker-compose.yml
```

---

## 🔧 技术栈

| 层 | 选型 |
|----|------|
| 后端框架 | FastAPI (Python) |
| 前端框架 | React 18 + TypeScript |
| 构建工具 | Vite 5 |
| LLM 接口 | OpenAI SDK + OpenRouter |
| 代码沙箱 | subprocess 子进程隔离 |
| 数据分析 | Pandas + NumPy + SciPy |
| 可视化 | Matplotlib + Seaborn |
| 样式 | 纯 CSS（无第三方 UI 库） |
| 部署 | Docker Compose 可选 |

---

## 📌 注意事项

- 首次启动需在 `.env` 中配置 `OPENROUTER_API_KEY`
- 代码执行默认 30 秒超时
- 会话数据保存在 `backend/sessions/` 目录下
- 上传文件保存在 `backend/uploads/` 目录下
- 前端开发模式下 API 代理到 `localhost:8000`
