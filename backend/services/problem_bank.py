"""
历年赛题数据库 — CUMCM / MCM / ICM 真题（2015-2025）
从 JSON 文件加载，支持全文检索
"""

import json, os
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "problems_data.json")


def _load_all() -> list[dict]:
    """从 JSON 文件加载所有赛题"""
    path = DATA_FILE
    if not os.path.exists(path):
        # fallback: try relative to cwd
        path = os.path.join(os.getcwd(), "data", "problems_data.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# 在模块级别缓存，避免每次请求都读磁盘
_PROBLEM_CACHE: Optional[list[dict]] = None


def _get_all() -> list[dict]:
    global _PROBLEM_CACHE
    if _PROBLEM_CACHE is None:
        _PROBLEM_CACHE = _load_all()
    return _PROBLEM_CACHE


def search_problems(
    keyword: str = "",
    competition: str = "",
    year: int = 0,
    category: str = "",
    difficulty: str = "",
) -> list[dict]:
    """按条件搜索赛题（仅返回元信息，不含 content）"""
    results = _get_all()
    if keyword:
        kw = keyword.lower()
        results = [
            p for p in results
            if kw in p["title"].lower()
            or kw in p["description"].lower()
            or kw in p["category"].lower()
            or any(kw in t.lower() for t in p.get("tags", []))
            or any(kw in m.lower() for m in p.get("models", []))
        ]
    if competition:
        results = [p for p in results if p["competition"] == competition.upper()]
    if year:
        results = [p for p in results if p["year"] == year]
    if category:
        results = [p for p in results if category.lower() in p["category"].lower()]
    if difficulty:
        results = [p for p in results if p["difficulty"] == difficulty.upper()]
    return results


def get_problem(problem_id: str) -> Optional[dict]:
    for p in _get_all():
        if p["id"] == problem_id:
            return {k: v for k, v in p.items() if k != "content"}
    return None


def get_problem_content(problem_id: str) -> Optional[str]:
    """获取赛题原题全文"""
    for p in _get_all():
        if p["id"] == problem_id:
            return p.get("content", "")
    return None


def get_filters() -> dict:
    all_p = _get_all()
    years = sorted(set(p["year"] for p in all_p), reverse=True)
    competitions = sorted(set(p["competition"] for p in all_p))
    categories = sorted(set(p["category"] for p in all_p))
    difficulties = sorted(set(p["difficulty"] for p in all_p))
    return {
        "years": years,
        "competitions": competitions,
        "categories": categories,
        "difficulties": difficulties,
    }


def generate_reading_template(title: str, description: str) -> str:
    """生成题目速读模板"""
    return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 题目速读卡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📌 核心问题（一句话概括）
{title}
{description[:200]}

## 🔍 已知条件
- 数据提供情况：_______________
- 约束条件：_______________
- 目标函数/评价标准：_______________

## 🎯 问题类型判断
□ 优化类  □ 预测类  □ 评价类  □ 统计类  □ 分类/聚类
□ 微分方程  □ 几何/物理  □ 网络/图论
→ 判断依据：_______________

## 📊 数据特征分析
- 数据量：_______________ 行 × _______________ 列
- 缺失值情况：_______________
- 数据类型（数值/类别/文本/时序）：_______________

## 🧩 可能的模型（按优先级排序）
1. _______________
2. _______________
3. _______________

## 📋 任务分解
□ 任务 1：_______________
□ 任务 2：_______________
□ 任务 3：_______________
□ 任务 4：_______________

## ⚠️ 难点与风险
- 计算量：□ 大  □ 中  □ 小
- 数据获取难度：□ 难  □ 中  □ 易
- 模型复杂度：□ 高  □ 中  □ 低
- 论文创新点要求：□ 高  □ 中  □ 低

## 💡 初步思路
_______________

## ⏰ 时间规划建议
- 数据预处理：________ 小时
- 模型建立：________ 小时
- 代码调试：________ 小时
- 结果分析：________ 小时
- 论文写作：________ 小时
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
