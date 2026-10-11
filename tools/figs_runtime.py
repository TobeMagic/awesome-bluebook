#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝宝书 §12–§14 图（运行时：轮次生命周期 / 工具流水线 / 仅追加日志）。

配合 tools/build_figures.py 使用：
    python tools/build_figures.py --only 12-1 12-3 13-1 13-2 13-3 14-1 14-2 14-3
"""
from __future__ import annotations

from svgkit import (  # noqa: F401
    INK, GRAY, BLUE, CREAM, TEAL, LINE, HAIR, PAPER,
    B1, B2, B3, B4, ONB, T1,
    rect, txt, vtxt, path, line, circle, diamond, note, tag, banner, write,
    W,
)


def _chip(x, y, w, s, fill=PAPER, stroke=HAIR, fg=INK, size=10.5, h=24):
    """一格一个事件名（等宽）。"""
    return [
        rect(x, y, w, h, fill=fill, stroke=stroke, rx=5),
        txt(x + w / 2, y + h / 2, s, size=size, fill=fg, anchor="middle", mono=True),
    ]


def _hand(x, y, color, crossed=False):
    """一只简笔手。x,y 为指尖左上角，整体约 38x36。"""
    b = []
    for i in range(4):
        b.append(rect(x + 2 + i * 6, y, 4, 16, fill=color, rx=2))
    b.append(rect(x, y + 12, 26, 22, fill=color, rx=6))
    b.append(rect(x - 6, y + 16, 8, 12, fill=color, rx=4))
    if crossed:
        b.append(line(x - 8, y - 4, x + 32, y + 40, stroke=BLUE, sw=2.2))
        b.append(line(x + 32, y - 4, x - 8, y + 40, stroke=BLUE, sw=2.2))
    return b


# ---------------------------------------------------------------- 图 37
def fig_12_1(out_dir):
    persisted = ["接话 · 这趟开工", "定主意 · 起一步", "开场白落笔", "业主的话落笔",
                 "师傅的回话落笔", "动手 · 拧的每颗螺丝", "看结果 · 这一步收工", "再定 · 这趟交活"]
    live = ["领班忙还是闲", "回话逐字往外流", "有新话进门了"]
    b = []
    b.append(rect(40, 34, 360, 270, fill=PAPER, stroke=LINE, rx=10))
    b.append(rect(420, 34, 240, 270, fill=PAPER, stroke=HAIR, rx=10, dash="5 4"))
    b.append(txt(56, 22, "落进笔记 · 要留底的（能回放）", size=11.5, fill=BLUE, weight=600))
    b.append(txt(436, 22, "喊一嗓子 · 过路的（不落笔）", size=11.5, fill=GRAY, weight=600))
    for i, name in enumerate(persisted):
        y = 46 + i * 32
        b.append(rect(56, y, 328, 26, fill=B1, stroke=HAIR, rx=5))
        b.append(txt(70, y + 13, name, size=12, fill=INK))
    for i, name in enumerate(live):
        y = 76 + i * 76
        b.append(rect(436, y, 208, 32, fill=B1, stroke=HAIR, rx=5))
        b.append(txt(452, y + 16, name, size=11.5, fill=INK))
    b.append(line(410, 44, 410, 296, stroke=LINE, sw=1, dash="4 4"))
    b.append(vtxt(410, 170, "落笔分界", size=10.5, fill=GRAY))
    b.extend(banner(40, 316, 608, "能回放的都在左列；过路不落笔的都在右列。"))
    b.append(note(40, 368, "口径：要留底的落进笔记，日后能原样重念；喊一嗓子的只广播不落笔 · 官方架构文档的轮次流程一节", size=10.5))
    return write(
        out_dir, "fig-12-1-turn-skeleton.svg", 382,
        "图 28：一个轮次的持久骨架与实时信号",
        "一个轮次内两类事件并排对照。左列写进会话日志，是能回放的持久事实：turn/start、step/start、"
        "system/message、user/message、assistant/message、tool/*、step/end、turn/end。右列只在进程里广播，"
        "不落盘：agent/status、agent/assistant-stream、agent/inbox/*。"
        "核心反差：能回放的都在左列，过路不落盘的一律在右列。",
        b,
    )


# ---------------------------------------------------------------- 图 38
def fig_12_2(out_dir):
    """竖向时序图：七条生命线，时间自上而下。"""
    b = []
    # 生命线横坐标（间距 88px，首尾留边）
    X = {"u": 95, "s": 183, "d": 271, "h": 359, "sp": 447, "llm": 535, "tl": 623}
    HY, HH, BOT = 22, 42, 980

    def ew(s, size):
        """按「中文 1 字宽、英文 0.55 字宽」估算文本宽度。"""
        n = 0.0
        for ch in s:
            n += 1.0 if ord(ch) > 0x2E7F else 0.55
        return n * size

    # --- 参与者头框（一字排开）+ 生命线 ---
    heads = [
        ("u", "业主", 56),
        ("s", "记笔记的", 72),
        ("d", "领班的", 64),
        ("h", "公告栏", 64),
        ("sp", "拼开场白的", 86),
        ("llm", "师傅", 48),
        ("tl", "拧螺丝的", 64),
    ]
    for key, name, bw in heads:
        cx = X[key]
        if key == "u":            # 外部调用方：浅底深字
            b.append(rect(cx - bw / 2, HY, bw, HH, fill=B1, stroke=LINE, rx=8))
            b.append(txt(cx, HY + HH / 2, name, size=11, fill=INK, weight=600, anchor="middle"))
        else:                     # 系统内参与者：深蓝底白字
            b.append(rect(cx - bw / 2, HY, bw, HH, fill=BLUE, rx=8))
            b.append(txt(cx, HY + HH / 2, name, size=12, fill="#FFFFFF",
                         weight=600, anchor="middle"))
    for key in X:
        b.append(line(X[key], HY + HH, X[key], BOT, stroke=LINE, sw=1.0, dash="4 3"))

    # --- 左侧分支括号（竖线 + 顶端标签 + 可选分隔标签）；最后绘制，压在消息之上 ---
    def bracket(x, y0, y1, label, div=None, div_label=None):
        b.append(line(x, y0, x, y1, stroke=BLUE, sw=1.3))
        b.append(line(x, y0, x + 9, y0, stroke=BLUE, sw=1.3))
        b.append(line(x, y1, x + 9, y1, stroke=BLUE, sw=1.3))
        lw = ew(label, 10.5) + 16
        b.append(rect(x + 10, y0 - 11, lw, 16, fill=B1, rx=8))
        b.append(txt(x + 10 + lw / 2, y0 - 3, label, size=10.5, fill=INK, anchor="middle", mono=True))
        if div is not None:
            b.append(line(x, div, x + 9, div, stroke=BLUE, sw=1.3))
            lw2 = ew(div_label, 10.5) + 16
            b.append(rect(x + 10, div - 11, lw2, 16, fill=CREAM, rx=8))
            b.append(txt(x + 10 + lw2 / 2, div - 3, div_label, size=10.5,
                         fill=INK, anchor="middle", mono=True))

    # --- 消息：横向箭头连两条生命线，标签压在线上方 ---
    msgs = [
        ("u", "d", 94, "业主一句话进门", "call"),
        ("d", "u", 121, "回执：话已并进这一趟", "ret"),
        ("d", "d", 146, "排队的活唤醒领班", "self"),
        ("d", "u", 173, "喊一嗓子：开工了", "ret"),
        ("d", "s", 200, "笔记：这趟开工", "call"),
        ("d", "sp", 227, "拼开场白（一道道过）", "call"),
        ("d", "h", 254, "起这一步前先过一道手", "call"),
        ("h", "d", 281, "回话：拦下 / 放行（要不要另起新账）", "ret"),
        ("d", "s", 327, "笔记：这趟空收，不记步骤", "call"),
        ("d", "s", 373, "笔记：起一步", "call"),
        ("d", "h", 400, "问师傅前先过一道手", "call"),
        ("d", "llm", 427, "把问题递到师傅手里", "call"),
        ("d", "s", 454, "笔记：开场白与业主的话", "call"),
        ("d", "s", 481, "笔记：这次问的底细（按需）", "call"),
        ("d", "llm", 508, "请师傅作答（边答边传）", "call"),
        ("llm", "d", 535, "师傅逐字回话", "ret"),
        ("d", "u", 562, "喊一嗓子：回话在往外流", "ret"),
        ("d", "s", 608, "笔记：师傅这一答的草稿", "call"),
        ("d", "h", 635, "没答成，过一道手", "call"),
        ("h", "d", 662, "回话：原话重问 或 认下这次错", "ret"),
        ("d", "s", 708, "笔记：师傅的回话", "call"),
        ("d", "tl", 735, "排活：哪些能同时干", "call"),
        ("d", "s", 781, "笔记：要拧这颗螺丝", "call"),
        ("d", "tl", 808, "先过五道手，能同时的同时动手", "call"),
        ("tl", "s", 835, "笔记：拧的结果（直达）", "call"),
        ("d", "s", 862, "笔记：这一步收工", "call"),
        ("d", "h", 908, "这趟收尾前再过一道手", "call"),
        ("d", "s", 935, "笔记：这趟交活", "call"),
        ("d", "u", 962, "喊一嗓子：收工了", "ret"),
    ]
    for frm, to, y, label, style in msgs:
        if style == "self":                       # 领班自唤醒
            x = X[frm]
            b.append(path(f"M{x},{y} h26 v14 h-16", stroke=GRAY, sw=1.3, marker="ar"))
            lx = x + 34
            lw = ew(label, 10.5) + 10
            b.append(rect(lx - 4, y + 1, lw, 15, fill="#FFFFFF"))
            b.append(txt(lx, y + 9, label, size=10.5, fill=INK))
            continue
        x1, x2 = X[frm], X[to]
        if style == "ret":                        # 返回 / 回话：蓝虚线
            b.append(line(x1, y, x2, y, stroke=BLUE, sw=1.3, dash="5 3", marker="arb"))
        else:                                     # 普通调用：灰实线
            b.append(line(x1, y, x2, y, stroke=GRAY, sw=1.3, marker="ar"))
        lx = (x1 + x2) / 2
        lw = ew(label, 10.5) + 10
        b.append(rect(lx - lw / 2, y - 17, lw, 15, fill="#FFFFFF"))
        b.append(txt(lx, y - 9, label, size=10.5, fill=INK, anchor="middle"))

    # 分支括号最后画，保证标签完整、不被消息遮罩切边
    bracket(46, 305, 925, "alt  被拦 / 没活 / 起步前没过", 351, "else  放行")
    bracket(58, 586, 850, "alt  这一答没成", 686, "else  师傅答成了")
    bracket(70, 759, 848, "loop  收齐结果再往下，一批有上限")
    bracket(58, 886, 925, "opt  师傅说完了，也没新话进门")

    b.extend(banner(40, 990, 608, "除了拧螺丝的交回的结果直接落笔记，其余每句话都经领班的转一手。"))
    b.append(note(40, 1038, "灰实线＝派活，蓝虚线＝回话；左侧括号标分支（alt / loop / opt）", size=10.5))
    b.append(note(40, 1058, "简化自 官方生命周期文档", size=10.5))
    return write(
        out_dir, "fig-12-2-turn-sequence.svg", 1072,
        "图 29：从 followup 到工具结果，一次轮次的完整时序",
        "竖向时序图，七条生命线自左向右：用户/SDK、Session、Driver、hooks、ctx.systemPrompt、ctx.llm、"
        "ctx.tools，时间自上而下。followup 进来后 Driver 开轮次（turn/start），组装提示词、跑 agent/pre-step；"
        "被拒或首批为空则空轮次结束，接纳则开步骤（step/start），协调请求、llm/stream 流式返回，"
        "模型成功后进工具循环（tool/call → 有序 pre、并发 execute → tool/result），最后 step/end、turn/end、"
        "agent/status idle。左侧括号标出 alt / else / loop / opt 分支。",
        b,
    )


# ---------------------------------------------------------------- 图 39
def fig_12_3(out_dir):
    b = []
    lanes = [
        ("① startsRequestSeries —— 要不要开一串新请求", 34),
        ("② retry —— 本次尝试失败后只重发，不重拼", 112),
        ("③ 提示词准入 —— 走历史，不走请求体", 190),
    ]
    for title, y in lanes:
        b.append(rect(40, y, 560, 64, fill=PAPER, stroke=HAIR, rx=10))
        b.append(txt(56, y + 18, title, size=11.5, fill=INK, weight=600))
    # 泳道 1：turn/start → agent/pre-step → startsRequestSeries
    for x, w, s in [(56, 80, "turn/start"), (154, 112, "agent/pre-step")]:
        b.extend(_chip(x, 66, w, s))
    b.append(line(138, 78, 152, 78, marker="ar"))
    b.append(line(268, 78, 282, 78, marker="ar"))
    b.append(rect(284, 66, 140, 24, fill=TEAL, rx=12))
    b.append(txt(354, 78, "startsRequestSeries", size=10.5, fill="#FFFFFF", anchor="middle", mono=True))
    b.append(txt(436, 78, "enter 决策里带上这个布尔量", size=10.5, fill=GRAY))
    # 泳道 2：step/start → agent/request-error → retry
    for x, w, s in [(56, 80, "step/start"), (154, 140, "agent/request-error")]:
        b.extend(_chip(x, 144, w, s))
    b.append(line(138, 156, 152, 156, marker="ar"))
    b.append(line(296, 156, 310, 156, marker="ar"))
    b.append(rect(312, 144, 52, 24, fill=TEAL, rx=12))
    b.append(txt(338, 156, "retry", size=10.5, fill="#FFFFFF", anchor="middle", mono=True))
    b.append(txt(376, 156, "同一步骤内重发", size=10.5, fill=GRAY))
    # 泳道 3：step/start → system/message
    b.extend(_chip(56, 222, 80, "step/start"))
    b.append(line(138, 234, 152, 234, marker="ar"))
    b.append(rect(154, 222, 108, 24, fill=TEAL, rx=12))
    b.append(txt(208, 234, "system/message", size=10.5, fill="#FFFFFF", anchor="middle", mono=True))
    b.append(txt(276, 234, "占 surface 第 0 号节点", size=10.5, fill=GRAY))
    # 轮次边界（三个决策点都不与它相交）
    b.append(line(626, 22, 626, 258, stroke=BLUE, sw=1.6))
    b.append(circle(626, 22, 3, fill=BLUE))
    b.append(circle(626, 258, 3, fill=BLUE))
    b.append(vtxt(654, 140, "轮次边界", size=11, fill=BLUE))
    b.extend(banner(40, 268, 608, "三个决策点都卡在轮次内部，一个都不碰右侧那条轮次边界。"))
    b.append(note(40, 320, "位置来源：官方架构文档的轮次流程一节", size=10.5))
    return write(
        out_dir, "fig-12-3-three-decisions.svg", 334,
        "图 30：三个决策点在时序里的位置",
        "三条泳道各标一个决策点。startsRequestSeries 卡在 agent/pre-step 的返回里；retry 卡在 "
        "agent/request-error；提示词准入发生在 step/start 之后，写成 system/message 事件。"
        "右侧竖线是轮次边界，三个决策点都在它左边、都不与它相交——核心反差：三个决策点全在轮次内部。",
        b,
    )


# ---------------------------------------------------------------- 图 40
def fig_13_1(out_dir):
    cols = [40, 169, 298, 427, 556]
    names = ["登记", "审查", "放行", "执行", "落账"]
    duties = ["先记账，后动手", "安检一道接一道", "把门的点头才放", "真正动手", "盖章定稿"]
    ins = ["有人想拧这颗", "账上那颗", "审完的那颗", "放了行的那颗", "拧完的结果"]
    outs = ["账上落一笔", "拦下 或 原样上送", "放 或 拒", "拧完的结果", "定稿的回话"]
    arc = {1: "只拦不放 · 只能更严", 2: "点一次头只放这一颗", 3: "递家伙的管计时催工"}
    bottom = {0: ("只记账", "不拦人"), 4: ("只定稿", "章一落就冻结")}
    b = []
    for i, x in enumerate(cols):
        cx = x + 52
        if i in arc:
            b.append(rect(x, 60, 104, 54, fill=BLUE, rx=8))
            b.append(txt(cx, 82, names[i], size=12.5, fill="#FFFFFF", weight=600, anchor="middle"))
            b.append(txt(cx, 102, duties[i], size=10.5, fill=ONB, anchor="middle"))
            b.append(path(f"M{x + 8},58 Q{cx},8 {x + 96},58", stroke=TEAL, sw=1.4))
            b.append(txt(cx, 20, arc[i], size=10.5, fill=TEAL, anchor="middle"))
        else:
            b.append(rect(x, 60, 104, 54, fill=PAPER, stroke=LINE, rx=8))
            b.append(txt(cx, 82, names[i], size=12.5, fill=INK, weight=600, anchor="middle"))
            b.append(txt(cx, 102, duties[i], size=10.5, fill=GRAY, anchor="middle"))
            b.append(line(cx - 30, 168, cx + 30, 168, stroke=LINE, sw=1, dash="3 3"))
            t1, t2 = bottom[i]
            b.append(txt(cx, 188, t1, size=11, fill=TEAL, anchor="middle"))
            b.append(txt(cx, 204, t2, size=10.5, fill=GRAY, anchor="middle"))
        b.append(txt(cx, 134, ins[i], size=10.5, fill=GRAY, anchor="middle"))
        b.append(txt(cx, 152, outs[i], size=10.5, fill=BLUE, weight=600, anchor="middle"))
    for i in range(4):
        b.append(line(cols[i] + 106, 87, cols[i + 1] - 2, 87, stroke=GRAY, sw=1.3, marker="ar"))
    b.extend(banner(40, 220, 608,
                    "越靠前越能决定这颗拧不拧，越靠后越只能决定看到什么；",
                    "登记只记账，落账只定稿，章一落就冻结。", size2=11.5))
    b.append(note(40, 286, "灰字为进，蓝字为出 · 简化自 官方工具流水线文档", size=10.5))
    return write(
        out_dir, "fig-13-1-five-stages.svg", 300,
        "图 31：一次工具调用要穿过的五段",
        "一条横向链 pre → guards → execute → post → finalize。上方三条弧线标出三个 waterfall："
        "tools/pre-execute、tools/execute、tools/post-execute；下方标出两个非 waterfall 的收紧点："
        "guards 只能收紧、finalize 是定稿。每段下方是它的输入与输出，关键类型是 PreToolDecision、"
        "工具函数体、ToolExecutionResult。核心反差：能改写这次调用的只有三个 waterfall。",
        b,
    )


# ---------------------------------------------------------------- 图 41
def fig_13_2(out_dir):
    cols = [40, 169, 298, 427, 556]
    names = ["登记", "审查", "放行", "执行", "落账"]
    b = []
    for i, x in enumerate(cols):
        cx = x + 52
        b.append(rect(x, 40, 104, 44, fill=PAPER, stroke=LINE, rx=8))
        b.append(txt(cx, 62, names[i], size=12, fill=INK, weight=600, anchor="middle"))
    for i in range(4):
        b.append(line(cols[i] + 106, 62, cols[i + 1] - 2, 62, stroke=GRAY, sw=1.3, marker="ar"))
    # 三只手：审查与放行能喊停，执行那道递家伙的被打叉
    b.extend(_hand(202, 96, TEAL))
    b.extend(_hand(331, 96, TEAL))
    b.extend(_hand(460, 96, GRAY, crossed=True))
    # 无手的两道用虚线小框占位
    for cx in (92, 608):
        b.append(rect(cx - 19, 96, 38, 34, fill="none", stroke=HAIR, rx=6, dash="3 3"))
        b.append(txt(cx, 113, "—", size=11, fill=LINE, anchor="middle"))
    b.append(txt(92, 156, "先记账，不拦人", size=10.5, fill=GRAY, anchor="middle"))
    b.append(txt(221, 148, "能拒", size=11, fill=TEAL, weight=600, anchor="middle"))
    b.append(txt(221, 164, "只拦不放，能喊停", size=10.5, fill=GRAY, anchor="middle"))
    b.append(txt(350, 148, "能不放", size=11, fill=TEAL, weight=600, anchor="middle"))
    b.append(txt(350, 164, "把门的点头才过，能喊停", size=10.5, fill=GRAY, anchor="middle"))
    b.append(txt(479, 148, "递家伙的喊不停", size=10.5, fill=INK, weight=600, anchor="middle"))
    b.append(txt(479, 164, "调得动闹钟，停不下这颗", size=10.5, fill=TEAL, anchor="middle"))
    b.append(txt(608, 156, "定稿与观察", size=10.5, fill=GRAY, anchor="middle"))
    # 链外两只手
    b.append(rect(40, 186, 608, 40, fill=PAPER, stroke=HAIR, rx=8))
    b.extend(_hand(54, 190, TEAL))
    b.append(txt(104, 206, "把门的——审查拿不准时报他；他不点头，这颗就拦下，能喊停", size=11, fill=INK))
    b.append(rect(40, 232, 608, 40, fill=PAPER, stroke=HAIR, rx=8))
    b.extend(_hand(54, 236, TEAL))
    b.append(txt(104, 252, "外头下活的——随时收回这颗，能喊停；换个闹钟也切不断收回", size=11, fill=INK))
    b.extend(banner(40, 288, 608, "叫停不是无声的：先记账，后动手；拦下的、拧砸的、收回的，都归成同一张回话。"))
    b.append(note(40, 340, "链上只有递家伙的那只手喊不停 · 简化自 官方工具流水线文档", size=10.5))
    return write(
        out_dir, "fig-13-2-who-can-abort.svg", 354,
        "图 32：这条链上谁能喊停",
        "沿五个阶段各标一只表示「能不能喊停」的手。pre 有 deny / cancel，guards 有 reason，两只手能停；"
        "execute 的包装层是打叉的手，只能改 exec.signal，停不下来。链外还有两只手：审批在 pre 的 ask 处拒绝，"
        "外部调用方随时取消。核心反差：整条链上唯一停不下来的，是真正干活的 execute 包装层。",
        b,
    )


# ---------------------------------------------------------------- 图 42
def fig_13_3(out_dir):
    entries = [("拦下的", "把门的不点头", 40, 60), ("拧砸了的", "活干到一半出错", 100, 120), ("半道收回的", "下活的反悔", 160, 180)]
    rows = [("拦下", "附理由", 108), ("拧砸", "没拧成", 130),
            ("收回 · 已动手", "算拧过", 152), ("收回 · 未动手", "没派活", 174),
            ("没这号活", "报不上名", 196)]
    b = []
    for cn, sub, y, _c in entries:
        b.append(rect(40, y, 150, 40, fill=B1, stroke=HAIR, rx=8))
        b.append(txt(58, y + 15, cn, size=12, fill=INK, weight=600))
        b.append(txt(58, y + 31, sub, size=10.5, fill=GRAY))
    b.append(rect(360, 40, 290, 170, fill=BLUE, rx=10))
    b.append(txt(380, 64, "同一张回话", size=13, fill="#FFFFFF", weight=600))
    b.append(txt(380, 84, "所有叫停与失败都归一成这一条", size=10.5, fill=ONB))
    for i, (label, code, y) in enumerate(rows):
        b.append(circle(386, y, 3.5, fill=T1 if i < 2 else "#FFFFFF"))
        b.append(txt(398, y, label, size=11, fill="#FFFFFF"))
        b.append(txt(640, y, code, size=11, fill=ONB, anchor="end"))
    for (_cn, _sub, _y, cy), (row_l, _code, row_y) in zip(entries, rows):
        b.append(path(f"M192,{cy} C280,{cy} 300,{row_y} 354,{row_y}", stroke=GRAY, sw=1.3, marker="ar"))
    b.extend(banner(40, 228, 608, "拦下的、拧砸的、半道收回的，三条路出口都是同一张回话；这颗拧砸了，这趟活不跟着黄。"))
    b.append(note(40, 278, "回话上标的区别：拦下附理由；拧砸标「没拧成」；报不上名的就是没这号活", size=10.5))
    b.append(note(40, 296, "收回分两种：已经动了手的算拧过，还没派活的算没动手", size=10.5))
    return write(
        out_dir, "fig-13-3-trace-lands.svg", 310,
        "图 33：中止和失败都汇到同一条 tool/result",
        "左侧三条入口：拒绝 denied、异常 throw、取消 cancelled，各画一条线。三条线汇进右侧同一个工具结果框 "
        "tool/result，框内逐条标出各自的错误码：拒绝带 reason、异常归一化成 isError、取消分 ABORTED 与 "
        "ABORTED_BEFORE_DISPATCH、不存在的工具是 UNKNOWN_TOOL。核心反差：三条看着不同的路，出口只有一个，"
        "共同点是调用失败但不终止当前轮次。",
        b,
    )


# ---------------------------------------------------------------- 图 43
def fig_14_1(out_dir):
    b = []
    b.append(rect(60, 40, 84, 200, fill=BLUE, rx=8))
    b.append(vtxt(102, 140, "总账", size=12.5, fill="#FFFFFF"))
    b.append(line(144, 71, 158, 71, stroke=HAIR))
    b.append(rect(160, 58, 90, 26, fill=CREAM, stroke=HAIR, rx=13))
    b.append(txt(205, 71, "只写不改", size=11, fill=INK, anchor="middle"))
    b.append(line(146, 140, 292, 140, stroke=BLUE, sw=1.8, marker="arb"))
    b.append(txt(150, 124, "照账誊抄", size=10.5, fill=BLUE))
    b.append(rect(300, 60, 340, 170, fill=PAPER, stroke=LINE, rx=10))
    b.append(txt(320, 88, "抄件", size=13, fill=INK, weight=600))
    b.append(txt(320, 112, "从总账誊抄，从不单独记账", size=11, fill=GRAY))
    b.append(rect(320, 136, 108, 26, fill=TEAL, rx=13))
    b.append(txt(374, 149, "可撕可重誊", size=11, fill="#FFFFFF", anchor="middle"))
    b.append(txt(320, 186, "重誊 = 从同一本总账再抄一遍", size=11, fill=INK))
    b.append(txt(320, 208, "它是抄件，不是第二本账", size=10.5, fill=GRAY))
    b.extend(banner(40, 246, 608, "只有一支笔写真账：事情记进总账；撕掉抄件，不丢任何东西。"))
    b.append(note(40, 296, "口径：总账只往后添、从不涂改，是唯一真源。", size=10.5))
    b.append(note(40, 314, "抄件由总账誊抄而来，从不单独记账 · 简化自 官方会话子系统说明", size=10.5))
    return write(
        out_dir, "fig-14-1-log-is-truth.svg", 330,
        "图 34：日志是唯一真源，消息历史是它的投影",
        "左侧一个窄的 SessionEvent 日志竖条，旁标「只写不改」；一支箭头由它指向右侧派生的「消息历史」框，"
        "框旁标「可删可重算」。核心反差：日志是唯一真源，消息历史只是它的投影——"
        "删掉这个视图不丢任何东西，回放就是从同一组事件重新派生。",
        b,
    )


# ---------------------------------------------------------------- 图 44
def fig_14_2(out_dir):
    b = []
    b.append(line(60, 150, 620, 150, stroke=BLUE, sw=2))
    b.append(circle(60, 150, 3, fill=BLUE))
    b.append(circle(620, 150, 3, fill=BLUE))
    b.append(rect(280, 138, 120, 24, fill=BLUE, rx=12))
    b.append(txt(340, 150, "总账流水", size=11, fill="#FFFFFF", anchor="middle"))
    b.append(txt(340, 174, "每记一笔就往前推一次", size=10.5, fill=GRAY, anchor="middle"))
    # 上层：抄件缓存
    b.append(rect(120, 42, 440, 68, fill=B1, stroke=HAIR, rx=10))
    b.append(txt(140, 66, "抄件缓存", size=12, fill=INK, weight=600))
    b.append(txt(140, 90, "每份抄件首次用到时誊一次；对应账目改动才重誊", size=10.5, fill=GRAY))
    b.append(line(200, 112, 200, 146, stroke=GRAY, sw=1.2, dash="4 3", marker="ar"))
    b.append(txt(210, 130, "记账驱动", size=10.5, fill=GRAY))
    # 下层：登记簿缓存
    b.append(rect(120, 194, 440, 68, fill=B1, stroke=HAIR, rx=10))
    b.append(txt(140, 218, "登记簿缓存", size=12, fill=INK, weight=600))
    b.append(txt(140, 242, "只在总账上挂一个听差；每记一笔就更新各栏现值", size=10.5, fill=GRAY))
    b.append(line(480, 192, 480, 154, stroke=GRAY, sw=1.2, dash="4 3", marker="ar"))
    b.append(txt(490, 174, "记账驱动", size=10.5, fill=GRAY))
    b.extend(banner(40, 288, 608, "正主只有总账一份；两份影子都由记账驱动，随时能重长，撕了重算都对。"))
    b.append(note(40, 338, "第一层管「这页能看到什么」，第二层管「某一栏现在是什么值」", size=10.5))
    return write(
        out_dir, "fig-14-2-derivation-cost.svg", 354,
        "图 35：派生的代价与两层缓存",
        "中间一条「事件流」横线。上方挂 deriveMessages() 的 surface 缓存，管「这一步会话看到什么」；"
        "下方挂 ctx.sessionProjections 的单元缓存，管「某个域现在是什么值」。两条缓存都用虚线回指事件流，"
        "表示都由事件驱动。核心反差：派生的代价靠两层缓存压住，但两层都不落成第二份真源，删掉重算都对。",
        b,
    )


# ---------------------------------------------------------------- 图 45
def fig_14_3(out_dir):
    b = []
    b.append(txt(340, 20, "Session.append 一次", size=11, fill=GRAY, anchor="middle"))
    b.append(line(340, 30, 340, 56, stroke=GRAY, sw=1.3, marker="ar"))
    b.append(rect(240, 60, 200, 64, fill=BLUE, rx=10))
    b.append(txt(340, 84, "内存日志", size=13, fill="#FFFFFF", weight=600, anchor="middle"))
    b.append(txt(340, 106, "唯一真源", size=10.5, fill=ONB, anchor="middle"))
    b.append(path("M340,126 C340,172 200,168 140,204", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(path("M340,126 V204", stroke=GRAY, sw=1.3, marker="ar"))
    b.append(path("M340,126 C340,172 480,168 540,204", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(txt(132, 182, "可丢", size=10.5, fill=GRAY))
    b.append(txt(350, 182, "会等", size=10.5, fill=GRAY))
    b.append(txt(500, 182, "另一 seam", size=10.5, fill=GRAY))
    outs = [
        (40, "session/event", "提交后广播 · 可丢"),
        (245, "session/flush", "awaited 屏障 · 会等"),
        (450, "持久化后端", "另一 seam，落盘归它"),
    ]
    for x, name, sub in outs:
        b.append(rect(x, 210, 190, 96, fill=PAPER, stroke=LINE, rx=10))
        b.append(txt(x + 16, 246, name, size=12, fill=INK, weight=600, mono=(x != 450)))
        b.append(txt(x + 16, 272, sub, size=10.5, fill=GRAY))
    b.extend(banner(40, 320, 608, "一次 append 只动内存日志；三条路互不相同，观察者再慢也拖不住写入。"))
    b.append(note(40, 370, "session/event 是提交后 fire-and-forget 广播，回调抛了不影响这次提交。", size=10.5))
    b.append(note(40, 388, "session/flush 是 awaited 并行屏障，调用方等所有监听器落完盘", size=10.5))
    return write(
        out_dir, "fig-14-3-log-broadcast-persistence.svg", 404,
        "图 36：内存日志、广播与持久化是三条不同的路",
        "先画一个「内存日志」框，一次 Session.append 进去后分三条出线：session/event 是提交后广播、标注「可丢」；"
        "session/flush 是 awaited 并行屏障、标注「会等」；持久化后端标注「另一 seam」。"
        "核心反差：一次 append 只动内存日志，三条路互不相同，所以观察者再慢也拖不住写入。",
        b,
    )


FIGURES = [
    ("12-1", fig_12_1),
    ("12-2", fig_12_2),
    ("12-3", fig_12_3),
    ("13-1", fig_13_1),
    ("13-2", fig_13_2),
    ("13-3", fig_13_3),
    ("14-1", fig_14_1),
    ("14-2", fig_14_2),
    ("14-3", fig_14_3),
]
