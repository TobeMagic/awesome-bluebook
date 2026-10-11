#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
§07 预览用图（3 张）。目录定稿后并入 figs_core.py。

对外暴露：
    FIGURES = [("07-a", fig_07_a), ("07-b", fig_07_b), ("07-c", fig_07_c)]
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from svgkit import (B1, B2, B3, BLUE, CREAM, GRAY, HAIR, INK, LINE, ONB,
                    PAPER, T1, TEAL, banner, circle, head, line, note, path,
                    rect, tag, txt, write)

# ----------------------------------------------------------------------------
# 图 A：一句话进来，七件事出去
# ----------------------------------------------------------------------------

ROWS_A = [
    ("找到坏的那段线", "得有人动手查"),
    ("把它换掉", "得有人动手改"),
    ("通一下电看亮不亮", "得有人验结果"),
    ("记住刚试过什么", "得有人记笔记"),
    ("想拆开电表", "得有人拦住"),
    ("收工明天再来", "得有人接着上次的"),
    ("换个更便宜的师傅", "师傅得能换"),
]


def fig_07_a(out_dir: str) -> str:
    b = []
    b.append(rect(40, 16, 280, 36, fill=B1, stroke=B3, rx=18))
    b.append(txt(60, 34, "家里厨房的灯不亮了", size=12.5, fill=BLUE))

    for i, (act, need) in enumerate(ROWS_A):
        y = 76 + i * 44
        b.append(rect(40, y, 210, 32, fill=PAPER, stroke=HAIR, rx=6))
        b.append(txt(56, y + 16, act, size=12.5, fill=INK))
        b.append(line(254, y + 16, 274, y + 16, stroke=LINE, sw=1.0))
        b.append(txt(282, y + 16, need, size=12, fill=GRAY))

    b.extend(banner(40, 392, 600,
                    "师傅只会想。这七件事，都得队伍里另外有人补上。", h=32))
    return write(out_dir, "fig-07-a-seven-needs.svg", 448,
                 "一句话进来，七件事出去",
                 "师傅只会想，七件事都得队伍里另外有人干。",
                 b)


# ----------------------------------------------------------------------------
# 图 B（主图）：中心是空的
# ----------------------------------------------------------------------------


def fig_07_b(out_dir: str) -> str:
    b = []
    b.append(txt(40, 26, "多数系统", size=12.5, fill=GRAY))
    b.append(txt(350, 26, "这套系统", size=12.5, fill=TEAL))

    b.append(rect(40, 42, 290, 132, fill="#FCFCFA", stroke=HAIR, rx=10))
    b.append(rect(350, 42, 290, 132, fill="#FCFCFA", stroke=HAIR, rx=10))

    b.append(rect(125, 58, 120, 38, fill=BLUE, rx=8))
    b.append(txt(185, 77, "领班", size=13, fill="#FFFFFF", weight=600, anchor="middle"))

    kids_l = ["递工具的", "记笔记的", "把门的"]
    cx_l = [97, 185, 273]
    b.append(line(185, 96, 185, 116, stroke=B3, sw=1.4))
    b.append(line(97, 116, 273, 116, stroke=B3, sw=1.4))
    for cx, name in zip(cx_l, kids_l):
        b.append(line(cx, 116, cx, 130, stroke=B3, sw=1.4))
        b.append(rect(cx - 36, 130, 72, 30, fill=PAPER, stroke=LINE, rx=6))
        b.append(txt(cx, 145, name, size=11, fill=GRAY, anchor="middle"))

    b.append(rect(395, 58, 200, 38, fill=CREAM, stroke=B3, rx=8))
    b.append(txt(495, 77, "排班表", size=13, fill=BLUE, anchor="middle"))

    kids_r = ["领班", "递工具", "记笔记", "把门的"]
    cx_r = [390, 460, 530, 600]
    b.append(line(495, 96, 495, 116, stroke=B3, sw=1.4))
    b.append(line(390, 116, 600, 116, stroke=B3, sw=1.4))
    for cx, name in zip(cx_r, kids_r):
        b.append(line(cx, 116, cx, 130, stroke=B3, sw=1.4))
        b.append(rect(cx - 30, 130, 60, 30, fill=PAPER, stroke=LINE, rx=6))
        b.append(txt(cx, 145, name, size=11, fill=BLUE, anchor="middle"))

    b.append(line(340, 52, 340, 166, stroke=HAIR, sw=1.0, dash="4,4"))

    b.extend(banner(40, 194, 600,
                    "左边：领班是公司的一部分，想换，得连公司一起动。",
                    "右边：领班和帮手站在同一层，一张表决定今天谁上。", h=48))
    return write(out_dir, "fig-07-b-empty-center.svg", 262,
                 "中心是空的",
                 "左边把领班放在公司顶端，其余帮手依附于他；右边所有岗位并列，同一张排班表决定谁被请进来。",
                 b)


