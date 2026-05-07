from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.ai_service import AIService

router = APIRouter(prefix="/api/chat", tags=["对话"])
ai_service = AIService()

@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        reply = ai_service.chat(req.message, req.history, req.mode)
        return ChatResponse(reply=reply, mode=req.mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
