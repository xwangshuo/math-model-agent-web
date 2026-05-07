from fastapi import APIRouter, HTTPException
from models.schemas import PaperRequest, PaperResponse
from services.ai_service import AIService
from services.latex_service import get_template

router = APIRouter(prefix="/api/paper", tags=["论文排版"])
ai_service = AIService()

@router.post("/generate", response_model=PaperResponse)
async def generate_paper(req: PaperRequest):
    try:
        prompt = f"""请生成数学建模竞赛论文的LaTeX内容。

标题: {req.title}
摘要: {req.abstract}
章节内容:
{chr(10).join([f"### {s['heading']}nn{s['content']}" for s in req.sections])}

请将以上内容组织成符合数学建模竞赛论文规范的完整LaTeX代码。
以以下JSON格式回复：
{{
  "latex": "完整LaTeX代码",
  "preview": "Markdown预览版本（用于网页展示）"
}}"""
        reply = ai_service.chat(prompt, [], "paper")
        import json, re
        json_match = re.search(r'\{.*\}', reply, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return PaperResponse(**data)
        # Fallback: use template and fill with AI content
        template = get_template(req.template)
        return PaperResponse(
            latex=template,
            preview=reply
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
