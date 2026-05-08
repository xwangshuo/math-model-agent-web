"""
历年赛题数据库 — CUMCM / MCM / ICM 真题
"""

from typing import Optional

PROBLEM_BANK = [
    {
        "id": "cumcm-2024-a",
        "year": 2024,
        "competition": "CUMCM",
        "label": "A题",
        "title": "\u201c猪头\u201d形状的板凳龙与螺线",
        "category": "几何/物理",
        "difficulty": "B",
        "description": "分析舞龙队沿螺线运动的轨迹、速度与碰撞问题。",
        "models": ["微分方程", "几何建模", "数值模拟"],
        "tags": ["运动轨迹", "螺线", "碰撞检测"],
        "data_type": "无数据",
    },
    {
        "id": "cumcm-2024-b",
        "year": 2024,
        "competition": "CUMCM",
        "label": "B题",
        "title": "小微企业供应链韧性分析",
        "category": "评价/优化",
        "difficulty": "B",
        "description": "评估小微企业在供应链中断情况下的韧性，制定库存与订货策略。",
        "models": ["蒙特卡洛模拟", "时间序列", "多目标优化"],
        "tags": ["供应链", "韧性评估", "库存优化"],
        "data_type": "模拟数据",
    },
    {
        "id": "cumcm-2024-c",
        "year": 2024,
        "competition": "CUMCM",
        "label": "C题",
        "title": "农作物种植策略优化",
        "category": "优化",
        "difficulty": "C",
        "description": "基于多种农作物价格波动和亩产数据，优化种植方案。",
        "models": ["线性规划", "整数规划", "预测模型"],
        "tags": ["农业优化", "资源配置", "规划"],
        "data_type": "大表数据",
    },
    {
        "id": "cumcm-2024-d",
        "year": 2024,
        "competition": "CUMCM",
        "label": "D题",
        "title": "反潜航空深弹命中概率问题",
        "category": "概率/优化",
        "difficulty": "A",
        "description": "计算深弹对潜艇的命中概率，优化投弹策略。",
        "models": ["概率论", "几何概率", "蒙特卡洛模拟"],
        "tags": ["军事建模", "命中概率", "优化"],
        "data_type": "无数据",
    },
    {
        "id": "cumcm-2024-e",
        "year": 2024,
        "competition": "CUMCM",
        "label": "E题",
        "title": "高速公路应急车道启用策略",
        "category": "优化/评价",
        "difficulty": "C",
        "description": "根据交通流量数据设计应急车道动态启用策略。",
        "models": ["交通流模型", "元胞自动机", "优化"],
        "tags": ["交通", "应急管理", "动态策略"],
        "data_type": "大表数据",
    },
    {
        "id": "cumcm-2023-a",
        "year": 2023,
        "competition": "CUMCM",
        "label": "A题",
        "title": "定日镜场的优化设计",
        "category": "优化/几何",
        "difficulty": "A",
        "description": "优化塔式太阳能光热发电站中定日镜场的布局和效率。",
        "models": ["几何光学", "优化模型", "模拟退火"],
        "tags": ["新能源", "镜场布局", "光学效率"],
        "data_type": "提供公式",
    },
    {
        "id": "cumcm-2023-b",
        "year": 2023,
        "competition": "CUMCM",
        "label": "B题",
        "title": "多波束测线布设问题",
        "category": "几何/优化",
        "difficulty": "B",
        "description": "海底地形多波束测线布设的覆盖宽度和重叠率优化。",
        "models": ["几何建模", "微分方程", "数值优化"],
        "tags": ["海洋测绘", "测线布设", "覆盖优化"],
        "data_type": "无数据/公式",
    },
    {
        "id": "cumcm-2023-c",
        "year": 2023,
        "competition": "CUMCM",
        "label": "C题",
        "title": "蔬菜类商品的自动定价与补货决策",
        "category": "预测/优化",
        "difficulty": "C",
        "description": "基于历史销售数据预测蔬菜需求并优化补货和定价策略。",
        "models": ["时间序列", "需求预测", "优化模型"],
        "tags": ["零售", "定价", "库存管理"],
        "data_type": "大表数据",
    },
    {
        "id": "cumcm-2022-a",
        "year": 2022,
        "competition": "CUMCM",
        "label": "A题",
        "title": "波浪能发电装置输出功率的优化设计",
        "category": "物理/优化",
        "difficulty": "A",
        "description": "优化波浪能发电装置的浮子/振子结构和参数。",
        "models": ["物理建模", "微分方程", "优化"],
        "tags": ["新能源", "波浪能", "参数优化"],
        "data_type": "提供公式",
    },
    {
        "id": "cumcm-2022-b",
        "year": 2022,
        "competition": "CUMCM",
        "label": "B题",
        "title": "无人机编队飞行中的定位问题",
        "category": "几何/优化",
        "difficulty": "A",
        "description": "无人机编队中纯方位定位的无源定位模型。",
        "models": ["几何定位", "优化模型", "数值计算"],
        "tags": ["无人机", "定位", "编队"],
        "data_type": "提供部分数据",
    },
    {
        "id": "cumcm-2022-c",
        "year": 2022,
        "competition": "CUMCM",
        "label": "C题",
        "title": "古代玻璃制品的成分分析与鉴别",
        "category": "统计/分类",
        "difficulty": "B",
        "description": "基于玻璃成分数据分类高钾/铅钡玻璃，追溯风化前后成分规律。",
        "models": ["聚类分析", "分类模型", "主成分分析"],
        "tags": ["文物鉴定", "成分分析", "分类"],
        "data_type": "小表数据",
    },
    {
        "id": "mcm-2024-a",
        "year": 2024,
        "competition": "MCM",
        "label": "A题",
        "title": "Gender Balance in the Olympics",
        "category": "统计/评价",
        "difficulty": "B",
        "description": "分析奥运会性别平衡趋势，建立评价指标和预测模型。",
        "models": ["时间序列", "综合评价", "预测"],
        "tags": ["体育统计", "性别研究", "趋势分析"],
        "data_type": "需自行收集",
    },
    {
        "id": "mcm-2024-b",
        "year": 2024,
        "competition": "MCM",
        "label": "B题",
        "title": "Searching for Submersibles",
        "category": "搜索/优化",
        "difficulty": "A",
        "description": "设计在海洋中搜索失联潜水器的策略，考虑洋流和不确定性。",
        "models": ["搜索论", "蒙特卡洛", "随机过程"],
        "tags": ["搜索优化", "海洋", "不确定性"],
        "data_type": "需自行收集",
    },
    {
        "id": "mcm-2024-c",
        "year": 2024,
        "competition": "MCM",
        "label": "C题",
        "title": "Tennis Momentum",
        "category": "统计/数据挖掘",
        "difficulty": "B",
        "description": "分析网球比赛中“势头”是否存在及其对比赛结果的影响。",
        "models": ["统计检验", "时间序列", "机器学习"],
        "tags": ["体育数据", "势头分析", "假设检验"],
        "data_type": "大表数据",
    },
    {
        "id": "icm-2024-d",
        "year": 2024,
        "competition": "ICM",
        "label": "D题",
        "title": "Great Lakes Water Level",
        "category": "环境/预测",
        "difficulty": "B",
        "description": "预测五大湖水位变化并制定管理策略。",
        "models": ["时间序列", "系统动力学", "优化"],
        "tags": ["环境", "水位预测", "水资源"],
        "data_type": "大表数据",
    },
    {
        "id": "icm-2024-e",
        "year": 2024,
        "competition": "ICM",
        "label": "E题",
        "title": "Climate Change and Property Insurance",
        "category": "评价/预测",
        "difficulty": "B",
        "description": "评估气候变化对财产保险业的影响，提出可持续策略。",
        "models": ["风险评估", "预测模型", "多目标决策"],
        "tags": ["气候变化", "保险", "风险评估"],
        "data_type": "需自行收集",
    },
    {
        "id": "icm-2024-f",
        "year": 2024,
        "competition": "ICM",
        "label": "F题",
        "title": "Reducing Wildlife Trafficking",
        "category": "策略/评价",
        "difficulty": "C",
        "description": "建模分析野生动物非法贸易网络并提出干预策略。",
        "models": ["网络分析", "博弈论", "系统动力学"],
        "tags": ["野生动物", "非法贸易", "网络"],
        "data_type": "需自行收集",
    },
    {
        "id": "cumcm-2021-a",
        "year": 2021,
        "competition": "CUMCM",
        "label": "A题",
        "title": "FAST 反射面的形状调节",
        "category": "几何/优化",
        "difficulty": "A",
        "description": "调节 FAST 天线的反射面形状使接收效率最大化。",
        "models": ["几何建模", "优化模型", "数值模拟"],
        "tags": ["天文", "反射面", "形状优化"],
        "data_type": "提供公式",
    },
    {
        "id": "cumcm-2021-b",
        "year": 2021,
        "competition": "CUMCM",
        "label": "B题",
        "title": "乙醇偶合制备烯烃催化剂的优化",
        "category": "优化/统计",
        "difficulty": "B",
        "description": "优化乙醇催化反应条件提高乙烯等产物产率。",
        "models": ["回归分析", "优化模型", "响应面"],
        "tags": ["化工", "催化剂", "工艺优化"],
        "data_type": "小表数据",
    },
    {
        "id": "cumcm-2021-c",
        "year": 2021,
        "competition": "CUMCM",
        "label": "C题",
        "title": "生产企业原材料的订购与运输",
        "category": "优化/预测",
        "difficulty": "C",
        "description": "基于供应商数据和运输数据优化原材料订购和转运方案。",
        "models": ["整数规划", "预测模型", "物流优化"],
        "tags": ["生产管理", "供应链", "物流"],
        "data_type": "大表数据",
    },
    {
        "id": "cumcm-2020-b",
        "year": 2020,
        "competition": "CUMCM",
        "label": "B题",
        "title": "穿越沙漠",
        "category": "优化/决策",
        "difficulty": "B",
        "description": "在有限补给条件下规划穿越沙漠的最优策略。",
        "models": ["动态规划", "决策论", "优化"],
        "tags": ["路径规划", "资源管理", "决策"],
        "data_type": "无数据",
    },
    {
        "id": "cumcm-2020-c",
        "year": 2020,
        "competition": "CUMCM",
        "label": "C题",
        "title": "中小微企业的信贷决策",
        "category": "评价/分类",
        "difficulty": "C",
        "description": "基于企业发票数据评估信誉并制定信贷策略。",
        "models": ["分类模型", "综合评价", "优化"],
        "tags": ["金融", "信贷评估", "风险控制"],
        "data_type": "大表数据",
    },
    {
        "id": "mcm-2023-c",
        "year": 2023,
        "competition": "MCM",
        "label": "C题",
        "title": "Wordle 的预测",
        "category": "统计/信息论",
        "difficulty": "B",
        "description": "分析 Wordle 单词游戏的猜词模式和难度分布。",
        "models": ["信息论", "统计分析", "模式识别"],
        "tags": ["游戏", "信息熵", "模式"],
        "data_type": "大表数据",
    },
]


