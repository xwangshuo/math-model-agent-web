"""
团队角色分配顾问 — 根据团队成员的能力和偏好，推荐角色分配
"""
import json
import re
from services.ai_service import AIService

# ─── 预设角色定义 ──────────────────────────────────────

PREDEFINED_ROLES = [
    {
        "id": "modeler",
        "name": "建模手",
        "description": "负责数学模型的建立和推导",
        "responsibilities": [
            "分析题目，确定问题类型和建模方向",
            "建立数学模型（公式推导、变量定义、假设条件）",
            "将模型转化为可编程的算法描述",
            "撰写模型建立和理论分析的论文部分",
        ],
        "required_skills": ["数学推导", "问题分析", "文献调研", "模型创新"],
    },
    {
        "id": "programmer",
        "name": "编程手",
        "description": "负责代码实现和数据分析",
        "responsibilities": [
            "将数学模型转化为可运行的代码",
            "数据预处理和特征工程",
            "模型求解、参数调优和结果可视化",
            "灵敏度分析和模型验证",
        ],
        "required_skills": ["Python编程", "数据分析", "算法实现", "可视化"],
    },
    {
        "id": "writer",
        "name": "写作手",
        "description": "负责论文撰写和排版",
        "responsibilities": [
            "论文结构设计和整体行文把控",
            "撰写摘要、问题重述和结论",
            "图表排版和格式规范",
            "全文校对和 LaTeX 排版",
        ],
        "required_skills": ["写作能力", "LaTeX排版", "图表设计", "时间管理"],
    },
]

TEAM_ADVISOR_SYSTEM_PROMPT = """你是一位数学建模竞赛团队管理专家。根据团队成员的特点分析最佳角色分配。

## 角色说明
- **建模手**: 负责问题分析、数学推导、模型建立。需要数学推导能力、问题分析能力。
- **编程手**: 负责代码实现、数据处理、可视化。需要Python编程、数据分析能力。
- **写作手**: 负责论文撰写、排版、图表。需要写作能力、LaTeX排版、图表设计能力。

## 分析要求
根据每个成员的技能特长和个人偏好，推荐最适合的角色，并说明理由。同时给出团队协作建议和潜在风险。

请严格按照以下 JSON 格式返回，不要包含其他内容：
{
  "roles": {
    "成员名": {
      "role": "建模手/编程手/写作手",
      "reason": "推荐理由",
      "tasks": ["该成员在此角色下的主要任务1", "任务2"]
    }
  },
  "collaboration_tips": ["协作建议1", "协作建议2"],
  "risk_warnings": ["潜在风险1", "潜在风险2"]
}
"""

ai_service = AIService()


def get_predefined_roles() -> list[dict]:
    """获取预设的角色定义"""
    return PREDEFINED_ROLES


def analyze_team(members: list[dict]) -> dict:
    """分析团队成员，推荐角色分配

    Args:
        members: 成员列表，每项包含 name, strengths (list[str]), preferences (str)

    Returns:
        包含角色分配、协作建议和风险警告的 dict
    """
    members_text = "\n".join(
        [
            f"- {m['name']}: 擅长 {', '.join(m.get('strengths', []))}，偏好 {m.get('preferences', '未说明')}"
            for m in members
        ]
    )

    prompt = f"""请分析以下数学建模竞赛团队成员，推荐最佳角色分配：

## 团队成员
{members_text}

请严格按照 JSON 格式返回分析结果。
"""

    reply = ai_service.chat(
        prompt,
        [],
        max_tokens=4096,
        system_prompt=TEAM_ADVISOR_SYSTEM_PROMPT,
    )

    json_match = re.search(r"\{.*\}", reply, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # 解析失败时的兜底
    roles = {}
    for m in members:
        roles[m["name"]] = {
            "role": "待定",
            "reason": "AI 分析失败，请手动分配",
            "tasks": ["待补充"],
        }

    return {
        "roles": roles,
        "collaboration_tips": ["建议团队先讨论彼此优势，再手动分配角色"],
        "risk_warnings": ["AI 分析结果不可用，建议人工复核"],
    }
