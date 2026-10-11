#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝宝书 §18–§20 图（范式与迁移部分）。

配合 tools/build_figures.py 使用：
    python tools/build_figures.py --only 18-1 18-2 18-3 19-1 19-2 19-3 20-1 20-2 20-3
"""
from __future__ import annotations

from svgkit import (  # noqa: F401
    INK, GRAY, BLUE, CREAM, TEAL, LINE, HAIR, PAPER,
    B1, B2, B3, B4, ONB, T1,
    rect, txt, vtxt, path, line, circle, diamond, note, tag, banner, write,
    W,
)


# ---------------------------------------------------------------- 图 55
def fig_18_1(out_dir):
    rows = [
        ("1", "能力按 key 分发", "消费方写的是 key，还是实现", "§04", BLUE),
        ("2", "依赖声明式", "删掉手写调用，顺序还对不对", "§05", BLUE),
        ("3", "副作用可撤销", "每个注册能不能追到 disposer", "§07", BLUE),
        ("4", "真源唯一", "删掉派生数据能不能重建", "§14", BLUE),
        ("5", "信号绑上下文", "信号的产生路径是不是生产路径", "§17", TEAL),
    ]
    b = []
    b.extend(banner(40, 12, 608, "总判据：删掉一个插件，系统回到装它之前的样子。", fill=B1))
    y0, step, rh = 62, 52, 44
    for i, (num, name, how, sec, fill) in enumerate(rows):
        y = y0 + i * step
        b.append(rect(40, y, 608, rh, fill=PAPER, stroke=HAIR))
        b.append(rect(52, y + 9, 26, 26, fill=fill, rx=13))
        b.append(txt(65, y + 22, num, size=12, fill="#FFFFFF", weight=600, anchor="middle", mono=True))
        b.append(txt(92, y + 22, name, size=12.5, fill=INK, weight=600))
        b.append(txt(300, y + 22, how, size=11, fill=GRAY))
        b.append(tag(576, y + 11, sec, fill=B1 if fill == BLUE else B3, fg=BLUE, w=64))
    b.append(note(40, 344, "五道检验为本书原创，抽自 §04 / §05 / §07 / §14 / §17 的结论 · 末一道管前四道可不可信"))
    return write(
        out_dir, "fig-18-1-five-checks.svg", 358,
        "图 46：五道检验各查一个侧面",
        "五道检验排成一列：能力按 key 分发、依赖声明式、副作用可撤销、真源唯一、信号绑上下文。"
        "每道右边标着它回扣的节号，第五道用青色标出。五道各查一段，没有两道查同一件事；"
        "末一道管的是前四道可不可信。",
        b,
    )


# ---------------------------------------------------------------- 图 56
def fig_18_2(out_dir):
    checks = [
        ("检验一", "能力按 key 分发", "过 0 道 · 单体加钩子"),
        ("检验二", "依赖声明式", "过 1 道 · 单体加钩子"),
        ("检验三", "副作用可撤销", "过 2 道 · 能力能换，顺序还要人排"),
        ("检验四", "真源唯一", "过 3 道 · 能干净地卸，状态不唯一"),
        ("检验五", "信号绑上下文", "过 4 道 · 状态能重建，信号不可信"),
    ]
    b = []
    y0, step, rh = 30, 60, 40
    for i, (no, name, stage) in enumerate(checks):
        y = y0 + i * step
        b.append(rect(40, y, 300, rh, fill=B1, stroke=HAIR))
        b.append(txt(58, y + 20, no + " · " + name, size=12, fill=INK, weight=600))
        b.append(path(f"M342,{y + 20} H368", stroke=GRAY, sw=1.2, marker="ar"))
        b.append(txt(355, y + 7, "不合规", size=10.5, fill=GRAY, anchor="middle"))
        b.append(rect(372, y, 276, rh, fill=PAPER, stroke=LINE, dash="4 3"))
        b.append(txt(390, y + 20, stage, size=11, fill=GRAY))
        if i < len(checks) - 1:
            b.append(path(f"M190,{y + rh} V{y + step - 2}", stroke=TEAL, sw=1.4, marker="art"))
            b.append(txt(198, y + rh + 10, "通过", size=10.5, fill=TEAL))
    ytail = y0 + 4 * step + rh
    b.append(path(f"M190,{ytail} V326", stroke=TEAL, sw=1.4, marker="art"))
    b.append(txt(198, ytail + 8, "通过", size=10.5, fill=TEAL))
    b.append(rect(40, 328, 300, 40, fill=TEAL, rx=8))
    b.append(txt(190, 348, "过 5 道 · 热插拔成立", size=12.5, fill="#FFFFFF", weight=600, anchor="middle"))
    b.append(txt(372, 348, "删掉一个插件，系统回到装它之前的样子", size=11, fill=TEAL))
    b.append(note(40, 396, "从顶上那道起逐道向下；前一道是后一道的地基，任何一道不过就卡在那一段 · 本书原创"))
    return write(
        out_dir, "fig-18-2-decision-tree.svg", 410,
        "图 47：五道检验的过关路径",
        "决策树从顶上「能力按 key 分发」开始，逐道向下。每道一个判断框，不合规就侧向停在一个阶段框，"
        "阶段框按已过道数标出所处阶段。五道全过，落在「过 5 道 · 热插拔成立」。"
        "前一道是后一道的地基，任何一道不过就卡在那一段。",
        b,
    )


# ---------------------------------------------------------------- 图 57
def fig_18_3(out_dir):
    rows = [
        ("过 5 道 · 热插拔成立", 5, BLUE, "#FFFFFF"),
        ("过 4 道 · 状态能重建，信号不可信", 4, B3, INK),
        ("过 3 道 · 能干净地卸，状态不唯一", 3, B2, INK),
        ("过 2 道 · 能力能换，顺序还要人排", 2, B1, INK),
        ("过 1 道 · 单体加钩子", 1, B1, INK),
    ]
    b = []
    x0, unit = 256, 72
    for k in range(1, 6):
        b.append(line(x0 + k * unit, 250, x0 + k * unit, 26, stroke=HAIR, sw=1.0, dash="3 3"))
    b.append(line(x0, 22, x0, 250, stroke=LINE, sw=1.0))
    b.append(line(x0, 250, 620, 250, stroke=LINE, sw=1.0, marker="ar"))
    for k in range(6):
        x = x0 + k * unit
        b.append(line(x, 250, x, 245, stroke=LINE, sw=1.0))
        b.append(txt(x, 264, str(k), size=10.5, fill=GRAY, anchor="middle", mono=True))
    b.append(txt(620, 236, "过关数（每格 1 道检验）", size=10.5, fill=GRAY, anchor="end"))
    y0, step, rh = 30, 44, 30
    for i, (label, n, fill, fg) in enumerate(rows):
        y = y0 + i * step
        b.append(txt(244, y + rh / 2, label, size=11.5, fill=INK, anchor="end"))
        b.append(rect(x0, y, n * unit, rh, fill=fill, stroke=None if fill == BLUE else HAIR, rx=4))
        b.append(txt(x0 + n * unit + 9, y + rh / 2, str(n), size=12, fill=BLUE if fill == BLUE else GRAY, weight=600, mono=True))
    b.extend(banner(40, 286, 608, "过满五道才叫热插拔；少一道，就少一层能力。"))
    b.append(note(40, 340, "五个阶段名与过关数取自 §18.7 的分层 · 五道检验为本书原创"))
    return write(
        out_dir, "fig-18-3-score-ladder.svg", 354,
        "图 48：过关数与插件化的阶段",
        "横轴是过关数 0 到 5，每格 1 道检验；纵轴是五个阶段名，条形长度等于已过的道数。"
        "过 1 道只是单体加钩子，过 4 道状态能重建但信号不可信，过满 5 道才是热插拔成立。"
        "少一道，就少一层能力。",
        b,
    )


# ---------------------------------------------------------------- 图 58
def fig_19_1(out_dir):
    b = []
    b.append(txt(40, 26, "空间可组合性 · 能声明并响应式管理依赖", size=11, fill=BLUE))
    b.append(txt(440, 26, "reactive coeffects / inject", size=10.5, fill=TEAL))
    b.append(line(340, 284, 340, 44, stroke=BLUE, sw=1.2, marker="arb"))
    b.append(line(56, 170, 620, 170, stroke=BLUE, sw=1.2, marker="arb"))
    b.append(circle(340, 170, 3, fill=GRAY))
    b.append(txt(616, 150, "revertible effects / ctx.effect()", size=10.5, fill=TEAL, anchor="end"))
    b.append(txt(616, 186, "时间可组合性 · 组件移除时能完全撤销副作用", size=11, fill=BLUE, anchor="end"))

    quads = [
        (84, 76, "依赖能声明，卸不干净", "顺序交给系统，注册没配撤销", PAPER),
        (356, 76, "Cordis：两维都落地", "可逆效应与响应式余效应同时成立", B1),
        (356, 194, "卸得干净，顺序写死", "启动脚本里一串手写 init 调用", PAPER),
        (84, 194, "两样都不成立", "单体加钩子：插件是外挂", PAPER),
    ]
    for x, y, title, sub, fill in quads:
        b.append(rect(x, y, 240, 60, fill=fill, stroke=HAIR))
        b.append(txt(x + 14, y + 22, title, size=11.5, fill=INK, weight=600))
        b.append(txt(x + 14, y + 42, sub, size=11, fill=GRAY))

    b.append(note(40, 306, "两根轴互不推导：修好一个不会顺手修好另一个 · 图据 本书对那篇论文的整理"))
    return write(
        out_dir, "fig-19-1-two-axes.svg", 320,
        "图 49：可组合性有两个正交维度",
        "一个二维坐标。横轴是时间可组合性，管装和卸，右端挂可逆效应 revertible effects，"
        "对应 ctx.effect()；纵轴是空间可组合性，管谁需要谁，上端挂响应式余效应 reactive coeffects，"
        "对应 inject。Cordis 落在右上象限；另外三个象限分别是卸得干净但顺序写死、依赖能声明但卸不干净、"
        "两样都不成立。两根轴互不推导。",
        b,
    )


# ---------------------------------------------------------------- 图 59
def fig_19_3(out_dir):
    rows = [
        ("ctx.effect() 返回 disposer", "revertible effect（时间可组合性）"),
        ("inject 声明依赖，就绪才启动", "reactive coeffect（空间可组合性）"),
        ("ctx.<key> 服务容器", "统一的 effect / coeffect context"),
        ("插件卸载时撤销注册", "时间可组合性的运行时兑现"),
        ("HMR 热模块替换", "时空可组合性的可观测后果"),
    ]
    b = []
    b.append(txt(40, 24, "Cordis 工程实践", size=11.5, fill=BLUE, weight=600))
    b.append(txt(352, 24, "论文的形式定义", size=11.5, fill=TEAL, weight=600))
    y0, step, rh = 44, 52, 46
    for i, (left, right) in enumerate(rows):
        y = y0 + i * step
        b.append(rect(40, y, 288, rh, fill=B1, stroke=HAIR))
        b.append(txt(58, y + rh / 2, left, size=11.5, fill=BLUE, weight=600 if i < 3 else 400))
        b.append(rect(352, y, 288, rh, fill=PAPER, stroke=LINE))
        b.append(txt(370, y + rh / 2, right, size=11.5, fill=TEAL))
        b.append(line(332, y + rh / 2, 348, y + rh / 2, stroke=GRAY, sw=1.2, marker="ar"))
        b.append(line(348, y + rh / 2, 332, y + rh / 2, stroke=GRAY, sw=1.2, marker="ar"))
    b.extend(banner(40, 312, 608, "左边是能跑的代码，右边是形式定义，说的是同一件事，不是比喻。"))
    b.append(note(40, 366, "论文 arXiv:2608.25512 · 92 页 · 2026-08-26 · cs.PL / cs.SE"))
    b.append(note(40, 386, "标题《A Programming Paradigm for Spatiotemporal Composability》"))
    b.append(note(40, 406, "本书未精读论文正文：映射为本书据二手整理所做，非论文原表呈现。"))
    return write(
        out_dir, "fig-19-3-mapping.svg", 420,
        "图 50：同一件事的两种写法",
        "一张五行对照表。左列是 Cordis 的工程实践，右列是论文的形式定义，每行一条双向箭头。"
        "ctx.effect() 返回 disposer 对应 revertible effect；inject 声明依赖、就绪才启动对应 reactive coeffect；"
        "ctx.<key> 服务容器对应统一的 effect / coeffect context；插件卸载时撤销注册是时间可组合性的运行时兑现；"
        "HMR 热模块替换是时空可组合性的可观测后果。左边是能跑的代码，右边是形式定义，不是比喻。",
        b,
    )


# ---------------------------------------------------------------- 图 61
def fig_20_1(out_dir):
    b = []
    b.append(rect(225, 26, 230, 52, fill=BLUE, rx=8))
    b.append(txt(243, 45, "① 服务容器", size=12.5, fill="#FFFFFF", weight=600))
    b.append(txt(243, 65, "能力按 key 分发 · §04", size=10.5, fill=ONB))

    branches = [
        (40, "② inject 声明", "系统推出加载顺序 · §05"),
        (245, "③ effect 与 disposer", "每个注册配一个撤销 · §07"),
        (450, "④ 单一真源", "只存事件，状态当投影 · §14"),
    ]
    for x, title, sub in branches:
        b.append(rect(x, 110, 190, 58, fill=B1, stroke=HAIR))
        b.append(txt(x + 14, 132, title, size=11.5, fill=INK, weight=600))
        b.append(txt(x + 14, 153, sub, size=10.5, fill=GRAY))

    b.append(path("M340,78 C340,94 135,90 135,104", stroke=BLUE, sw=1.3, marker="arb"))
    b.append(path("M340,78 V104", stroke=BLUE, sw=1.3, marker="arb"))
    b.append(path("M340,78 C340,94 545,90 545,104", stroke=BLUE, sw=1.3, marker="arb"))

    b.append(rect(40, 200, 190, 50, fill=PAPER, stroke=LINE))
    b.append(txt(54, 219, "三层叠加", size=11.5, fill=INK, weight=600))
    b.append(txt(54, 238, "按 id 整体替换 · §09", size=10.5, fill=GRAY))
    b.append(rect(245, 200, 190, 50, fill=PAPER, stroke=LINE))
    b.append(txt(259, 219, "热替换", size=11.5, fill=INK, weight=600))
    b.append(txt(259, 238, "卸掉旧注册后换实现", size=10.5, fill=GRAY))
    b.append(path("M135,168 V194", stroke=BLUE, sw=1.3, marker="arb"))
    b.append(path("M340,168 V194", stroke=BLUE, sw=1.3, marker="arb"))

    b.append(rect(40, 286, 608, 52, fill=B1, stroke=HAIR))
    b.append(txt(58, 306, "⑤ 让测试走生产那条装配路径 · §17", size=12, fill=INK, weight=600))
    b.append(txt(58, 328, "排在末尾不是因为最难，是因为它管前四步可不可信", size=11, fill=GRAY))
    b.append(path("M135,286 V256", stroke=GRAY, sw=1.2, dash="4 3", marker="ar"))
    b.append(path("M340,286 V256", stroke=GRAY, sw=1.2, dash="4 3", marker="ar"))
    b.append(path("M545,286 V172", stroke=GRAY, sw=1.2, dash="4 3", marker="ar"))
    b.append(txt(352, 276, "虚线 = 让前面各步可验", size=10.5, fill=GRAY))

    b.append(note(40, 366, "五步顺序由依赖推出，不能乱序；第二步与第三步可并行，但都建在第一步之上。"))
    b.append(note(40, 386, "本书原创 · 回扣 §04 / §05 / §07 / §09 / §14 / §17"))
    return write(
        out_dir, "fig-20-1-migration-order.svg", 400,
        "图 51：迁移步骤的依赖顺序",
        "起点是①服务容器，能力按 key 分发。它带出三条分支：②inject 声明、③effect 与 disposer、"
        "④单一真源。②之后才谈得上三层叠加与按 id 整体替换，③之后才谈得上热替换。"
        "末尾是⑤让测试走生产那条装配路径，用虚线指向前面各框。末尾那步不产出新能力，只让前面的成果可信。",
        b,
    )


# ---------------------------------------------------------------- 图 62
FIGURES = [
    ("18-1", fig_18_1),
    ("18-2", fig_18_2),
    ("18-3", fig_18_3),
    ("19-1", fig_19_1),
    ("19-3", fig_19_3),
    ("20-1", fig_20_1),
]
