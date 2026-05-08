"""
选题决策工具 — 分析赛题匹配度，辅助选题
"""

from typing import Optional

# 难度等级说明
DIFFICULTY_INFO = {
    "A": {"label": "A（最难）", "desc": "通常为物理/几何类，数学推导量大，无现成数据"},
    "B": {"label": "B（中等）", "desc": "需要一定建模技巧，可能有部分数据"},
    "C": {"label": "C（较易）", "desc": "通常提供大表数据，偏数据分析和优化"},
}

# 各类别题目的特征
CATEGORY_PROFILES = {
    "几何/物理": {
        "requires": ["空间想象能力", "物理直觉", "数学推导", "数值计算"],
        "data_needed": "通常无数据或提供公式",
        "good_for": ["物理/数学专业背景", "擅长理论推导"],
        "bad_for": ["数据科学背景", "不擅长数学公式"],
    },
    "优化": {
        "requires": ["运筹学基础", "编程能力", "算法设计"],
        "data_needed": "大表数据或模拟数据",
        "good_for": ["计算机/工科背景", "掌握线性规划/整数规划"],
        "bad_for": ["理论推导能力弱", "不熟悉优化求解器"],
    },
    "统计/分类": {
        "requires": ["统计学基础", "数据分析", "机器学习"],
        "data_needed": "小表或大表数据",
        "good_for": ["统计/数据科学背景", "会用 Python 数据分析库"],
        "bad_for": ["没有数据处理经验", "不熟悉统计检验"],
    },
    "评价": {
        "requires": ["综合评价方法", "指标体系设计", "权重确定"],
        "data_needed": "中等量数据",
        "good_for": ["管理/社科背景", "熟悉 AHP/TOPSIS"],
        "bad_for": ["需要客观数据支撑", "主观评价经验不足"],
    },
    "预测": {
        "requires": ["时间序列分析", "预测方法", "模型评估"],
        "data_needed": "时间序列数据",
        "good_for": ["有数据分析基础", "熟悉预测模型"],
        "bad_for": ["数据量不足", "不懂时间序列方法"],
    },
    "概率/优化": {
        "requires": ["概率论", "随机过程", "模拟方法"],
        "data_needed": "无需数据或自行生成",
        "good_for": ["统计/数学背景", "熟悉蒙特卡洛"],
        "bad_for": ["概率基础薄弱", "不擅长随机模拟"],
    },
}


def analyze_selection(
    problems: list[dict],
    team_strengths: list[str],
    preferred_category: str = "",
    hours_available: int = 72,
) -> dict:
    """分析多个题目的选题建议

    Args:
        problems: 候选题目列表
        team_strengths: 团队优势列表，如 ["数据分析", "优化算法", "数学推导"]
        preferred_category: 偏好类别
        hours_available: 可用时间（小时）

    Returns:
        包含每道题评分 + 推荐排序的 dict
    """
    strength_keywords = [s.lower() for s in team_strengths]

    scored = []
    for p in problems:
        score = _score_problem(p, strength_keywords, preferred_category, hours_available)
        scored.append(score)

    scored.sort(key=lambda x: x["total_score"], reverse=True)

    # 生成对比结论
    conclusions = _generate_conclusions(scored, team_strengths)

    return {
        "rankings": scored,
        "conclusions": conclusions,
        "top_pick": scored[0] if scored else None,
    }


def _score_problem(
    p: dict, strengths: list[str], preferred: str, hours: int
) -> dict:
    """给一道题打分"""
    details = {}
    total = 0

    # 1. 类别匹配 (0-30分)
    category = p.get("category", "")
    profile = CATEGORY_PROFILES.get(category, {})
    category_score = 15  # 默认中等
    if preferred and preferred.lower() in category.lower():
        category_score = 30
    elif any(s in category.lower() for s in strengths):
        category_score = 25
    details["category_match"] = {"score": category_score, "max": 30, "note": f"类别: {category}"}
    total += category_score

    # 2. 能力匹配 (0-30分)
    required = profile.get("requires", [])
    match_count = sum(1 for r in required if any(s in r.lower() for s in strengths))
    ability_score = min(30, match_count * 10)
    details["ability_match"] = {"score": ability_score, "max": 30, "note": f"匹配 {match_count}/{len(required)} 项能力"}
    total += ability_score

    # 3. 数据可得性 (0-20分)
    data_type = p.get("data_type", "")
    if "大表" in data_type:
        data_score = 20
    elif "小表" in data_type or "提供" in data_type:
        data_score = 15
    elif "模拟" in data_type:
        data_score = 12
    elif "自行" in data_type or "收集" in data_type:
        data_score = 5
    else:
        data_score = 10
    details["data_availability"] = {"score": data_score, "max": 20, "note": f"数据: {data_type}"}
    total += data_score

    # 4. 难度与时间 (0-20分)
    diff = p.get("difficulty", "B")
    if diff == "A":
        time_score = 5 if hours < 72 else 15
    elif diff == "B":
        time_score = 15
    else:  # C
        time_score = 20
    details["time_feasibility"] = {"score": time_score, "max": 20, "note": f"难度 {diff}, 时间 {hours}h"}
    total += time_score

    return {
        "problem_id": p["id"],
        "title": p.get("title", ""),
        "label": p.get("label", ""),
        "competition": p.get("competition", ""),
        "year": p.get("year", ""),
        "category": category,
        "difficulty": p.get("difficulty", ""),
        "description": p.get("description", "")[:100],
        "data_type": data_type,
        "total_score": total,
        "details": details,
    }


def _generate_conclusions(scored: list, strengths: list) -> str:
    if not scored:
        return "没有候选题目可供分析。"

    top = scored[0]
    s = f"## 📊 选题分析结论\n\n"
    s += f"**推荐选题**: {top['competition']} {top['year']} {top['label']}「{top['title']}」\n"
    s += f"**综合评分**: {top['total_score']}/100\n\n"
    s += f"### 评分明细\n\n"
    for k, v in top["details"].items():
        bar = "█" * (v["score"] // 2) + "░" * ((v["max"] - v["score"]) // 2)
        s += f"- {v['note']}: {bar} {v['score']}/{v['max']}\n"

    s += f"\n### 团队优势利用\n"
    s += f"你的团队优势: {', '.join(strengths)}\n"
    if top["total_score"] >= 70:
        s += f"✅ 该题与你的团队匹配度较高，推荐选择。\n"
    elif top["total_score"] >= 50:
        s += f"⚠️ 该题有一定挑战，但可以尝试。\n"
    else:
        s += f"❌ 该题匹配度较低，建议考虑其他题目。\n"

    # 对比
    if len(scored) > 1:
        s += f"\n### 多题对比\n\n"
        for i, item in enumerate(scored[:3]):
            s += f"{'🥇' if i==0 else '🥈' if i==1 else '🥉'} **{item['title']}** — {item['total_score']}分\n"
            if i > 0:
                diff = scored[0]["total_score"] - item["total_score"]
                s += f"   与第一名相差 {diff} 分\n"
    return s