# ----------------------------------------------------------------------------
# 图 C：换掉它，要动几个地方
# ----------------------------------------------------------------------------


def fig_07_c(out_dir: str) -> str:
    b = []
    b.append(txt(40, 26, "直接点名", size=12.5, fill=GRAY))
    b.append(txt(350, 26, "隔一张排班表", size=12.5, fill=TEAL))

    b.append(rect(40, 42, 290, 196, fill="#FCFCFA", stroke=HAIR, rx=10))
    b.append(rect(350, 42, 290, 196, fill="#FCFCFA", stroke=HAIR, rx=10))

    lc = (185, 148)
    spots = [(76, 84), (185, 70), (294, 84), (76, 212), (185, 226), (294, 212)]
    for sx, sy in spots:
        b.append(line(sx, sy, lc[0], lc[1], stroke=B3, sw=1.2))
    b.append(rect(lc[0] - 50, lc[1] - 19, 100, 38, fill=BLUE, rx=8))
    b.append(txt(lc[0], lc[1], "小张", size=12.5, fill="#FFFFFF", anchor="middle"))
    for sx, sy in spots:
        b.append(rect(sx - 30, sy - 12, 60, 24, fill=PAPER, stroke=LINE, rx=5))

    tops = [404, 495, 586]
    for cx in tops:
        b.append(rect(cx - 36, 62, 72, 28, fill=PAPER, stroke=LINE, rx=5))
        b.append(txt(cx, 76, "找人的人", size=11, fill=GRAY, anchor="middle"))
        b.append(line(cx, 90, cx, 126, stroke=B3, sw=1.2, marker="arb"))

    b.append(rect(390, 126, 200, 34, fill=CREAM, stroke=B3, rx=8))
    b.append(txt(490, 143, "排班表", size=12.5, fill=BLUE, anchor="middle"))

    bots = [440, 540]
    for cx in bots:
        b.append(line(cx, 160, cx, 196, stroke=B3, sw=1.2, marker="arb"))
        b.append(rect(cx - 44, 196, 88, 28, fill=PAPER, stroke=LINE, rx=5))
        b.append(txt(cx, 210, "顶上的人", size=11, fill=GRAY, anchor="middle"))

    b.extend(banner(40, 256, 600,
                    "左边：小张一请假，六个人全得换着找。",
                    "右边：谁都只认表上那行字，换人就改那行。", h=48))
    return write(out_dir, "fig-07-c-swap-radius.svg", 324,
                 "换掉他，要动几个人",
                 "左图小张被六个人直接点名，他一请假六个人全得换着找；右图所有人都只认排班表，换人就改表上一行。",
                 b)


# ----------------------------------------------------------------------------
# 图 D（§02）：材料店、图纸铺、成品房
# ----------------------------------------------------------------------------


