import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="数模竞赛智能体",
    description="数学建模竞赛全流程辅助工具 - 选题分析、模型推荐、代码生成、论文排版",
    version="1.0.0"
)

# CORS - allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
from routers.chat import router as chat_router
from routers.analysis import router as analysis_router
from routers.recommend import router as recommend_router
from routers.code_gen import router as code_router
from routers.paper import router as paper_router
from routers.system import router as system_router
from routers.data_analysis import router as data_router
from routers.problem_bank import router as problem_router
from routers.model_knowledge import router as model_knowledge_router
from routers.excellent_papers import router as papers_router
from routers.code_explainer import router as code_explainer_router
from routers.simulation import router as simulation_router
from routers.tutor_mode import router as tutor_router
from routers.team_advisor import router as team_router

app.include_router(chat_router)
app.include_router(analysis_router)
app.include_router(recommend_router)
app.include_router(code_router)
app.include_router(paper_router)
app.include_router(system_router)
app.include_router(data_router)
app.include_router(problem_router)
app.include_router(model_knowledge_router)
app.include_router(papers_router)
app.include_router(code_explainer_router)
app.include_router(simulation_router)
app.include_router(tutor_router)
app.include_router(team_router)


@app.get("/api/health")
async def health():
    import sys
    return {"status": "ok", "version": "1.0.0", "python": sys.executable}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
