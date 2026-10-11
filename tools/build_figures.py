#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝宝书 SVG 总装入口

用法：
    python tools/build_figures.py                       # 全部书的全部图
    python tools/build_figures.py --book deepseek-harness
    python tools/build_figures.py --only 4-1 5-3        # 只重生成指定图

每个 figs_*.py 模块暴露一个 FIGURES 列表，元素是 (fig_id, callable) 或 callable。
fig_id 形如 "4-1"，便于 --only 过滤。
"""
from __future__ import annotations

import argparse
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODULES = [
    "figs_intro",       # §01–§02（背景部）
    "figs_core",        # §03–§07（设计主张）
    "figs_assembly",    # §08–§09（架构）
    "figs_runtime",     # §10–§12（运行）
    "figs_bounds",      # §13–§14（边界）
    "figs_paradigm",    # §15–§16（带走）
]

# gen_figures.py 里的 §01–§03 图（自带 FIGURES，元素是裸 callable）
LEGACY = "gen_figures"


def load_modules():
    mods = []
    for name in MODULES:
        try:
            mods.append(importlib.import_module(name))
        except ModuleNotFoundError:
            print(f"[skip] {name}.py 不存在，跳过")
    try:
        mods.append(importlib.import_module(LEGACY))
    except ModuleNotFoundError:
        pass
    return mods


def collect(mods):
    """返回 [(fig_id_or_None, fn), ...]"""
    out = []
    for m in mods:
        for item in getattr(m, "FIGURES", []):
            if isinstance(item, tuple):
                out.append(item)
            else:
                out.append((None, item))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="deepseek-harness")
    ap.add_argument("--root", default="books")
    ap.add_argument("--only", nargs="*", default=None,
                    help="只生成指定 fig id，如 4-1 5-3；不给则全生成")
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(root, args.root, args.book, "figures")

    items = collect(load_modules())
    n = 0
    for fid, fn in items:
        if args.only and fid not in args.only:
            continue
        fp = fn(out_dir)
        n += 1
        print(f"wrote {os.path.relpath(fp, root)}")
    print(f"\n共生成 {n} 张图 → {os.path.relpath(out_dir, root)}")


if __name__ == "__main__":
    main()
