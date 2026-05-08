"""
AI 服务 — 多模型路由 + Streaming + Tool Calling
"""

import os
import json
from openai import OpenAI

from . import sandbox as sandbox_mod
from . import file_handler as file_mod

# ─── 模型配置 ─────────────────────────────────────────

AVAILABLE_MODELS = [
    {"id": "deepseek/deepseek-chat-v3.1", "name": "DeepSeek V3.1", "provider": "DeepSeek"},
    {"id": "deepseek/deepseek-r1", "name": "DeepSeek R1", "provider": "DeepSeek"},
    {"id": "glm-4-plus", "name": "GLM-4 Plus", "provider": "智谱"},
    {"id": "qwen-turbo-latest", "name": "Qwen Turbo", "provider": "阿里云"},
    {"id": "openai/gpt-4o-mini", "name": "GPT-4o Mini", "provider": "OpenAI"},
]

# ─── 内置模型知识库 ───────────────────────────────────

_MODEL_KNOWLEDGE = {
    "灰色预测模型 GM(1,1)": {"category": "预测类", "desc": "基于灰色系统理论，适用于小样本（≥4个数据点）、贫信息、不确定系统的预测。通过累加生成序列减弱随机性。"},
    "层次分析法 (AHP)": {"category": "评价类", "desc": "将决策问题分解为目标层、准则层、方案层，通过构造两两比较判断矩阵计算权重。"},
    "TOPSIS 法": {"category": "评价类", "desc": "构造理想解和负理想解，计算各评价对象与理想解的相对贴近度进行排序。"},
    "线性规划 (LP)": {"category": "优化类", "desc": "在满足一组线性约束条件下，求解线性目标函数的最大值或最小值。"},
    "主成分分析 (PCA)": {"category": "统计降维", "desc": "通过正交变换将多个相关变量转换为少数不相关的主成分。"},
    "K-means 聚类": {"category": "机器学习", "desc": "将 n 个样本划分为 k 个簇，使得簇内样本相似度高、簇间相似度低。"},
    "Logistic 回归": {"category": "统计分类", "desc": "广义线性模型，通过 Sigmoid 函数将线性回归输出映射到 (0,1) 区间。"},
    "微分方程模型": {"category": "机理建模", "desc": "通过建立微分方程描述系统的动态变化规律。"},
}

# 知识库摘要文本
_KNOWLEDGE_INDEX = "\n\n## 📚 内置模型知识库\n"
for name, info in _MODEL_KNOWLEDGE.items():
    _KNOWLEDGE_INDEX += f"- **{name}** ({info['category']}): {info['desc'][:60]}...\n"
_KNOWLEDGE_INDEX += "\n使用 `query_model_knowledge` 工具查看各模型的完整原理、优缺点和适用场景。\n"

# ─── 系统提示词 ───────────────────────────────────────

SYSTEM_PROMPT = """你是一个专业的数学建模竞赛智能体。

## 能力
1. **问题分析** — 分析赛题类型（优化/统计/预测/评价/分类/微分方程等），给出解题思路
2. **模型推荐** — 根据问题特征推荐合适的数学模型，说明原理和适用场景
3. **代码生成与执行** — 自动生成 Python 求解代码，通过 execute_python 工具实际运行
4. **数据可视化** — 使用 matplotlib 生成专业图表
5. **论文生成** — 使用 generate_paper_latex 工具生成标准竞赛论文 LaTeX 模板
6. **模型知识库** — 使用 query_model_knowledge 查询内置的常用模型知识

## 工具使用规则
- **execute_python**: 写代码求解时使用。代码必须完整可运行，含所有 import。用 matplotlib 生成图表。
- **analyze_data**: 分析用户上传的 CSV/Excel 文件，看数据概况后再决定用什么模型。
- **generate_paper_latex**: 当用户要求生成论文/排版/LaTeX 时使用。接收标题、摘要、章节列表。
- **query_model_knowledge**: 当用户询问某模型的详细信息，或想确认模型适用条件时使用。

## 回答风格
- 先分析问题本质，再给出模型和方案
- 使用公式时用 LaTeX 格式 $$...$$
- 需要代码时用 ```python ... ``` 包裹
- 给出可操作的步骤""" + _KNOWLEDGE_INDEX

