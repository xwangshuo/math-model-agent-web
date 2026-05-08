import uuid
import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from models.schemas import (
    SessionListResponse, SessionSummary,
    SessionSaveRequest, SessionSaveResponse,
    SessionLoadResponse,
    ModelListResponse, ModelInfo,
    UploadResponse,
)
from services import session_manager, file_handler, ai_service

router = APIRouter(tags=["系统"])

ALLOWED_EXTENSIONS = {".csv", ".xls", ".xlsx"}


# ─── 会话 ─────────────────────────────────────────────


@router.get("/api/sessions", response_model=SessionListResponse)
async def list_sessions():
    sessions = session_manager.list_sessions()
    return SessionListResponse(sessions=[SessionSummary(**s) for s in sessions])


@router.post("/api/sessions", response_model=SessionSaveResponse)
async def save_session(req: SessionSaveRequest):
    sid = session_manager.save_session(req.messages, req.model, req.title, req.session_id)
    title = req.title or "未命名会话"
    if not req.title and req.messages:
        for m in req.messages:
            if m.get("role") == "user":
                title = m["content"][:40]
                break
    return SessionSaveResponse(session_id=sid, title=title)


@router.get("/api/sessions/{session_id}", response_model=SessionLoadResponse)
async def load_session(session_id: str):
    data = session_manager.load_session(session_id)
    if data is None:
        raise HTTPException(status_code=404, detail="会话不存在")
    return SessionLoadResponse(**data)


@router.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    if session_manager.delete_session(session_id):
        return {"status": "ok", "message": "已删除"}
    raise HTTPException(status_code=404, detail="会话不存在")


# ─── 文件上传 ─────────────────────────────────────────


@router.post("/api/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件格式: {ext}，仅支持 CSV/Excel")

    content = await file.read()
    saved_path = file_handler.save_uploaded_file(content, file.filename or "upload")
    analysis = file_handler.analyze_data_file(saved_path)

    return UploadResponse(
        file_path=saved_path,
        filename=file.filename or "upload",
        analysis=analysis,
    )


# ─── 模型列表 ─────────────────────────────────────────


@router.get("/api/models", response_model=ModelListResponse)
async def list_models():
    models = ai_service.AVAILABLE_MODELS
    return ModelListResponse(
        models=[ModelInfo(id=m["id"], name=m["name"], provider=m["provider"]) for m in models]
    )
