#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝宝书 SVG 共用工具（色板 + 元素助手）

所有图生成模块（gen_figures.py / figs_*.py）都从这里 import。
约束见 CONVENTIONS.md §5：
    - viewBox "0 0 680 H"，width="100%"，role="img"，必带 <title> / <desc>
    - 配色只用两套：蓝 #1B3A6B（主）+ 青 #0F6E56（强调），灰阶做底
    - 无渐变、无阴影、无发光；正文字号 >= 11px
    - 箭头用 <defs> 里的 marker，不在元素上硬画三角
"""
from __future__ import annotations

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

W = 680      # 画布宽（固定）
MAXW = 680   # 溢出校验用的右边界


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
        f'  <marker id="art" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="6.5" '
        f'markerHeight="6.5" orient="auto"><path d="M0,1 L9,5 L0,9 Z" fill="{TEAL}"/></marker>\n'
        "</defs>\n"
    )


def rect(x, y, w, h, fill="none", stroke=None, rx=6, dash=None, sw=1.0):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        s += f' stroke-dasharray="{dash}"'
    return s + "/>"


def txt(x, y, s, size=11, fill=INK, weight=400, anchor="start", mono=False, rot=None):
    fam = f' font-family="{MONO}"' if mono else ""
    r = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="central"'
        f'{fam}{r}>{esc(s)}</text>'
    )


def vtxt(x, y, s, size=11, fill=GRAY, anchor="middle"):
    """竖排文字（整体旋转 -90 度）。x,y 是旋转中心。"""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" transform="rotate(-90 {x} {y})">{esc(s)}</text>'
    )


def path(d, stroke=GRAY, sw=1.4, marker=None, dash=None):
    s = f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        s += f' stroke-dasharray="{dash}"'
    if marker:
        s += f' marker-end="url(#{marker})"'
    return s + "/>"


def line(x1, y1, x2, y2, stroke=HAIR, sw=1.0, dash=None, marker=None):
    return path(f"M{x1},{y1} L{x2},{y2}", stroke=stroke, sw=sw, marker=marker, dash=dash)


def circle(cx, cy, r, fill="none", stroke=None, sw=1.0):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    return s + "/>"


def diamond(cx, cy, w, h, fill=PAPER, stroke=BLUE, sw=1.2):
    return (
        f'<path d="M{cx},{cy - h / 2} L{cx + w / 2},{cy} L{cx},{cy + h / 2} '
        f'L{cx - w / 2},{cy} Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def note(x, y, s, size=11, fill=GRAY):
    return txt(x, y, s, size=size, fill=fill)


def tag(x, y, s, fill=BLUE, fg="#FFFFFF", size=11, pad=10, h=22, rx=11, w=None):
    """圆角标签胶囊。w 为 None 时按字数粗估。"""
    if w is None:
        w = pad * 2 + int(size * 0.62 * (len_estimate(s)))
    return (
        rect(x, y, w, h, fill=fill, rx=rx)
        + txt(x + w / 2, y + h / 2, s, size=size, fill=fg, anchor="middle")
    )


def len_estimate(s: str) -> float:
    """中文按 1 字宽、英文按 0.55 字宽估算。"""
    n = 0.0
    for ch in s:
        n += 1.0 if ord(ch) > 0x2E7F else 0.55
    return n


def banner(x, y, w, t1, t2=None, fill=CREAM, stroke=HAIR, fg1=INK, fg2=TEAL,
           size1=11.5, size2=11.5, pad=18, h=None):
    """浅底结论条。"""
    if h is None:
        h = 44 if t2 else 30
    b = [rect(x, y, w, h, fill=fill, stroke=stroke, rx=6)]
    if t2:
        b.append(txt(x + pad, y + h / 2 - 10, t1, size=size1, fill=fg1))
        b.append(txt(x + pad, y + h / 2 + 10, t2, size=size2, fill=fg2))
    else:
        b.append(txt(x + pad, y + h / 2, t1, size=size1, fill=fg1))
    return b


def write(out_dir: str, name: str, h: int, title: str, desc: str, body: list) -> str:
    os.makedirs(out_dir, exist_ok=True)
    fp = os.path.join(out_dir, name)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(head(h, title, desc))
        for el in body:
            f.write(el + "\n")
        f.write("</svg>\n")
    return fp
