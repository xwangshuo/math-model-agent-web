from pydantic import BaseModel
from typing import Optional, List

# === Chat ===
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []
    mode: str = "chat"  # chat | analysis | recommend | code | paper

class ChatResponse(BaseModel):
    reply: str
    mode: str

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

class ModelInfo(BaseModel):
    name: str
    type: str
    description: str
    applicable_scenarios: List[str]
    pros: List[str]
    cons: List[str]
    code_template: str = ""

class RecommendResponse(BaseModel):
    models: List[ModelInfo]
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
    sections: List[dict]  # [{"heading": "...", "content": "..."}]
    template: str = "simple"  # simple | detailed

class PaperResponse(BaseModel):
    latex: str
    preview: str
