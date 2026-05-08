"""
优秀论文库 API
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

from services import excellent_papers

router = APIRouter(tags=["优秀论文库"])


class PaperCard(BaseModel):
    id: str
    year: int
    competition: str
    problem: str
    award: str
    team: str
    abstract: str
    highlights: List[str]
    chart_quality: str
    code_quality: str


class PaperFull(PaperCard):
    structure: dict
    innovation: List[str]
    scoring_analysis: dict
    key_lessons: List[str]


class PaperListResponse(BaseModel):
    papers: List[PaperCard]
    total: int
    filters: dict


@router.get("/api/papers", response_model=PaperListResponse)
async def list_papers(
    keyword: str = "",
    competition: str = "",
    year: int = Query(default=0),
):
    """获取优秀论文列表"""
    results = excellent_papers.search(keyword, competition, year)
    filters = excellent_papers.get_filters()
    return PaperListResponse(
        papers=[PaperCard(**p) for p in results],
        total=len(results),
        filters=filters,
    )


@router.get("/api/papers/{paper_id}", response_model=PaperFull)
async def get_paper(paper_id: str):
    """获取单篇论文详情"""
    p = excellent_papers.get_paper(paper_id)
    if not p:
        raise HTTPException(status_code=404, detail="论文不存在")
    return PaperFull(**p)
