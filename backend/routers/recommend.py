from fastapi import APIRouter, HTTPException
from models.schemas import RecommendRequest, RecommendResponse, ModelInfo
from services.ai_service import AIService

router = APIRouter(prefix="/api/recommend", tags=["模型推荐"])
ai_service = AIService()

@router.post("", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    try:
        prompt = f"""根据以下数学建模题目信息，推荐最适合的数学模型：

题目类型: {req.problem_type}
题目描述: {req.description}
数据特征: {req.data_features or '未提供'}

请按以下JSON格式回复（至少推荐3个模型）：
{{
  "models": [
    {{
      "name": "模型名称（如：灰色预测模型GM(1,1)）",
      "type": "模型类别（如：预测类）",
      "description": "核心原理简述",
      "applicable_scenarios": ["场景1", "场景2"],
      "pros": ["优点1", "优点2"],
      "cons": ["缺点1", "缺点2"],
      "code_template": "核心代码片段"
    }}
  ],
  "recommended": "最推荐的模型名称",
  "reason": "推荐理由"
}}"""
        reply = ai_service.chat(prompt, [], "recommend")
        import json, re
        json_match = re.search(r'\{.*\}', reply, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return RecommendResponse(**data)
        return RecommendResponse(
            models=[],
            recommended="",
            reason=reply
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
