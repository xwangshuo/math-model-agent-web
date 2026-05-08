"""
团队角色分配 API — 分析团队、获取预设角色
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from services.team_advisor import analyze_team, get_predefined_roles

router = APIRouter(prefix="/api/team", tags=["团队顾问"])


# ─── Schemas ──────────────────────────────────────────


class TeamMember(BaseModel):
    name: str
    strengths: List[str]
    preferences: str = ""


class TeamAnalysisRequest(BaseModel):
    members: List[TeamMember]


class MemberRole(BaseModel):
    role: str
    reason: str
    tasks: List[str]


class TeamAnalysisResponse(BaseModel):
    roles: Dict[str, MemberRole]
    collaboration_tips: List[str]
    risk_warnings: List[str]


class RoleResponsibility(BaseModel):
    id: str
    name: str
    description: str
    responsibilities: List[str]
    required_skills: List[str]


class RoleListResponse(BaseModel):
    roles: List[RoleResponsibility]


# ─── Routes ───────────────────────────────────────────


@router.post("/analyze", response_model=TeamAnalysisResponse)
async def analyze(req: TeamAnalysisRequest):
    """分析团队成员能力和偏好，推荐最佳角色分配"""
    try:
        members = [m.model_dump() for m in req.members]
        result = analyze_team(members)
        return TeamAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/roles", response_model=RoleListResponse)
async def list_roles():
    """获取预设的团队角色定义和职责说明"""
    roles = get_predefined_roles()
    return RoleListResponse(roles=[RoleResponsibility(**r) for r in roles])
