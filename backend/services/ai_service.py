import os
import json
from openai import OpenAI
from typing import Optional

class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY", ""),
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        )
        self.model = os.getenv("AI_MODEL", "deepseek/deepseek-chat-v3.1")
        self.system_prompt = """你是数模竞赛助手，擅长数学建模竞赛的全流程辅导。
你可以：
1. 选题分析：分析赛题类型、难度、数据特征，给出选题建议
2. 模型推荐：根据题目特征推荐合适的数学模型，并解释原理
3. 代码生成：生成模型求解的Python代码，含完整注释
4. 论文排版：生成LaTeX论文模板和内容
5. 对话解题：解答数学建模相关问题

回复要专业、详细、可操作，包含公式和代码时用LaTeX/代码块格式。"""

    def chat(self, message: str, history: list = [], mode: str = "chat") -> str:
        system = self._get_system_prompt(mode)
        messages = [{"role": "system", "content": system}]

        # Add history (last 10 turns)
        for h in history[-10:]:
            messages.append(h)

        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=4096
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI服务调用失败: {str(e)}"

    def _get_system_prompt(self, mode: str) -> str:
        prompts = {
            "chat": self.system_prompt,
            "analysis": """你是数学建模竞赛选题分析专家。
分析赛题时：
1. 判断题目类型（优化/统计/预测/评价/分类等）
2. 评估难度系数
3. 指出核心考点和关键数据特征
4. 给出选题建议（适合新手/高手）
5. 推荐可能的解题方向

输出格式：markdown，包含分类标签、难度星级、详细分析。""",
            "recommend": """你是数学建模竞赛模型推荐专家。
根据题目描述和数据类型，推荐最合适的数学模型。
每个推荐包含：
- 模型名称和类别
- 核心原理简述
- 适用场景
- 优缺点
- Python实现要点
- 推荐优先级排序""",
            "code": """你是数学建模代码生成专家。
根据选定的模型生成可运行的Python代码：
1. 包含完整导入和依赖
2. 数据预处理部分
3. 模型求解核心代码
4. 结果可视化（matplotlib）
5. 详细中文注释
6. 代码可以直接复制运行""",
            "paper": """你是数学建模竞赛论文写作专家。
协助生成LaTeX格式的竞赛论文：
- 标准模板结构（摘要/关键词/问题重述/模型假设/符号说明/模型建立/求解/分析/评价/参考文献）
- 排版规范、公式美观
- 中英文摘要
- 表格和图表的LaTeX代码"""
        }
        return prompts.get(mode, self.system_prompt)
