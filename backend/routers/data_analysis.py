"""
数据分析路由 — EDA / 异常值检测 / 缺失值分析（直接调用沙箱）
"""

import json
import base64
import tempfile
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from services import sandbox, data_tools

router = APIRouter(prefix="/api/data", tags=["数据分析"])


class AnalysisRequest(BaseModel):
    file_path: str
    analysis_type: str  # "eda" | "outlier" | "missing"
    method: Optional[str] = "iqr"  # for outlier: iqr / zscore / iforest


class AnalysisResponse(BaseModel):
    output: str
    figures: list  # base64 列表
    code: str  # 生成的代码（调试用）


@router.post("/analyze", response_model=AnalysisResponse)
async def run_analysis(req: AnalysisRequest):
    """一键数据分析"""
    import os
    if not os.path.exists(req.file_path):
        raise HTTPException(status_code=400, detail=f"文件不存在: {req.file_path}")

    # 生成代码
    if req.analysis_type == "eda":
        code = data_tools.generate_eda_code(req.file_path)
    elif req.analysis_type == "outlier":
        code = data_tools.generate_outlier_detection_code(req.file_path, req.method or "iqr")
    elif req.analysis_type == "missing":
        code = data_tools.generate_missing_value_code(req.file_path)
    else:
        raise HTTPException(status_code=400, detail=f"未知分析类型: {req.analysis_type}")

    # 执行
    result = sandbox.run_python_code(code, timeout=60)

    # Debug: print raw stdout
    import logging
    logging.warning(f"Raw result: success={result['success']}, output_len={len(result['output'])}, figures={len(result['figures'])}")

    if not result["success"]:
        return AnalysisResponse(
            output=f"❌ 分析执行失败:\n{result['error']}",
            figures=[],
            code=code,
        )

    return AnalysisResponse(
        output=result["output"],
        figures=result["figures"],
        code=code,
    )
