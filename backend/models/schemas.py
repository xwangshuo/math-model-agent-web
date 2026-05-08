from pydantic import BaseModel
from typing import Optional, List


# === 聊天 ===
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []
    model: str = "deepseek/deepseek-chat-v3.1"
    file_path: str = ""


class ChatResponse(BaseModel):
    reply: str


# === 会话 ===
class SessionSummary(BaseModel):
    id: str
    title: str
    model: str
    message_count: int
    created_at: int
    updated_at: int


class SessionListResponse(BaseModel):
    sessions: List[SessionSummary]


class SessionSaveRequest(BaseModel):
    messages: List[dict]
    model: str
    title: str = ""
    session_id: str = ""


class SessionSaveResponse(BaseModel):
    session_id: str
    title: str


class SessionLoadResponse(BaseModel):
    id: str
    title: str
    model: str
    messages: List[dict]
    created_at: int
    updated_at: int


# === 上传 ===
class UploadResponse(BaseModel):
    file_path: str
    filename: str
    analysis: str


# === 模型 ===
class ModelInfo(BaseModel):
    id: str
    name: str
    provider: str


class ModelListResponse(BaseModel):
    models: List[ModelInfo]


# === 选题分析 ===
class AnalysisRequest(BaseModel):
    title: str = ""
    description: str
    context: str = ""


class AnalysisResponse(BaseModel):
    problem_type: str
    difficulty: str
    direction: str
    analysis: str
    suggestions: List[str]


# === 模型推荐 ===
class RecommendRequest(BaseModel):
    problem_type: str
    description: str
    data_features: str = ""


class ModelInfoDetail(BaseModel):
    name: str
    type: str
    description: str
    applicable_scenarios: List[str]
    pros: List[str]
    cons: List[str]
    code_template: str = ""


class RecommendResponse(BaseModel):
    models: List[ModelInfoDetail]
    recommended: str
    reason: str


# === 代码生成 ===
class CodeGenRequest(BaseModel):
    model_name: str
    problem_description: str
    data_description: str = ""
    requirements: List[str] = []


class CodeGenResponse(BaseModel):
    code: str
    explanation: str
    dependencies: List[str]


# === 论文排版 ===
class PaperRequest(BaseModel):
    title: str
    abstract: str
    sections: List[dict]
    template: str = "simple"


class PaperResponse(BaseModel):
    latex: str
    preview: str
