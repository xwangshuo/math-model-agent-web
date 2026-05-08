"""
代码解释与调试助手 API — 分析数学建模代码
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.code_explainer import explain_code

router = APIRouter(prefix="/api/code", tags=["代码解释"])


# ─── Schemas ──────────────────────────────────────────


class CodeExplainRequest(BaseModel):
    code: str
    language: str = "python"
    problem_context: str = ""


class CodeSectionExplanation(BaseModel):
    code_snippet: str
    math_meaning: str


class CommonError(BaseModel):
    error: str
    cause: str
    fix: str


class CodeExplainResponse(BaseModel):
    explanation_by_section: List[CodeSectionExplanation]
    parameter_tuning: str
    common_errors: List[CommonError]
    dependencies: List[str]


# ─── Routes ───────────────────────────────────────────


@router.post("/explain", response_model=CodeExplainResponse)
async def explain_code_endpoint(req: CodeExplainRequest):
    """分析数学建模代码，返回逐段解释、参数调优、常见错误和依赖"""
    try:
        result = explain_code(req.code, req.language, req.problem_context)
        return CodeExplainResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
