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
    {
        "id": "integer-programming",
        "name": "整数规划 (IP)",
        "category": "优化类",
        "icon": "🔢",
        "tags": ["整数", "0-1规划", "组合优化"],
        "summary": "在线性规划基础上要求部分或全部变量取整数值，适用于选址、背包、指派等问题。",
        "applicable_scenarios": ["工厂选址(0-1变量)", "背包问题(物品选择)", "旅行商问题(TSP)", "生产调度", "投资决策"],
        "math_principles": (
            "**整数规划 = LP + 整数约束**\\n\\n"
            "$$\\min \\; c^T x$$\\n"
            "$$\\text{s.t.} \\; Ax \\leq b, \\; x \\geq 0, \\; x \\in \\mathbb{Z}^n$$\\n\\n"
            "**分支定界法**:\\n"
            "1. 求解松弛LP（去掉整数约束）\\n"
            "2. 解非整数: 分两支(向上/向下取整)递归求解\\n"
            "3. 比较上下界剪枝\\n\\n"
            "**0-1规划**: 变量只能取0或1, 常用于选址、指派等问题"
        ),
        "code_template": (
            "```python\\n"
            "import pulp\\n\\n"
            "prob = pulp.LpProblem('选址问题', pulp.LpMinimize)\\n"
            "x = [pulp.LpVariable(f'x{{i}}', cat='Binary') for i in range(5)]\\n"
            "prob += pulp.lpSum([100*x[i] for i in range(5)])  # 建设成本\\n"
            "prob += pulp.lpSum(x) >= 2  # 至少选2个\\n"
            "prob.solve(pulp.PULP_CBC_CMD(msg=False))\\n"
            "selected = [i for i in range(5) if pulp.value(x[i]) > 0.5]\\n"
            "print(f'选中: {selected}')\\n"
            "```"
        ),
        "pros": ["建模灵活(逻辑约束)", "0-1变量适合决策问题", "中小规模求解高效"],
        "cons": ["NP-hard大规模求解慢", "分支定界最坏指数时间", "敏感性分析困难"],
        "python_packages": ["pulp", "scipy.optimize.milp", "ortools"],
        "common_errors": [
            ["求解时间过长", "减少整数变量或松弛求解"],
            ["无可行解", "检查约束是否矛盾"],
            ["内存不足", "用分支定界+启发式截断"],
        ],
    },
    

    {
        "id": "simulated-annealing",
        "name": "模拟退火 (SA)",
        "category": "优化类",
        "icon": "🔥",
        "tags": ["全局优化", "随机搜索", "冶金"],
        "summary": "模拟金属退火过程，通过概率性接受劣解来跳出局部最优，适合复杂组合优化。",
        "applicable_scenarios": ["TSP旅行商", "背包问题", "连续函数全局优化", "调度问题", "布局优化"],
        "math_principles": (
            "**Metropolis准则**:\\n"
            "- $\\Delta E < 0$（更好）: 一定接受\\n"
            "- $\\Delta E > 0$（更差）: 以概率 $P = \\exp(-\\Delta E/T)$ 接受\\n\\n"
            "**算法流程**:\\n"
            "1. 初始化: 温度 $T_0$, 初始解 $s_0$\\n"
            "2. 扰动生成新解 $s'$\\n"
            "3. 计算 $\\Delta E = E(s') - E(s)$\\n"
            "4. 按Metropolis准则决定是否接受\\n"
            "5. 降温: $T \\leftarrow \\alpha T$ （$\\alpha = 0.85 \\sim 0.99$）\\n"
            "6. 重复至满足终止条件"
        ),
        "code_template": (
            "```python\\n"
            "import numpy as np\\n\\n"
            "def simulated_annealing(func, bounds, T0=100, alpha=0.95, max_iter=500):\\n"
            "    x = np.random.uniform(*bounds)\\n"
            "    f_best = func(x); x_best = x; T = T0\\n"
            "    for _ in range(max_iter):\\n"
            "        x_new = np.clip(x + np.random.normal(0, 0.1), *bounds)\\n"
            "        delta = func(x_new) - func(x)\\n"
            "        if delta < 0 or np.random.rand() < np.exp(-delta/T):\\n"
            "            x = x_new\\n"
            "            if func(x) > f_best: f_best = func(x); x_best = x\\n"
            "        T *= alpha\\n"
            "    return x_best, f_best\\n"
            "```"
        ),
        "pros": ["跳出局部最优", "实现简单通用", "不要求目标可导", "理论保证收敛"],
        "cons": ["收敛速度慢", "参数敏感(T0,α)", "结果随机", "无梯度信息利用"],
        "python_packages": ["numpy", "scipy.optimize.dual_annealing"],
        "common_errors": [
            ["初始温度太低", "T0设为目标值10-100倍"],
            ["降温太快", "α推荐0.95-0.99"],
            ["结果不稳定", "多跑几次取最优"],
        ],
    },
    

    {
        "id": "genetic-algorithm",
        "name": "遗传算法 (GA)",
        "category": "优化类",
        "icon": "🧬",
        "tags": ["进化", "全局搜索", "种群"],
        "summary": "模拟自然选择和遗传机制，通过选择、交叉、变异操作逐代进化出最优解。",
        "applicable_scenarios": ["TSP与路径规划", "多目标优化", "参数调优", "布局设计", "机器学习特征选择"],
        "math_principles": (
            "**算法框架**:\\n"
            "1. **编码**: 解 $\\to$ 染色体（二进制/实数）\\n"
            "2. **初始化**: 随机生成N个个体\\n"
            "3. **选择**: 按适应度比例（轮盘赌/锦标赛）\\n"
            "4. **交叉**: 父代交换基因（单点/两点/均匀）\\n"
            "5. **变异**: 小概率随机改变基因\\n"
            "6. **更新**: 新种群替代旧种群，回到3\\n\\n"
            "**关键参数**: 种群大小(50-200)、交叉率(0.7-0.9)、变异率(0.01-0.1)"
        ),
        "code_template": (
            "```python\\n"
            "import numpy as np\\n\\n"
            "def ga(fitness_func, bounds, pop_size=50, gens=100, mut_rate=0.05):\\n"
            "    pop = np.random.uniform(*bounds, (pop_size, len(bounds)))\\n"
            "    for _ in range(gens):\\n"
            "        fits = np.array([fitness_func(ind) for ind in pop])\\n"
            "        best_idx = np.argmax(fits); best = pop[best_idx].copy()\\n"
            "        # 锦标赛选择 + 均匀交叉 + 变异\\n"
            "        new_pop = []\\n"
            "        for _ in range(pop_size//2):\\n"
            "            i,j = np.random.randint(0,pop_size,2)\\n"
            "            p1,p2 = pop[i] if fits[i]>fits[j] else pop[j], pop[j] if fits[i]>fits[j] else pop[i]\\n"
            "            alpha = np.random.rand(len(bounds))\\n"
            "            c1 = alpha*p1 + (1-alpha)*p2\\n"
            "            c2 = (1-alpha)*p1 + alpha*p2\\n"
            "            new_pop.extend([c1, c2])\\n"
            "        # 精英保留\\n"
            "        pop = np.array(new_pop)\\n"
            "        pop[0] = best\\n"
            "    return best, fitness_func(best)\\n"
            "```"
        ),
        "pros": ["全局搜索能力强", "不依赖梯度", "适合并行计算", "可多目标优化"],
        "cons": ["计算量大", "参数敏感", "编码影响效率", "局部搜索弱(可混合SA)"],
        "python_packages": ["numpy", "scipy.optimize.differential_evolution", "deap"],
        "common_errors": [
            ["过早收敛", "增大种群或变异率"],
            ["迟迟不收敛", "检查编码是否合理"],
            ["适应度不变", "增大交叉率或重启"],
        ],
    },
    

    {
        "id": "time-series",
        "name": "时间序列分析 (ARIMA)",
        "category": "统计类",
        "icon": "📊",
        "tags": ["预测", "平稳性", "自相关"],
        "summary": "分析按时间顺序排列的数据点，提取趋势和季节性规律进行预测。",
        "applicable_scenarios": ["销量预测", "经济指标预测", "交通流量预测", "股票价格分析", "气象数据预测"],
        "math_principles": (
            "**ARIMA(p,d,q)**:\\n"
            "- **AR(p)**: $y_t = c + \\phi_1 y_{t-1} + \\cdots + \\phi_p y_{t-p} + \\varepsilon_t$\\n"
            "- **I(d)**: $d$ 次差分使序列平稳\\n"
            "- **MA(q)**: $y_t = c + \\varepsilon_t + \\theta_1 \\varepsilon_{t-1} + \\cdots + \\theta_q \\varepsilon_{t-q}$\\n\\n"
            "**建模步骤**:\\n"
            "1. ADF检验平稳性 $\\to$ 确定 $d$\\n"
            "2. 看ACF/PACF图确定 $p,q$\\n"
            "3. 拟合模型 $\\to$ 残差白噪声检验\\n"
            "4. AIC/BIC选择最优模型 $\\to$ 预测"
        ),
        "code_template": (
            "```python\\n"
            "import numpy as np\\n"
            "from statsmodels.tsa.arima.model import ARIMA\\n"
            "from statsmodels.tsa.stattools import adfuller\\n"
            "import matplotlib.pyplot as plt\\n\\n"
            "# 模拟数据\\n"
            "np.random.seed(42); t = np.arange(100)\\n"
            "y = 10 + 0.3*t + np.sin(t/5)*3 + np.random.randn(100)\\n\\n"
            "# 平稳性检验\\n"
            "p_val = adfuller(y)[1]\\n"
            "print(f'p = {p_val:.4f}, 需差分' if p_val>0.05 else '序列平稳')\\n\\n"
            "# 拟合 ARIMA(2,1,2)\\n"
            "model = ARIMA(y, order=(2,1,2)).fit()\\n"
            "print(f'AIC = {model.aic:.1f}')\\n"
            "pred = model.forecast(5)\\n"
            "print(f'预测: {np.round(pred, 2)}')\\n"
            "```"
        ),
        "pros": ["理论体系完善", "短期预测精度高", "可解释性强", "有完整统计检验"],
        "cons": ["长期预测误差累积", "需较多数据(>50)", "对突变点敏感", "单序列建模"],
        "python_packages": ["statsmodels", "prophet", "pmdarima"],
        "common_errors": [
            ["非平稳序列", "差分至平稳(A检p<0.05)"],
            ["过拟合", "用AIC/BIC选择简约模型"],
            ["残差非白噪声", "增大p,q或改用SARIMA"],
        ],
    },
    

    {
        "id": "random-forest",
        "name": "随机森林 (RF)",
        "category": "机器学习",
        "icon": "🌲",
        "tags": ["集成学习", "Bagging", "特征重要性"],
        "summary": "通过构建多棵决策树并集成投票，大幅提升预测准确性和稳定性。",
        "applicable_scenarios": ["分类预测", "回归预测", "特征重要性排序", "缺失值填补", "异常检测"],
        "math_principles": (
            "**随机森林 = Bagging + 决策树 + 随机特征**\\n\\n"
            "**构建过程**:\\n"
            "1. 从原始数据有放回抽样(Bootstrap)构建B个子集\\n"
            "2. 每个子集训练一棵决策树\\n"
            "   - 每个节点随机选 $m \\ll p$ 个特征\\n"
            "   - 学最优分裂\\n"
            "3. 集成预测: 分类取众数, 回归取均值\\n\\n"
            "**OOB误差**: 约1/3的袋外样本用于评估, 无需单独验证集\\n\\n"
            "**特征重要性**: 该特征在所有树中不纯度下降总和"
        ),
        "code_template": (
            "```python\\n"
            "from sklearn.ensemble import RandomForestClassifier\\n"
            "from sklearn.model_selection import train_test_split\\n"
            "from sklearn.metrics import classification_report\\n"
            "import numpy as np\\n\\n"
            "X = np.random.randn(500, 10); y = np.random.randint(0, 2, 500)\\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\\n\\n"
            "rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)\\n"
            "rf.fit(X_train, y_train)\\n"
            "print(f'准确率: {rf.score(X_test, y_test):.3f}')\\n"
            "print(f'特征重要性: {np.round(rf.feature_importances_, 3)}')\\n"
            "```"
        ),
        "pros": ["无需特征缩放", "抗过拟合", "特征重要性好用", "可并行训练"],
        "cons": ["模型体积大", "预测较慢(大数据)", "可解释性不如单树", "不平衡数据需调整"],
        "python_packages": ["scikit-learn", "xgboost", "lightgbm"],
        "common_errors": [
            ["过拟合", "限制max_depth=10-20"],
            ["类别不平衡", "设class_weight='balanced'"],
            ["特征太多", "增大max_features"],
        ],
    },
    

    {
        "id": "pca",
        "name": "主成分分析 (PCA)",
        "category": "统计类",
        "icon": "📉",
        "tags": ["降维", "特征提取", "可视化"],
        "summary": "通过正交变换将多个相关变量转换为少数不相关的主成分，用于降维和去噪。",
        "applicable_scenarios": ["高维数据降维", "消除多重共线性", "数据可视化(2D/3D)", "特征提取", "综合评价"],
        "math_principles": (
            "**核心思想**: 找到方差最大的投影方向\\n\\n"
            "**步骤**:\\n"
            "1. 中心化: $x_{ij} \\leftarrow x_{ij} - \\bar{x}_j$\\n"
            "2. 协方差矩阵: $\\Sigma = \\frac{1}{n-1}X^T X$\\n"
            "3. 特征分解: $\\Sigma v_i = \\lambda_i v_i$\\n"
            "4. 取前k个特征向量 $W_k$\\n"
            "5. 投影: $Z = X W_k$\\n\\n"
            "**主成分贡献率**: $\\lambda_i / \\sum \\lambda_i$\\n"
            "通常取累计贡献率 $\\geq 85\\%$ 的前k个主成分"
        ),
        "code_template": (
            "```python\\n"
            "from sklearn.decomposition import PCA\\n"
            "from sklearn.preprocessing import StandardScaler\\n"
            "import numpy as np\\n\\n"
            "X = np.random.randn(100, 20)  # 100样本 20特征\\n"
            "X_scaled = StandardScaler().fit_transform(X)\\n\\n"
            "pca = PCA().fit(X_scaled)\\n"
            "ratio = pca.explained_variance_ratio_\\n"
            "cumsum = np.cumsum(ratio)\\n"
            "n = np.argmax(cumsum >= 0.85) + 1\\n"
            "print(f'保留 {n} 个主成分(累计{np.round(cumsum[n-1]*100,1)}%)')\\n\\n"
            "Z = PCA(n_components=n).fit_transform(X_scaled)\\n"
            "print(f'降维: {X.shape[1]}特征 -> {Z.shape[1]}主成分')\\n"
            "```"
        ),
        "pros": ["消除特征相关", "有效降维降噪", "主成分独立", "有解释性(载荷)"],
        "cons": ["主成分可解释性差", "方差大≠区分力强", "对异常值敏感", "标准化影响结果"],
        "python_packages": ["scikit-learn", "numpy", "matplotlib"],
        "common_errors": [
            ["未标准化", "PCA前必须标准化(同单位除外)"],
            ["过度降维", "保留85%以上方差"],
            ["异常值干扰", "PCA前先处理异常值"],
        ],
    },
    

    {
        "id": "logistic-regression",
        "name": "逻辑回归",
        "category": "统计类",
        "icon": "📋",
        "tags": ["分类", "概率", "线性"],
        "summary": "广义线性模型，通过Sigmoid函数将线性输出映射到(0,1)区间进行二分类。",
        "applicable_scenarios": ["二分类问题", "信用评分", "疾病诊断", "用户流失预测", "风险概率评估"],
        "math_principles": (
            "**模型形式**:\\n"
            "$$P(y=1|x) = \\sigma(w^T x + b) = \\frac{1}{1+e^{-(w^T x + b)}}$$\\n\\n"
            "**决策边界**: $P=0.5$ 即 $w^T x + b = 0$\\n\\n"
            "**损失函数(交叉熵)**:\\n"
            "$$J(w) = -\\frac{1}{m}\\sum [y\\log(\\hat{y}) + (1-y)\\log(1-\\hat{y})]$$\\n\\n"
            "**优点**: 输出可解释为概率, 特征系数有明确含义"
        ),
        "code_template": (
            "```python\\n"
            "from sklearn.linear_model import LogisticRegression\\n"
            "from sklearn.model_selection import train_test_split\\n"
            "from sklearn.metrics import classification_report, roc_auc_score\\n"
            "import numpy as np\\n\\n"
            "X = np.random.randn(300, 5)\\n"
            "y = (X[:,0]*0.5 + X[:,1]*0.3 + np.random.randn(300)*0.2 > 0).astype(int)\\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\\n\\n"
            "lr = LogisticRegression().fit(X_train, y_train)\\n"
            "y_pred = lr.predict(X_test)\\n"
            "y_prob = lr.predict_proba(X_test)[:,1]\\n"
            "print(f'AUC = {roc_auc_score(y_test, y_prob):.4f}')\\n"
            "print(f'系数: {np.round(lr.coef_[0], 3)}')\\n"
            "```"
        ),
        "pros": ["输出为概率", "特征系数可解释", "训练快", "正则化版本成熟"],
        "cons": ["仅线性决策边界", "对异常值敏感", "多重共线性影响", "多分类需OvR/OvO"],
        "python_packages": ["scikit-learn", "statsmodels"],
        "common_errors": [
            ["线性不可分", "引入多项式特征或换SVM"],
            ["样本不平衡", "设class_weight='balanced'"],
            ["过拟合", "用L1/L2正则化(C调小)"],
        ],
    },
    

    {
        "id": "decision-tree",
        "name": "决策树",
        "category": "机器学习",
        "icon": "🌳",
        "tags": ["可解释", "规则", "非参数"],
        "summary": "通过树形结构学习决策规则，各节点按特征划分样本，叶节点输出预测结果。",
        "applicable_scenarios": ["可解释性强的分类", "客户画像规则提取", "医疗诊断", "信用评估", "特征筛选"],
        "math_principles": (
            "**分裂准则**:\\n"
            "- **信息增益**: $IG = H(D) - \\sum \\frac{|D_v|}{|D|} H(D_v)$\\n"
            "- **Gini指数**: $G = 1 - \\sum p_k^2$\\n\\n"
            "**剪枝策略**:\\n"
            "- 预剪枝: max_depth, min_samples_split\\n"
            "- 后剪枝: CCP(Cost Complexity Pruning)\\n\\n"
            "**优点**: 完全可解释, 不需要特征缩放"
        ),
        "code_template": (
            "```python\\n"
            "from sklearn.tree import DecisionTreeClassifier, plot_tree\\n"
            "from sklearn.model_selection import train_test_split\\n"
            "import numpy as np; import matplotlib.pyplot as plt\\n\\n"
            "X = np.random.randn(300, 4)\\n"
            "y = (X[:,0] + X[:,1] > 0).astype(int)\\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\\n\\n"
            "tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=5, random_state=42)\\n"
            "tree.fit(X_train, y_train)\\n"
            "print(f'准确率: {tree.score(X_test, y_test):.3f}')\\n"
            "print(f'特征重要性: {np.round(tree.feature_importances_, 3)}')\\n"
            "plt.figure(figsize=(12,8)); plot_tree(tree, filled=True); plt.show()\\n"
            "```"
        ),
        "pros": ["完全可解释", "不需特征缩放", "捕获非线性", "特征重要性自然"],
        "cons": ["容易过拟合", "对数据变化敏感", "方差大(改RF)", "贪心分裂非全局最优"],
        "python_packages": ["scikit-learn", "graphviz"],
        "common_errors": [
            ["过拟合", "限制max_depth/用随机森林"],
            ["连续值分裂", "离散化或使用回归树"],
            ["类别过多", "减少类别或换模型"],
        ],
    },
    

    {
        "id": "fuzzy-evaluation",
        "name": "模糊综合评价",
        "category": "评价类",
        "icon": "🌀",
        "tags": ["模糊", "评价", "隶属度"],
        "summary": "基于模糊数学理论，用隶属度描述评价对象的等级归属，处理不确定性和模糊性。",
        "applicable_scenarios": ["质量评价", "风险等级评估", "环境评价", "教师/学生评价", "方案优选"],
        "math_principles": (
            "**步骤**:\\n"
            "1. **因素集**: $U = \\{u_1, u_2, ..., u_m\\}$\\n"
            "2. **评语集**: $V = \\{v_1, v_2, ..., v_n\\}$\\n"
            "3. **隶属度矩阵**: $R = (r_{ij})_{m \\times n}$\\n"
            "4. **权重向量**: $W = (w_1, ..., w_m)$\\n"
            "5. **综合评价**: $B = W \\circ R$ （模糊合成运算）\\n\\n"
            "**常用算子**:\\n"
            "- $M(\\wedge, \\vee)$: 主因素突出型\\n"
            "- $M(\\cdot, \\oplus)$: 加权平均型(推荐)"
        ),
        "code_template": (
            "```python\\n"
            "import numpy as np\\n\\n"
            "def fuzzy_eval(weights, R):\\n"
            "    # 加权平均型 M(.,oplus)\\n"
            "    B = weights @ R\\n"
            "    return B / B.sum() if B.sum() > 0 else B\\n\\n"
            "weights = np.array([0.3, 0.25, 0.25, 0.2])  # 4个因素\\n"
            "R = np.array([\\n"
            "    [0.2, 0.5, 0.2, 0.1, 0.0],  # 因素1\\n"
            "    [0.1, 0.3, 0.4, 0.1, 0.1],\\n"
            "    [0.0, 0.2, 0.5, 0.2, 0.1],\\n"
            "    [0.3, 0.4, 0.2, 0.1, 0.0],\\n"
            "])\\n"
            "result = fuzzy_eval(weights, R)\\n"
            "grades = ['优','良','中','差','很差']\\n"
            "for i, v in enumerate(result):\\n"
            "    print(f'{grades[i]}: {v:.2%}')\\n"
            "print(f'综合评级: {grades[np.argmax(result)]}')\\n"
            "```"
        ),
        "pros": ["处理模糊性", "定性定量结合", "结果直观(隶属度)", "灵活(可选算子)"],
        "cons": ["隶属度函数主观", "权重影响大", "评语等级有限", "模糊算子选择无标准"],
        "python_packages": ["numpy"],
        "common_errors": [
            ["权重和不为1", "归一化处理"],
            ["隶属度越界", "确保0-1之间"],
            ["算子选择", "推荐加权平均型M(.,oplus)"],
        ],
    },
    

    {
        "id": "grey-prediction",
        "name": "灰色预测 GM(1,1)",
        "category": "预测类",
        "icon": "📈",
        "tags": ["小样本", "预测", "灰色系统"],
        "summary": "针对小样本(≥4)、贫信息的不确定系统，通过累加生成规整序列进行预测。",
        "applicable_scenarios": ["小样本数据预测", "短期趋势预测", "经济指标预测", "缺乏历史数据的预测", "数据量不足时的替代方案"],
        "math_principles": (
            "**GM(1,1)**: 一阶灰色模型, 1个变量\\n\\n"
            "**步骤**:\\n"
            "1. **累加生成(AGO)**: $x^{(1)}(k) = \\sum_{i=1}^k x^{(0)}(i)$\\n"
            "2. **建立微分方程**: $\\frac{dx^{(1)}}{dt} + a x^{(1)} = b$\\n"
            "3. **参数估计**: 最小二乘求 $a,b$\\n"
            "4. **时间响应**: $\\hat{x}^{(1)}(k+1) = (x^{(0)}(1)-b/a)e^{-ak} + b/a$\\n"
            "5. **累减还原**: $\\hat{x}^{(0)}(k+1) = \\hat{x}^{(1)}(k+1) - \\hat{x}^{(1)}(k)$\\n\\n"
            "**适用条件**: 任意4个以上数据点即可建模"
        ),
        "code_template": (
            "```python\\n"
            "import numpy as np\\n\\n"
            "def gm11(data):\\n"
            "    n = len(data)\\n"
            "    x1 = np.cumsum(data)\\n"
            "    B = np.array([[-0.5*(x1[i-1]+x1[i]), 1] for i in range(1,n)])\\n"
            "    Y = data[1:].reshape(-1,1)\\n"
            "    a,b = np.linalg.lstsq(B, Y, rcond=None)[0].flatten()\\n"
            "    pred = [(data[0]-b/a)*np.exp(-a*k) - (data[0]-b/a)*np.exp(-a*(k-1)) for k in range(1,n+5)]\\n"
            "    return np.array(pred)\\n\\n"
            "data = np.array([2.874, 3.278, 3.337, 3.390, 3.679])  # 5个数据点\\n"
            "pred = gm11(data)\\n"
            "for i, v in enumerate(pred):\\n"
            "    print(f'{\"拟合\" if i<5 else \"预测\"} {i+1}: {v:.4f}')\\n"
            "```"
        ),
        "pros": ["仅需4个数据点", "计算简单", "短期预测精度高", "不要求典型分布"],
        "cons": ["仅短期预测有效", "只能预测单调趋势", "波动数据效果差", "缺少统计检验"],
        "python_packages": ["numpy", "pandas"],
        "common_errors": [
            ["数据波动大", "先做平滑预处理"],
            ["预测长期", "仅建议预测3-5步"],
            ["数据量不足4", "无法应用GM(1,1)"],
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
