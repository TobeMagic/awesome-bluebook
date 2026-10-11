#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把一本书的全部 fragment 装成单文件 HTML（封面 + 目录 + 正文 + 附录，SVG 全内联）。

用法：
    python tools/build_book.py                       # 默认 deepseek-harness
    python tools/build_book.py --book deepseek-harness
    python tools/build_book.py --open                # 生成后打印路径

产出：books/<book>/<book>-bluebook.html
"""
from __future__ import annotations

import argparse
import base64
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preview import render  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- 书元信息
META = {
    "deepseek-harness": {
        "series": "蓝宝书 · 01",
        "title": "DeepSeek Harness",
        "subtitle": "一切皆插件：一个 agent harness 是怎么长出来的",
        "author": "蓝宝书",
        "tagline": "从一个能干活的外壳，讲到一套能搬走的设计",
        "release": "2026-10-09 · v3.1",
        "license": "MIT",
    }
}

# 正文顺序：§01–§16 + 附录 A/B/C/D
ORDER = [
    "00-preface.md",
    "01-model-cant-work.md",
    "02-what-is-harness.md",
    "03-three-ways.md",
    "04-four-hard-things.md",
    "05-six-layers.md",
    "06-how-assembled.md",
    "07-kernel-is-empty.md",
    "08-name-only.md",
    "09-bulletin-board.md",
    "10-take-it-down.md",
    "11-one-copy.md",
    "12-one-question.md",
    "13-five-steps.md",
    "14-three-gates.md",
    "15-four-accidents.md",
    "16-how-to-tell.md",
    "17-the-bet.md",
    "appendix-a-glossary.md",
    "appendix-b-figure-index.md",
    "appendix-c-code-map.md",
]

# 分部归属（用于目录分组）
PARTS = {
    "00": "序章",
    "01": "第 1 部 · 进门",
    "02": "第 1 部 · 进门",
    "03": "第 1 部 · 进门",
    "04": "第 1 部 · 进门",
    "05": "第 2 部 · 先看一眼",
    "06": "第 2 部 · 先看一眼",
    "07": "第 3 部 · 拆内核",
    "08": "第 3 部 · 拆内核",
    "09": "第 3 部 · 拆内核",
    "10": "第 3 部 · 拆内核",
    "11": "第 3 部 · 拆内核",
    "12": "第 4 部 · 走一遍",
    "13": "第 4 部 · 走一遍",
    "14": "第 5 部 · 碰边界",
    "15": "第 5 部 · 碰边界",
    "16": "第 6 部 · 收",
    "17": "第 6 部 · 收",
    "appendix-a": "附录",
    "appendix-b": "附录",
    "appendix-c": "附录",
}

# 各部题图（assets/ 下的文件名，随成书内联为 data URI）
FRONTIS = {
    "第 1 部 · 进门":     ("part-1-panorama.jpg", "差的不是师傅的脑子，是外面那一圈人马。"),
    "第 2 部 · 先看一眼": ("part-3-assembly.jpg", "先给地图，不给理由。"),
    "第 3 部 · 拆内核":   ("part-2-kernel.jpg",   "五个房间，各放一样东西。"),
    "第 4 部 · 走一遍":   ("part-4-flow.jpg",     "一趟活从进门到交活，中间经过谁。"),
    "第 5 部 · 碰边界":   ("part-5-boundary.jpg", "把门的三种拦法。"),
    "第 6 部 · 收":       ("part-6-paradigm.jpg", "连根拔起，种到另一块地里。"),
}
COVER_IMG = "cover.jpg"


def img_uri(name: str) -> str:
    """把 assets/ 下的图片读成 data URI，保证成书单文件自包含。"""
    fp = os.path.join(ROOT, "books", "deepseek-harness", "assets", name)
    ext = "jpeg" if name.lower().endswith((".jpg", ".jpeg")) else "png"
    with open(fp, "rb") as f:
        return f"data:image/{ext};base64," + base64.b64encode(f.read()).decode()


CSS = """
:root{--ink:#2C2C2A;--gray:#5F5E5A;--blue:#1B3A6B;--cream:#F5F0E8;--teal:#0F6E56;--line:#E3E1D8}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:#F5F0E8;color:var(--ink);
     font-family:system-ui,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;
     margin:0;padding:0;line-height:1.85;-webkit-text-size-adjust:100%}
