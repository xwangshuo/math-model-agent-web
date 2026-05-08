"""
优秀论文库 — 历年国赛/美赛获奖论文结构与分析
"""

import json, os
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "excellent_papers.json")

_cache: Optional[list[dict]] = None


def _load() -> list[dict]:
    global _cache
    if _cache is None:
        path = DATA_FILE
        if not os.path.exists(path):
            path = os.path.join(os.getcwd(), "data", "excellent_papers.json")
        with open(path, "r", encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def get_all() -> list[dict]:
    """返回论文列表（不含详细分析内容）"""
    papers = []
    for p in _load():
        card = {k: v for k, v in p.items()
                if k not in ("structure", "innovation", "key_lessons", "scoring_analysis")}
        papers.append(card)
    return papers


def get_paper(paper_id: str) -> Optional[dict]:
    """返回单篇论文完整信息"""
    for p in _load():
        if p["id"] == paper_id:
            return p
    return None


def get_filters() -> dict:
    all_p = _load()
    return {
        "years": sorted(set(p["year"] for p in all_p), reverse=True),
        "competitions": sorted(set(p["competition"] for p in all_p)),
        "awards": sorted(set(p["award"] for p in all_p)),
    }


def search(keyword: str = "", competition: str = "", year: int = 0) -> list[dict]:
    results = _load()
    if keyword:
        kw = keyword.lower()
        results = [
            p for p in results
            if kw in p["problem"].lower()
            or kw in p["abstract"].lower()
            or kw in p["team"].lower()
            or any(kw in h.lower() for h in p.get("highlights", []))
        ]
    if competition:
        results = [p for p in results if p["competition"] == competition.upper()]
    if year:
        results = [p for p in results if p["year"] == year]
    # 返回不含详细分析的版本
    return [{k: v for k, v in p.items()
             if k not in ("structure", "innovation", "key_lessons", "scoring_analysis")}
            for p in results]
