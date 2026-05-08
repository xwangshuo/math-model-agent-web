"""
代码沙箱 — 在子进程中安全执行 Python 代码，返回 stdout + base64 图表
"""

import io
import os
import sys
import json
import base64
import traceback
import subprocess
import tempfile
from pathlib import Path


def run_python_code(code: str, timeout: int = 30) -> dict:
    """在子进程中安全执行 Python 代码, 返回 stdout + 图表 base64 列表.

    返回:
        {"success": True/False, "output": str, "figures": [base64, ...], "error": str}
    """
    _VENV_PYTHON = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".venv", "bin", "python3")
    python_exe = _VENV_PYTHON if os.path.exists(_VENV_PYTHON) else sys.executable

    with tempfile.TemporaryDirectory(prefix="mathmodel_") as tmpdir:
        code_path = os.path.join(tmpdir, "user_code.py")
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(code)

        runner_path = os.path.join(tmpdir, "_runner.py")
        runner_code = f"""import sys, os, io, json, base64, traceback
os.chdir({json.dumps(tmpdir)})

old_out = sys.stdout
sys.stdout = buf = io.StringIO()

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

result_str = None
error_str = None
try:
    exec(open({json.dumps(code_path)}, encoding="utf-8").read())
except SystemExit:
    pass
except Exception:
    error_str = traceback.format_exc()
finally:
    stdout_text = buf.getvalue() or ""

# 收集 matplotlib 图表（SystemExit 后也能收集）
fig_b64s = []
for n in plt.get_fignums():
    fig = plt.figure(n)
    bio = io.BytesIO()
    fig.savefig(bio, format="png", dpi=100, bbox_inches="tight")
    bio.seek(0)
    fig_b64s.append(base64.b64encode(bio.read()).decode())
    plt.close(fig)

if stdout_text.strip() or fig_b64s:
    result_str = json.dumps({{"output": stdout_text, "figures": fig_b64s}})

sys.stdout = old_out

if result_str is not None:
    print("__MATH_RESULT__" + result_str)
elif error_str is not None:
    print("__MATH_ERROR__" + error_str)
else:
    print("__MATH_EMPTY__")
"""
        with open(runner_path, "w", encoding="utf-8") as f:
            f.write(runner_code)

        try:
            proc = subprocess.run(
                [python_exe, runner_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
        except subprocess.TimeoutExpired:
            return {"success": False, "output": "", "figures": [], "error": f"⏰ 代码执行超时（{timeout}秒）"}
        except Exception as e:
            return {"success": False, "output": "", "figures": [], "error": f"执行失败: {e}"}

        stdout = proc.stdout or ""

        if "__MATH_RESULT__" in stdout:
            data_str = stdout.split("__MATH_RESULT__")[1].strip()
            # Remove any remaining markers
            if "__MATH_ERROR__" in data_str:
                data_str = data_str.split("__MATH_ERROR__")[0].strip()
            if "__MATH_EMPTY__" in data_str:
                data_str = data_str.split("__MATH_EMPTY__")[0].strip()
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError:
                return {"success": True, "output": data_str, "figures": [], "error": ""}
            return {
                "success": True,
                "output": data.get("output", data_str),
                "figures": data.get("figures", []),
                "error": "",
            }
        elif "__MATH_ERROR__" in stdout:
            error = stdout.split("__MATH_ERROR__")[1].strip()
            return {"success": False, "output": "", "figures": [], "error": error}
        else:
            return {"success": True, "output": stdout or "✅ 执行成功", "figures": [], "error": ""}