.page{max-width:800px;margin:0 auto;background:#F5F0E8}

/* ---------- 封面：企鹅经典三段式 30 / 45 / 25 ---------- */
.cover{display:flex;flex-direction:column;min-height:100vh;position:relative}
.cover .wm{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:6}
.cover-top,.cover-mid,.cover-bot{position:relative;z-index:1}
.cover-top{background:#1B3A6B;color:#fff;flex:30 1 0;display:flex;flex-direction:column;
           justify-content:center;padding:48px 56px 40px}
.cover-top .series{font-size:13px;letter-spacing:.32em;opacity:.82;margin:0 0 20px;color:#fff}
.cover-top h1{font-size:44px;line-height:1.16;margin:0 0 10px;font-weight:700;
              letter-spacing:-.01em;color:#fff}
.cover-top .rule{width:64px;height:3px;background:#5DCAA5;margin:22px 0 0}
.cover-mid{background:#F5F0E8;flex:45 1 0;display:flex;flex-direction:column;
           justify-content:center;padding:34px 56px}
.cover-mid .illus{max-width:560px;width:100%;margin:0 auto 22px}
.cover-mid .illus img{display:block;width:100%;height:auto;border-radius:6px}
.cover-mid .sub{font-size:17px;color:var(--gray);text-align:center;margin:0;line-height:1.7}
.cover-bot{background:#1B3A6B;color:#fff;flex:25 1 0;display:flex;flex-direction:column;
           justify-content:center;align-items:center;gap:8px;padding:32px 56px;text-align:center}
.cover-bot .author{font-size:19px;letter-spacing:.14em}
.cover-bot .meta{font-size:12px;opacity:.78;line-height:1.9}
.cover-bot code{font-family:ui-monospace,Consolas,monospace;font-size:11.5px;opacity:.9}

/* ---------- 内页 ---------- */
.wrap{padding:56px 44px 96px}
h1{font-size:27px;color:var(--blue);margin:0 0 8px;line-height:1.4;letter-spacing:-.005em}
h2{font-size:18px;color:var(--blue);margin:40px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}
h3{font-size:15px;color:var(--blue);margin:26px 0 8px}
p{margin:0 0 15px;font-size:15.5px}
hr{border:0;border-top:1px solid var(--line);margin:40px 0}
ul{padding-left:22px;margin:0 0 15px}
li{font-size:15.5px;margin:5px 0}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13px;
     background:#EFEDE6;padding:1px 5px;border-radius:3px}
pre{background:#FBFAF7;border:1px solid var(--line);border-radius:8px;padding:14px 16px;
    overflow-x:auto;margin:0 0 16px}
pre code{background:none;padding:0;font-size:12.5px;line-height:1.7}
blockquote{margin:0 0 16px;padding:2px 0 2px 16px;border-left:3px solid #A9C4E4;color:#45443F}
blockquote p{font-size:14.5px;margin:0}
table{border-collapse:collapse;width:100%;margin:0 0 16px;font-size:14px}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#EDF2F9;color:var(--blue);font-weight:600}
figure{margin:22px 0;background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 20px 12px}
figure svg{display:block;width:100%;height:auto}
figcaption{font-size:13px;line-height:1.7;margin-top:12px;color:var(--gray)}
.src{color:var(--gray)}
.sec{page-break-before:always}
.sec-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.partlabel{display:inline-block;font-size:11.5px;letter-spacing:.12em;color:#fff;background:var(--blue);
           border-radius:4px;padding:3px 10px}
.part-open{margin:0}
.part-open .front{margin:22px 0 34px;background:#fff;border:1px solid var(--line);border-radius:10px;
                  padding:14px 14px 10px}
.part-open .front img{display:block;width:100%;height:auto;border-radius:6px}
.part-open .front figcaption{font-size:13px;color:var(--gray);margin-top:10px;text-align:center}

/* ---------- 目录 ---------- */
.toc{background:#fff;border:1px solid var(--line);border-radius:10px;padding:26px 30px}
.toc h2{margin-top:0;border:0;font-size:20px}
.toc-part{font-size:12px;letter-spacing:.14em;color:var(--gray);margin:22px 0 8px}
.toc-part:first-of-type{margin-top:8px}
.toc ol{list-style:none;padding:0;margin:0}
.toc li{margin:5px 0;font-size:14.5px}
.toc a{color:var(--blue);text-decoration:none;border-bottom:1px solid transparent}
.toc a:hover{border-bottom-color:#A9C4E4}
.toc .sub{display:block;font-size:13px;color:var(--gray);padding-left:16px;margin:2px 0}
.toc .sub a{color:var(--gray)}

/* ---------- 打印 / PDF ---------- */
@media print{
  body{background:#fff}
  .page{max-width:none}
  .cover{min-height:auto;height:100vh}
  figure{break-inside:avoid;background:#fff}
  pre,table{break-inside:avoid}
  h1,h2,h3{break-after:avoid}
  .toc{break-after:page}
}
@media (max-width:680px){
  .wrap{padding:32px 20px 64px}
  .cover-top,.cover-mid,.cover-bot{padding-left:26px;padding-right:26px}
  .cover-top h1{font-size:32px}
}
"""


def slug_from_h1(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not m:
        return ""
    t = re.sub(r"<[^>]+>", "", m.group(1))
    m2 = re.match(r"^§(\d+)", t.strip())
    if m2:
        return "s" + m2.group(1)
    m3 = re.match(r"^附录\s*([A-Z])", t.strip())
    if m3:
        return "apx-" + m3.group(1).lower()
    return re.sub(r"[^\w\u4e00-\u9fff]+", "-", t.strip()).strip("-")[:40]


def add_ids(html: str, base: str) -> str:
    """给 h1/h2 加锚点 id。h2 的编号形如 4.1 / 12.4.1、附录里的 A.1。"""
    def h1rep(m):
        inner = m.group(2)
        sid = base
        return f'<h1 id="{sid}">{inner}</h1>'

    html = re.sub(r"<h1([^>]*)>(.*?)</h1>", h1rep, html, flags=re.S)

    counter = [0]

    def h2rep(m):
        inner = m.group(2)
        t = re.sub(r"<[^>]+>", "", inner)
        m2 = re.match(r"^\s*([0-9A-Z]+(?:\.[0-9]+)*)", t)
        if m2:
            sid = f"{base}-{m2.group(1).replace('.', '-')}"
        else:
            counter[0] += 1
            sid = f"{base}-h{counter[0]}"
        return f'<h2 id="{sid}">{inner}</h2>'

    return re.sub(r"<h2([^>]*)>(.*?)</h2>", h2rep, html, flags=re.S)


def build_toc(entries) -> str:
    """entries: [(part, sid, title, [(hsid, htitle), ...]), ...]"""
    out = ['<div class="toc" id="toc"><h2>目录</h2>']
    last_part = None
    open_ol = False
    for part, sid, title, subs in entries:
        if part != last_part:
            if open_ol:
                out.append("</ol>")
            out.append(f'<div class="toc-part">{part}</div><ol>')
            open_ol = True
            last_part = part
        out.append(f'<li><a href="#{sid}">{title}</a>')
        if subs:
            for hsid, htitle in subs:
                out.append(f'<span class="sub"><a href="#{hsid}">{htitle}</a></span>')
        out.append("</li>")
    if open_ol:
        out.append("</ol>")
    out.append("</div>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="deepseek-harness")
    ap.add_argument("--open", action="store_true", help="生成后打印绝对路径")
    args = ap.parse_args()

    meta = META.get(args.book)
    if not meta:
        sys.exit(f"没有 {args.book} 的元信息，请先在 META 里补")

    frag_dir = os.path.join(ROOT, "books", args.book, "fragments")
    bodies, entries = [], []
    cur_part = None
    part_n = 0

    for name in ORDER:
        fp = os.path.join(frag_dir, name)
        if not os.path.exists(fp):
            print(f"[warn] 缺 {name}，跳过")
            continue
        md = open(fp, encoding="utf-8").read()
        html = render(md, frag_dir)
        key = name.split("-")[0]
        if name.startswith("appendix"):
            key = "-".join(name.split("-")[:2])
        sid = slug_from_h1(html) or key
        html = add_ids(html, sid)

        title = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        title = re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else name
        subs = [
            (m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip())
            for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', html, re.S)
        ]
        entries.append((PARTS.get(key, "其他"), sid, title, subs))

        part = PARTS.get(key, "其他")
        # 换部时插一张题图；附录无题图，只插一条分隔标签
        if part != cur_part:
            cur_part = part
            part_n += 1
            if part in FRONTIS:
                img, cap = FRONTIS[part]
                bodies.append(
                    f'<section class="part-open" id="part-{part_n}"><span class="partlabel">{part}</span>'
                    f'<figure class="front"><img src="{img_uri(img)}" alt="{part}题图"/>'
                    f"<figcaption>{cap}</figcaption></figure></section>"
                )
            else:
                bodies.append(f'<section class="part-open" id="part-{part_n}"><span class="partlabel">{part}</span></section>')
        bodies.append(f'<section class="sec" id="{sid}-sec">{html}</section>')

    cover = f"""
<section class="cover" id="cover">
  <div class="cover-top">
    <p class="series">{meta['series']}</p>
    <h1>{meta['title']}</h1>
    <div class="rule"></div>
  </div>
  <div class="cover-mid">
    <div class="illus"><img src="{img_uri(COVER_IMG)}" alt="封面插画：一棵树干极细的插件树，枝头挂着可拆卸的方块零件"/></div>
    <p class="sub">{meta['subtitle']}</p>
  </div>
  <div class="cover-bot">
    <div class="author">{meta['author']} 著</div>
    <div class="meta">{meta['tagline']}<br>
      版本 {meta['release']}<br>
      许可 {meta['license']} · 与上游项目一致</div>
  </div>
  <svg class="wm" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <pattern id="wm-p" width="240" height="150" patternUnits="userSpaceOnUse"
               patternTransform="rotate(-22)">
        <text x="12" y="24" font-size="15" font-family="system-ui,'PingFang SC','Microsoft YaHei',sans-serif"
              fill="#808080" fill-opacity="0.16" letter-spacing="2">计算机魔术师</text>
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#wm-p)"/>
  </svg>
</section>
"""

    toc = build_toc(entries)

    html = (
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{meta['title']} · 蓝宝书</title>"
        f"<style>{CSS}</style></head><body><div class='page'>"
        f"{cover}<div class='wrap'>{toc}"
        + "\n".join(bodies)
        + "</div></div></body></html>"
    )

    dst = os.path.join(ROOT, "books", args.book, f"{args.book}-bluebook.html")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {os.path.relpath(dst, ROOT)}  ({len(html) / 1024:.0f} KB, {len(entries)} 节)")
    if args.open:
        print(dst)


if __name__ == "__main__":
    main()