def search_problems(
    keyword: str = "",
    competition: str = "",
    year: int = 0,
    category: str = "",
    difficulty: str = "",
) -> list[dict]:
    """按条件搜索赛题"""
    results = PROBLEM_BANK
    if keyword:
        kw = keyword.lower()
        results = [
            p for p in results
            if kw in p["title"].lower()
            or kw in p["description"].lower()
            or kw in p["category"].lower()
            or any(kw in t.lower() for t in p["tags"])
            or any(kw in m.lower() for m in p["models"])
        ]
    if competition:
        results = [p for p in results if p["competition"] == competition.upper()]
    if year:
        results = [p for p in results if p["year"] == year]
    if category:
        results = [p for p in results if category.lower() in p["category"].lower()]
    if difficulty:
        results = [p for p in results if p["difficulty"] == difficulty.upper()]
    return results


def get_problem(problem_id: str) -> Optional[dict]:
    for p in PROBLEM_BANK:
        if p["id"] == problem_id:
            return p
    return None


def get_filters() -> dict:
    years = sorted(set(p["year"] for p in PROBLEM_BANK), reverse=True)
    competitions = sorted(set(p["competition"] for p in PROBLEM_BANK))
    categories = sorted(set(p["category"] for p in PROBLEM_BANK))
    difficulties = sorted(set(p["difficulty"] for p in PROBLEM_BANK))
    return {
        "years": years,
        "competitions": competitions,
        "categories": categories,
        "difficulties": difficulties,
    }


