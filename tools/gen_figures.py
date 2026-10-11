#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝宝书 SVG 图生成器

用法：
    python tools/gen_figures.py                 # 生成 deepseek-harness 的全部图
    python tools/gen_figures.py --book <主题>    # 生成指定书的图

产出：
    books/<主题>/figures/fig-N-N-<name>.svg

约束（CONVENTIONS.md §5）：
    - viewBox "0 0 680 H"，width="100%"，role="img"，必带 <title> / <desc>
    - 配色只用两套：蓝 #1B3A6B（主）+ 青 #0F6E56（强调），灰阶做底
    - 无渐变、无阴影、无发光；正文字号 >= 11px
    - 箭头用 <defs> 里的 marker，不在元素上硬画三角
"""
from __future__ import annotations

import argparse
import os

INK = "#2C2C2A"
GRAY = "#5F5E5A"
BLUE = "#1B3A6B"
CREAM = "#F5F0E8"
TEAL = "#0F6E56"
LINE = "#B4B2A9"
HAIR = "#D8D6CD"
PAPER = "#FBFAF7"

B1 = "#EDF2F9"   # 蓝 1（最浅）
B2 = "#D3DFF0"
B3 = "#A9C4E4"
B4 = "#85B7EB"
ONB = "#C9DBF1"  # 深蓝底上的浅字
T1 = "#5DCAA5"   # 青 1（浅）

FONT = "system-ui, -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

W = 680


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def head(h: int, title: str, desc: str) -> str:
    return (
        f'<svg viewBox="0 0 {W} {h}" width="100%" role="img" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">\n'
        f'<title>{esc(title)}</title>\n'
        f'<desc>{esc(desc)}</desc>\n'
        "<defs>\n"
        f'  <marker id="ar" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="6.5" '
        f'markerHeight="6.5" orient="auto"><path d="M0,1 L9,5 L0,9 Z" fill="{GRAY}"/></marker>\n'
        f'  <marker id="arb" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="6.5" '
        f'markerHeight="6.5" orient="auto"><path d="M0,1 L9,5 L0,9 Z" fill="{BLUE}"/></marker>\n'
        "</defs>\n"
    )


def rect(x, y, w, h, fill="none", stroke=None, rx=6, dash=None, sw=1.0):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        s += f' stroke-dasharray="{dash}"'
    return s + "/>"


def txt(x, y, s, size=11, fill=INK, weight=400, anchor="start", mono=False):
    fam = f' font-family="{MONO}"' if mono else ""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="central"'
        f'{fam}>{esc(s)}</text>'
    )


def path(d, stroke=GRAY, sw=1.4, marker=None, dash=None):
    s = f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        s += f' stroke-dasharray="{dash}"'
    if marker:
        s += f' marker-end="url(#{marker})"'
    return s + "/>"


def note(x, y, s, size=11, fill=GRAY):
    return txt(x, y, s, size=size, fill=fill)


def write(out_dir: str, name: str, h: int, title: str, desc: str, body: list[str]) -> str:
    os.makedirs(out_dir, exist_ok=True)
    fp = os.path.join(out_dir, name)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(head(h, title, desc))
        for el in body:
            f.write(el + "\n")
        f.write("</svg>\n")
    return fp


# ---------------------------------------------------------------- 图 1
def fig_1_1(out_dir):
    b = []
    b.append(rect(140, 28, 150, 46, fill=B2, stroke=HAIR, rx=6))
    b.append(txt(215, 51, "base", size=13, fill=INK, weight=600, anchor="middle", mono=True))
    b.append(rect(390, 28, 150, 46, fill=B2, stroke=HAIR, rx=6))
    b.append(txt(465, 51, "sdk-minimal", size=13, fill=INK, weight=600, anchor="middle", mono=True))

    b.append(path("M215,74 C215,110 300,110 322,138", stroke=BLUE, sw=1.6, marker="arb"))
    b.append(path("M465,74 C465,110 380,110 358,138", stroke=BLUE, sw=1.6, marker="arb"))
    b.append(txt(340, 104, "运行时依赖", size=11, fill=BLUE, anchor="middle"))

    b.append(rect(250, 140, 180, 54, fill=BLUE, rx=8))
    b.append(txt(340, 160, "agent-loop", size=14, fill="#FFFFFF", weight=600, anchor="middle", mono=True))
    b.append(txt(340, 180, "唯一的具体循环插件", size=11, fill=ONB, anchor="middle"))

    b.append(rect(40, 140, 170, 54, fill="#FFFFFF", stroke=HAIR, rx=8, dash="4 3"))
    b.append(txt(125, 160, "46 个包", size=13, fill=INK, weight=600, anchor="middle"))
    b.append(txt(125, 180, "只在测试里引用", size=11, fill=GRAY, anchor="middle"))
    b.append(path("M212,167 H244", stroke=GRAY, sw=1.2, marker="ar", dash="3 3"))

    b.append(rect(470, 140, 170, 54, fill=PAPER, stroke=HAIR, rx=8))
    b.append(txt(555, 160, "267 个包", size=13, fill=INK, weight=600, anchor="middle"))
    b.append(txt(555, 180, "一次都没提过它", size=11, fill=GRAY, anchor="middle"))

    b.append(note(40, 228, "316 个包 = 3 个运行时依赖 + 46 个仅测试引用 + 267 个未提及；运行时那 3 个含测试工具包 agent-loop-testkit"))
    b.append(note(40, 248, "口径：316 个 package.json 的三类依赖字段"))
    return write(
        out_dir, "fig-1-1-loop-dependents.svg", 266,
        "图 5：谁在依赖 agent-loop",
        "316 个包里，运行时依赖 agent-loop 的只有 base 和 sdk-minimal 两个装配包，外加测试工具包 "
        "agent-loop-testkit。46 个包只在测试里引用它。267 个包一次都没提过它。",
        b,
    )


# ---------------------------------------------------------------- 图 2
def fig_2_1(out_dir):
    rows = [
        ("client", 31.7, BLUE),
        ("experimental", 8.3, B4),
        ("api", 6.1, B4),
        ("session", 5.1, B4),
        ("core", 5.1, TEAL),
        ("llm", 3.8, B4),
    ]
    b = []
    b.append(txt(40, 22, "分组", size=11, fill=GRAY))
    b.append(txt(150, 22, "代码行数占比", size=11, fill=GRAY))
    y0, rh, gap = 40, 22, 16
    scale = 380 / 31.7
    for i, (name, pct, fill) in enumerate(rows):
        y = y0 + i * (rh + gap)
        w = pct * scale
        b.append(txt(40, y + rh / 2, name, size=12.5, fill=INK, mono=True))
        b.append(rect(150, y, w, rh, fill=fill, rx=3))
        b.append(txt(150 + w + 10, y + rh / 2, f"{pct}%", size=11, fill=GRAY))
    b.append(f'<line x1="150" y1="34" x2="150" y2="282" stroke="{HAIR}" stroke-width="1"/>')
    # 反差标注：client 的条尾拉到 core 的条尾
    top = y0 + rh / 2
    core_y = y0 + 4 * (rh + gap) + rh / 2
    b.append(path(f"M{150 + 31.7 * scale},28 H644 V{core_y} H{150 + 5.1 * scale + 4}",
                  stroke=TEAL, sw=1.2, marker="ar", dash="4 3"))
    b.append(txt(644, 18, "六倍多", size=11, fill=TEAL, anchor="end"))
    b.append(note(40, 306, "深蓝 = 代码量最大的分组 · 青 = 名字叫 core 的那个 · 含测试，排除 node_modules 与 dist"))
    b.append(note(40, 326, "316 个包 / 944,704 行 /"))
    return write(
        out_dir, "fig-2-1-group-code-share.svg", 344,
        "图 6：各分组代码量占比",
        "横条按代码行数占比排序：client 31.7% 最大，experimental 8.3%、api 6.1%、session 5.1%、"
        "core 5.1%、llm 3.8%。青色虚线标出 client 与 core 的反差，前者是后者的六倍多。",
        b,
    )


# ---------------------------------------------------------------- 图 4
def fig_2_2(out_dir):
    left = [
        ("client", 31.7, "31.7%"),
        ("experimental", 8.3, "8.3%"),
        ("api", 6.1, "6.1%"),
        ("session", 5.1, "5.1%"),
        ("core", 5.1, "5.1%"),
        ("llm", 3.8, "3.8%"),
    ]
    right = [
        ("session", 101, BLUE),
        ("llm", 94, T1),
        ("agent", 76, T1),
        ("brand", 60, T1),
        ("tools", 55, T1),
        ("util-values", 47, T1),
    ]
    b = []
    b.append(txt(40, 24, "代码量占比", size=14, weight=500))
    b.append(txt(360, 24, "被依赖度（多少个包依赖它）", size=14, weight=500))

    y0, step, bh = 48, 34, 18
    scale_l = 130 / 31.7
    for i, (name, pct, label) in enumerate(left):
        y = y0 + i * step
        b.append(txt(40, y + bh / 2, name, size=12))
        b.append(rect(124, y, max(8, pct * scale_l), bh, fill=B4, rx=3))
        b.append(txt(258, y + bh / 2, label, size=12, fill=GRAY))

    b.append(f'<line x1="336" y1="40" x2="336" y2="244" stroke="{LINE}" '
             f'stroke-width="0.5" stroke-dasharray="3 3"/>')

    scale_r = 121 / 94
    for i, (name, n, fill) in enumerate(right):
        y = y0 + i * step
        b.append(txt(360, y + bh / 2, name, size=12))
        b.append(rect(444, y, max(8, n * scale_r), bh, fill=fill, rx=3))
        b.append(txt(578, y + bh / 2, str(n), size=12, fill=GRAY))

    b.append(note(40, 256, "两栏各按本栏最大值归一化 · 量纲不同，只看相对关系 · 316 个包 / 944,704 行 /"))
    return write(
        out_dir, "fig-2-2-code-vs-dependence.svg", 272,
        "图 7：代码量与被依赖度的反差",
        "左栏按代码量占比排序，client 占 31.7% 最高；右栏按被依赖度排序，session 被 101 个包依赖。"
        "两栏排序完全不同，说明代码量不等于重要性。",
        b,
    )


# ---------------------------------------------------------------- 图 5
def fig_2_3(out_dir):
    rows = [
        ("深度 14", "装配顶层", 1, "bundle/base · 94 行", BLUE),
        ("深度 12–13", "组合层", 20, "20 个包", "#4E74B4"),
        ("深度 4–11", "中间层", 144, "144 个包", B4),
        ("深度 1–3", "薄层", 54, "54 个包", B3),
        ("深度 0", "叶子", 98, "98 个包 · 谁都不依赖", TEAL),
    ]
    b = []
    b.append(txt(40, 20, "离根的距离", size=11, fill=GRAY))
    b.append(txt(200, 20, "条长 = 包数（最长的 144 个包）", size=11, fill=GRAY))
    y0, rh, gap = 38, 34, 12
    scale = 2.6
    for i, (depth, name, n, label, fill) in enumerate(rows):
        y = y0 + i * (rh + gap)
        b.append(txt(40, y + 17, depth, size=11, fill=GRAY, mono=True))
        b.append(txt(40, y + 30, name, size=11, fill=INK))
        w = max(8, n * scale)
        b.append(rect(200, y + 8, w, 18, fill=fill, rx=3))
        b.append(txt(200 + w + 10, y + 17, label, size=11, fill=INK))
    leaf_y = y0 + 4 * (rh + gap)
    b.append(path(f"M188,54 V{leaf_y + 17}", stroke=LINE, sw=1.2, marker="ar"))
    b.append(
        '<text x="176" y="170" font-size="11" fill="#5F5E5A" text-anchor="middle" '
        'transform="rotate(-90 176 170)">越往上越容易被替换</text>'
    )
    b.append(note(40, 268, "深度 = 从该包向上走到根要经过的层数 · 统计含 dependencies 与 peerDependencies"))
    return write(
        out_dir, "fig-2-3-depth-layers.svg", 286,
        "图 8：依赖深度分层",
        "五层按依赖深度排列：深度 14 的装配顶层只有 bundle/base 一个包、94 行；"
        "深度 12–13 的组合层 20 个包；深度 4–11 的中间层 144 个包；深度 1–3 的薄层 54 个包；"
        "深度 0 的叶子层 98 个包，它们不依赖任何内部包。",
        b,
    )


# ---------------------------------------------------------------- 图 6
def fig_3_1(out_dir):
    rows = [
        ("第1层", "装配层", "写排班表的：定这次装什么"),
        ("第2层", "宿主层", "门房：人在哪儿用，接待传话"),
        ("第3层", "内核层", "班组：一次任务绕不开的几件"),
        ("第4层", "能力层", "临时工：真正动手干活"),
        ("第5层", "边界层", "踩刹车的地方：哪些事不能做"),
        ("第6层", "支撑层", "杂物间：试验田与基建"),
    ]
    b = []
    y0, rh, step = 22, 46, 52
    for i, (badge, name, duty) in enumerate(rows):
        y = y0 + i * step
        b.append(rect(40, y, 608, rh, fill=PAPER, stroke=HAIR))
        b.append(rect(48, y + 11, 48, 24, fill=BLUE, rx=12))
        b.append(txt(72, y + 23, badge, size=11, fill="#FFFFFF", anchor="middle"))
        b.append(txt(112, y + 23, name, size=13, fill=INK, weight=600))
        b.append(txt(240, y + 23, duty, size=11.5, fill=GRAY))
    top, bot = y0 + 11, y0 + 5 * step + 35
    b.append(path(f"M28,{top} V{bot - 6}", stroke=BLUE, sw=1.2, marker="arb"))
    b.append(
        '<text x="14" y="175" font-size="11" fill="#5F5E5A" text-anchor="middle" '
        'transform="rotate(-90 14 175)">越靠上的层越容易整体换掉</text>'
    )
    b.append(note(40, 352, "箭头 = 覆盖方向，不是调用方向：越靠上的层定得越晚，换起来越省事 · 六层为本书归类，非官方"))
    return write(
        out_dir, "fig-3-1-six-layers.svg", 368,
        "图 9：DeepSeek Harness 的六层结构",
        "从上到下六层：装配层 14 包 3%、宿主层 87 包 40%、内核层 57 包 19%、能力层 74 包 18%、边界层 14 包 3%、支撑层 70 包 17%。"
        "左侧箭头表示上层决定下层装配什么。最上层最小，越往下越大。",
        b,
    )


# ---------------------------------------------------------------- 图 7
def fig_3_2(out_dir):
    stack = [
        ("1", "bundle", "官方预打包的零件", B1, INK, GRAY),
        ("2", "profile 补丁", "某个 profile 自己的修改", B2, INK, GRAY),
        ("3", "home 补丁", "用户机器上的全局修改", B3, INK, "#3A4A63"),
        ("4", "--patch", "本次启动临时塞进去的", BLUE, "#FFFFFF", ONB),
    ]
    b = []
    y0, ch, step = 18, 40, 66
    for i, (idx, name, desc, fill, fg, sub) in enumerate(stack):
        y = y0 + i * step
        b.append(rect(92, y, 380, ch, fill=fill, stroke=HAIR if fill != BLUE else None))
        b.append(f'<circle cx="64" cy="{y + 20}" r="13" fill="{CREAM}" stroke="{HAIR}"/>')
        b.append(txt(64, y + 20, idx, size=11, fill=GRAY, anchor="middle"))
        b.append(txt(108, y + 20, name, size=12.5, fill=fg, weight=600, mono=(i == 3)))
        b.append(txt(456, y + 20, desc, size=11, fill=sub, anchor="end"))
        if i < 3:
            b.append(path(f"M282,{y + 42} V{y + step - 2}", stroke=BLUE, sw=1.4, marker="arb"))
    last_y = y0 + 3 * step
    b.append(rect(492, last_y + 8, 76, 24, fill=TEAL, rx=12))
    b.append(txt(530, last_y + 20, "最终生效", size=11, fill="#FFFFFF", anchor="middle"))
    b.append(path("M472,236 H488", stroke=LINE, sw=1.2))
    b.append(note(92, 282, "箭头 = 覆盖方向：后者整体替换前者，不做合并 · 简化自 architecture.zh.md §Profile 与组合包"))
    return write(
        out_dir, "fig-3-2-config-overlay.svg", 296,
        "图 10：启动时配置的叠加顺序",
        "四层配置自上而下依次叠加：bundle（官方预打包）、profile 补丁、home 补丁（用户全局）、--patch（本次启动临时）。"
        "每下一层整体覆盖上一层，最后 --patch 生效，全程不做合并。",
        b,
    )


# ---------------------------------------------------------------- 图 8
def fig_3_3(out_dir):
    clients = ["网页", "桌面", "黑窗口", "别家程序"]
    b = []
    b.append(rect(240, 88, 180, 80, fill=BLUE, rx=8))
    b.append(txt(330, 118, "门房 · 宿主层", size=14, fill="#FFFFFF", weight=600, anchor="middle"))
    b.append(txt(330, 142, "接待传话，不拿主意", size=11, fill=ONB, anchor="middle"))

    b.append(rect(500, 88, 140, 80, fill=PAPER, stroke=LINE, rx=8))
    b.append(txt(570, 118, "班组 · 内核层", size=13, fill=INK, weight=600, anchor="middle"))
    b.append(txt(570, 142, "真正拿主意的地方", size=11, fill=GRAY, anchor="middle"))

    for i, c in enumerate(clients):
        cy = 52 + i * 50
        b.append(rect(40, cy - 18, 118, 36, fill=PAPER, stroke=LINE, rx=6))
        b.append(txt(99, cy, c, size=12, fill=INK, anchor="middle"))
        b.append(path(f"M158,{cy} C200,{cy} 202,127 238,127", stroke=GRAY, sw=1.4, marker="ar"))
    b.append(path("M420,127 H498", stroke=BLUE, sw=1.6, marker="arb"))
    b.append(note(40, 206, "四种来法都从这一个窗口进 · 窗口能加，班组不必跟着长"))
    return write(
        out_dir, "fig-3-3-host-entry.svg", 226,
        "图 11：宿主层是所有客户端的入口",
        "浏览器、桌面 App、CLI、编辑器四种客户端都连到宿主层（client / api / host / sdk，87 个包，约 40% 代码），"
        "宿主层再接到内核层（session / llm / core / context）。",
        b,
    )


# ---------------------------------------------------------------- 图 9
def fig_3_4(out_dir):
    left = [
        ("门脸（界面）", 190, BLUE),
        ("工具箱", 44, B4),
        ("翻译官", 40, B4),
        ("花名册", 36, B4),
        ("流水账", 32, B4),
    ]
    right = [
        ("流水账", 176, TEAL),
        ("翻译官", 150, T1),
        ("花名册", 118, T1),
        ("工具箱", 92, T1),
        ("门脸（界面）", 14, HAIR),
    ]
    b = []
    b.append(txt(40, 24, "按代码量排", size=13, fill=INK, weight=600))
    b.append(txt(360, 24, "按被依赖排", size=13, fill=INK, weight=600))

    y0, step, bh = 48, 40, 20
    for i, (name, w, fill) in enumerate(left):
        y = y0 + i * step
        b.append(txt(40, y + bh / 2, name, size=11.5, fill=INK))
        b.append(rect(150, y, w, bh, fill=fill, rx=3))
    for i, (name, w, fill) in enumerate(right):
        y = y0 + i * step
        b.append(txt(360, y + bh / 2, name, size=11.5, fill=INK))
        b.append(rect(470, y, w, bh, fill=fill, rx=3))
    b.append(txt(644, y0 + 4 * step + bh / 2, "排不进前列", size=11, fill=GRAY, anchor="end"))
    b.append(f'<line x1="350" y1="40" x2="350" y2="232" stroke="{LINE}" '
             f'stroke-width="0.5" stroke-dasharray="3 3"/>')

    b.append(path("M344,58 C400,96 424,160 462,206", stroke=TEAL, sw=1.2, marker="ar", dash="4 3"))
    b.append(txt(340, 258, "同一个「门脸」，换个排法就垫底", size=11.5, fill=TEAL, anchor="middle"))

    b.append(rect(40, 278, 608, 30, fill=CREAM, stroke=HAIR, rx=6))
    b.append(txt(58, 293, "代码量不等于重要性：按工程量排门脸最大，按被依赖排流水账最靠前。", size=11.5, fill=INK))
    b.append(note(40, 330, "条长只表相对多少，不标数字 · 被依赖 = 有多少东西离不开它"))
    return write(
        out_dir, "fig-3-4-core-four.svg", 350,
        "图 12：内核四件套的依赖关系",
        "agent 依赖 llm、tools 和 session；tools 也依赖 session。四个节点标注被依赖包数："
        "session 101、llm 94、agent 76、tools 55。session 位于最底部，被所有组件依赖。",
        b,
    )


# ---------------------------------------------------------------- 图 10
def fig_3_5(out_dir):
    hands = [
        ("shell", "跑命令"),
        ("fs", "读写文件"),
        ("mcp", "接外部工具"),
        ("skill", "加载技能"),
        ("subagent", "派小弟"),
    ]
    b = []
    b.append(rect(270, 18, 140, 42, fill=BLUE, rx=8))
    b.append(txt(340, 39, "agent 循环", size=13, fill="#FFFFFF", weight=600, anchor="middle"))
    b.append(path("M340,60 V102", stroke=BLUE, sw=1.4))
    b.append(path("M100,104 H580", stroke=LINE, sw=1.2))
    for i, (name, desc) in enumerate(hands):
        cx = 100 + i * 120
        x = cx - 52
        b.append(path(f"M{cx},106 V118", stroke=GRAY, sw=1.2, marker="ar"))
        b.append(rect(x, 120, 104, 50, fill=PAPER, stroke=LINE, rx=6))
        b.append(txt(cx, 139, name, size=12.5, fill=INK, weight=600, anchor="middle", mono=True))
        b.append(txt(cx, 157, desc, size=11, fill=GRAY, anchor="middle"))
    b.append(note(48, 194, "装哪个包，agent 就多哪只手 · 能力层共 19 个分组、74 个包，此处列出 5 个代表性分组"))
    return write(
        out_dir, "fig-3-5-capability-hands.svg", 214,
        "图 13：能力层是 agent 的手",
        "agent 循环下挂一排能力包：shell 跑命令、fs 读写文件、mcp 接外部工具、skill 加载技能、subagent 派小弟。"
        "装哪个包，agent 就多哪只手。",
        b,
    )


# ---------------------------------------------------------------- 图 11
def fig_3_7(out_dir):
    b = []
    b.append(rect(40, 24, 250, 104, fill=PAPER, stroke=HAIR, rx=6))
    b.append(txt(56, 46, "tools 的 package.json", size=12, fill=INK, weight=600))
    b.append(txt(56, 70, '"dependencies": {', size=11, fill=GRAY, mono=True))
    b.append(txt(56, 88, '"@deepseek-ai/dsh-session"', size=11, fill=BLUE, mono=True))
    b.append(txt(56, 106, ': "workspace:*" }', size=11, fill=GRAY, mono=True))

    b.append(path("M290,76 C322,76 330,50 362,50", stroke=BLUE, sw=1.4, marker="arb"))
    b.append(txt(324, 88, "Cordis 读清单", size=10.5, fill=GRAY, anchor="middle"))

    b.append(rect(364, 24, 276, 52, fill=B1, stroke=HAIR, rx=6))
    b.append(txt(380, 44, "session 还没就绪", size=12.5, fill=INK, weight=600))
    b.append(txt(380, 62, "先把 session 装好", size=11, fill=GRAY))

    b.append(path("M502,76 V94", stroke=BLUE, sw=1.4, marker="arb"))

    b.append(rect(364, 96, 276, 52, fill=BLUE, rx=6))
    b.append(txt(380, 116, "session 就绪了", size=12.5, fill="#FFFFFF", weight=600))
    b.append(txt(380, 134, "再装 tools", size=11, fill=ONB))

    b.append(txt(40, 168, "包与包的关系写在配置里，不写在代码里：加一个包知道该等谁，删一个包知道牵连谁", size=11, fill=TEAL))
    b.append(note(40, 188, "机制为 Cordis 依赖解析，§05 细讲 · 例取自 packages/core/tools/package.json"))
    return write(
        out_dir, "fig-3-7-load-order.svg", 206,
        "图 14：加载顺序由依赖声明推导",
        "tools 的 package.json 里声明依赖 session。Cordis 读到这张清单，发现 session 还没就绪就先装 session，"
        "就绪后再装 tools。加载顺序由依赖声明推导，不是手工排班表。",
        b,
    )


FIGURES = [
    ("1-1", fig_1_1),
    ("2-1", fig_2_1), ("2-2", fig_2_2), ("2-3", fig_2_3),
    ("3-1", fig_3_1), ("3-2", fig_3_2), ("3-3", fig_3_3), ("3-4", fig_3_4),
    ("3-5", fig_3_5), ("3-7", fig_3_7),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="deepseek-harness")
    ap.add_argument("--root", default="books")
    args = ap.parse_args()
    out_dir = os.path.join(args.root, args.book, "figures")
    for item in FIGURES:
        fn = item[1] if isinstance(item, tuple) else item
        fp = fn(out_dir)
        print("wrote", fp)


if __name__ == "__main__":
    main()
