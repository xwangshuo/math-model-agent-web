from fastapi import APIRouter, HTTPException
from models.schemas import CodeGenRequest, CodeGenResponse
from services.ai_service import AIService

router = APIRouter(prefix="/api/code", tags=["代码生成"])
ai_service = AIService()

@router.post("/generate", response_model=CodeGenResponse)
async def generate_code(req: CodeGenRequest):
    try:
        prompt = f"""请生成数学建模求解代码：

选用模型: {req.model_name}
问题描述: {req.problem_description}
数据说明: {req.data_description or '未提供'}
特殊要求: {', '.join(req.requirements) if req.requirements else '无'}

请生成完整的Python代码，包含：
1. 数据导入与预处理
2. 模型求解核心代码
3. 结果可视化
4. 详细中文注释

以以下JSON格式回复：
{{
  "code": "完整Python代码（字符串）",
  "explanation": "代码说明和用法",
  "dependencies": ["numpy", "pandas", "matplotlib", ...]
}}"""
        reply = ai_service.chat(prompt, [], max_tokens=2048, system_prompt="你是一个数学建模代码生成专家。生成可直接运行的Python代码，返回JSON格式。")
        import json, re
        json_match = re.search(r'\{.*\}', reply, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return CodeGenResponse(**data)
        return CodeGenResponse(code=reply, explanation="", dependencies=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
