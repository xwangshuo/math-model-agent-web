"""
模拟竞赛训练 API — 启动模拟、获取状态、提交阶段成果
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from services.simulation import (
    start_simulation,
    get_session,
    submit_phase,
    get_all_phases,
    get_phase_tasks,
)

router = APIRouter(prefix="/api/simulation", tags=["模拟竞赛"])


# ─── Schemas ──────────────────────────────────────────


class StartSimulationRequest(BaseModel):
    problem_ids: List[str]
    hours: int = 72


class PhaseInfo(BaseModel):
    id: str
    name: str
    label: str
    order: int
    allocated_hours: int
    started_at: int
    tasks: List[str]
    completed: bool = False


class SimulationProblem(BaseModel):
    id: str
    title: str
    description: str = ""


class SimulationSession(BaseModel):
    id: str
    problems: List[SimulationProblem]
    total_hours: int
    started_at: int
    current_phase: int
    phases: List[PhaseInfo]
    submissions: dict = {}
    status: str


class SimulationSubmitRequest(BaseModel):
    phase: str
    content: str


class SubmitResponse(BaseModel):
    success: bool
    session_id: str
    phase: str
    submission_count: int
    next_phase: Optional[str] = None
    status: str


class PhaseDescription(BaseModel):
    id: str
    name: str
    label: str
    hours: int
    order: int
    tasks: List[str]
    description: str
    role_focus: dict


class PhaseListResponse(BaseModel):
    phases: List[PhaseDescription]


# ─── Routes ───────────────────────────────────────────


@router.post("/start", response_model=SimulationSession)
async def start(req: StartSimulationRequest):
    """开始一场模拟竞赛，返回包含阶段分配的会话信息"""
    try:
        session = start_simulation(req.problem_ids, req.hours)
        return SimulationSession(**session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/phases", response_model=PhaseListResponse)
async def list_phases():
    """获取所有阶段的描述和任务列表"""
    phases = get_all_phases()
    return PhaseListResponse(phases=[PhaseDescription(**p) for p in phases])


@router.get("/{session_id}", response_model=SimulationSession)
async def get_simulation(session_id: str):
    """获取当前模拟会话的完整状态"""
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="模拟会话不存在")
    return SimulationSession(**session)


@router.post("/{session_id}/submit", response_model=SubmitResponse)
async def submit(session_id: str, req: SimulationSubmitRequest):
    """提交某个阶段的成果，自动推进到下一阶段"""
    result = submit_phase(session_id, req.phase, req.content)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error", "提交失败"))
    return SubmitResponse(**result)
