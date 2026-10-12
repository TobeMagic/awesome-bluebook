#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 fragment markdown 渲染成单页 HTML 预览（SVG 内联，脱离相对路径也能看）。

用法：
    python tools/preview.py                                  # 默认渲染 §03
    python tools/preview.py books/deepseek-harness/fragments/03-full-map.md

产出：与源文件同目录的 <同名>.html

只支持蓝宝书实际用到的 markdown 子集：标题 / 分隔线 / 围栏代码 / 表格 /
无序列表 / 图片 / 段落 / 行内 code 与加粗。够用即可，不追求通用。
"""
from __future__ import annotations

import argparse
import os
import re
import sys

CSS = """
body{background:#F5F0E8;color:#2C2C2A;font-family:system-ui,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;
     margin:0;padding:40px 20px 80px;line-height:1.85}
.wrap{max-width:760px;margin:0 auto}
h1{font-size:24px;color:#1B3A6B;margin:0 0 6px;line-height:1.4}
h2{font-size:18px;color:#1B3A6B;margin:38px 0 12px;padding-bottom:6px;border-bottom:1px solid #E3E1D8}
h3{font-size:15px;color:#1B3A6B;margin:26px 0 8px}
p{margin:0 0 14px;font-size:15px}
hr{border:0;border-top:1px solid #E3E1D8;margin:34px 0}
ul{padding-left:22px;margin:0 0 14px}
li{font-size:15px;margin:4px 0}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13px;
     background:#EFEDE6;padding:1px 5px;border-radius:3px}
pre{background:#FBFAF7;border:1px solid #E3E1D8;border-radius:8px;padding:14px 16px;overflow-x:auto;margin:0 0 14px}
pre code{background:none;padding:0;font-size:12.5px;line-height:1.7}
table{border-collapse:collapse;width:100%;margin:0 0 14px;font-size:14px}
th,td{border:1px solid #E3E1D8;padding:7px 10px;text-align:left}
th{background:#EDF2F9;color:#1B3A6B;font-weight:600}
figure{margin:20px 0;background:#fff;border:1px solid #E3E1D8;border-radius:10px;padding:18px 20px 12px}
figure svg{display:block}
figcaption{font-size:13px;line-height:1.7;margin-top:12px}
.src{color:#5F5E5A}
.tag{display:inline-block;font-size:12px;color:#5F5E5A;background:#EFEDE6;border-radius:4px;
     padding:2px 8px;margin-bottom:20px}
"""


def inline(s: str) -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"〔([^〔〕]*)〕", r'<span class="src">〔\1〕</span>', s)
    return s


def render(md: str, base_dir: str, inline_svg: bool = True) -> str:
    lines = md.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # HTML 注释（如 <!-- FIGURES ... --> 画图规格），不进正文
        if line.strip().startswith("<!--"):
            while i < n and "-->" not in lines[i]:
                i += 1
            i += 1
            continue

        # 围栏代码块
        if line.startswith("```"):
            lang = line[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{lang}"' if lang else ""
            out.append("<pre><code" + cls + ">" + inline("\n".join(buf)) + "</code></pre>")
            continue

        # 分隔线
        if line.strip() == "---":
            out.append("<hr/>")
            i += 1
            continue

        # 标题
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            lv = len(m.group(1))
            out.append(f"<h{lv}>{inline(m.group(2))}</h{lv}>")
            i += 1
            continue

        # 图片（SVG 内联，其余走 <img>）
        m = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", line)
        if m:
            alt, rel = m.group(1), m.group(2)
            fp = os.path.join(base_dir, rel.replace("/", os.sep))
            parts = []
            if inline_svg and rel.lower().endswith(".svg") and os.path.exists(fp):
                parts.append(open(fp, encoding="utf-8").read().strip())
            else:
                parts.append(f'<img src="{rel}" alt="{alt}" width="100%"/>')
            i += 1
            # 紧随其后的 **图 N-N：……** 行收进 figcaption
            j = i
            while j < n and not lines[j].strip():
                j += 1
            if j < n and re.match(r"^\*\*图\s*", lines[j].strip()):
                cap = re.sub(r"^\*\*(.+?)\*\*", r"\1", lines[j].strip())
                parts.append("<figcaption>" + inline(cap) + "</figcaption>")
                i = j + 1
            out.append("<figure>" + "".join(parts) + "</figure>")
            continue

        # 引用块（官方原话）
        if re.match(r"^>\s?", line):
            buf = []
            while i < n and re.match(r"^>\s?", lines[i]):
                buf.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            # 块内空行分段
            paras, cur = [], []
            for b in buf:
                if b.strip():
                    cur.append(b.strip())
                elif cur:
                    paras.append(cur)
                    cur = []
            if cur:
                paras.append(cur)
            body = "".join(
                "<p>" + inline("".join(p)) + "</p>" for p in paras if p
            )
            out.append("<blockquote>" + body + "</blockquote>")
            continue

        # 表格
        if line.strip().startswith("|"):
            buf = []
            while i < n and lines[i].strip().startswith("|"):
                buf.append(lines[i].strip())
                i += 1
            rows = []
            for r in buf:
                cells = [c.strip() for c in r.strip("|").split("|")]
                if all(set(c) <= set("-: ") for c in cells):
                    continue
                rows.append(cells)
            if rows:
                head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
                body = "".join(
                    "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                    for r in rows[1:]
                )
                out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
            continue

        # 无序列表
        if re.match(r"^[-*]\s+", line):
            buf = []
            while i < n and re.match(r"^[-*]\s+", lines[i]):
                buf.append(re.sub(r"^[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in buf) + "</ul>")
            continue

        # 空行
        if not line.strip():
            i += 1
            continue

        # 段落
        buf = []
        while i < n and lines[i].strip() and not re.match(
            r"^(```|---|#{1,3}\s|!\[|\||[-*]\s|>\s?)", lines[i]
        ):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append("<p>" + inline("".join(buf)) + "</p>")

    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "fragment",
        nargs="?",
        default="books/deepseek-harness/fragments/03-full-map.md",
    )
    args = ap.parse_args()

    src = args.fragment
    if not os.path.exists(src):
        sys.exit(f"找不到：{src}")
    base_dir = os.path.dirname(src)

    md = open(src, encoding="utf-8").read()
    body = render(md, base_dir)
    title = os.path.basename(src)

    html = (
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{title}</title><style>{CSS}</style></head><body><div class='wrap'>"
        "<span class='tag'>蓝宝书 · 片段预览 · SVG 内联</span>"
        f"{body}</div></body></html>"
    )

    dst = os.path.splitext(src)[0] + ".html"
    with open(dst, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", dst)


if __name__ == "__main__":
    main()