def generate_reading_template(title: str, description: str) -> str:
    """生成题目速读模板"""
    return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 题目速读卡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📌 核心问题（一句话概括）
{title}
{description[:200]}

## 🔍 已知条件
- 数据提供情况：_______________
- 约束条件：_______________
- 目标函数/评价标准：_______________

## 🎯 问题类型判断
□ 优化类  □ 预测类  □ 评价类  □ 统计类  □ 分类/聚类
□ 微分方程  □ 几何/物理  □ 网络/图论
→ 判断依据：_______________

## 📊 数据特征分析
- 数据量：_______________ 行 × _______________ 列
- 缺失值情况：_______________
- 数据类型（数值/类别/文本/时序）：_______________

## 🧩 可能的模型（按优先级排序）
1. _______________
2. _______________
3. _______________

## 📋 任务分解
□ 任务 1：_______________
□ 任务 2：_______________
□ 任务 3：_______________
□ 任务 4：_______________

## ⚠️ 难点与风险
- 计算量：□ 大  □ 中  □ 小
- 数据获取难度：□ 难  □ 中  □ 易
- 模型复杂度：□ 高  □ 中  □ 低
- 论文创新点要求：□ 高  □ 中  □ 低

## 💡 初步思路
_______________

## ⏰ 时间规划建议
- 数据预处理：________ 小时
- 模型建立：________ 小时
- 代码调试：________ 小时
- 结果分析：________ 小时
- 论文写作：________ 小时
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
