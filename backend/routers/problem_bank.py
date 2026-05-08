"""
赛题库 + 选题决策 + 速读模板 API
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

from services import problem_bank, topic_selector

router = APIRouter(tags=["赛题库与选题"])


# ─── 请求/响应 Schemas ────────────────────────────────

class ProblemItem(BaseModel):
    id: str
    year: int
    competition: str
    label: str
    title: str
    category: str
    difficulty: str
    description: str
    models: List[str]
    tags: List[str]
    data_type: str


class ProblemListResponse(BaseModel):
    problems: List[ProblemItem]
    total: int
    filters: dict


class SelectionRequest(BaseModel):
    problem_ids: List[str]
    team_strengths: List[str] = ["数据分析", "编程", "数学推导"]
    preferred_category: str = ""
    hours_available: int = 72


class SelectionResponse(BaseModel):
    rankings: list
    conclusions: str
    top_pick: Optional[dict]


class ReadingTemplateRequest(BaseModel):
    title: str
    description: str


class ReadingTemplateResponse(BaseModel):
    template: str


class AnalysisByAIRequest(BaseModel):
    problem_ids: List[str]
    description: str = ""


# ─── 路由 ─────────────────────────────────────────────


@router.get("/api/problem-bank", response_model=ProblemListResponse)
async def list_problems(
    keyword: str = "",
    competition: str = "",
    year: int = Query(default=0),
    category: str = "",
    difficulty: str = "",
):
    """搜索历年赛题"""
    results = problem_bank.search_problems(keyword, competition, year, category, difficulty)
    filters = problem_bank.get_filters()
    return ProblemListResponse(
        problems=[ProblemItem(**p) for p in results],
        total=len(results),
        filters=filters,
    )


@router.get("/api/problem-bank/{problem_id}", response_model=ProblemItem)
async def get_problem(problem_id: str):
    p = problem_bank.get_problem(problem_id)
    if not p:
        raise HTTPException(status_code=404, detail="赛题不存在")
    return ProblemItem(**p)


@router.post("/api/topic-selection/analyze", response_model=SelectionResponse)
async def analyze_selection(req: SelectionRequest):
    """选题决策分析"""
    problems = []
    for pid in req.problem_ids:
        p = problem_bank.get_problem(pid)
        if p:
            problems.append(p)

    if not problems:
        raise HTTPException(status_code=400, detail="未找到有效的赛题 ID")

    result = topic_selector.analyze_selection(
        problems=problems,
        team_strengths=req.team_strengths,
        preferred_category=req.preferred_category,
        hours_available=req.hours_available,
    )
    return SelectionResponse(**result)


@router.get("/api/problem-bank/{problem_id}/reading-template", response_model=ReadingTemplateResponse)
async def get_reading_template(problem_id: str):
    """生成题目速读模板"""
    p = problem_bank.get_problem(problem_id)
    if not p:
        raise HTTPException(status_code=404, detail="赛题不存在")
    template = problem_bank.generate_reading_template(p["title"], p["description"])
    return ReadingTemplateResponse(template=template)


@router.post("/api/topic-selection/reading-template", response_model=ReadingTemplateResponse)
async def generate_reading_template(req: ReadingTemplateRequest):
    """根据自定义题目生成速读模板"""
    template = problem_bank.generate_reading_template(req.title, req.description)
    return ReadingTemplateResponse(template=template)
