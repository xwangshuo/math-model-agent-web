"""
代码解释与调试助手 — 分析数学建模代码的数学含义、参数调优、常见错误
"""
import json
import re
from typing import Optional
from services.ai_service import AIService

CODE_EXPLAINER_SYSTEM_PROMPT = """你是一个数学建模代码分析专家。用户会提供一段数学建模相关的代码，你需要分析：

1. **explanation_by_section** — 将代码按功能分成多个片段，解释每个片段的数学含义
2. **parameter_tuning** — 代码中关键参数的含义和调优建议
3. **common_errors** — 这段代码可能出现的常见错误、原因和修复方法
4. **dependencies** — 代码依赖的 Python 包列表

请严格按照以下 JSON 格式返回，不要包含其他内容：
{
  "explanation_by_section": [
    {"code_snippet": "代码片段", "math_meaning": "数学含义解释"}
  ],
  "parameter_tuning": "参数调优建议",
  "common_errors": [
    {"error": "错误描述", "cause": "原因", "fix": "修复方法"}
  ],
  "dependencies": ["numpy", "scipy"]
}
"""

ai_service = AIService()


def explain_code(code: str, language: str = "python", problem_context: str = "") -> dict:
    """分析代码，返回逐段解释、参数调优建议、常见错误和依赖列表"""
    prompt = f"""请分析以下 {language} 代码：

## 代码
```{language}
{code}
```
"""
    if problem_context:
        prompt += f"\n## 问题背景\n{problem_context}\n"

    prompt += """
请按要求的 JSON 格式返回分析结果。
"""

    reply = ai_service.chat(
        prompt,
        [],
        max_tokens=4096,
        system_prompt=CODE_EXPLAINER_SYSTEM_PROMPT,
    )

    json_match = re.search(r"\{.*\}", reply, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    return {
        "explanation_by_section": [{"code_snippet": code[:200], "math_meaning": reply[:500]}],
        "parameter_tuning": "无法解析 AI 返回结果，请重试。",
        "common_errors": [{"error": "解析失败", "cause": "AI 返回了非 JSON 格式", "fix": "重新提问"}],
        "dependencies": [],
    }
