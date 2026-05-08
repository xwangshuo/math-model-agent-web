"""
数模数据分析工具箱 — 生成可直接在沙箱中运行的 Python 代码
"""

from pathlib import Path


def generate_eda_code(file_path: str) -> str:
    """生成一键 EDA 的 Python 代码"""
    ext = Path(file_path).suffix.lower()
    return f'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

if "{ext}" == ".csv":
    df = pd.read_csv(r"{file_path}", encoding="utf-8")
elif "{ext}" in (".xls", ".xlsx"):
    df = pd.read_excel(r"{file_path}")
else:
    print("❌ 不支持的文件格式")
    exit()

output_lines = []

# 1. 数据概览
output_lines.append("=" * 50)
output_lines.append("📊 数据概览")
output_lines.append("=" * 50)
output_lines.append(f"形状: {{df.shape[0]}} 行 × {{df.shape[1]}} 列")

# 2. 缺失值统计
output_lines.append("\\n" + "=" * 50)
output_lines.append("🔍 缺失值统计")
output_lines.append("=" * 50)
missing = df.isnull().sum()
mv = missing[missing > 0]
if len(mv) > 0:
    for col, cnt in mv.items():
        output_lines.append(f"  {{col}}: {{cnt}} ({{cnt/len(df)*100:.1f}}%)")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, ax=ax)
    ax.set_title("缺失值热图")
else:
    output_lines.append("  ✅ 无缺失值")

# 3. 数值列统计
numeric_cols = df.select_dtypes(include=[np.number]).columns
output_lines.append("\\n" + "=" * 50)
output_lines.append("📈 数值列描述统计")
output_lines.append("=" * 50)
if len(numeric_cols) > 0:
    output_lines.append(df[numeric_cols].describe().round(3).to_string())

# 4. 相关性矩阵
if len(numeric_cols) >= 2:
    fig, ax = plt.subplots(figsize=(8, 6))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax)
    ax.set_title("相关性矩阵")

# 5. 分布图（前 6 个数值列）
for col in numeric_cols[:6]:
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    df[col].hist(bins=30, ax=axes[0], edgecolor="black")
    axes[0].set_title(f"{{col}} 分布")
    df.boxplot(column=col, ax=axes[1])
    axes[1].set_title(f"{{col}} 箱线图")
    plt.tight_layout()

print("\\n".join(output_lines))
'''


def generate_outlier_detection_code(file_path: str, method: str = "iqr") -> str:
    """生成异常值检测代码"""
    ext = Path(file_path).suffix.lower()
    return f'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

if "{ext}" == ".csv":
    df = pd.read_csv(r"{file_path}", encoding="utf-8")
elif "{ext}" in (".xls", ".xlsx"):
    df = pd.read_excel(r"{file_path}")
else:
    print("❌ 不支持的文件格式")
    exit()

numeric_cols = df.select_dtypes(include=[np.number]).columns
output_lines = []
method = "{method}"
output_lines.append(f"异常值检测方法: {{method}}")
output_lines.append("=" * 50)

for col in numeric_cols:
    data = df[col].dropna()
    outliers = pd.Series(dtype=float)

    if method == "iqr":
        q1, q3 = data.quantile(0.25), data.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
        outliers = data[(data < lower) | (data > upper)]
    elif method == "zscore":
        z = (data - data.mean()) / data.std()
        outliers = data[z.abs() > 3]
    else:
        continue

    if len(outliers) > 0:
        output_lines.append(f"  {{col}}: {{len(outliers)}} 个异常值 ({{len(outliers)/len(data)*100:.1f}}%)")
        fig, ax = plt.subplots(figsize=(10, 2.5))
        ax.boxplot(data, vert=False, patch_artist=True)
        ax.scatter(outliers, [1]*len(outliers), color="red", alpha=0.6, s=30)
        ax.set_title(f"{{col}} - 红色=异常值 [{{method}}]")
        ax.set_yticks([])
        plt.tight_layout()

if len(output_lines) == 1:
    output_lines.append("  ✅ 未检测到异常值")

print("\\n".join(output_lines))
'''


def generate_missing_value_code(file_path: str) -> str:
    """生成缺失值分析 + 策略推荐代码"""
    ext = Path(file_path).suffix.lower()
    return f'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

if "{ext}" == ".csv":
    df = pd.read_csv(r"{file_path}", encoding="utf-8")
elif "{ext}" in (".xls", ".xlsx"):
    df = pd.read_excel(r"{file_path}")
else:
    print("❌ 不支持的文件格式")
    exit()

output_lines = []

# 缺失值概览
output_lines.append("=" * 50)
output_lines.append("🔍 缺失值全景分析")
output_lines.append("=" * 50)
total_missing = df.isnull().sum().sum()
total_cells = df.shape[0] * df.shape[1]
output_lines.append(f"总缺失值: {{total_missing}} / {{total_cells}} ({{total_missing/total_cells*100:.2f}}%)")
output_lines.append(f"完整行: {{df.dropna().shape[0]}} / {{df.shape[0]}}")

missing = df.isnull().sum()
mv = missing[missing > 0].sort_values(ascending=False)
if len(mv) == 0:
    output_lines.append("\\n✅ 无缺失值")
    print("\\n".join(output_lines))
    exit()

output_lines.append(f"\\n有缺失值的列 ({{len(mv)}} 列):")
for col, cnt in mv.items():
    output_lines.append(f"  {{col}}: {{cnt}} ({{cnt/len(df)*100:.1f}}%)")

# 缺失值热图
fig, ax = plt.subplots(figsize=(10, 4))
sns.heatmap(df.isnull(), cbar=False, yticklabels=False, ax=ax)
ax.set_title("缺失值模式热图（亮色=缺失）")

# 缺失率条形图
fig, ax = plt.subplots(figsize=(10, 4))
rates = (mv / len(df) * 100).head(20)
ax.barh(range(len(rates)), rates.values, color="coral", edgecolor="black")
ax.set_yticks(range(len(rates)))
ax.set_yticklabels(rates.index)
ax.set_xlabel("缺失率 (%)")
ax.set_title("各列缺失率 Top20")
ax.invert_yaxis()
plt.tight_layout()

# 推荐策略
output_lines.append("\\n" + "=" * 50)
output_lines.append("💡 推荐缺失值处理策略")
output_lines.append("=" * 50)
for col in mv.index:
    rate = mv[col] / len(df) * 100
    is_num = np.issubdtype(df[col].dtype, np.number)
    output_lines.append(f"\\n📌 {{col}} (缺失率 {{rate:.1f}}%)")
    if rate > 50:
        output_lines.append(f"   ⚠️ 缺失率 >50%，建议删除此列")
        output_lines.append(f"   df.drop(columns=['{{col}}'])")
    elif is_num:
        skew = df[col].skew()
        if abs(skew) < 1:
            output_lines.append(f"   ✅ 推荐: 均值填充 (分布对称)")
            output_lines.append(f"   df['{{col}}'].fillna(df['{{col}}'].mean())")
        else:
            output_lines.append(f"   ✅ 推荐: 中位数填充 (偏态分布)")
            output_lines.append(f"   df['{{col}}'].fillna(df['{{col}}'].median())")
        output_lines.append(f"   🔧 进阶: KNNImputer / 插值法")
    else:
        mode_val = df[col].mode()
        if len(mode_val) > 0:
            output_lines.append(f"   ✅ 推荐: 众数填充 (分类变量)")
            output_lines.append(f"   df['{{col}}'].fillna('{{mode_val.iloc[0]}}')")

print("\\n".join(output_lines))
'''
