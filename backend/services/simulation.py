"""
模拟竞赛训练 — 模拟真实竞赛流程，分阶段推进
无 AI 核心逻辑，纯数据结构驱动
"""
import uuid
import time
from typing import Optional
from services import problem_bank

# ─── 阶段定义 ──────────────────────────────────────────

PHASES = [
    {
        "id": "day1",
        "name": "选题分析",
        "label": "Day 1 — 选题分析",
        "hours": 24,
        "order": 1,
        "tasks": [
            "通读所有候选题目，理解问题背景和要求",
            "分析每道题的类型（优化/预测/评价/统计等）",
            "评估团队能力与各题的匹配度",
            "初步确定选题，进行文献调研",
            "明确已知条件和数据特征",
            "制定初步解题思路和任务分解",
        ],
        "description": "第一天的主要任务是快速浏览所有题目，结合团队优势做出选题决策，并理解问题本质。"
    },
    {
        "id": "day2",
        "name": "建模求解",
        "label": "Day 2 — 建模求解",
        "hours": 32,
        "order": 2,
        "tasks": [
            "建立数学模型（公式推导、变量定义）",
            "编写求解代码并进行调试",
            "进行数据预处理和分析",
            "运行模型并收集结果",
            "进行灵敏度分析和模型验证",
            "结果可视化（图表生成）",
        ],
        "description": "第二天是建模和求解的核心阶段，需要完成模型建立、编码实现和结果分析。"
    },
    {
        "id": "day3",
        "name": "论文写作",
        "label": "Day 3 — 论文写作",
        "hours": 16,
        "order": 3,
        "tasks": [
            "整理模型结果和图表",
            "撰写论文摘要和关键词",
            "撰写问题重述和模型假设",
            "撰写模型建立和求解过程",
            "撰写结果分析和模型评价",
            "撰写结论和改进方向",
            "全文排版、检查格式和参考文献",
        ],
        "description": "第三天专注于论文写作和排版，将建模成果转化为规范的竞赛论文。"
    },
]

# 角色分工建议
PHASE_ROLES = {
    "day1": {"leader": "建模手", "focus": "问题分析 + 文献调研"},
    "day2": {"leader": "编程手", "focus": "代码实现 + 结果分析"},
    "day3": {"leader": "写作手", "focus": "论文撰写 + 排版规范"},
}

# ─── Session 存储（内存，生产环境应改用 Redis/DB） ──────

_sessions: dict = {}


# ─── 核心逻辑 ──────────────────────────────────────────


def get_phase_tasks(phase_id: str) -> Optional[dict]:
    """获取指定阶段的详细任务"""
    for p in PHASES:
        if p["id"] == phase_id:
            return {**p, "role_focus": PHASE_ROLES.get(phase_id, {})}
    return None


def get_all_phases() -> list[dict]:
    """获取所有阶段描述"""
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "label": p["label"],
            "hours": p["hours"],
            "order": p["order"],
            "tasks": p["tasks"],
            "description": p["description"],
            "role_focus": PHASE_ROLES.get(p["id"], {}),
        }
        for p in sorted(PHASES, key=lambda x: x["order"])
    ]


def start_simulation(problem_ids: list[str], hours: int = 72) -> dict:
    """开始一场模拟竞赛"""
    problems = []
    for pid in problem_ids:
        p = problem_bank.get_problem(pid)
        if p:
            problems.append(p)

    if not problems:
        problems = problem_bank.search_problems(limit=3)
        if not problems:
            problems = [{"id": "unknown", "title": "模拟赛题", "description": "请从题库选择题目"}]

    session_id = str(uuid.uuid4())[:8]
    now = int(time.time())

    # 按时间比例分配各阶段
    phase_allocation = _allocate_time(hours, len(PHASES))

    session = {
        "id": session_id,
        "problems": problems,
        "total_hours": hours,
        "started_at": now,
        "current_phase": 0,
        "phases": [],
        "submissions": {},
        "status": "running",
    }

    for i, p in enumerate(PHASES):
        session["phases"].append({
            "id": p["id"],
            "name": p["name"],
            "label": p["label"],
            "order": p["order"],
            "allocated_hours": phase_allocation[i],
            "started_at": now + sum(phase_allocation[:i]) * 3600,
            "tasks": p["tasks"],
            "completed": False,
        })

    _sessions[session_id] = session
    return session


def submit_phase(session_id: str, phase_id: str, content: str) -> dict:
    """提交某一阶段的成果"""
    session = _sessions.get(session_id)
    if not session:
        return {"error": "模拟会话不存在", "success": False}

    if phase_id not in session["submissions"]:
        session["submissions"][phase_id] = []

    submission = {
        "phase_id": phase_id,
        "content": content,
        "submitted_at": int(time.time()),
    }
    session["submissions"][phase_id].append(submission)

    # 标记阶段完成
    for p in session["phases"]:
        if p["id"] == phase_id:
            p["completed"] = True
            break

    # 推进到下一阶段
    for i, p in enumerate(session["phases"]):
        if p["id"] == phase_id:
            if i + 1 < len(session["phases"]):
                session["current_phase"] = i + 1
            else:
                session["status"] = "completed"
            break

    return {
        "success": True,
        "session_id": session_id,
        "phase": phase_id,
        "submission_count": len(session["submissions"][phase_id]),
        "next_phase": session["phases"][session["current_phase"]]["id"]
        if session["current_phase"] < len(session["phases"])
        else None,
        "status": session["status"],
    }


def get_session(session_id: str) -> Optional[dict]:
    """获取模拟会话状态"""
    return _sessions.get(session_id)


def _allocate_time(total_hours: int, num_phases: int) -> list[int]:
    """根据预设比例分配各阶段时间"""
    ratios = [p["hours"] for p in PHASES]
    total_ratio = sum(ratios)
    allocation = [max(1, int(total_hours * r / total_ratio)) for r in ratios]
    # 调整余量
    diff = total_hours - sum(allocation)
    if diff > 0:
        allocation[-1] += diff
    return allocation