# ─── 工具定义 ─────────────────────────────────────────

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "执行 Python 代码（数学建模求解/数据分析/可视化），代码应完整可运行，包含必要 import。返回 stdout 输出和 matplotlib 图表。",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "完整可运行的 Python 代码，包含 import 语句",
                    }
                },
                "required": ["code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_data",
            "description": "分析已上传的 CSV 或 Excel 数据文件，返回数据摘要（行数、列名、统计信息等）。只有用户上传了文件后才调用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "数据文件的完整路径",
                    }
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_paper_latex",
            "description": "生成数学建模竞赛论文的完整 LaTeX 代码。包含标准模板结构（摘要、关键词、问题重述、模型假设、符号说明、模型建立、求解、分析、评价、参考文献）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "论文标题"},
                    "abstract": {"type": "string", "description": "论文摘要"},
                    "sections": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "heading": {"type": "string", "description": "章节标题"},
                                "content": {"type": "string", "description": "章节内容"},
                            },
                            "required": ["heading", "content"],
                        },
                        "description": "论文章节列表",
                    },
                },
                "required": ["title", "abstract", "sections"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_model_knowledge",
            "description": "查询内置数学建模模型知识库，获取常用模型的描述、适用场景、优缺点等信息。支持的模型包括：灰色预测GM(1,1)、层次分析法AHP、TOPSIS、线性规划、主成分分析PCA、K-means聚类、Logistic回归、微分方程模型等。",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_name": {
                        "type": "string",
                        "description": "模型名称",
                    }
                },
                "required": ["model_name"],
            },
        },
    },
]

MAX_TOOL_TURNS = 5


# ─── 辅助函数 ──────────────────────────────────────────


def _generate_latex(title: str, abstract: str, sections: list) -> str:
    secs = []
    for s in sections:
        heading = s.get("heading", "")
        content = s.get("content", "")
        secs.append(f"\\section{{{heading}}}\n{content}" if heading else content)
    return f"""\\documentclass[12pt,a4paper]{{ctexart}}
\\usepackage{{amsmath,amssymb,amsfonts,graphicx,booktabs,geometry,hyperref,float}}
\\geometry{{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}}
\\title{{\\textbf{{{title}}}}}
\\author{{}}
\\date{{}}
\\begin{{document}}
\\maketitle
\\begin{{abstract}}
{abstract}
\\end{{abstract}}
\\tableofcontents\\newpage
{chr(10).join(secs)}
\\end{{document}}"""


# ─── 工具执行 ─────────────────────────────────────────

_last_execution_figures: list = []


def get_last_figures() -> list:
    return _last_execution_figures


def execute_tool(name: str, args_str: str, uploaded_file: str = "") -> str:
    global _last_execution_figures
    _last_execution_figures = []

    try:
        args = json.loads(args_str) if isinstance(args_str, str) else args_str
    except json.JSONDecodeError:
        return f"❌ 工具参数解析失败: {args_str}"

    if name == "execute_python":
        code = args.get("code", "")
        if not code.strip():
            return "❌ 代码为空"
        result = sandbox_mod.run_python_code(code)
        _last_execution_figures = result.get("figures", [])
        if result["success"]:
            output = result["output"]
            if result["figures"]:
                output += f"\n📊 生成了 {len(result['figures'])} 张图表"
            if result["error"]:
                output += f"\n⚠️ 警告:\n{result['error']}"
            return output
        return f"❌ 执行错误:\n{result['error']}"

    elif name == "analyze_data":
        fp = args.get("file_path", uploaded_file)
        if not fp or not os.path.exists(fp):
            return f"❌ 找不到数据文件: {fp}"
        return file_mod.analyze_data_file(fp)

    elif name == "generate_paper_latex":
        latex = _generate_latex(
            args.get("title", "论文标题"),
            args.get("abstract", ""),
            args.get("sections", []),
        )
        return f"✅ LaTeX 论文已生成\n\n```latex\n{latex}\n```\n\n保存为 .tex 文件后用 XeLaTeX 编译。"

    elif name == "query_model_knowledge":
        model_name = args.get("model_name", "")
        best = None
        for key in _MODEL_KNOWLEDGE:
            if model_name.lower() in key.lower() or key.lower() in model_name.lower():
                best = key
                break
        if not best:
            return f"未找到「{model_name}」。可用模型: {'、'.join(_MODEL_KNOWLEDGE.keys())}"
        info = _MODEL_KNOWLEDGE[best]
        return f"📚 **{best}**\n**类别**: {info['category']}\n**原理**: {info['desc']}"

    return f"❌ 未知工具: {name}"


