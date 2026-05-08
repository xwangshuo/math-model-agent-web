# -*- coding: utf-8 -*-
"""
模型知识库 — 10个常用数学建模模型的完整知识卡片
"""
from typing import Optional, List

MODEL_CARDS = [
    {
        "id": "linear-programming",
        "name": "线性规划 (LP)",
        "category": "优化类",
        "icon": "📐",
        "tags": ["规划", "优化", "资源分配"],
        "summary": "在满足一组线性约束条件下，求解线性目标函数的最大值或最小值。",
        "applicable_scenarios": ["资源分配问题", "生产计划优化", "运输调度问题", "投资组合优化", "人员排班问题"],
        "math_principles": (
            "**标准形式**:\n"
            "$$\\min \\quad c^T x$$\n"
            "$$\\text{s.t.} \\quad Ax \\leq b, \\quad x \\geq 0$$\n"
            "\n"
            "- **决策变量**: $x = (x_1, x_2, ..., x_n)^T$\n"
            "- **目标函数**: $c^T x$ — 线性组合\n"
            "- **约束条件**: $Ax \\leq b$ — 线性不等式组\n"
            "- **非负约束**: $x_i \\geq 0$\n"
            "\n"
            "**求解方法**:\n"
            "- **单纯形法**: 沿可行域顶点迭代\n"
            "- **内点法**: 从内部逼近（大规模问题）\n"
        ),
        "code_template": (
            "```python\n"
            "import pulp\n"
            "\n"
            "prob = pulp.LpProblem('生产优化', pulp.LpMaximize)\n"
            "\n"
            "x1 = pulp.LpVariable('产品A', lowBound=0, cat='Continuous')\n"
            "x2 = pulp.LpVariable('产品B', lowBound=0, cat='Continuous')\n"
            "\n"
            "prob += 40 * x1 + 30 * x2, '总利润'\n"
            "\n"
            "prob += 2 * x1 + 3 * x2 <= 100, '原材料约束'\n"
            "prob += 4 * x1 + 2 * x2 <= 120, '工时约束'\n"
            "prob += x1 <= 40, '市场需求约束'\n"
            "\n"
            "prob.solve(pulp.PULP_CBC_CMD(msg=False))\n"
            "\n"
            "print(f'最优解: 产品A={pulp.value(x1):.2f}, 产品B={pulp.value(x2):.2f}')\n"
            "print(f'最大利润: {pulp.value(prob.objective):.2f}')\n"
            "```\n"
        ),
        "pros": ["原理简单求解快", "有成熟求解器", "灵敏度分析成熟", "全局最优解有保证"],
        "cons": ["要求所有关系线性", "不能处理不确定性", "变量过多时维数灾难", "实际问题往往非线性"],
        "python_packages": ["pulp", "scipy.optimize.linprog", "cvxopt", "ortools"],
        "common_errors": [
            ["无可行解", "检查约束是否矛盾，放宽约束"],
            ["无界解", "缺少必要约束，加入边界"],
            ["整数规划求解慢", "减少整数变量或用启发式算法"],
        ],
    },
    {
        "id": "ahp",
        "name": "层次分析法 (AHP)",
        "category": "评价类",
        "icon": "📊",
        "tags": ["评价", "决策", "权重"],
        "summary": "将决策问题分解为目标层、准则层、方案层，通过两两比较矩阵计算权重。",
        "applicable_scenarios": ["方案优选", "评价指标体系权重确定", "风险因素排序", "人才选拔", "供应商评估"],
        "math_principles": (
            "**步骤**:\n"
            "1. **建立层次结构**: 目标层 → 准则层 → 方案层\n"
            "2. **构造判断矩阵**: $A = (a_{ij})_{n \\times n}$\n"
            "\n"
            "   Saaty 1-9 标度法:\n"
            "   - 1=同等重要, 3=稍微重要, 5=明显重要\n"
            "   - 7=强烈重要, 9=极端重要, 2/4/6/8=中间值\n"
            "\n"
            "3. **计算权重**: 几何平均法\n"
            "   $$w_i = \\frac{(\\prod_j a_{ij})^{1/n}}{\\sum_k (\\prod_j a_{kj})^{1/n}}$$\n"
            "\n"
            "4. **一致性检验**:\n"
            "   $$CR = \\frac{CI}{RI} < 0.1$$\n"
            "   其中 $CI = \\frac{\\lambda_{max} - n}{n-1}$\n"
        ),
        "code_template": (
            "```python\n"
            "import numpy as np\n"
            "\n"
            "def ahp_weights(matrix):\n"
            "    n = len(matrix)\n"
            "    geom_mean = np.prod(matrix, axis=1) ** (1/n)\n"
            "    weights = geom_mean / geom_mean.sum()\n"
            "    Aw = matrix @ weights\n"
            "    lambda_max = (Aw / weights).mean()\n"
            "    CI = (lambda_max - n) / (n - 1)\n"
            "    RI = {1:0, 2:0, 3:0.58, 4:0.90, 5:1.12, 6:1.24, 7:1.32, 8:1.41, 9:1.45, 10:1.49}[n]\n"
            "    CR = CI / RI if RI > 0 else 0\n"
            "    return weights, CR\n"
            "\n"
            "criteria = np.array([\n"
            "    [1, 1/3, 2, 2],\n"
            "    [3, 1, 4, 3],\n"
            "    [1/2, 1/4, 1, 1/2],\n"
            "    [1/2, 1/3, 2, 1]\n"
            "])\n"
            "w, cr = ahp_weights(criteria)\n"
            "print(f'权重: {w}')\n"
            "print(f'CR = {cr:.4f} {\"OK\" if cr < 0.1 else \"FAIL\"}')\n"
            "```\n"
        ),
        "pros": ["定性定量结合", "所需数据少", "计算简单", "适合多准则决策"],
        "cons": ["主观性强", "指标过多时一致性难保", "不能新增方案", "1-9标度精细度有限"],
        "python_packages": ["numpy", "scipy"],
        "common_errors": [
            ["CR > 0.1", "调整不一致元素或减少准则数"],
            ["矩阵非互反", "确保 a[i][j] = 1/a[j][i]"],
            ["方案层遗漏", "每个准则下都考虑所有方案"],
        ],
    },
    {
        "id": "topsis",
        "name": "TOPSIS 法",
        "category": "评价类",
        "icon": "🎯",
        "tags": ["评价", "排序", "多属性决策"],
        "summary": "构造理想解和负理想解，计算各评价对象与理想解的相对贴近度排序选优。",
        "applicable_scenarios": ["多指标综合评价", "方案比选", "供应商评估", "选址问题", "项目风险评估"],
        "math_principles": (
            "**步骤**:\n"
            "1. **构建决策矩阵** $X = (x_{ij})_{m \\times n}$\n"
            "2. **归一化**: $r_{ij} = x_{ij} / \\sqrt{\\sum x_{ij}^2}$\n"
            "3. **加权**: $v_{ij} = w_j \\cdot r_{ij}$\n"
            "4. **理想解** $A^+$ 和 **负理想解** $A^-$\n"
            "5. **距离**: $S_i^+ = \\sqrt{\\sum (v_{ij} - v_j^+)^2}$, $S_i^- = \\sqrt{\\sum (v_{ij} - v_j^-)^2}$\n"
            "6. **贴近度**: $C_i^* = S_i^- / (S_i^+ + S_i^-)$, 越大越优\n"
        ),
        "code_template": (
            "```python\n"
            "import numpy as np\n"
            "\n"
            "def topsis(matrix, weights, benefits):\n"
            "    m, n = matrix.shape\n"
            "    norm = matrix / np.sqrt((matrix**2).sum(axis=0))\n"
            "    weighted = norm * weights\n"
            "    ideal = np.where(benefits, weighted.max(0), weighted.min(0))\n"
            "    neg_ideal = np.where(benefits, weighted.min(0), weighted.max(0))\n"
            "    d_pos = np.sqrt(((weighted - ideal)**2).sum(1))\n"
            "    d_neg = np.sqrt(((weighted - neg_ideal)**2).sum(1))\n"
            "    scores = d_neg / (d_pos + d_neg)\n"
            "    return scores\n"
            "\n"
            "data = np.array([[0.8,2500,0.15,90],[0.6,1800,0.20,80],[0.9,3000,0.10,95]])\n"
            "w = np.array([0.3,0.2,0.2,0.3])\n"
            "ben = np.array([True,False,True,True])\n"
            "scores = topsis(data, w, ben)\n"
            "for i,s in enumerate(scores):\n"
            "    print(f'方案{i+1}: {s:.4f}')\n"
            "```\n"
        ),
        "pros": ["计算简单结果直观", "对数据分布要求低", "充分利用原始数据", "同时处理正负向指标"],
        "cons": ["需预先确定权重", "对异常值敏感", "不能处理指标相关", "理想解现实中不存在"],
        "python_packages": ["numpy", "pandas"],
        "common_errors": [
            ["负值指标处理不当", "用极差变换预处理"],
            ["权重和不为1", "weights = weights/weights.sum()"],
            ["指标方向错配", "成本指标在benefits中=False"],
        ],
    },
    {
        "id": "grey-correlation",
        "name": "灰色关联分析",
        "category": "评价类",
        "icon": "🔗",
        "tags": ["评价", "关联度", "小样本"],
        "summary": "通过序列几何形状的相似程度判断因素之间的关联强度，适用于小样本贫信息分析。",
        "applicable_scenarios": ["影响因素分析", "综合评价", "小样本关联分析", "经济指标相关性", "质量因素排序"],
        "math_principles": (
            "**步骤**:\n"
            "1. 确定**参考序列** $X_0$ 和**比较序列** $X_i$\n"
            "2. **无量纲化**（均值化/初值化）\n"
            "3. **关联系数**:\n"
            "   $$\\xi_i(k) = \\frac{\\min\\min|x_0' - x_i'| + \\rho \\cdot \\max\\max|x_0' - x_i'|}{|x_0'(k) - x_i'(k)| + \\rho \\cdot \\max\\max|x_0' - x_i'|}$$\n"
            "   $\\rho \\in (0,1)$, 通常取 0.5\n"
            "4. **关联度**: $r_i = \\frac{1}{n}\\sum_{k=1}^n \\xi_i(k)$\n"
        ),
        "code_template": (
            "```python\n"
            "import numpy as np\n"
            "\n"
            "def grey_correlation(ref, seqs, rho=0.5):\n"
            "    ref_n = ref / ref.mean()\n"
            "    seqs_n = seqs / seqs.mean(axis=1, keepdims=True)\n"
            "    diff = np.abs(seqs_n - ref_n)\n"
            "    min_v, max_v = diff.min(), diff.max()\n"
            "    corr = (min_v + rho*max_v) / (diff + rho*max_v)\n"
            "    return corr.mean(axis=1)\n"
            "\n"
            "ref = np.array([1, 1.2, 1.5, 1.8, 2.0])\n"
            "seqs = np.array([[0.8,1.0,1.3,1.6,2.1], [2.0,1.8,1.5,1.2,0.9]])\n"
            "d = grey_correlation(ref, seqs)\n"
            "print(f'因素1: {d[0]:.4f}, 因素2: {d[1]:.4f}')\n"
            "```\n"
        ),
        "pros": ["小样本即用", "计算量小", "不要求典型分布", "定量定性均可"],
        "cons": ["ρ选取主观", "反映趋势非因果", "对无量纲化敏感", "缺严格统计检验"],
        "python_packages": ["numpy", "pandas"],
        "common_errors": [
            ["数据不足", "至少4个数据点"],
            ["ρ取值不当", "通常取0.5，区分度不够可减小"],
            ["序列方向不一致", "确保所有序列趋势同向后比较"],
        ],
    },
    {
        "id": "regression",
        "name": "回归分析",
        "category": "统计类",
        "icon": "📈",
        "tags": ["统计", "预测", "因果分析"],
        "summary": "研究变量之间相关关系的统计方法，建立回归方程描述因变量与自变量的依赖关系。",
        "applicable_scenarios": ["因果关系分析", "趋势预测", "影响因素识别", "数据插补", "参数标定"],
        "math_principles": (
            "**线性回归**: $y = \\beta_0 + \\beta_1 x_1 + \\cdots + \\beta_p x_p + \\varepsilon$\n"
            "\n"
            "**最小二乘法**: $\\hat{\\beta} = (X^T X)^{-1} X^T y$\n"
            "\n"
            "**模型评价**:\n"
            "- $R^2$: 决定系数\n"
            "- $F$ 检验: 整体显著性\n"
            "- $t$ 检验: 系数显著性\n"
            "\n"
            "**常用变体**:\n"
            "- Ridge 回归: L2 正则化，抗共线性\n"
            "- Lasso 回归: L1 正则化，特征选择\n"
            "- 多项式回归: 引入高次项\n"
        ),
        "code_template": (
            "```python\n"
            "import numpy as np\n"
            "from sklearn.linear_model import LinearRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import r2_score, mean_squared_error\n"
            "\n"
            "np.random.seed(42)\n"
            "X = np.random.randn(100, 3)\n"
            "y = X @ [2.0, -1.5, 0.8] + np.random.randn(100)*0.5\n"
            "\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\n"
            "model = LinearRegression().fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n"
            "print(f'R2 = {r2_score(y_test, y_pred):.4f}')\n"
            "print(f'RMSE = {np.sqrt(mean_squared_error(y_test,y_pred)):.4f}')\n"
            "print(f'系数: {model.coef_}')\n"
            "```\n"
        ),
        "pros": ["理论基础扎实", "结果可解释性强", "预测快", "有完整假设检验体系"],
        "cons": ["对异常值敏感", "需满足统计假设", "难处理非线性", "多重共线性影响稳定性"],
        "python_packages": ["scikit-learn", "statsmodels", "numpy"],
        "common_errors": [
            ["过拟合", "用Ridge/Lasso正则化或减少特征"],
            ["多重共线性", "计算VIF或使用岭回归"],
            ["异方差", "对数变换或加权最小二乘"],
            ["残差非正态", "Box-Cox变换"],
        ],
    },
    {
        "id": "clustering",
        "name": "聚类分析",
        "category": "机器学习",
        "icon": "🔮",
        "tags": ["分类", "无监督", "模式识别"],
        "summary": "将数据集的样本划分为若干簇，使簇内相似度高、簇间相似度低，属于无监督学习。",
        "applicable_scenarios": ["客户画像与市场细分", "图像分割", "异常检测", "文本主题聚类", "地理区域划分"],
        "math_principles": (
            "**K-Means**:\n"
            "1. 选 $k$ 个初始聚类中心\n"
            "2. 分配: 样本归属最近中心\n"
            "3. 更新: 重算质心\n"
            "4. 迭代至收敛\n"
            "\n"
            "**距离度量**:\n"
            "- **欧氏距离**: $d(x,y) = \\sqrt{\\sum (x_i-y_i)^2}$\n"
            "- **曼哈顿距离**: $d(x,y) = \\sum |x_i-y_i|$\n"
            "\n"
            "**K 值选择**: 肘部法、轮廓系数($\\in[-1,1]$，越大越好)、Gap 统计量\n"
        ),
        "code_template": (
            "```python\n"
            "import numpy as np\n"
            "from sklearn.cluster import KMeans\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.metrics import silhouette_score\n"
            "\n"
            "np.random.seed(42)\n"
            "X = np.concatenate([np.random.randn(50,2)+[2,2], np.random.randn(50,2)+[-2,2], np.random.randn(50,2)+[0,-2]])\n"
            "X = StandardScaler().fit_transform(X)\n"
            "\n"
            "kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\n"
            "labels = kmeans.fit_predict(X)\n"
            "print(f'轮廓系数: {silhouette_score(X,labels):.4f}')\n"
            "\n"
            "# 肘部法找K\n"
            "sse = [KMeans(n_clusters=k, random_state=42, n_init=10).fit(X).inertia_ for k in range(1,10)]\n"
            "# 拐点即最佳K\n"
            "```\n"
        ),
        "pros": ["无需标签", "发现数据内在结构", "K-Means 快", "多种变体适应不同场景"],
        "cons": ["K 值需指定", "对初始中心敏感", "对异常值敏感", "非球形簇效果差"],
        "python_packages": ["scikit-learn", "scipy.cluster", "matplotlib"],
        "common_errors": [
            ["K值不当", "肘部法+轮廓系数综合判断"],
            ["未标准化", "聚类前必须标准化"],
            ["高维诅咒", "先用PCA降维"],
            ["非球形差", "改用DBSCAN或谱聚类"],
        ],
    },
    {
        "id": "svm",
        "name": "支持向量机 (SVM)",
        "category": "机器学习",
        "icon": "🎯",
        "tags": ["分类", "监督学习", "核方法"],
        "summary": "通过寻找最大间隔超平面将不同类别样本分开，利用核技巧处理非线性可分问题。",
        "applicable_scenarios": ["文本分类", "图像识别", "生物信息学", "异常检测", "小样本高维分类"],
        "math_principles": (
            "**线性 SVM**:\n"
            "$$\\min \\frac{1}{2}\\|w\\|^2, \\quad y_i(w^T x_i + b) \\geq 1$$\n"
            "\n"
            "**核技巧**:\n"
            "- **线性核**: $K(x_i,x_j) = x_i^T x_j$\n"
            "- **RBF 核**: $K(x_i,x_j) = \\exp(-\\gamma\\|x_i-x_j\\|^2)$\n"
            "- **多项式核**: $K(x_i,x_j) = (\\gamma x_i^T x_j + r)^d$\n"
        ),
        "code_template": (
            "```python\n"
            "from sklearn.svm import SVC\n"
            "from sklearn.model_selection import train_test_split, GridSearchCV\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.metrics import classification_report\n"
            "import numpy as np\n"
            "\n"
            "X = np.random.randn(150, 2)\n"
            "y = (X[:,0]**2 + X[:,1]**2 > 1.5).astype(int)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)\n"
            "X_train = StandardScaler().fit_transform(X_train)\n"
            "X_test = StandardScaler().fit_transform(X_test)\n"
            "\n"
            "svm = SVC(kernel='rbf', C=1.0, gamma='scale').fit(X_train, y_train)\n"
            "y_pred = svm.predict(X_test)\n"
            "print(classification_report(y_test, y_pred))\n"
            "```\n"
        ),
        "pros": ["高维表现优秀", "小样本效果好", "核技巧处理非线性", "泛化能力强"],
        "cons": ["大数据训练慢", "参数敏感(C,γ,核)", "多分类需策略", "可解释性不如树"],
        "python_packages": ["scikit-learn"],
        "common_errors": [
            ["未标准化", "SVM对尺度敏感，务必标准化"],
            ["C参数不当", "C大=过拟合, C小=欠拟合"],
            ["核函数选择", "先试RBF, 特征多试线性"],
            ["样本不均衡", "设置 class_weight='balanced'"],
        ],
    },
    {
        "id": "neural-network",
        "name": "神经网络 (BP/MLP)",
        "category": "机器学习",
        "icon": "🧠",
        "tags": ["深度学习", "非线性", "拟合"],
        "summary": "模拟人脑神经元结构的计算模型，通过多层非线性变换学习数据的复杂模式。",
        "applicable_scenarios": ["复杂非线性拟合", "图像识别", "序列预测", "模式识别", "参数反演"],
        "math_principles": (
            "**单神经元**: $y = \\sigma(w^T x + b)$\n"
            "\n"
            "**激活函数**:\n"
            "- Sigmoid: $\\sigma(x)=1/(1+e^{-x})$\n"
            "- ReLU: $\\max(0,x)$\n"
            "- Tanh: $(e^x-e^{-x})/(e^x+e^{-x})$\n"
            "\n"
            "**反向传播**: 链式法则求梯度 $\\to$ 梯度下降更新权重\n"
            "\n"
            "**关键超参**: 层数、神经元数、学习率、批大小、轮数\n"
        ),
        "code_template": (
            "```python\n"
            "import numpy as np\n"
            "import torch\n"
            "import torch.nn as nn\n"
            "import torch.optim as optim\n"
            "\n"
            "X = torch.FloatTensor(np.random.randn(500,1))\n"
            "y = torch.sin(2*X).reshape(-1,1) + 0.1*torch.randn(500,1)\n"
            "\n"
            "model = nn.Sequential(nn.Linear(1,32), nn.ReLU(), nn.Linear(32,32), nn.ReLU(), nn.Linear(32,1))\n"
            "opt = optim.Adam(model.parameters(), lr=0.01)\n"
            "loss_fn = nn.MSELoss()\n"
            "\n"
            "for epoch in range(500):\n"
            "    opt.zero_grad()\n"
            "    loss = loss_fn(model(X), y)\n"
            "    loss.backward()\n"
            "    opt.step()\n"
            "\n"
            "print(f'最终损失: {loss.item():.6f}')\n"
            "```\n"
        ),
        "pros": ["万能逼近定理", "自动特征学习", "非结构化数据好", "迁移学习支持好"],
        "cons": ["需大量数据", "训练时间长", "调参复杂", "可解释性差(黑箱)"],
        "python_packages": ["torch / tensorflow", "scikit-learn"],
        "common_errors": [
            ["过拟合", "Dropout/早停/数据增强/L2"],
            ["梯度消失", "ReLU替代Sigmoid+批归一化"],
            ["学习率不当", "太大震荡,太小过慢"],
            ["未标准化", "神经网络对尺度敏感"],
        ],
    },
    {
        "id": "differential-equation",
        "name": "微分方程模型",
        "category": "机理建模",
        "icon": "📉",
        "tags": ["机理", "动态系统", "物理"],
        "summary": "通过建立微分方程描述系统的动态变化规律，用于物理/生物/经济等领域的机理建模。",
        "applicable_scenarios": ["物理系统建模", "人口增长与生态", "传染病传播(SIR)", "化学反应动力学", "经济动态系统"],
        "math_principles": (
            "**ODE**: $dy/dt = f(t,y)$, $y(t_0)=y_0$\n"
            "\n"
            "**数值解法**:\n"
            "- **欧拉法**: $y_{n+1}=y_n + h\\cdot f(t_n,y_n)$\n"
            "- **RK4**: 四阶龙格-库塔法\n"
            "\n"
            "**常见模型**:\n"
            "- **Malthus**: $dP/dt = rP$ 指数增长\n"
            "- **Logistic**: $dP/dt = rP(1-P/K)$ 有限增长\n"
            "- **SIR**: 易感-感染-康复模型\n"
        ),
        "code_template": (
            "```python\n"
            "import numpy as np\n"
            "from scipy.integrate import solve_ivp\n"
            "\n"
            "def sir(t, y, beta, gamma):\n"
            "    S, I, R = y\n"
            "    return [-beta*S*I, beta*S*I - gamma*I, gamma*I]\n"
            "\n"
            "beta, gamma = 0.3, 0.1\n"
            "sol = solve_ivp(sir, [0,100], [0.99,0.01,0.0], args=(beta,gamma), t_eval=np.linspace(0,100,200))\n"
            "S, I, R = sol.y\n"
            "print(f'感染峰值时间: {sol.t[I.argmax()]:.1f}')\n"
            "print(f'峰值感染率: {I.max():.4f}')\n"
            "```\n"
        ),
        "pros": ["机理明确意义清晰", "可外推预测", "参数有实际含义", "物理/生物标准方法"],
        "cons": ["复杂系统难精确建模", "需数值求解", "参数估计需实验", "对初值敏感"],
        "python_packages": ["scipy.integrate", "numpy", "matplotlib"],
        "common_errors": [
            ["刚性问题", "改用method=Radau或BDF"],
            ["初值不当", "检查单位和合理性"],
            ["步长不当", "用dense_output=True插值"],
            ["模型发散", "检查参数是否过大"],
        ],
    },
    {
        "id": "monte-carlo",
        "name": "蒙特卡洛模拟",
        "category": "模拟类",
        "icon": "🎲",
        "tags": ["随机模拟", "概率", "数值计算"],
        "summary": "利用大量随机样本进行统计试验来求解确定性问题，适用于高维积分、优化和风险评估。",
        "applicable_scenarios": ["数值积分(高维)", "金融风险分析(VaR)", "随机优化", "物理粒子模拟", "系统可靠性分析"],
        "math_principles": (
            "**基本原理**: 用大量随机样本的统计结果近似问题的解\n"
            "\n"
            "**蒙特卡洛积分**:\n"
            "$$\\int_a^b f(x)dx \\approx \\frac{b-a}{N}\\sum_{i=1}^N f(x_i)$$\n"
            "\n"
            "**方差缩减**: 重要抽样、分层抽样、对偶变量、控制变量\n"
        ),
        "code_template": (
            "```python\n"
            "import numpy as np\n"
            "\n"
            "# 蒙特卡洛估计 PI\n"
            "n = 10000\n"
            "x = np.random.uniform(-1, 1, n)\n"
            "y = np.random.uniform(-1, 1, n)\n"
            "pi_est = 4 * (x**2 + y**2 <= 1).sum() / n\n"
            "print(f'estimated PI = {pi_est:.6f} (real: {np.pi:.6f})')\n"
            "\n"
            "# 收敛性: 增大n得更好估计\n"
            "```\n"
        ),
        "pros": ["实现简单通用", "适合高维问题", "误差与维数无关", "可处理复杂约束"],
        "cons": ["收敛慢(O(1/sqrt(N)))", "计算量大", "结果有随机波动", "对PRNG质量有要求"],
        "python_packages": ["numpy.random", "scipy.stats", "matplotlib"],
        "common_errors": [
            ["样本量不足", "用 sigma/sqrt(N) 估计误差"],
            ["种子未设", "np.random.seed(42)确保可复现"],
            ["方差过大", "用重要抽样/分层抽样"],
            ["模拟过多", "先少量试探再增加"],
        ],
    },
]


def get_all_models() -> list[dict]:
    """返回所有模型卡片（不含code_template）"""
    return [{k: v for k, v in card.items() if k != "code_template"} for card in MODEL_CARDS]


def get_model_by_id(model_id: str) -> Optional[dict]:
    for card in MODEL_CARDS:
        if card["id"] == model_id:
            return card
    return None


def get_models_by_category(category: str) -> list[dict]:
    return [{k: v for k, v in card.items() if k != "code_template"} for card in MODEL_CARDS if card["category"] == category]


def get_categories() -> list[str]:
    return sorted(set(c["category"] for c in MODEL_CARDS))
