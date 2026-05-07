# 数模竞赛智能体 — 构建方案

## 技术栈
- **后端**: FastAPI + Python
- **前端**: React + Vite (或 Vue3)
- **AI**: 调用大模型 API (支持多模型切换)
- **部署**: Docker 一键部署

## 功能模块

### 1. 选题分析
- 上传赛题/输入题目描述
- AI分析题目类型（优化/统计/预测/评价等）
- 给出难度评估、推荐方向

### 2. 模型推荐
- 根据题目特征推荐数学模型
- 显示模型原理、适用场景、优缺点对比

### 3. 代码生成
- 自动生成模型求解代码（Python）
- 支持可视化图表生成
- 代码解释 + 可直接运行

### 4. 论文排版
- 生成 LaTeX 论文模板
- 自动填充内容
- 导出 PDF

### 5. 对话式解题
- 类似 ChatGPT 的对话界面
- 上传附件（数据文件、图片）
- 历史会话管理

## 项目结构
```
math-model-agent/
├── backend/
│   ├── main.py              # FastAPI 入口
│   ├── routers/             # API 路由
│   ├── services/            # AI 服务逻辑
│   ├── models/              # 数据模型
│   └── templates/           # LaTeX 模板
├── frontend/
│   ├── src/
│   │   ├── pages/           # 页面
│   │   ├── components/      # 组件
│   │   └── api/             # API 调用
│   └── ...
└── docker-compose.yml
```
