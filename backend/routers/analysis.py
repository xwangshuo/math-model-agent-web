from fastapi import APIRouter, HTTPException
from models.schemas import AnalysisRequest, AnalysisResponse
from services.ai_service import AIService

router = APIRouter(prefix="/api/analysis", tags=["选题分析"])
ai_service = AIService()

@router.post("", response_model=AnalysisResponse)
async def analyze(req: AnalysisRequest):
    try:
        prompt = f"""请分析以下数学建模竞赛题目：

题目标题: {req.title or '（未提供）'}
题目描述: {req.description}
上下文: {req.context or '（无）'}

请按以下格式回复（JSON格式）：
{{
  "problem_type": "题目类型",
  "difficulty": "难度评估（简单/中等/困难）",
  "direction": "解题方向",
  "analysis": "详细分析（500字左右）",
  "suggestions": ["建议1", "建议2", "建议3"]
}}"""
        reply = ai_service.chat(prompt, [], max_tokens=1024, system_prompt="你是一个数学建模竞赛助手。请根据问题直接回答，返回JSON格式。")
        # Try to parse JSON from response
        import json
        import re
        json_match = re.search(r'\{.*\}', reply, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return AnalysisResponse(**data)
        return AnalysisResponse(
            problem_type="未识别",
            difficulty="未知",
            direction="无法分析",
            analysis=reply,
            suggestions=["请重新描述题目"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