# ─── AI 服务类 ────────────────────────────────────────


class AIService:
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=60.0, max_retries=1)
        self.system_prompt = SYSTEM_PROMPT

    def get_available_models(self) -> list:
        return AVAILABLE_MODELS

    def chat(self, message: str, history: list, model_id: str = "deepseek/deepseek-chat-v3.1",
             uploaded_file: str = "", max_tokens: int = 2048, use_tools: bool = False,
             system_prompt: str = "") -> str:
        full_text = ""
        for event in self.chat_stream(message, history, model_id, uploaded_file, max_tokens, use_tools, system_prompt):
            if event["type"] == "text":
                full_text += event["content"]
            elif event["type"] == "error":
                return f"❌ {event['content']}"
        return full_text or "抱歉，我暂时无法回答。"

    def chat_stream(self, message: str, history: list, model_id: str,
                    uploaded_file: str = "", max_tokens: int = 8192,
                    use_tools: bool = True, system_prompt: str = ""):
        sp = system_prompt if system_prompt else self.system_prompt
        messages = [{"role": "system", "content": sp}]

        if uploaded_file and os.path.exists(uploaded_file):
            file_info = file_mod.analyze_data_file(uploaded_file)
            messages.append({"role": "system", "content": f"用户已上传数据文件: {uploaded_file}\n\n{file_info}"})

        for h in history[-40:]:
            if isinstance(h, dict) and "role" in h and "content" in h:
                messages.append({"role": h["role"], "content": h["content"]})

        messages.append({"role": "user", "content": message})

        if not use_tools:
            try:
                completion = self.client.chat.completions.create(
                    model=model_id, messages=messages, stream=True,
                    temperature=0.3, max_tokens=max_tokens,
                )
                for chunk in completion:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield {"type": "text", "content": chunk.choices[0].delta.content}
            except Exception as e:
                yield {"type": "error", "content": f"❌ LLM 调用失败: {e}"}
            yield {"type": "done"}
            return

        tools = TOOL_DEFINITIONS.copy()

        for turn in range(MAX_TOOL_TURNS):
            collected_content = ""
            tool_calls = {}
            finish_reason = None

            try:
                stream = self.client.chat.completions.create(
                    model=model_id, messages=messages, tools=tools,
                    stream=True, temperature=0.7, max_tokens=max_tokens,
                )
                for chunk in stream:
                    if not chunk.choices:
                        continue
                    delta = chunk.choices[0].delta
                    if not delta:
                        continue
                    if delta.content:
                        collected_content += delta.content
                        yield {"type": "text", "content": delta.content}
                    if delta.tool_calls:
                        for tc in delta.tool_calls:
                            idx = tc.index
                            if idx not in tool_calls:
                                tool_calls[idx] = {"id": tc.id or "", "function": {"name": "", "arguments": ""}}
                            if tc.id:
                                tool_calls[idx]["id"] = tc.id
                            if tc.function:
                                if tc.function.name:
                                    tool_calls[idx]["function"]["name"] += tc.function.name
                                if tc.function.arguments:
                                    tool_calls[idx]["function"]["arguments"] += tc.function.arguments
                    if chunk.choices[0].finish_reason:
                        finish_reason = chunk.choices[0].finish_reason
            except Exception as e:
                yield {"type": "error", "content": f"❌ LLM 调用失败: {e}"}
                return

            if collected_content:
                messages.append({"role": "assistant", "content": collected_content})

            is_tool_call = finish_reason == "tool_calls" and bool(tool_calls)
            if is_tool_call:
                for idx in sorted(tool_calls.keys()):
                    tc = tool_calls[idx]
                    name = tc["function"]["name"]
                    args_str = tc["function"]["arguments"]
                    tid = tc["id"] or f"call_{idx}"
                    if not name:
                        continue
                    yield {"type": "tool_start", "name": name}
                    result = execute_tool(name, args_str, uploaded_file)
                    messages.append({"role": "tool", "tool_call_id": tid, "content": result})
                    yield {"type": "tool_result", "content": result}
                    if name == "execute_python":
                        figures = get_last_figures()
                        if figures:
                            yield {"type": "figures", "figures": figures, "count": len(figures)}
            else:
                break
        else:
            yield {"type": "text", "content": "\n\n*（已达到最大工具调用次数）*"}
        yield {"type": "done"}
