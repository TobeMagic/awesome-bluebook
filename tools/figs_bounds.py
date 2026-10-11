#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝宝书 §15–§17 图（边界部分）。

配合 tools/build_figures.py 使用：
    python tools/build_figures.py --only 15-1 15-2 15-3 16-1 16-2 16-3 17-1 17-2 17-3
"""
from __future__ import annotations

from svgkit import (  # noqa: F401
    INK, GRAY, BLUE, CREAM, TEAL, LINE, HAIR, PAPER,
    B1, B2, B3, B4, ONB, T1,
    rect, txt, vtxt, path, line, circle, diamond, note, tag, banner, write,
    W,
)


# ---------------------------------------------------------------- 图 46
def fig_15_1(out_dir):
    rows = [
        ("core", "核心主干服务", "空", BLUE, "#FFFFFF"),
        ("seam", "可替换的能力 seam", "有平级实现包", TEAL, "#FFFFFF"),
        ("service", "独立服务", "空", B3, INK),
        ("bundle", "组合包／组合点", "空", B1, INK),
    ]
    b = []
    b.append(txt(40, 22, "角色", size=11, fill=GRAY))
    b.append(txt(180, 22, "官方名", size=11, fill=GRAY))
    b.append(txt(392, 22, "实现列", size=11, fill=GRAY))
    y0, step, rh = 40, 54, 42
    for i, (role, name, why, fill, fg) in enumerate(rows):
        y = y0 + i * step
        b.append(rect(40, y, 608, rh, fill=PAPER, stroke=HAIR))
        b.append(rect(52, y + 8, 92, 26, fill=fill, rx=13))
        b.append(txt(98, y + 21, role, size=11.5, fill=fg, anchor="middle", mono=True))
        b.append(txt(180, y + 21, name, size=12.5, fill=INK, weight=600))
        b.append(txt(392, y + 21, why, size=11, fill=GRAY if i != 1 else TEAL))
    b.extend(banner(40, 264, 608, "实现列有平级实现包的一定是 seam；空的三类靠官方角色列区分。", fill=CREAM))
    b.append(note(40, 306, "92 个 ctx 键：core 55 / seam 33 / service 3 / bundle 1 · 实现列与角色列取自官方能力表"))
    return write(
        out_dir, "fig-15-1-four-roles.svg", 320,
        "图 37：四种角色看实现列",
        "四种角色并排：core 核心主干服务、seam 可替换的能力 seam、service 独立服务、bundle 组合包。"
        "core、service、bundle 三格的实现列都是空的，只能靠官方角色列区分；seam 那格有平级实现包。",
        b,
    )


# ---------------------------------------------------------------- 图 47
def fig_15_2(out_dir):
    b = []
    b.append(rect(60, 20, 190, 46, fill=PAPER, stroke=LINE, rx=8))
    b.append(txt(155, 43, "agent-loop", size=12.5, fill=INK, weight=600, anchor="middle", mono=True))
    b.append(rect(430, 20, 190, 46, fill=PAPER, stroke=LINE, rx=8))
    b.append(txt(525, 43, "compaction-basic", size=12.5, fill=INK, weight=600, anchor="middle", mono=True))

    b.append(rect(240, 118, 200, 58, fill=BLUE, rx=8))
    b.append(txt(340, 139, "ctx.llm", size=14, fill="#FFFFFF", weight=600, anchor="middle", mono=True))
    b.append(txt(340, 159, "适配器注册表", size=11, fill=ONB, anchor="middle"))

    b.append(path("M155,66 C155,96 300,92 322,116", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(path("M525,66 C525,96 380,92 358,116", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(txt(160, 92, "查 key", size=10.5, fill=GRAY))
    b.append(txt(486, 92, "查 key", size=10.5, fill=GRAY))

    impls = [("llm-deepseek", 40), ("llm-pi-ai", 250), ("llm-replay", 460)]
    for name, x in impls:
        b.append(rect(x, 244, 180, 46, fill=B1, stroke=HAIR, rx=8))
        b.append(txt(x + 90, 267, name, size=12, fill=INK, weight=600, anchor="middle", mono=True))
        b.append(path(f"M{x + 90},242 C{x + 90},210 340,208 340,178", stroke=GRAY, sw=1.2, marker="ar"))
    b.append(txt(148, 226, "供 key", size=10.5, fill=GRAY))
    b.append(txt(340, 226, "供 key", size=10.5, fill=GRAY))
    b.append(txt(548, 226, "供 key", size=10.5, fill=GRAY))

    b.extend(banner(40, 308, 608, "消费方只认 key，实现平级挂着；换掉一个实现，消费方不动。"))
    b.append(note(40, 350, "ctx.llm 三个实现：llm-deepseek / llm-pi-ai / llm-replay（后者在 test-support 分组）"))
    return write(
        out_dir, "fig-15-2-seam-fanout.svg", 364,
        "图 38：一个 seam 的多个实现平级挂在同一个 key 下",
        "上方两个消费方 agent-loop 与 compaction-basic 只连到 ctx.llm 这个 key；下方 llm-deepseek、"
        "llm-pi-ai、llm-replay 三个实现包平级挂在同一个 key 下。消费方与实现之间没有直接的边。",
        b,
    )


# ---------------------------------------------------------------- 图 48
def fig_15_3(out_dir):
    b = []
    cols = 11
    cw, ch, gx, gy, y0 = 22, 22, 3, 8, 48
    lw = cols * (cw + gx) - gx
    x_l, x_r = 60, 368
    b.append(txt(x_l + lw / 2, 30, "有替换位", size=13, fill=INK, weight=600, anchor="middle"))
    b.append(txt(x_r + lw / 2, 30, "已备好第二个实现", size=13, fill=INK, weight=600, anchor="middle"))
    for n in range(33):
        i, j = n % cols, n // cols
        b.append(rect(x_l + i * (cw + gx), y0 + j * (ch + gy), cw, ch, fill=B1, stroke=HAIR, rx=3))
    for n in range(33):
        i, j = n % cols, n // cols
        x, y = x_r + i * (cw + gx), y0 + j * (ch + gy)
        if n < 15:
            b.append(rect(x, y, cw, ch, fill=TEAL, rx=3))
        else:
            b.append(rect(x, y, cw, ch, fill="#FFFFFF", stroke=LINE, rx=3, dash="3 3"))
    solid_bot = y0 + (ch + gy) + ch
    grid_bot = y0 + 2 * (ch + gy) + ch
    b.append(line(x_r + lw + 4, solid_bot, x_r + lw + 4, grid_bot, stroke=LINE, sw=1.2, dash="3 3"))
    b.append(vtxt(x_r + lw + 14, (solid_bot + grid_bot) / 2, "还空着", size=11, fill=GRAY))
    b.extend(banner(40, 170, 608, "有替换位，不等于备好了第二个实现。"))
    b.append(note(40, 218, "一格里一个位子 · 实心 = 第二个实现已到岗 · 虚线空格 = 契约立好了，实现还只有一份"))
    return write(
        out_dir, "fig-15-3-seam-second-impl.svg", 268,
        "图 39：33 个 seam 里只有 15 个备好了第二个实现",
        "一条横轴摆 33 格，每格一个 seam。绿色的 15 格已有两个以上平级实现；灰色的 18 格契约立好了，"
        "眼下只有一份实现。有替换位和有没有现成的第二个实现，是两笔账。",
        b,
    )


# ---------------------------------------------------------------- 图 49
def fig_16_1(out_dir):
    rows = [
        ("guard", "策略把关", "策略写到的模式", "策略没写到的模式", BLUE),
        ("approval", "人工审批", "没被授权的操作", "人批错；无人应答按拒绝", BLUE),
        ("sandbox", "受限执行", "越出文件边界的写", "获准访问的资源；旧内核只部分强制", BLUE),
    ]
    b = []
    y0, step, rh = 16, 88, 74
    for i, (name, duty, can, cannot, fill) in enumerate(rows):
        y = y0 + i * step
        b.append(rect(40, y, 608, rh, fill=PAPER, stroke=HAIR))
        b.append(rect(52, y + 16, 118, 42, fill=fill, rx=6))
        b.append(txt(111, y + 30, name, size=12.5, fill="#FFFFFF", weight=600, anchor="middle", mono=True))
        b.append(txt(111, y + 47, duty, size=10.5, fill=ONB, anchor="middle"))
        b.append(rect(186, y + 12, 226, 50, fill=B1, stroke=HAIR, rx=6))
        b.append(txt(299, y + 27, "挡得住", size=11, fill=TEAL, anchor="middle"))
        b.append(txt(299, y + 46, can, size=11, fill=INK, anchor="middle"))
        b.append(rect(422, y + 12, 214, 50, fill="#FFFFFF", stroke=HAIR, rx=6, dash="4 3"))
        b.append(txt(529, y + 27, "挡不住", size=11, fill=GRAY, anchor="middle"))
        b.append(txt(529, y + 46, cannot, size=11, fill=INK, anchor="middle"))
    b.extend(banner(40, 288, 608, "三道闸降低风险，不保证隔离。", "官方安全说明：项目尚未接受安全审计。", fill=CREAM))
    b.append(note(40, 348, "三层依次是 guard → approval → sandbox · 据官方沙箱、审批与安全说明概括"))
    return write(
        out_dir, "fig-16-1-three-layers.svg", 362,
        "图 40：三道闸各挡什么、挡不住什么",
        "guard 策略把关挡得住的只有策略写到的模式；approval 人工审批挡不住人批错与无人应答；"
        "sandbox 受限执行挡不住获准访问的资源，旧内核还可能只部分强制。三层都降低风险，都不保证隔离。",
        b,
    )


# ---------------------------------------------------------------- 图 50
def fig_16_2(out_dir):
    b = []
    b.append(rect(40, 108, 176, 68, fill=BLUE, rx=8))
    b.append(txt(128, 132, "approval/request", size=12, fill="#FFFFFF", weight=600, anchor="middle", mono=True))
    b.append(txt(128, 152, "瀑布式分派", size=11, fill=ONB, anchor="middle"))
    outs = [
        ("allowed-once", "唯一放行", TEAL, "#FFFFFF"),
        ("rejected", "拒绝", PAPER, INK),
        ("cancelled", "撤回", PAPER, INK),
        ("unavailable", "无人应答 → 拒绝", PAPER, INK),
    ]
    for i, (name, desc, fill, fg) in enumerate(outs):
        y = 20 + i * 56
        b.append(rect(300, y, 336, 42, fill=fill, stroke=HAIR if fill != TEAL else None, rx=6))
        b.append(txt(318, y + 21, name, size=12, fill=fg, weight=600, mono=True))
        b.append(txt(620, y + 21, desc, size=11, fill=TEAL if fill == TEAL else GRAY, anchor="end"))
        b.append(path(f"M218,142 C258,142 262,{y + 21} 296,{y + 21}", stroke=GRAY, sw=1.2, marker="ar"))
    b.extend(banner(40, 258, 596, "四个结果里只有 allowed-once 放行；没有应答复方，不等于放行。"))
    b.append(note(40, 300, "ApprovalOutcome 是闭合枚举，失败时拒绝（fail closed）· 简化自 官方审批说明"))
    return write(
        out_dir, "fig-16-2-approval-outcomes.svg", 314,
        "图 41：审批的四个结果，只有一个放行",
        "approval/request 经瀑布式分派后只有四种结果：allowed-once（授权所问的那一个操作）、rejected、"
        "cancelled、unavailable。只有 allowed-once 放行；缺失或抛错的应答方归为 unavailable，同样拒绝。",
        b,
    )


# ---------------------------------------------------------------- 图 51
def fig_16_3(out_dir):
    rows = [
        ("read-only", "只放行 /dev/null 之类的接收器", B1),
        ("workspace-write", "加工作区根与后端承诺的临时区", B2),
        ("danger-full-access", "绕开隔离，不走 ctx.sandbox", BLUE),
    ]
    b = []
    y0, step, rh = 34, 60, 44
    for i, (name, desc, fill) in enumerate(rows):
        y = y0 + i * step
        b.append(rect(40, y, 300, rh, fill=fill, rx=6))
        fg = "#FFFFFF" if fill == BLUE else INK
        b.append(txt(58, y + 22, name, size=12, fill=fg, weight=600, mono=True))
        b.append(txt(356, y + 22, desc, size=11, fill=GRAY))
    b.append(vtxt(628, 130, "只管文件系统效果 · 网络与进程可见性不在范围内"))
    b.append(rect(40, 222, 150, 26, fill=TEAL, rx=13))
    b.append(txt(115, 235, "full", size=11, fill="#FFFFFF", anchor="middle", mono=True))
    b.append(rect(200, 222, 150, 26, fill=B3, rx=13))
    b.append(txt(275, 235, "partial", size=11, fill=INK, anchor="middle", mono=True))
    b.append(txt(366, 235, "旧内核 ABI 或后端子集 → 只部分强制", size=11, fill=GRAY))
    b.extend(banner(40, 264, 608, "沙箱管文件效果；网络与进程可见性不在它范围。"))
    b.append(note(40, 306, "SandboxMode 三档 · 只有前两档会送进 ctx.sandbox · 简化自 官方沙箱说明"))
    return write(
        out_dir, "fig-16-3-sandbox-modes.svg", 318,
        "图 42：沙箱的三档模式与两种强制完整性",
        "SandboxMode 三档：read-only 只放行 /dev/null 之类接收器，workspace-write 再加工作区根与临时区，"
        "danger-full-access 绕开隔离、不走 ctx.sandbox。强制完整性分 full 与 partial。它只管文件效果。",
        b,
    )


# ---------------------------------------------------------------- 图 52
def fig_17_1(out_dir):
    rows = [
        ("100% 行覆盖率", "装配路径从未被测"),
        ("快照通过", "回放确定性 ≠ 行为正确"),
        ("HTTP 200", "页面白屏"),
        ("非零退出码", "子程序正常完成"),
    ]
    b = []
    b.append(txt(56, 24, "看起来对的信号", size=11, fill=GRAY))
    b.append(txt(368, 24, "真实状态", size=11, fill=GRAY))
    y0, step, rh = 42, 54, 42
    for i, (sig, real) in enumerate(rows):
        y = y0 + i * step
        b.append(rect(40, y, 290, rh, fill=B1, stroke=HAIR, rx=6))
        b.append(txt(58, y + 21, sig, size=12, fill=INK, weight=600, mono=(i != 1)))
        b.append(path(f"M334,{y + 21} H364", stroke=GRAY, sw=1.2, marker="ar"))
        b.append(rect(368, y, 280, rh, fill="#FFFFFF", stroke=HAIR, rx=6, dash="4 3"))
        b.append(txt(386, y + 21, real, size=12, fill=INK))
    b.extend(banner(40, 268, 608, "四个看起来对的信号，指向四个错的状态。"))
    b.append(note(40, 310, "四起事故的信号与真实状态对照 · 整理自 官方复盘 0001–0004"))
    return write(
        out_dir, "fig-17-1-four-signals.svg", 322,
        "图 43：四起事故的信号都指向错的状态",
        "四起事故的信号分别是 100% 行覆盖率、快照通过、HTTP 200 和非零退出码。它们的真实状态分别是装配路径"
        "从未被测、回放确定性不等于行为正确、页面白屏、子程序正常完成。看起来对的信号，指向错的状态。",
        b,
    )


# ---------------------------------------------------------------- 图 53
def fig_17_2(out_dir):
    b = []
    b.append(rect(40, 30, 608, 64, fill=B1, stroke=HAIR, rx=8))
    b.append(txt(58, 50, "测试路径", size=12, fill=INK, weight=600))
    b.append(txt(58, 72, "直接构造插件 → 手动提供 inject → 绿信号", size=11, fill=GRAY))
    b.append(rect(560, 42, 74, 26, fill=TEAL, rx=13))
    b.append(txt(597, 55, "通过", size=11, fill="#FFFFFF", anchor="middle"))

    b.append(rect(40, 150, 608, 64, fill=PAPER, stroke=LINE, rx=8))
    b.append(txt(58, 170, "生产路径", size=12, fill=INK, weight=600))
    b.append(txt(58, 192, "Loader 加载导出 → 真实解析服务 → 崩溃", size=11, fill=GRAY))
    b.append(rect(560, 162, 74, 26, fill=GRAY, rx=13))
    b.append(txt(597, 175, "失败", size=11, fill="#FFFFFF", anchor="middle"))

    b.append(path("M420,96 V148", stroke=GRAY, sw=1.2, dash="4 3", marker="ar"))
    b.append(txt(432, 122, "信号测的是上面这条路", size=10.5, fill=GRAY))
    b.extend(banner(40, 236, 608, "检验：这个信号是在哪条路径上产生的？那条路径和生产路径是同一条吗？"))
    b.append(note(40, 286, "整理自 官方复盘 0001"))
    return write(
        out_dir, "fig-17-2-signal-path.svg", 298,
        "图 44：信号产生的路径与生产路径不是同一条",
        "上一条是测试路径：直接构造插件、手动提供 inject，信号为通过。下一条是生产路径：Loader 加载导出、"
        "真实解析服务，结果是崩溃。信号测的是上面这条路，所以它不能证明下面这条也对。",
        b,
    )


# ---------------------------------------------------------------- 图 54
def fig_17_3(out_dir):
    b = []
    b.append(rect(40, 60, 250, 74, fill="#FFFFFF", stroke=HAIR, rx=8, dash="4 3"))
    b.append(txt(165, 84, "agent 自述", size=12.5, fill=INK, weight=600, anchor="middle"))
    b.append(txt(165, 106, "事后报告，反推意图", size=11, fill=GRAY, anchor="middle"))

    b.append(rect(390, 60, 250, 74, fill=BLUE, rx=8))
    b.append(txt(515, 84, "持久化事件日志", size=12.5, fill="#FFFFFF", weight=600, anchor="middle"))
    b.append(txt(515, 106, "session-3eb796c2", size=11, fill=ONB, anchor="middle", mono=True))

    b.append(rect(288, 74, 104, 46, fill=CREAM, stroke=HAIR, rx=6))
    b.append(txt(340, 97, "复盘", size=12.5, fill=INK, weight=600, anchor="middle"))

    b.append(path("M290,97 H288", stroke=LINE, sw=1.2))
    b.append(path("M340,60 C340,40 200,40 180,56", stroke=GRAY, sw=1.2, dash="4 3"))
    b.append(txt(206, 34, "不可作为事实", size=10.5, fill=GRAY))
    b.append(path("M428,97 H392", stroke=BLUE, sw=1.6, marker="arb"))
    b.append(txt(410, 82, "依据", size=10.5, fill=BLUE, anchor="middle"))

    b.extend(banner(40, 168, 608, "复盘以事件日志为依据，不以事后报告反推意图。"))
    b.append(note(40, 210, "证据来源 session-3eb796c2-5159-4686-affe-df8719f6f987 · 整理自 官方复盘 0003"))
    return write(
        out_dir, "fig-17-3-log-is-evidence.svg", 224,
        "图 45：复盘依据事件日志，不依据事后报告",
        "左边是 agent 自述，属事后报告、反推意图，不能作为事实。右边是持久化事件日志 session-3eb796c2，"
        "带序号、可回放，是复盘的依据。复盘只走日志这一条路。",
        b,
    )


FIGURES = [
    ("15-1", fig_15_1),
    ("15-2", fig_15_2),
    ("15-3", fig_15_3),
    ("16-1", fig_16_1),
    ("16-2", fig_16_2),
    ("16-3", fig_16_3),
    ("17-1", fig_17_1),
    ("17-2", fig_17_2),
    ("17-3", fig_17_3),
]
