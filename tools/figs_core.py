#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝宝书 §04–§08 图（服务与 ctx、inject、分发模式、可逆副作用、waterfall）。

配合 tools/build_figures.py 使用：
    python tools/build_figures.py --only 4-1 4-2 4-3 5-1 5-2 5-3 6-1 6-2 6-3 7-1 7-2 7-3 8-1 8-2 8-3
"""
from __future__ import annotations

from svgkit import (  # noqa: F401
    INK, GRAY, BLUE, CREAM, TEAL, LINE, HAIR, PAPER,
    B1, B2, B3, B4, ONB, T1,
    rect, txt, vtxt, path, line, circle, diamond, note, tag, banner, write,
    W,
)


# ---------------------------------------------------------------- 图 13
def fig_4_1(out_dir):
    b = []
    # 左右两个插件框，中间是 ctx 的 key 框
    b.append(rect(40, 70, 172, 64, fill=B1, stroke=LINE, rx=8))
    b.append(txt(126, 92, "消费方插件", size=12.5, fill=INK, weight=600, anchor="middle"))
    b.append(txt(126, 112, "只写字符串 tools", size=11, fill=GRAY, anchor="middle"))

    b.append(rect(254, 60, 172, 84, fill=BLUE, rx=8))
    b.append(txt(340, 88, "ctx.tools", size=14, fill="#FFFFFF", weight=600, anchor="middle", mono=True))
    b.append(txt(340, 110, "一个固定的 key", size=11, fill=ONB, anchor="middle"))

    b.append(rect(468, 70, 172, 64, fill=B1, stroke=LINE, rx=8))
    b.append(txt(554, 92, "提供方插件", size=12.5, fill=INK, weight=600, anchor="middle"))
    b.append(txt(554, 112, "供 tools", size=11, fill=GRAY, anchor="middle"))

    # 两条边都被中间截断
    b.append(path("M216,102 H250", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(path("M468,102 H432", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(txt(233, 84, "查 key", size=11, fill=GRAY, anchor="middle"))
    b.append(txt(451, 84, "供 key", size=11, fill=GRAY, anchor="middle"))
    b.append(txt(340, 158, "两条边都被中间截断；两边之间没有连线", size=11, fill=GRAY, anchor="middle"))

    # 对比：import 的写法，两个包直连
    b.append(rect(40, 178, 608, 76, fill=PAPER, stroke=HAIR, rx=8))
    b.append(txt(56, 200, "对比 import 的写法", size=11.5, fill=TEAL, weight=600))
    b.append(txt(56, 226, "两个包直连，换一个要动另一个", size=11, fill=GRAY))
    b.append(rect(300, 190, 96, 40, fill=B3, rx=6))
    b.append(txt(348, 210, "包 A", size=11.5, fill=INK, weight=600, anchor="middle"))
    b.append(path("M400,210 H440", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(txt(420, 198, "直连", size=11, fill=GRAY, anchor="middle"))
    b.append(rect(444, 190, 96, 40, fill=B3, rx=6))
    b.append(txt(492, 210, "包 B", size=11.5, fill=INK, weight=600, anchor="middle"))

    b.extend(banner(40, 268, 608, "消费方查 key，提供方供 key；两边互不认识，换提供方不动消费方。"))
    b.append(note(40, 316, "两条边都止于中间的 key 框，两边之间没有直连的边 · 对比 import 的写法"))
    return write(
        out_dir, "fig-4-1-key-lookup.svg", 330,
        "图 15：消费方查 key，提供方供 key",
        "左边是消费方插件，右边是提供方插件，中间是 ctx.tools 这个固定的 key。两边各一条箭头指向中间，"
        "左标查 key、右标供 key，两条边都被中间截断，两边之间没有连线。下方画出 import 的写法作对比："
        "两个包直接相连，换一个要动另一个。",
        b,
    )


# ---------------------------------------------------------------- 图 14
def fig_4_2(out_dir):
    b = []
    b.append(txt(40, 30, "① 一个消费方，两个可换的实现", size=11.5, fill=GRAY))
    b.append(rect(230, 52, 220, 54, fill=BLUE, rx=8))
    b.append(txt(340, 74, "消费方", size=12.5, fill="#FFFFFF", weight=600, anchor="middle"))
    b.append(txt(340, 94, "只报一个名字，不认实现", size=11, fill=ONB, anchor="middle"))

    b.append(rect(96, 150, 200, 50, fill=B1, stroke=HAIR, rx=8))
    b.append(txt(196, 168, "原来的实现", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(txt(196, 186, "眼下挂着的那一个", size=11, fill=GRAY, anchor="middle"))
    b.append(rect(384, 150, 200, 50, fill=B1, stroke=HAIR, rx=8))
    b.append(txt(484, 168, "顶替上来的实现", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(txt(484, 186, "挂上它即完成替换", size=11, fill=GRAY, anchor="middle"))

    b.append(path("M340,106 C340,128 196,128 196,146", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(path("M340,106 C340,128 484,128 484,146", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(txt(341, 172, "可互换", size=11, fill=TEAL, anchor="middle"))
    b.append(path("M300,164 H322", stroke=TEAL, sw=1.3, marker="art"))
    b.append(path("M382,180 H360", stroke=TEAL, sw=1.3, marker="art"))

    b.append(line(40, 222, 648, 222, stroke=HAIR, sw=1.0))
    b.append(txt(40, 244, "② 换更大的件，改的还是这一格", size=11.5, fill=GRAY))
    b.append(rect(40, 258, 236, 64, fill=B1, stroke=LINE, rx=8))
    b.append(txt(158, 282, "装配清单", size=12.5, fill=INK, weight=600, anchor="middle"))
    b.append(txt(158, 304, "列清单，不实现循环", size=11, fill=GRAY, anchor="middle"))
    b.append(path("M280,290 H356", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(txt(318, 276, "改动落在这格", size=11, fill=TEAL, anchor="middle"))
    b.append(rect(360, 258, 208, 64, fill=TEAL, rx=8))
    b.append(txt(464, 282, "循环本体", size=13, fill="#FFFFFF", weight=600, anchor="middle"))
    b.append(txt(464, 304, "可替换", size=11, fill="#FFFFFF", anchor="middle"))

    b.extend(banner(40, 340, 608, "换后端与换循环，改动都落在装配清单那一格。"))
    b.append(note(40, 388, "消费方从头到尾没动过：它做的事，一直只是报出一个名字"))
    return write(
        out_dir, "fig-4-2-swap-backend.svg", 402,
        "图 16：换掉循环，只有装配清单要动",
        "上半是一个消费方，注入 shell，下面并排两个可互换的后端；换后端只改装配清单那一行。"
        "下半是装配清单指向 agent-loop，316 个包的依赖图里只有 3 条边指向 agent-loop，两条来自装配包。"
        "换后端与换循环，改动都落在装配清单这一格。",
        b,
    )


# ---------------------------------------------------------------- 图 15
def fig_5_1(out_dir):
    left = ["甲", "乙", "丙", "丁"]
    right = ["丙", "丁", "甲", "乙"]
    b = []
    b.append(txt(56, 24, "书写的次序", size=11, fill=GRAY))
    b.append(txt(416, 24, "推导的次序", size=11, fill=GRAY))
    b.append(txt(340, 44, "由「谁需要谁」推出 →", size=11, fill=TEAL, anchor="middle"))

    y0, step, rh = 60, 52, 42
    pairs = []
    for i in range(4):
        ly = y0 + i * step
        ry = y0 + right.index(left[i]) * step
        pairs.append((ly, ry))
        b.append(rect(40, ly, 240, rh, fill=B1, stroke=HAIR, rx=6))
        b.append(txt(56, ly + 21, str(i + 1), size=11, fill=GRAY, mono=True))
        b.append(txt(80, ly + 21, left[i], size=12, fill=INK, weight=600))
        b.append(rect(400, ry, 240, rh, fill=PAPER, stroke=HAIR, rx=6))
        b.append(txt(416, ry + 21, str(right.index(left[i]) + 1), size=11, fill=GRAY, mono=True))
        b.append(txt(440, ry + 21, left[i], size=12, fill=INK, weight=600))
    for ly, ry in pairs:
        b.append(path(f"M280,{ly + 21} H396", stroke=LINE, sw=1.0, dash="3 3"))
        b.append(path(f"M280,{ly + 21} C330,{ly + 21} 350,{ry + 21} 396,{ry + 21}",
                      stroke=LINE, sw=1.0, dash="3 3"))

    b.append(txt(56, 276, "序号对不上：写在前面的不一定先办。", size=11, fill=GRAY))
    b.append(txt(400, 276, "被依靠的排前，依靠人的排后。", size=11, fill=TEAL))

    b.extend(banner(40, 296, 608, "写下来的顺序不算数，声明才算数：次序由「谁需要谁」推出来。"))
    b.append(note(40, 344, "被需要的那一方必须先就绪；对调清单上两行，结果不变 · 据 官方服务教程"))
    return write(
        out_dir, "fig-5-1-inject-derived-order.svg", 358,
        "图 17：顺序由声明推出来",
        "左边一列是配置文件里的书写顺序，右边一列是实际加载顺序，两列序号对不上。右边那列由 inject 的边"
        "推出来，提供方排在消费方前面。核心反差：写文件的顺序不算数，声明才算数。",
        b,
    )


# ---------------------------------------------------------------- 图 17
def fig_5_3(out_dir):
    b = []
    # 上图：安装关系，边连向一件设备
    b.append(rect(40, 20, 608, 128, fill=PAPER, stroke=HAIR, rx=8))
    b.append(txt(58, 42, "安装关系", size=11.5, fill=TEAL, weight=600))
    b.append(rect(70, 70, 150, 46, fill=B1, stroke=HAIR, rx=8))
    b.append(txt(145, 93, "甲部门", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(path("M224,93 H326", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(txt(275, 79, "装机时要带上它", size=11, fill=GRAY, anchor="middle"))
    b.append(rect(330, 70, 180, 46, fill=B2, rx=8))
    b.append(txt(420, 93, "乙部门", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(txt(58, 134, "边连向一件设备：管安装期，答「装不装得上」。", size=11, fill=GRAY))

    # 下图：事件往来，边连向一个名号
    b.append(rect(40, 164, 608, 148, fill=PAPER, stroke=HAIR, rx=8))
    b.append(txt(58, 186, "事件往来", size=11.5, fill=BLUE, weight=600))
    b.append(rect(70, 214, 150, 46, fill=B1, stroke=HAIR, rx=8))
    b.append(txt(145, 237, "甲部门", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(path("M224,237 H296", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(txt(260, 223, "点名叫它", size=11, fill=GRAY, anchor="middle"))
    b.append(rect(300, 214, 170, 46, fill=BLUE, rx=8))
    b.append(txt(385, 237, "「办事」这个名号", size=12, fill="#FFFFFF", weight=600, anchor="middle"))
    b.append(rect(500, 208, 138, 58, fill="#FFFFFF", stroke=LINE, rx=6, dash="5 4"))
    b.append(txt(569, 230, "名册上划掉了", size=11, fill=GRAY, anchor="middle"))
    b.append(txt(569, 250, "岗上没人", size=11, fill=GRAY, anchor="middle"))
    b.append(txt(58, 286, "边连向一个名号：管开张之后，答「点名时人在不在」。", size=11, fill=GRAY))

    b.extend(banner(40, 328, 608, "两张图看着像一张，其实不重叠：边连的东西不同，还能分叉 —— 设备装上了，岗上可以没人。"))
    b.append(note(40, 376, "安装关系答「装不装得上」，事件往来答「人在不在」；设备在、岗上可缺席（名册上划掉）"))
    return write(
        out_dir, "fig-5-3-two-graphs.svg", 390,
        "图 18：同一批包上的两张图",
        "同一批包上叠两张图。上面是 package.json 的模块图，边连向一个包；下面是 inject 的服务图，边连向"
        "一个字符串 key。下图里那个 key 旁还挂着一个虚线框 disabled: true，说明包在、服务可以不在。"
        "核心反差：两张图看着像一张，其实不是。",
        b,
    )


# ---------------------------------------------------------------- 图 19
def fig_6_1(out_dir):
    b = []
    # 左：三个纵向开关
    b.append(rect(40, 36, 240, 196, fill=PAPER, stroke=HAIR, rx=8))
    b.append(txt(56, 58, "三个开关", size=11.5, fill=INK, weight=600))
    switches = [("等待", "等 / 不等"), ("顺序", "按序 / 并发"), ("返回值", "收 / 不收")]
    for i, (name, vals) in enumerate(switches):
        y = 100 + i * 52
        b.append(txt(56, y, name, size=12, fill=INK, weight=600))
        b.append(rect(120, y - 11, 66, 22, fill=HAIR, rx=11))
        b.append(circle(134, y, 9, fill="#FFFFFF", stroke=LINE))
        b.append(txt(200, y, vals, size=11, fill=GRAY))

    # 右：五种模式的开关组合
    b.append(rect(300, 36, 348, 224, fill=PAPER, stroke=HAIR, rx=8))
    b.append(txt(312, 62, "模式", size=11, fill=GRAY))
    for j, lab in enumerate(["等待", "顺序", "返回值"]):
        b.append(txt(468 + j * 60, 62, lab, size=11, fill=GRAY, anchor="middle"))
    b.append(line(312, 78, 636, 78, stroke=HAIR, sw=1.0))

    combos = [
        ("emit", (0, 0, 0)),
        ("waterfall", (0, 0, 1)),
        ("parallel", (1, 0, 0)),
        ("serial", (1, 1, 1)),
        ("bail", (0, 1, 1)),
    ]
    for i, (name, sw) in enumerate(combos):
        y = 104 + i * 30
        b.append(txt(312, y, name, size=12, fill=INK, weight=600, mono=True))
        for j, on in enumerate(sw):
            cx = 468 + j * 60
            if on:
                b.append(circle(cx, y, 6, fill=TEAL))
            else:
                b.append(circle(cx, y, 6, fill="none", stroke=LINE, sw=1.4))
        if i == 0:
            b.append(txt(636, y, "全关", size=11, fill=TEAL, anchor="end"))
        if i == 3:
            b.append(txt(636, y, "全开", size=11, fill=TEAL, anchor="end"))

    b.extend(banner(40, 274, 608, "名字有五个，开关只有三组：emit 全关，serial 全开。"))
    b.append(note(40, 322, "对照官方五模式表；emit 59 个、waterfall 17、parallel 3、serial 2、bail 0"))
    return write(
        out_dir, "fig-6-1-three-switches.svg", 336,
        "图 19：五种模式只差三个开关",
        "左边三个纵向开关：等待、顺序、返回值。右边五行模式列出各自的开关组合：emit 三点全空、serial 三点全实心。"
        "核心反差：名字有五个，开关只有三组。",
        b,
    )


# ---------------------------------------------------------------- 图 20
def fig_7_1(out_dir):
    b = []
    b.append(txt(160, 40, "装上时 · 登记", size=12, fill=TEAL, weight=600, anchor="middle"))
    b.append(txt(520, 40, "拆下时 · 撤销", size=12, fill=GRAY, weight=600, anchor="middle"))
    b.append(rect(300, 60, 80, 236, fill=BLUE, rx=8))
    b.append(vtxt(340, 178, "同一份手续", size=11.5, fill="#FFFFFF"))

    rows = [
        ("挂一个听差", "留意公告栏的新消息", "把听差撤下"),
        ("登记一件工具", "名字写上排班表", "把名字从排班表划掉"),
        ("装一个下手", "子插件跟着主家走", "随主家一起拆下"),
        ("雇一个临时工", "定时、长连线、盯梢", "说好的解雇动作执行"),
    ]
    y0, step = 72, 56
    for i, (act, sub, rel) in enumerate(rows):
        y = y0 + i * step
        b.append(rect(40, y, 240, 44, fill=B1, stroke=HAIR, rx=6))
        b.append(txt(54, y + 15, act, size=11.5, fill=INK, weight=600))
        b.append(txt(54, y + 31, sub, size=11, fill=GRAY))
        b.append(rect(400, y, 240, 44, fill=PAPER, stroke=HAIR, rx=6))
        b.append(txt(414, y + 15, rel, size=11.5, fill=INK, weight=600))
        b.append(txt(414, y + 31, "撤销动作", size=11, fill=GRAY))
        b.append(path(f"M280,{y + 22} H296", stroke=LINE, sw=1.2, dash="4 3"))
        b.append(path(f"M384,{y + 22} H400", stroke=LINE, sw=1.2, dash="4 3"))

    b.extend(banner(40, 302, 608, "登记和撤销不是两份工作，是同一份手续的两个时刻。"),)
    b.append(note(40, 350, "手续的正文在装上时执行，撤销动作留到拆下时执行 · 据 官方生命周期教程"))
    return write(
        out_dir, "fig-7-1-load-unload-symmetry.svg", 364,
        "图 20：加载期和卸载期共用一份代码",
        "左栏是加载期，写注册动作；右栏是卸载期，写释放动作；中间一条 effect 竖条连接两栏，左右用虚线"
        "一一配对。核心反差：注册和撤销不是两份工作，是同一份 effect 的两个时刻。",
        b,
    )


# ---------------------------------------------------------------- 图 23
def fig_7_2(out_dir):
    b = []
    # 上：拆干净
    b.append(txt(56, 42, "① 拆干净：旧登记已撤销", size=12, fill=TEAL, weight=600))
    b.append(rect(40, 78, 100, 44, fill=B2, rx=8))
    b.append(txt(90, 100, "公告", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(path("M144,100 H430", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(txt(287, 84, "消息送达", size=11, fill=GRAY, anchor="middle"))
    b.append(rect(434, 78, 206, 44, fill=B1, stroke=LINE, rx=8))
    b.append(txt(537, 100, "新班子 · 唯一在岗", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(rect(190, 136, 220, 40, fill="#FFFFFF", stroke=LINE, rx=6, dash="4 3"))
    b.append(txt(300, 156, "旧登记 · 已撤销", size=11, fill=GRAY, anchor="middle"))
    b.append(line(196, 144, 404, 168, stroke=LINE, sw=1.2))

    b.append(line(40, 196, 648, 196, stroke=HAIR, sw=1.0))

    # 下：拆一半留一半
    b.append(txt(56, 218, "② 拆一半留一半：旧登记还挂着", size=12, fill=GRAY, weight=600))
    b.append(rect(40, 250, 100, 48, fill=B2, rx=8))
    b.append(txt(90, 274, "公告", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(rect(196, 246, 200, 48, fill="#FFFFFF", stroke=LINE, rx=8, dash="4 3"))
    b.append(txt(296, 266, "旧登记（幽灵）", size=11.5, fill=GRAY, weight=600, anchor="middle"))
    b.append(txt(296, 284, "还挂在公告栏上", size=11, fill=GRAY, anchor="middle"))
    b.append(rect(420, 246, 220, 48, fill=B1, stroke=LINE, rx=8))
    b.append(txt(530, 270, "新班子", size=11.5, fill=INK, weight=600, anchor="middle"))
    b.append(path("M144,274 C168,274 176,268 192,268", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(path("M144,274 C240,274 330,268 416,268", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(txt(340, 316, "同一条消息被办了两回", size=11, fill=TEAL, anchor="middle"))

    b.extend(banner(40, 334, 608, "拆一半留一半，就是幽灵状态：少一步撤销，系统里就多一个还会应答的旧人手。"),)
    b.append(note(40, 382, "热替换先拆下再装上；漏撤的旧听差留在公告栏上 · 官方组合与热替换教程"))
    return write(
        out_dir, "fig-7-2-ghost-state.svg", 396,
        "图 21：漏掉 disposer，旧注册会在新实例旁边继续应答",
        "两个对比面板。上面是正确撤销：旧注册框只剩一个虚线空位，标着已释放，事件只送达到唯一的新实例。"
        "下面是漏写：旧注册虚线框留在原处，与新实例如并排，事件箭头同时打到两个框，同一事件被处理两次。",
        b,
    )


# ---------------------------------------------------------------- 图 24
def fig_7_3(out_dir):
    states = [
        ("PENDING", B1, INK, None),
        ("LOADING", B2, INK, None),
        ("ACTIVE", BLUE, "#FFFFFF", None),
        ("UNLOADING", B2, INK, TEAL),
        ("DISPOSED", B3, INK, None),
    ]
    b = []
    w, gap, x0, y, h = 100, 28, 34, 90, 44
    for i, (name, fill, fg, stroke) in enumerate(states):
        x = x0 + i * (w + gap)
        b.append(rect(x, y, w, h, fill=fill, stroke=stroke, rx=8, sw=1.6 if stroke else 1.0))
        b.append(txt(x + w / 2, y + h / 2, name, size=11.5, fill=fg, weight=600, anchor="middle", mono=True))
    for i in range(4):
        sx = x0 + i * (w + gap) + w
        ex = x0 + (i + 1) * (w + gap) - 4
        b.append(path(f"M{sx},112 H{ex}", stroke=GRAY, sw=1.4, marker="ar"))

    # FAILED 支线
    b.append(path("M340,134 V186", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(txt(352, 160, "出错", size=11, fill=GRAY))
    b.append(rect(290, 190, 100, 44, fill="#FFFFFF", stroke=LINE, rx=6, dash="4 3"))
    b.append(txt(340, 212, "FAILED", size=11.5, fill=GRAY, weight=600, anchor="middle", mono=True))
    b.append(txt(468, 158, "等所有 disposer 结算", size=11, fill=TEAL, anchor="middle"))

    # 不能直达：ACTIVE 直接跳到 DISPOSED
    b.append(path("M390,96 C440,48 540,50 590,90", stroke=LINE, sw=1.2, dash="5 4"))
    b.append(line(484, 52, 496, 64, stroke=GRAY, sw=1.3))
    b.append(line(496, 52, 484, 64, stroke=GRAY, sw=1.3))
    b.append(txt(490, 34, "不能直达", size=11, fill=GRAY, anchor="middle"))

    b.extend(banner(40, 252, 608, "DISPOSED 只能经由 UNLOADING 到达 —— 卸载是有终点的过程，不是瞬时动作。"),)
    b.append(note(40, 300, "fiber 状态机 PENDING → … → DISPOSED，另一路 FAILED · 据 官方生命周期教程"))
    return write(
        out_dir, "fig-7-3-fiber-states.svg", 314,
        "图 22：fiber 走完卸载才到 DISPOSED",
        "一条状态链 PENDING → LOADING → ACTIVE → UNLOADING → DISPOSED，ACTIVE 下方接一条 FAILED 支线。"
        "上方还有一条从 ACTIVE 直通 DISPOSED 的虚线，打叉表示不能直达。核心反差：DISPOSED 只能经由 "
        "UNLOADING 到达，卸载是有终点的过程。",
        b,
    )


# ---------------------------------------------------------------- 图 25
def fig_8_2(out_dir):
    b = []
    # 上：委托
    b.append(txt(40, 34, "① 委托：调 next()，请求穿到底，结果再回上来", size=11.5, fill=TEAL, weight=600))
    b.append(rect(40, 52, 140, 48, fill=B1, stroke=HAIR, rx=8))
    b.append(txt(110, 76, "监听器 A", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(path("M180,76 H256", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(txt(218, 62, "next()", size=11, fill=GRAY, anchor="middle", mono=True))
    b.append(rect(260, 52, 140, 48, fill=B1, stroke=HAIR, rx=8))
    b.append(txt(330, 76, "下游监听器", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(path("M400,76 H476", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(txt(438, 62, "next()", size=11, fill=GRAY, anchor="middle", mono=True))
    b.append(rect(480, 52, 150, 48, fill=BLUE, rx=8))
    b.append(txt(555, 76, "内置行为", size=12, fill="#FFFFFF", weight=600, anchor="middle"))
    b.append(path("M480,104 C420,140 170,140 110,104", stroke=TEAL, sw=1.4, marker="art"))
    b.append(txt(300, 150, "返回值一层层往外穿", size=11, fill=TEAL, anchor="middle"))

    b.append(line(40, 172, 648, 172, stroke=HAIR, sw=1.0))

    # 下：短路
    b.append(txt(40, 194, "② 短路：不调 next()，直接 return", size=11.5, fill=GRAY, weight=600))
    b.append(rect(40, 212, 140, 48, fill=B1, stroke=HAIR, rx=8))
    b.append(txt(110, 228, "监听器 A", size=11.5, fill=INK, weight=600, anchor="middle"))
    b.append(txt(110, 245, "直接 return", size=11, fill=GRAY, anchor="middle"))
    b.append(rect(260, 212, 140, 48, fill="#FFFFFF", stroke=LINE, rx=8, dash="4 3"))
    b.append(txt(330, 236, "下游监听器", size=11.5, fill=GRAY, weight=600, anchor="middle"))
    b.append(rect(480, 212, 150, 48, fill=HAIR, rx=8))
    b.append(txt(555, 236, "内置行为", size=12, fill=GRAY, weight=600, anchor="middle"))
    b.append(line(180, 236, 256, 236, stroke=LINE, sw=1.2, dash="4 3"))
    b.append(line(400, 236, 476, 236, stroke=LINE, sw=1.2, dash="4 3"))
    for cx in (218, 438):
        b.append(line(cx - 6, 230, cx + 6, 242, stroke=GRAY, sw=1.3))
        b.append(line(cx + 6, 230, cx - 6, 242, stroke=GRAY, sw=1.3))
    b.append(line(262, 270, 626, 270, stroke=LINE, sw=1.2, dash="4 3"))
    b.append(line(262, 264, 262, 270, stroke=LINE, sw=1.2))
    b.append(line(626, 264, 626, 270, stroke=LINE, sw=1.2))
    b.append(txt(444, 286, "被跳过（短路）", size=11, fill=GRAY, anchor="middle"))

    b.extend(banner(40, 306, 608, "调不调 next() 决定后面一大截代码跑不跑。"),)
    b.append(note(40, 354, "不调 next() 直接返回即短路；下游监听器与内置行为一起被跳过 · 简化自 官方事件教程"))
    return write(
        out_dir, "fig-8-2-delegate-or-veto.svg", 368,
        "图 23：委托与短路是两条路",
        "两条分叉路径。上路径是委托：监听器经 next() 走到内置行为，返回值再一层层往外穿。下路径是短路："
        "监听器直接 return，右侧内置行为框变灰，下游监听器框变虚并被一段虚线括起来标记为被跳过。"
        "核心反差：调不调 next() 决定后面一大截代码跑不跑。",
        b,
    )


# ---------------------------------------------------------------- 图 27
def fig_8_3(out_dir):
    b = []
    b.append(diamond(340, 56, 260, 72, fill=CREAM, stroke=BLUE))
    b.append(txt(340, 56, "有没有决策权？", size=12.5, fill=INK, weight=600, anchor="middle"))

    b.append(rect(60, 160, 200, 54, fill=B1, stroke=HAIR, rx=8))
    b.append(txt(160, 180, "可以不调 next", size=12.5, fill=INK, weight=600, anchor="middle"))
    b.append(txt(160, 200, "（有决策）", size=11, fill=GRAY, anchor="middle"))
    b.append(path("M212,58 C195,90 165,120 160,156", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(txt(172, 104, "有", size=11, fill=GRAY, anchor="middle"))

    b.append(rect(300, 160, 160, 54, fill=B2, rx=8))
    b.append(txt(380, 180, "必须调 next", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(txt(380, 200, "（策略型）", size=11, fill=INK, anchor="middle"))
    b.append(rect(480, 160, 160, 54, fill=B2, rx=8))
    b.append(txt(560, 180, "必须调 next", size=12, fill=INK, weight=600, anchor="middle"))
    b.append(txt(560, 200, "（标注型）", size=11, fill=INK, anchor="middle"))
    b.append(path("M340,92 C340,110 380,110 380,156", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(path("M340,92 C340,110 470,112 560,156", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(txt(352, 110, "没有", size=11, fill=GRAY))

    b.extend(banner(40, 240, 608, "短路不是随意返回，而是一种有归属的权力：有决策可以停链，做标注的必须往下传。"),)
    b.append(note(40, 302, "只负责观察或标注的监听器必须调 next()；不调即有意短路 · 据 官方 Cordis 入门的 waterfall 语义一节"))
    return write(
        out_dir, "fig-8-3-decision-owner.svg", 316,
        "图 24：有决策的停链，做标注的必须往下传",
        "三分支判定。顶部一个菱形问有没有决策权。答有通向可以不调 next；答没有通向两条并列的必须调 next，"
        "分别标注策略型与标注型。核心反差：短路不是随意返回，而是一种有归属的权力。",
        b,
    )


FIGURES = [
    ("4-1", fig_4_1),
    ("4-2", fig_4_2),
    ("5-1", fig_5_1),
    ("5-3", fig_5_3),
    ("6-1", fig_6_1),
    ("7-1", fig_7_1),
    ("7-2", fig_7_2),
    ("7-3", fig_7_3),
    ("8-2", fig_8_2),
    ("8-3", fig_8_3),
]