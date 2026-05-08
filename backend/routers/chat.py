import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from models.schemas import ChatRequest, ChatResponse
from services.ai_service import AIService

router = APIRouter(prefix="/api/chat", tags=["对话"])
ai_service = AIService()


@router.post("/stream")
async def chat_stream(req: ChatRequest):
    """SSE 流式聊天端点"""

    async def event_generator():
        events = ai_service.chat_stream(
            message=req.message,
            history=req.history,
            model_id=req.model,
            uploaded_file=req.file_path,
        )
        for event in events:
            yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("", response_model=ChatResponse)
async def chat_sync(req: ChatRequest):
    """非流式兼容端点（收集所有文本后一次性返回）"""
    try:
        full_text = ""
        for event in ai_service.chat_stream(
            message=req.message,
            history=req.history,
            model_id=req.model,
            uploaded_file=req.file_path,
        ):
            if event["type"] == "text":
                full_text += event["content"]
            elif event["type"] == "error":
                raise HTTPException(status_code=500, detail=event["content"])
        return ChatResponse(reply=full_text or "抱歉，我暂时无法回答这个问题。")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