def fig_02_shops(out_dir: str) -> str:
    b = []
    cols = [
        (40, "材料店", "木料、砖头、水泥", "附一本说明书", "怎么盖随买主便", GRAY),
        (245, "图纸铺", "空架子立在那儿", "血肉自己填", "盖完，架子就拆", GRAY),
        (450, "成品房", "拎包入住", "但门禁早就装好", "不刷卡门都别想进", TEAL),
    ]
    for x, name, l1, l2, l3, c in cols:
        b.append(rect(x, 30, 190, 150, fill="#FCFCFA", stroke=HAIR, rx=10))
        b.append(rect(x + 35, 48, 120, 34, fill=(CREAM if c == TEAL else PAPER),
                      stroke=(B3 if c == TEAL else LINE), rx=8))
        b.append(txt(x + 95, 65, name, size=13.5, fill=(BLUE if c == TEAL else INK),
                     weight=600, anchor="middle"))
        b.append(txt(x + 95, 108, l1, size=11.5, fill=INK, anchor="middle"))
        b.append(txt(x + 95, 132, l2, size=11.5, fill=INK, anchor="middle"))
        b.append(txt(x + 95, 156, l3, size=11.5, fill=c, anchor="middle"))

    b.extend(banner(40, 202, 600,
                    "前两家把决定权交出来；第三家把自己的规矩变成住户的规矩。",
                    "「有主见」，是它和前两家最大的分别。", h=48))
    return write(out_dir, "fig-02-three-shops.svg", 270,
                 "材料店、图纸铺、成品房",
                 "三种帮人盖房的店：材料店给材料自己盖，图纸铺给空架子盖完就拆，成品房拎包入住但门禁必装。",
                 b)


# ----------------------------------------------------------------------------
# 图 E（§03）：三家外壳，三种卖法
# ----------------------------------------------------------------------------


def fig_03_vendors(out_dir: str) -> str:
    b = []
    cols = [
        (40, "卖成品房", "拎包入住，明天开工", "代价：格局改不了", GRAY),
        (245, "卖图纸", "管线的口标得清楚", "代价：自己得懂行", GRAY),
        (450, "卖插座", "空房一排标准插座", "连管家都是插上去的", TEAL),
    ]
    for x, name, l1, l2, c in cols:
        b.append(rect(x, 30, 190, 128, fill="#FCFCFA", stroke=HAIR, rx=10))
        b.append(rect(x + 35, 46, 120, 32, fill=(CREAM if c == TEAL else PAPER),
                      stroke=(B3 if c == TEAL else LINE), rx=8))
        b.append(txt(x + 95, 62, name, size=13, fill=(BLUE if c == TEAL else INK),
                     weight=600, anchor="middle"))
        b.append(txt(x + 95, 104, l1, size=11.5, fill=INK, anchor="middle"))
        b.append(txt(x + 95, 130, l2, size=11.5, fill=c, anchor="middle"))

    b.append(rect(40, 180, 600, 34, fill=B1, stroke=B3, rx=8))
    b.append(txt(340, 197, "必做活三家都做：水电得通、门得能锁、干了活得有地方记账。",
                 size=12, fill=BLUE, anchor="middle"))
    b.extend(banner(40, 230, 600,
                    "拉开差距的是选做活：房子留不留得动、师傅换不换得了、账本让不让拿回家。",
                    "不是谁好谁坏，是三种卖法。", h=48))
    return write(out_dir, "fig-03-three-vendors.svg", 298,
                 "三家外壳，三种卖法",
                 "三家外壳的必做活相同，拉开差距的是选做活：成品房不许改格局，图纸铺把接口标清楚，插座房连管家都可替换。",
                 b)


FIGURES = [("07-a", fig_07_a), ("07-b", fig_07_b), ("07-c", fig_07_c),
           ("02-shops", fig_02_shops), ("03-vendors", fig_03_vendors)]


def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else "books/deepseek-harness/figures"
    for key, fn in FIGURES:
        print(f"{key:5s} -> {fn(out)}")


if __name__ == "__main__":
    main()
