LATEX_SIMPLE_TEMPLATE = r"""\documentclass[12pt,a4paper]{article}

% --- 中文支持 ---
\usepackage[UTF8]{ctex}
\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}

% --- 常用宏包 ---
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{caption}
\usepackage{float}
\usepackage{enumitem}
\usepackage{algorithm}
\usepackage{algorithmic}

\title{{{title}}}
\author{{姓名\thanks{{学号: 2024xxxxxx}} \\ 华北理工大学}}
\date{{\today}}

\begin{{document}}
\maketitle

\begin{{abstract}}
{abstract}
\end{{abstract}}

\section{{问题重述}}
{restatement}

\section{{模型假设}}
{assumptions}

\section{{符号说明}}
{notations}

\section{{模型建立与求解}}
{model_solution}

\section{{结果分析}}
{analysis}

\section{{模型评价与改进}}
{evaluation}

\begin{{thebibliography}}{{9}}
\bibitem{{ref1}} 参考书目1
\end{{thebibliography}}

\end{{document}}
"""

LATEX_DETAILED_TEMPLATE = r"""\documentclass[12pt,a4paper]{article}

% --- 中文支持 ---
\usepackage[UTF8]{ctex}
\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}

% --- 常用宏包 ---
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{float}
\usepackage{enumitem}
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{multirow}
\usepackage{array}
\usepackage{mathtools}
\usepackage{listings}
\usepackage{xcolor}

\lstset{{
    basicstyle=\small\ttfamily,
    numbers=left,
    numberstyle=\tiny,
    frame=single,
    breaklines=true,
    backgroundcolor=\color[gray]{{0.95}}
}}

\title{{{title}}}
\author{{姓名\thanks{{学号: 2024xxxxxx}} \\ 华北理工大学}}
\date{{\today}}

\begin{{document}}
\maketitle

\begin{{abstract}}
{abstract}
\keywords{{{keywords}}}
\end{{abstract}}

\section{{问题重述}}
{restatement}

\subsection{{问题背景}}
{background}

\subsection{{问题要求}}
{requirements}

\section{{模型假设}}
{assumptions}

\section{{符号说明}}
{notations}

\section{{模型建立与求解}}
{model_solution}

\subsection{{数据预处理}}
{data_preprocessing}

\subsection{{模型一: }}
{model1}

\subsection{{模型二: }}
{model2}

\subsection{{模型求解}}
{solving}

\section{{结果分析}}
{analysis}

\subsection{{灵敏度分析}}
{sensitivity}

\subsection{{稳定性检验}}
{stability}

\section{{模型评价与改进}}
{evaluation}

\subsection{{模型优点}}
{pros}

\subsection{{模型缺点}}
{cons}

\subsection{{改进方向}}
{improvements}

\begin{{thebibliography}}{{9}}
\bibitem{{ref1}} 参考书目1
\bibitem{{ref2}} 参考书目2
\end{{thebibliography}}

\appendix
\section{{附录: 主要代码}}
{appendix_code}

\end{{document}}
"""

def get_template(template_type: str = "simple") -> str:
    if template_type == "detailed":
        return LATEX_DETAILED_TEMPLATE
    return LATEX_SIMPLE_TEMPLATE
