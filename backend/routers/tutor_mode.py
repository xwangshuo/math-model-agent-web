"""
角色导师模式 API — 角色对话、模式列表
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from services.tutor_mode import tutor_chat, get_available_modes

router = APIRouter(prefix="/api/tutor", tags=["导师模式"])


# ─── Schemas ──────────────────────────────────────────


class TutorChatRequest(BaseModel):
    message: str
    history: List[dict] = []
    mode: str = "coach"
    context: str = ""


class TutorChatResponse(BaseModel):
    reply: str


class TutorModeInfo(BaseModel):
    id: str
    name: str
    description: str
    icon: str


class TutorModeListResponse(BaseModel):
    modes: List[TutorModeInfo]


# ─── Routes ───────────────────────────────────────────


@router.post("/chat", response_model=TutorChatResponse)
async def chat_with_tutor(req: TutorChatRequest):
    """以指定导师角色进行对话"""
    try:
        reply = tutor_chat(req.message, req.history, req.mode, req.context)
        return TutorChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/modes", response_model=TutorModeListResponse)
async def list_tutor_modes():
    """获取所有可用的导师角色和描述"""
    modes = get_available_modes()
    return TutorModeListResponse(modes=[TutorModeInfo(**m) for m in modes])
