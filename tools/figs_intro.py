#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 1 部「背景」配图（图 1 … 图 3）

这三张图回答的是全书之前的问题：harness 是什么、它站在哪、
以及它要对付的难处和它拿出的应对。
"""
from __future__ import annotations

from svgkit import (  # noqa: F401
    INK, GRAY, BLUE, CREAM, TEAL, LINE, HAIR, PAPER,
    B1, B2, B3, B4, ONB, T1,
    head, rect, txt, path, line, circle, diamond, note, tag, banner, write,
)


# ---------------------------------------------------------------- 图 1
def fig_0_1(out_dir):
    b = [txt(40, 24, "两种东西，名字只差一个词", size=11.5, fill=GRAY)]

    # 左：一次调用
    b.append(rect(40, 44, 250, 232, fill=PAPER, stroke=HAIR))
    b.append(txt(56, 68, "① 一次调用", size=12, fill=BLUE, weight=600))
    b.append(rect(56, 104, 80, 34, fill=B1))
    b.append(txt(96, 121, "一段文本", size=11, fill=INK, anchor="middle"))
    b.append(path("M140,121 H196", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(rect(200, 104, 74, 34, fill=B1))
    b.append(txt(237, 121, "一段文本", size=11, fill=INK, anchor="middle"))
    b.append(txt(56, 172, "一问一答，一步就完。", size=11.5, fill=GRAY))
    b.append(txt(56, 196, "字进去，字出来。", size=11.5, fill=GRAY))
    b.append(txt(56, 232, "文本之外的事，它不管。", size=11.5, fill=GRAY))

    # 右：一个能干活的 agent
    b.append(rect(310, 44, 330, 232, fill=PAPER, stroke=HAIR))
    b.append(txt(326, 68, "② 一个能干活的 agent", size=12, fill=BLUE, weight=600))

    cx, cy, rx, ry = 475, 182, 118, 70
    ring = [
        ("循环", 0, -1), ("工具", -1, -1), ("上下文", 1, -1),
        ("权限", -1, 1), ("状态", 1, 1), ("适配", 0, 1),
    ]
    bw, bh = 84, 26
    for name, dx, dy in ring:
        px, py = cx + dx * rx, cy + dy * ry
        b.append(rect(px - bw / 2, py - bh / 2, bw, bh, fill=B1, stroke=HAIR))
        b.append(txt(px, py, name, size=11, fill=INK, anchor="middle"))
        b.append(line(px, py, cx, cy, stroke=HAIR, sw=0.9))
    b.append(circle(cx, cy, 38, fill=BLUE))
    b.append(txt(cx, cy, "模型", size=12.5, fill="#FFFFFF", weight=600, anchor="middle"))

    b.extend(banner(40, 292, 600,
                    "模型只负责给主意。去动手、去记、去刹车的是外面那一圈。",
                    "差的那个词，就是这一圈。"))

    return write(
        out_dir, "fig-0-1-one-call-vs-agent.svg", 340,
        "图 1：一次调用和一个能干活的 agent，差的是外面那一圈",
        "左边是一次调用：一段文本进去，一段文本出来，中间没有任何别的环节。右边是一个能干活的 agent："
        "模型在中间，外面围着循环、工具、上下文、权限、状态、适配六件事，每一件都用细线连回模型。"
        "两边的差别不在模型本身，而在外面那一圈。",
        b,
    )


# ---------------------------------------------------------------- 图 2
def fig_0_2(out_dir):
    b = [txt(40, 24, "一句话要变成真实世界里的一个动作，中间必须有人接", size=11.5, fill=GRAY)]

    b.append(rect(190, 44, 300, 54, fill=B1))
    b.append(txt(340, 71, "模型：只会输出文本", size=12, fill=INK, weight=600, anchor="middle"))

    b.append(path("M340,98 V126", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(txt(352, 112, "它说的话", size=10.5, fill=GRAY))

    b.append(rect(120, 130, 440, 92, fill=CREAM, stroke=BLUE, sw=1.2))
    b.append(txt(140, 154, "Harness：把话变成动作，也把结果变回话", size=11.5, fill=BLUE, weight=600))
    chip_y, chip_h = 170, 32
    for i, label in enumerate(["变成动作", "拦住不该做的", "记住做过的"]):
        x = 140 + i * 138
        b.append(rect(x, chip_y, 126, chip_h, fill="#FFFFFF", stroke=HAIR))
        b.append(txt(x + 63, chip_y + chip_h / 2, label, size=11, fill=INK, anchor="middle"))

    b.append(path("M340,222 V250", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(txt(352, 236, "真的去动它", size=10.5, fill=GRAY))

    b.append(rect(190, 254, 300, 54, fill=PAPER, stroke=HAIR))
    b.append(txt(340, 281, "真实世界：文件、命令、网络、人", size=12, fill=INK, weight=600, anchor="middle"))

    b.append(path("M170,281 H96 V71 H188", stroke=TEAL, sw=1.4, marker="art"))
    b.append(txt(88, 176, "结", size=10.5, fill=TEAL, anchor="middle"))
    b.append(txt(88, 192, "果", size=10.5, fill=TEAL, anchor="middle"))

    b.extend(banner(40, 328, 600,
                    "模型碰不到真实世界。它只能说话，做事的是 harness。",
                    "所有风险也是从这儿来的：一道口令和一次删除之间，只隔着这一层。"))

    return write(
        out_dir, "fig-0-2-harness-in-between.svg", 376,
        "图 2：harness 站在模型和真实世界之间",
        "上框是模型，只会输出文本。中间是 harness，把文本变成动作、拦住不该做的、记住做过的。"
        "下框是真实世界：文件、命令、网络、人。向下的箭头是动作，左侧绕回来的青色箭头是结果。"
        "模型碰不到真实世界，中间这一层是唯一的通道，也是唯一能设卡的地方。",
        b,
    )


# ---------------------------------------------------------------- 图 3
def fig_0_3(out_dir):
    b = [txt(40, 24, "四个难处，四条应对", size=11.5, fill=GRAY)]
    b.append(txt(40, 52, "难在哪", size=11, fill=GRAY, weight=600))
    b.append(txt(380, 52, "设计的应对", size=11, fill=GRAY, weight=600))

    rows = [
        ("能力一直在变", "拼装和实现分开"),
        ("模型随时会换", "找能力靠名字，不靠位置"),
        ("环境不可信", "边界显式，挡不住就往拒绝倒"),
        ("任务又长又会断", "事实只留一份，其余都算得出"),
    ]
    y = 68
    for left, right in rows:
        cy = y + 23
        b.append(rect(40, y, 260, 46, fill=CREAM, stroke=HAIR))
        b.append(txt(58, cy, left, size=11.5, fill=INK))
        b.append(path(f"M306,{cy} H372", stroke=GRAY, sw=1.4, marker="ar"))
        b.append(rect(380, y, 260, 46, fill=B1, stroke=HAIR))
        b.append(txt(398, cy, right, size=11.5, fill=BLUE, weight=600))
        y += 62

    b.extend(banner(40, y + 8, 600,
                    "四条应对各干各的，方向是同一个：把会变的部分挪出主体。",
                    "下面五节讲的五条主张，都在做这件事。"))

    return write(
        out_dir, "fig-0-3-four-problems.svg", y + 78,
        "图 3：四个难处和它们各自引出的设计应对",
        "左栏是四个难处。能力一直在变，对应拼装和实现分开。模型随时会换，对应找能力靠名字而不靠位置。"
        "环境不可信，对应边界显式、挡不住就往拒绝倒。任务又长又会断，对应事实只留一份、其余都算得出。"
        "四条应对的两栏一一对齐。",
        b,
    )


# ---------------------------------------------------------------- 图 4
def fig_0_4(out_dir):
    b = [txt(40, 24, "设计的目标：左边怎么变，右边都不动", size=11.5, fill=GRAY)]

    b.append(rect(40, 44, 290, 262, fill=CREAM, stroke=HAIR))
    b.append(txt(58, 68, "一直在变的那一边", size=12, fill=INK, weight=600))
    left = ["模型换了一代", "工具多了几个", "权限策略收紧", "任务变得更长", "团队换了写法"]
    y = 88
    for s in left:
        b.append(rect(58, y, 254, 34, fill="#FFFFFF", stroke=HAIR))
        b.append(txt(74, y + 17, s, size=11, fill=INK))
        y += 42

    b.append(rect(350, 44, 290, 262, fill=B1, stroke=HAIR))
    b.append(txt(368, 68, "不该跟着动的那一边", size=12, fill=BLUE, weight=600))
    right = ["已经定下的业务规则", "留给人看的记录", "扩展的方式", "出问题时的追责线索", "别人接你的方法"]
    y = 88
    for s in right:
        b.append(rect(368, y, 254, 34, fill="#FFFFFF", stroke=HAIR))
        b.append(txt(384, y + 17, s, size=11, fill=INK))
        y += 42

    b.extend(banner(40, 322, 600,
                    "左边一定会变，拦不住。所以设计要做的不是让它不变。",
                    "是让它变的时候，右边不动。"))

    return write(
        out_dir, "fig-0-4-what-changes.svg", 372,
        "图 4：会变的一边和不该跟着动的一边",
        "左栏是必然会变的东西：模型换代、工具增减、权限收紧、任务变长、团队换写法。右栏是不该跟着动的："
        "定下的业务规则、留给人看的记录、扩展的方式、追责线索、别人接你的方法。两栏并列摆开，"
        "设计的目标不是让左栏不变，而是左栏变的时候右栏不动。",
        b,
    )


FIGURES = [
    ("0-1", fig_0_1),
    ("0-2", fig_0_2),
    ("0-3", fig_0_3),
    ("0-4", fig_0_4),
]
