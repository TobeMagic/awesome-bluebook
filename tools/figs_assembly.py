#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝宝书 §09–§11 图（装配部分）。

配合 tools/build_figures.py 使用：
    python tools/build_figures.py --only 9-1 9-2 9-3 10-1 10-2 10-3 11-1 11-2 11-3
"""
from __future__ import annotations

from svgkit import (  # noqa: F401
    INK, GRAY, BLUE, CREAM, TEAL, LINE, HAIR, PAPER,
    B1, B2, B3, B4, ONB, T1,
    rect, txt, vtxt, path, line, circle, diamond, note, tag, banner, write,
    W,
)


# ---------------------------------------------------------------- 图 28
def fig_9_1(out_dir):
    b = []
    boxes = [
        (40, "profile", BLUE, "一份名单", ["· 组合包（按序叠放）", "· 树外插件"]),
        (255, "bundle", BLUE, "一个 npm 包", ["· 配置项", "· 挂载代码"]),
        (470, "patch", BLUE, "按 id 定位一行", ["· 改已有行", "· 或 insert 新行"]),
    ]
    for x, name, accent, sub, lines_ in boxes:
        cx = x + 95
        b.append(rect(x, 30, 190, 112, fill=B1, stroke=HAIR))
        b.append(txt(cx, 54, name, size=13.5, fill=accent, weight=600, anchor="middle", mono=True))
        b.append(txt(cx, 74, sub, size=11, fill=GRAY, anchor="middle"))
        b.append(txt(x + 16, 98, lines_[0], size=11, fill=INK))
        b.append(txt(x + 16, 118, lines_[1], size=11, fill=INK))

    b.append(txt(135, 196, "决定装什么", size=11.5, fill=INK, anchor="middle"))
    b.append(line(178, 196, 244, 196, stroke=GRAY, sw=1.2, marker="ar"))
    b.append(txt(350, 196, "给默认值", size=11.5, fill=INK, anchor="middle"))
    b.append(line(393, 196, 459, 196, stroke=GRAY, sw=1.2, marker="ar"))
    b.append(txt(565, 196, "给最终值", size=11.5, fill=INK, anchor="middle"))

    b.extend(banner(40, 228, 620, "三者不重叠：profile 定名单，bundle 供零件，patch 只改具体行。"))
    b.append(note(40, 278, "profile = $DSH_HOME/profiles/<name> · bundle = npm 包 · patch = cordis.patch.yml"))
    return write(
        out_dir, "fig-9-1-three-roles.svg", 294,
        "图 25：三个角色各管一段，互不重叠",
        "三个并列方框。profile 是一份名单，列着组合包与树外插件；bundle 是一个 npm 包，装着配置项与挂载代码；"
        "patch 按 id 定位一行。下方箭头连成一段：决定装什么 → 给默认值 → 给最终值。三者管的事互不重叠。",
        b,
    )


# ---------------------------------------------------------------- 图 29
def fig_9_3(out_dir):
    b = []
    b.append(rect(40, 40, 160, 140, fill=B1, stroke=HAIR))
    b.append(txt(52, 62, "想改的字段", size=11.5, fill=INK, weight=600))
    b.append(txt(52, 88, "persona: 简洁", size=11, fill=INK, mono=True))
    b.append(txt(52, 110, "hmr: false", size=11, fill=INK, mono=True))
    b.append(txt(52, 140, "只写这两处", size=10.5, fill=GRAY))

    b.append(line(206, 110, 234, 110, stroke=GRAY, sw=1.2, marker="ar"))

    b.append(rect(240, 40, 160, 140, fill=PAPER, stroke=LINE, dash="4 3"))
    b.append(txt(252, 62, "差量", size=11.5, fill=INK, weight=600))
    b.append(txt(252, 88, "persona: 简洁", size=11, fill=GRAY, mono=True))
    b.append(txt(252, 110, "hmr: false", size=11, fill=GRAY, mono=True))
    b.append(line(250, 88, 318, 88, stroke=GRAY, sw=1.0))
    b.append(line(250, 110, 318, 110, stroke=GRAY, sw=1.0))
    b.append(txt(252, 140, "系统不收", size=10.5, fill=GRAY))

    b.append(line(406, 110, 434, 110, stroke=GRAY, sw=1.2, marker="ar"))

    b.append(rect(440, 40, 220, 140, fill=B1, stroke=HAIR))
    b.append(txt(452, 62, "整块 config", size=11.5, fill=INK, weight=600))
    b.append(txt(452, 84, "persona: 简洁", size=11, fill=INK, mono=True))
    b.append(txt(452, 106, "hmr: false", size=11, fill=INK, mono=True))
    b.append(txt(452, 128, "tools: { … }", size=11, fill=INK, mono=True))
    b.append(txt(452, 150, "# 其余字段照抄", size=11, fill=GRAY, mono=True))

    b.extend(banner(40, 196, 620, "系统不收差量：patch 交出的是整块 config，想保留的字段要重述一遍。"))
    b.append(note(40, 238, "官方已知限制：覆盖替换整个设置块，不自动合并 · 该包自己的说明"))
    return write(
        out_dir, "fig-9-3-replace-not-merge.svg", 252,
        "图 26：patch 交出的是整块 config，不是差量",
        "左右对照。左框是「想改的字段」，中框是「差量」并画了删除线，右框是「整块 config，其余字段照抄」。"
        "系统不收差量：patch 必须写全，想保留的字段要自己重述一遍。",
        b,
    )


# ---------------------------------------------------------------- 图 31
def fig_10_3(out_dir):
    bars = [
        ("共享底板", 94, 60, TEAL, False),
        ("满编", 112, 170, B3, False),
        ("不合群", 32, 280, B3, True),
        ("带徒弟", 7, 390, B3, False),
        ("轻装", 5, 500, B3, False),
        ("招新", 5, 610, B3, False),
    ]
    base_y, bw, scale = 300, 50, 240 / 112
    b = []
    b.append(line(40, 300, 660, 300, stroke=LINE, sw=1.0))
    b.append(line(40, base_y - 94 * scale, 660, base_y - 94 * scale, stroke=LINE, sw=1.0, dash="4 3"))
    for name, n, x, fill, odd in bars:
        h = n * scale
        if odd:
            b.append(rect(x, base_y - h, bw, h, fill=PAPER, stroke=LINE, dash="4 3"))
        else:
            b.append(rect(x, base_y - h, bw, h, fill=fill))
        b.append(txt(x + bw / 2, 318, name, size=11, fill=INK, weight=600, anchor="middle"))

    b.append(txt(654, 88, "底板的高度", size=11, fill=TEAL, anchor="end"))
    b.append(txt(390, 338, "各编制自己的薄清单", size=11, fill=GRAY, anchor="middle"))

    b.extend(banner(40, 356, 620, "共享底板比最重的那份编制还薄：会不一样的行，都被推到各编制自己的纸上。"))
    b.append(note(40, 398, "条高只表厚薄，不标数字 · 虚线框那份不踩底板，自己从头到尾写全"))
    return write(
        out_dir, "fig-10-3-base-vs-modes.svg", 412,
        "图 27：共享核心比最重的模式层还薄",
        "分组柱状对比 base 94 条与各模式层条目数：web-app 112、sdk-minimal 32、sdk-app 7、headless 5、"
        "acp-app 5。base 用强调色标出，并有一条虚线标出 base 的高度。共享核心比最重的模式层还薄。",
        b,
    )


# ---------------------------------------------------------------- 图 34
FIGURES = [
    ("9-1", fig_9_1),
    ("9-3", fig_9_3),
    ("10-3", fig_10_3),
]
