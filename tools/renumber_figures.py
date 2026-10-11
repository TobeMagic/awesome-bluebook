#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全书图号重排：以图片文件名为唯一权威源，按 build_book.ORDER 的顺序
把各片段里的局部图号（图 1、图 2……）重写成全书流水号。

规则：
- 图片文件名第一次出现 → 图注标〔本书〕；之后再出现 → 〔重印自 §NN〕（NN 为首用节）
- 图片行 alt、加粗图注行、正文里的「图 N」提及，全部按本文件局部映射改写
- 文末 <!-- FIGURES --> 清单同步重写
- 幂等：重跑结果不变（局部映射按图片行出现顺序重建，与旧图号无关）
"""
from __future__ import annotations

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_book import ORDER  # noqa: E402

FRAG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "books", "deepseek-harness", "fragments")

IMG_RE = re.compile(r"^(!\[图\s*[^\]]*?\]\(\.\./figures/([a-z0-9\-]+\.svg)\))\s*$")
CAP_RE = re.compile(r"^\*\*图\s*\d+(?:[-–]\d+)?[：:](.+?)\*\*(?:\s*〔([^〕]*)〕)?\s*$")
SEC_OF = {name: ("§" + name[:2]) if name[:2].isdigit()
          else "附录 " + name.split("-")[1].upper()
          for name in ORDER}


def sec_of_file(fname: str) -> str:
    key = fname[:-3] if fname.endswith(".md") else fname
    if key[:2].isdigit():
        return "§" + key[:2]
    return "附录 " + key.split("-")[1].upper()


def main() -> None:
    seq_of: dict[str, int] = {}      # filename -> global seq
    first_sec: dict[str, str] = {}   # filename -> first-use section label
    counter = 0
    index_rows = []                  # (seq, filename, caption, section)

    for fname in ORDER:
        path = os.path.join(FRAG, fname)
        if not os.path.exists(path):
            print(f"!! 缺文件 {fname}")
            continue
        raw = io.open(path, encoding="utf-8").read()
        lines = raw.split("\n")

        # 第一遍：本文件的局部映射（按图片行出现顺序）
        local: dict[int, int] = {}
        local_order: list[tuple[int, str]] = []
        for ln in lines:
            m = IMG_RE.match(ln)
            if m:
                fn = m.group(2)
                if fn not in seq_of:
                    counter += 1
                    seq_of[fn] = counter
                    first_sec[fn] = sec_of_file(fname)
                g = seq_of[fn]
                local_order.append((g, fn))
        # 局部旧号 = 出现次序（1 起），与文件里写的旧图号无关——
        # 但正文「图 N」提及用的是旧图号，所以按旧号映射：
        old_nums: list[int] = []
        for ln in lines:
            m = IMG_RE.match(ln)
            if m:
                mo = re.search(r"!\[图\s*(\d+)", ln)
                old_nums.append(int(mo.group(1)) if mo else len(old_nums) + 1)
        for old, (g, _fn) in zip(old_nums, local_order):
            local[old] = g

        # 第二遍：改写
        out = []
        in_comment = False
        pending_global: int | None = None  # 刚遇到的图片行对应的全局号
        fig_entries = []
        for ln in lines:
            if "<!--" in ln:
                in_comment = True
                if "FIGURES" in ln:
                    continue  # 旧的 FIGURES 块整段丢弃，最后重建
            if in_comment:
                if "-->" in ln:
                    in_comment = False
                continue
            m = IMG_RE.match(ln)
            if m:
                fn = m.group(2)
                g = seq_of[fn]
                alt_text = re.sub(r"^!\[图\s*\d+[：:]", "", m.group(1))
                alt_text = re.sub(r"^!\[图\s*[^\：:]*[：:]?", "", m.group(1))
                inner = re.search(r"!\[图\s*\d+[：:](.*?)\]\(", m.group(1))
                alt = inner.group(1) if inner else ""
                out.append(f"![图 {g}：{alt}](../figures/{fn})")
                pending_global = g
                continue
            c = CAP_RE.match(ln)
            if c and pending_global is not None:
                g = pending_global
                marker = "本书" if first_sec[seq_of and [k for k, v in seq_of.items() if v == g][0]] == sec_of_file(fname) else None
                # 首用节即本文件 → 〔本书〕，否则 〔重印自 §NN〕
                fn = [k for k, v in seq_of.items() if v == g][0]
                if first_sec[fn] == sec_of_file(fname):
                    mark = "〔本书〕"
                else:
                    mark = f"〔重印自 {first_sec[fn]}〕"
                caption = c.group(1).strip()
                out.append(f"**图 {g}：{caption}**{mark}")
                fig_entries.append((g, fn, caption, mark))
                index_rows.append((g, fn, caption, sec_of_file(fname), mark))
                pending_global = None
                continue
            # 正文里的「图 N」提及（跳过图片行与图注行，已在上面处理）
            def _sub(mo: re.Match) -> str:
                old = int(mo.group(1))
                return f"图 {local[old]}" if old in local else mo.group(0)
            ln2 = re.sub(r"图\s*(\d+)(?![-–\d])", _sub, ln)
            out.append(ln2)
        # 重建 FIGURES 清单
        out.append("")
        out.append("<!-- FIGURES")
        for g, fn, cap, mark in fig_entries:
            out.append(f"图 {g} {fn[:-4]} {mark}")
        out.append("-->")
        io.open(path, "w", encoding="utf-8").write("\n".join(out).rstrip("\n") + "\n")
        print(f"{fname}: {len(fig_entries)} 图")

    # 输出图索引数据（供附录 B 生成用）
    import json
    tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".tmp")
    os.makedirs(tmp, exist_ok=True)
    io.open(os.path.join(tmp, "figindex.json"), "w", encoding="utf-8").write(
        json.dumps([{"seq": g, "file": fn, "caption": cap, "section": sec, "mark": mark}
                    for g, fn, cap, sec, mark in index_rows],
                   ensure_ascii=False, indent=1))
    print(f"\n共 {counter} 张图（唯一文件），{len(index_rows)} 处引用 -> .tmp/figindex.json")


if __name__ == "__main__":
    main()
