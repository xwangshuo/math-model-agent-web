"""
文件上传处理 — CSV/Excel 解析与数据分析
"""

import os
import io
import shutil
import uuid
from pathlib import Path

import pandas as pd

UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"


def _ensure_dir():
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(file_bytes: bytes, original_filename: str) -> str:
    """保存上传文件到 uploads 目录，返回保存后的路径"""
    _ensure_dir()
    ext = Path(original_filename).suffix.lower() or ".bin"
    safe_name = f"{uuid.uuid4().hex[:8]}_{uuid.uuid4().hex[:8]}{ext}"
    dest = UPLOADS_DIR / safe_name
    dest.write_bytes(file_bytes)
    return str(dest)


def analyze_data_file(file_path: str) -> str:
    """读取 CSV/Excel 文件, 返回数据摘要文本"""
    try:
        ext = Path(file_path).suffix.lower()
        if ext == ".csv":
            df = pd.read_csv(file_path, encoding="utf-8")
        elif ext in (".xls", ".xlsx"):
            df = pd.read_excel(file_path)
        else:
            return f"不支持的文件格式: {ext}，仅支持 .csv / .xls / .xlsx"

        buf = io.StringIO()
        buf.write(f"📊 数据文件分析结果\n")
        buf.write(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        buf.write(f"行数: {df.shape[0]}  |  列数: {df.shape[1]}\n\n")
        buf.write(f"列名: {list(df.columns)}\n\n")
        buf.write(f"数据类型:\n{df.dtypes.to_string()}\n\n")
        buf.write(f"缺失值:\n{df.isnull().sum().to_string()}\n\n")
        buf.write(f"描述统计:\n{df.describe(include='all').to_string()}\n\n")
        buf.write(f"前5行:\n{df.head().to_string()}\n")
        return buf.getvalue()
    except Exception as e:
        return f"❌ 文件读取失败: {e}"
