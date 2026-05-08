"""
模型知识库 API — 知识卡片列表 + 详情
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from services import model_knowledge

router = APIRouter(prefix="/api/model-knowledge", tags=["模型知识库"])


# ─── Schemas ──────────────────────────────────────────

class ModelCardSummary(BaseModel):
    id: str
    name: str
    category: str
    icon: str
    tags: List[str]
    summary: str
    applicable_scenarios: List[str]
    pros: List[str]
    cons: List[str]
    python_packages: List[str]


class ModelCardDetail(ModelCardSummary):
    math_principles: str
    code_template: str
    common_errors: list


class KnowledgeListResponse(BaseModel):
    models: List[ModelCardSummary]
    categories: List[str]
    total: int


# ─── Routes ───────────────────────────────────────────


@router.get("", response_model=KnowledgeListResponse)
async def list_models(category: str = ""):
    """
    获取模型知识库列表，可按类别筛选
    """
    if category:
        models = model_knowledge.get_models_by_category(category)
    else:
        models = model_knowledge.get_all_models()

    categories = model_knowledge.get_categories()
    return KnowledgeListResponse(
        models=[ModelCardSummary(**m) for m in models],
        categories=categories,
        total=len(models),
    )


@router.get("/{model_id}", response_model=ModelCardDetail)
async def get_model_detail(model_id: str):
    """获取单个模型的完整详情（含数学原理、代码模板）"""
    card = model_knowledge.get_model_by_id(model_id)
    if not card:
        raise HTTPException(status_code=404, detail="模型不存在")
    return ModelCardDetail(**card)


@router.get("/categories/list")
async def list_categories():
    """获取所有模型类别"""
    return {"categories": model_knowledge.get_categories()}
