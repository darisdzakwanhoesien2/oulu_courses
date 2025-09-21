#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge per-video TXT annotations into one CSV for Kaggle submission.

TXT LINE FORMAT (this script expects):
    start_time end_time class

Output CSV columns:
    ID, video_id, class, start_time, end_time

Usage:
    python S3_merge_txt_to_csv.py input_dir submission.csv
Optional:
    --recursive           # search .txt files recursively
    --id_start 0          # starting ID index
"""

import os
import re
import csv
import argparse
from pathlib import Path
from typing import List, Tuple

def find_txt_files(root: Path, recursive: bool) -> List[Path]:
    if recursive:
        return sorted([p for p in root.rglob("*.txt") if p.is_file()])
    return sorted([p for p in root.glob("*.txt") if p.is_file()])

def parse_line_as_start_end_class(line: str, path: Path, line_no: int) -> Tuple[float, float, str]:
    """
    Parse a single line in the format:
        start_time end_time class
    Split by commas or whitespace. Extra columns are ignored.
    """
    raw = line.strip()
    if not raw or raw.startswith("#") or raw.startswith("//"):
        raise ValueError("SKIP")  # use exception to signal caller to skip silently

    parts = re.split(r"[,\s]+", raw)
    if len(parts) < 3:
        raise ValueError(f"{path.name} line {line_no}: expected 3 columns, got: '{line}'")

    # Expect: start, end, class
    try:
        start = float(parts[0])
        end = float(parts[1])
    except Exception:
        raise ValueError(f"{path.name} line {line_no}: start/end must be numeric, got: '{line}'")

    klass = parts[2]
    # tidy class: if purely numeric like '10' or '10.0' cast to int-string
    try:
        if re.fullmatch(r"[+-]?\d+(\.0+)?", klass):
            klass = str(int(float(klass)))
    except Exception:
        pass

    # fix swapped boundaries
    if end < start:
        start, end = end, start

    return start, end, str(klass)

def merge_txts_to_csv(input_dir: str, out_csv: str, recursive: bool = False, id_start: int = 0) -> None:
    in_dir = Path(input_dir)
    if not in_dir.exists():
        raise FileNotFoundError(f"Input dir not found: {in_dir}")

    txt_files = find_txt_files(in_dir, recursive)
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found under {in_dir} (recursive={recursive}).")

    rows = []
    next_id = id_start
    errors = 0
    parsed = 0

    for txt in txt_files:
        video_id = txt.stem  # 保留前导零，如 0012
        with txt.open("r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f, 1):
                try:
                    start, end, klass = parse_line_as_start_end_class(line, txt, i)
                except ValueError as e:
                    # "SKIP" 表示注释或空行
                    if str(e) == "SKIP":
                        continue
                    print(f"[WARN] {e}")
                    errors += 1
                    continue

                rows.append([next_id, video_id, klass, start, end])
                next_id += 1
                parsed += 1

    # write CSV
    out_path = Path(out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "video_id", "class", "start_time", "end_time"])
        writer.writerows(rows)

    print(f"✅ Done. Wrote {len(rows)} rows to: {out_path}")
    print(f"   Parsed lines: {parsed}, Warnings: {errors}")
    print(f"   Files merged: {len(txt_files)} (recursive={recursive})")

def main():
    ap = argparse.ArgumentParser(description="Merge TXT annotations (start end class) into submission.csv")
    ap.add_argument("input_dir", help="Directory containing per-video .txt files")
    ap.add_argument("out_csv", help="Output CSV path, e.g., submission.csv")
    ap.add_argument("--recursive", action="store_true", help="Search .txt files recursively")
    ap.add_argument("--id_start", type=int, default=0, help="Starting ID index (default 0)")
    args = ap.parse_args()

    merge_txts_to_csv(args.input_dir, args.out_csv, recursive=args.recursive, id_start=args.id_start)

if __name__ == "__main__":
    main()