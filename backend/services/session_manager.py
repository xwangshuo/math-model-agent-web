"""
会话管理 — JSON 文件持久化
"""

import os
import json
import uuid
import time
from pathlib import Path

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"


def _ensure_dir():
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def list_sessions() -> list[dict]:
    """返回所有会话摘要列表，按时间倒序"""
    _ensure_dir()
    sessions = []
    for f in sorted(SESSIONS_DIR.iterdir(), key=os.path.getmtime, reverse=True):
        if f.suffix == ".json":
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                sessions.append({
                    "id": f.stem,
                    "title": data.get("title", "未命名会话"),
                    "model": data.get("model", ""),
                    "message_count": len(data.get("messages", [])),
                    "created_at": data.get("created_at", 0),
                    "updated_at": data.get("updated_at", 0),
                })
            except (json.JSONDecodeError, OSError):
                continue
    return sessions


def save_session(messages: list, model: str, title: str = "", session_id: str = "") -> str:
    """保存会话，返回 session_id"""
    _ensure_dir()
    if not session_id:
        session_id = str(uuid.uuid4())[:8]
    if not title and messages:
        # 用第一条用户消息做标题
        for m in messages:
            if m.get("role") == "user":
                title = m["content"][:40]
                break
    if not title:
        title = "未命名会话"

    now = int(time.time())
    data = {
        "id": session_id,
        "title": title,
        "model": model,
        "messages": messages,
        "created_at": now,
        "updated_at": now,
    }

    path = SESSIONS_DIR / f"{session_id}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return session_id


def load_session(session_id: str) -> dict | None:
    """加载单个会话，返回完整数据或 None"""
    path = SESSIONS_DIR / f"{session_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def delete_session(session_id: str) -> bool:
    """删除会话，成功返回 True"""
    path = SESSIONS_DIR / f"{session_id}.json"
    if path.exists():
        path.unlink()
        return True
    return False
