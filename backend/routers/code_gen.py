from fastapi import APIRouter, HTTPException
from models.schemas import CodeGenRequest, CodeGenResponse
from services.ai_service import AIService

router = APIRouter(prefix="/api/code", tags=["代码生成"])
ai_service = AIService()

@router.post("/generate", response_model=CodeGenResponse)
async def generate_code(req: CodeGenRequest):
    try:
        prompt = f"""请生成数学建模求解代码，每段代码都要附带数学含义解释：

选用模型: {req.model_name}
问题描述: {req.problem_description}
数据说明: {req.data_description or '未提供'}
特殊要求: {', '.join(req.requirements) if req.requirements else '无'}

请生成完整的Python代码，格式要求：
1. **数据导入与预处理** — 如果是标准化/归一化，说明为什么需要
2. **模型求解核心代码** — 每段代码前加注释说明：
   - 📝 数学含义：这段代码对应什么数学公式/步骤
   - ⚙️ 参数可调：哪些参数可以改变，改变后对结果有什么影响
   - ⚠️ 常见错误：这个步骤容易出什么问题
3. **结果可视化** — 解释每个图表展示的是什么信息
4. **参数调优建议** — 如果数据量变化、数据分布变化，应该怎么调整参数

以以下JSON格式回复：
{{
  "code": "完整Python代码（含教学注释）",
  "explanation": "代码说明和用法（包含数学模型的原理解释）",
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
