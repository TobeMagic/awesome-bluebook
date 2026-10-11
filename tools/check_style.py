#!/usr/bin/env python3
"""蓝宝书 · 章节风格自检（质量门 2/3/6 的机械化部分）

用法:
    python tools/check_style.py books/deepseek-harness/fragments/02-numbers-in-harness.md

检查项:
    门2 风格   禁用词、伪第一人称体感
    门3 细节   句长、图注格式、图后解读
    门6 自包含  不许出现 docs/·research/·commit 这类读者感知不到的外部引用；
                图注仍须带 〔…〕 标注（〔本书〕即可，不必再指向外部）

退出码 0 = 通过；1 = 有问题需要修。
"""

import os
import re
import sys
from pathlib import Path

# 门2：禁用词（对照 STYLE.md §五）
BANNED = [
    "综上所述", "值得注意的是", "接下来我们将", "进行操作", "实现功能",
    "可以说", "一定程度上", "强大的", "革命性的", "在当今这个",
    "首先", "其次", "最后", "然而", "尽管",
]

# 门2：伪体感（无实测却装作有体验）
PSEUDO_EXPERIENCE = [
    r"我用(了|下来|着)", r"我(觉得|感觉|发现)",
    r"我的体验", r"亲测", r"实测下来",
]

# 门3：图注格式
# 图号是全书流水号 1…63（STYLE.md §五.2），同时兼容早期「章-序」写法（图 4-1）
FIG_CAPTION = re.compile(r"\*\*图\s*\d+(?:[-–]\d+)?[：:]")

# 去 AI 味（STYLE.md §二.2.10）：元话语导航词
META_NAV = [
    r"这里要注意", r"这里要(给|提)", r"这里要给个",
    r"接着往下", r"接下来我们先", r"上面提到", r"回到(开头|前面|上一)",
    r"总结(一下|来说)", r"总的来看", r"一句话概括", r"值得一提",
    r"简单来说", r"换句话说", r"顺便(说|提)一句", r"先看(看|一下)?这里",
    r"一起(来)?看看", r"让我们", r"不妨先",
]

# 每千字上限（STYLE.md §二.2.10 的六signal）
AI_LIMITS = {"bold": 2.0, "dash": 2.0, "question": 1.5, "meta": 3.0}

# 受控中文（STYLE.md §二.2.11，源自 ASD-STE100 的 80% 版）
# 规则 1：一动作一动词。同一组里出现两个以上 = 同义轮换。
# 写新书时按领域往这里补。
SYNONYM_GROUPS = [
    ["检查", "校验", "确认", "核查", "验证"],
    ["使用", "利用", "采用", "运用", "借助"],
    ["配置", "设置", "设定", "配制"],
    ["加载", "载入", "装载", "读入"],
    ["启动", "开启", "起动", "运行"],
    ["注册", "登记", "挂载", "登记注册"],
    ["替换", "替代", "取代", "置换"],
    ["依赖", "依靠", "仰赖"],
]

# 规则 8：模糊情态。有证据就写死，没证据写「未验证」。
HEDGES = [
    r"可能[会是要]", r"也许", r"大概", r"或许", r"似乎", r"应该[会能]",
    r"差不多", r"基本上", r"一般来说", r"通常情况下", r"在大多数情况下",
    r"有可能", r"不排除", r"某种意义上",
]

# 规则 6：无实义填充词
FILLERS = [
    r"进行(了)?[^，。]{0,6}(操作|处理|设置|配置|检查)",
    r"实现(了)?[^，。]{0,6}功能",
    r"强大的", r"无缝", r"全面地?", r"赋能", r"灵活地?",
    r"简单地说", r"值得一提", r"不容忽视", r"至关重要",
]

MAX_PARAGRAPH_SENTENCES = 6  # ASD-STE100 硬上限

# 门6：自包含 —— 书内不许出现读者感知不到的外部引用
#
# 立场：这本书是唯一交付物，读者手上没有源码树。
# 指向 `docs/`、`research/`、commit hash 这类东西的引用，读者没有感知，一律不放。
# 所有该交代的（数字口径、判别范围、例外）必须在正文当场讲完。
#
# 反过来，被讲解对象自身的结构允许提 —— `packages/core/tools/package.json`、
# `cordis.patch.yml`、`src/index.ts` 是内容的一部分，不是「这里请看别处」。
OUTSIDE_REF_PATTERNS = [
    r"(?:docs|research|apps)/[A-Za-z0-9_./-]+",   # 指向仓库/研究稿的路径
    r"dsh-src",                                     # 本地源码克隆目录
    r"\b639ed015",                                  # 溯源 commit（只在成书扉页留一处）
    r"\b(?:AGENTS|TERMS|PROJECT|README)\.md\b",     # 本系列的项目文件
    r"〔本节来源〕",                                 # 旧的来源清单标记
]
OUTSIDE_REF_RE = re.compile("|".join(OUTSIDE_REF_PATTERNS))

MAX_SENTENCE = 25  # 字


def strip_code(text: str) -> str:
    """去掉围栏代码块与行内代码，避免误判。"""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]+`", "", text)
    return text


def sentences(text: str):
    """按中文句末标点切句。跳过表格行与列表项。

    长度按「中文字符数 + 英文单词数」计，避免中英混排时误判超长。
    """
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        # 跳过表格行、列表项、标题、引用
        if stripped[0] in "|-#>":
            continue
        for p in re.split(r"[。！？；]+", stripped):
            p = re.sub(r"[*_`]", "", p)  # 去掉 markdown 强调标记再计长
            cjk = len(re.findall(r"[\u4e00-\u9fff]", p))
            words = len(re.findall(r"[A-Za-z][A-Za-z0-9._-]*", p))
            if cjk + words >= 2:
                yield p, cjk + words


def check(path: Path):
    raw = path.read_text(encoding="utf-8")
    body = strip_code(raw)
    issues = []
    warns = []

    chars = len(re.sub(r"\s+", "", body))  # 去空白后的正文字数，多处密度要用

    # --- 门2 禁用词 ---
    for w in BANNED:
        n = body.count(w)
        if n:
            issues.append(f"禁用词「{w}」出现 {n} 次")

    # --- 门2 伪体感 ---
    for pat in PSEUDO_EXPERIENCE:
        m = re.findall(pat, body)
        if m:
            issues.append(f"疑似伪第一人称体感：{pat}（{len(m)} 处）")

    # --- 门3 句长 ---
    all_s = list(sentences(body))
    long_s = [s for s, n in all_s if n > MAX_SENTENCE]
    if long_s:
        ratio = len(long_s) / max(1, len(all_s))
        msg = f"超长句 {len(long_s)} 处（>{MAX_SENTENCE} 字），占比 {ratio:.0%}"
        sample = " / ".join(s[:34] + "…" for s in long_s[:3])
        if ratio > 0.2:
            issues.append(f"{msg}：{sample}")
        else:
            warns.append(f"{msg}：{sample}")

    # --- 门3 图注 ---
    # 附录是查阅型材料（术语表、图索引、代码对照），本来就不放图，豁免
    is_index = "figure-index" in os.path.basename(path) or \
        os.path.basename(path).startswith("appendix")
    figs = FIG_CAPTION.findall(raw)
    if is_index:
        pass
    elif not figs:
        issues.append("未找到图注（应为 **图 N：…** 格式）")
    else:
        # 每张图后必须有解读段落
        blocks = FIG_CAPTION.split(raw)[1:]
        for i, b in enumerate(blocks, 1):
            after = re.sub(r"[*\s]", "", b[:200])
            if len(after) < 20:
                warns.append(f"图 {i} 后的解读文字偏少，确认是否有「这张图说明什么」")

    # --- 门6 自包含：不许有读者感知不到的外部引用 ---
    for i, line in enumerate(raw.split("\n"), 1):
        if line.strip().startswith("<!--"):
            break  # FIGURES 注释块是给画图脚本看的，不算正文
        hits = OUTSIDE_REF_RE.findall(line)
        if hits:
            issues.append(f"第 {i} 行有外部引用（应改写成书内自足的说法）：{hits[0]}")

    # --- 门6 图注必须带标注（〔本书〕也算，不必再指向外部）---
    for line in raw.split("\n"):
        if re.search(r"\*\*图\s*\d+(?:[-–]\d+)?[：:]", line) or re.match(r"图\s*\d+(?:[-–]\d+)?[：:]", line.strip()):
            if "〔" not in line:
                warns.append(f"图注行缺少来源标注：{line.strip()[:44]}")

    # --- 门2 文本表达 DNA ---
    paras = [p.strip() for p in body.split("\n") if p.strip()]
    body_paras = [p for p in paras if p[0] not in "|-#>" and not p.startswith("**图")]

    # 段落长度：>6 句（ASD-STE100 硬上限）
    fat = [(len(re.findall(r"[。！？]", p)), p[:30]) for p in body_paras
           if len(re.findall(r"[。！？]", p)) > MAX_PARAGRAPH_SENTENCES]
    if fat:
        warns.append(
            f"过长的段 {len(fat)} 处（>{MAX_PARAGRAPH_SENTENCES} 句）："
            + " / ".join(f"{n}句「{t}…」" for n, t in fat[:3])
        )

    # --- 受控中文（STYLE.md §二.2.11）---
    # 引文不改：官方原文引用必须逐字保留，不参与风格检查
    # （ASD-STE100 同样规定 quoted text 保持原样）
    own_text = "\n".join(ln for ln in body.split("\n") if not ln.strip().startswith(">"))

    # 规则 1：一动作一动词，抓同义轮换
    rotations = []
    for group in SYNONYM_GROUPS:
        hit = [w for w in group if w in own_text]
        if len(hit) >= 2:
            rotations.append("/".join(hit))
    if rotations:
        warns.append(
            "同义轮换（一动作一动词，ASD-STE100）："
            + "、".join(rotations) + " —— 同一动作请统一成一个动词，写进 TERMS.md"
        )

    # 规则 8：模糊情态
    hedge_hits = []
    for pat in HEDGES:
        m = re.findall(pat, own_text)
        if m:
            hedge_hits.extend(m if isinstance(m[0], str) else ["".join(x) for x in m])
    if hedge_hits:
        warns.append(
            f"模糊情态 {len(hedge_hits)} 处：{'/'.join(hedge_hits[:5])}"
            " —— 有证据就写死，没证据写「未验证」"
        )

    # 规则 6：无实义填充词
    filler_hits = []
    for pat in FILLERS:
        m = re.findall(pat, own_text)
        if m:
            filler_hits.extend(m if isinstance(m[0], str) else ["".join(x) for x in m])
    if filler_hits:
        warns.append(f"无实义填充词 {len(filler_hits)} 处：{'/'.join(filler_hits[:5])}")

    ste_line = (
        f"受控中文：同义轮换 {len(rotations)} 组 / 模糊情态 {len(hedge_hits)} / 填充词 {len(filler_hits)}"
    )

    # 电报体检测：整篇平均句数过低 = 通篇蹦字
    # 列表项天然一句一段，不计入
    prose = [p for p in body_paras if not re.match(r"^([-\d]+[.、)]|\d+\.)", p)]
    all_n = [len(re.findall(r"[。！？]", p)) for p in prose]
    if all_n and sum(all_n) / len(all_n) < 1.6:
        warns.append(f"疑似电报体：平均每段 {sum(all_n)/len(all_n):.1f} 句，建议 ≥1.6，别通篇蹦字（列表项已排除）")

    # 「你」过多告警：默认直接讲解，'你' 只留给检验/递工具类句子
    n_you = len(re.findall(r"(?<![你a-zA-Z])你(?!们)", body))
    if n_you > 4:
        warns.append(f"「你」出现 {n_you} 次，偏多（建议 ≤4）：直接讲解，主语交给事物本身")

    # 白话连接词
    n_conn = sum(body.count(w) for w in ["说白了", "其实", "你看", "简单说", "这里要注意", "别搞混", "也就是", "你可以"])
    if n_conn < 1:
        warns.append("缺少白话连接词（说白了 / 其实 / 简单说 / 别搞混 …）")

    # 极短句：有，但别过量
    punch = [p for p in body_paras
             if p.endswith(("。", "！")) and len(re.sub(r"[\s*_`]", "", p)) <= 12]
    if len(punch) < 1:
        warns.append("缺少极短句落锤，建议 ≥1 处")
    elif len(punch) / max(1, len(body_paras)) > 0.4:
        warns.append(f"极短句偏多（{len(punch)}/{len(body_paras)} 段），容易变成电报体")

    # --- 去 AI 味（STYLE.md §二.2.10）---
    # 统计对象：正文 prose（排除表格行、列表项、标题、图注、来源块）
    src_zone = re.split(r"〔本节来源〕", body)[0]
    prose_lines = [
        ln.strip()
        for ln in src_zone.split("\n")
        if ln.strip()
        and ln.strip()[0] not in "|-#>"
        and not ln.strip().startswith("**图")
    ]

    n_bold = sum(len(re.findall(r"\*\*[^*\n]+\*\*", ln)) for ln in prose_lines)
    n_dash = sum(ln.count("——") for ln in prose_lines)
    n_ques = sum(ln.count("？") for ln in prose_lines)
    n_meta = sum(len(re.findall(p, ln)) for ln in prose_lines for p in META_NAV)
    per_k = 1000.0 / max(1, chars)

    for key, label, cnt in [
        ("bold", "加粗", n_bold),
        ("dash", "破折号", n_dash),
        ("question", "自问自答", n_ques),
        ("meta", "元话语导航", n_meta),
    ]:
        density = cnt * per_k
        limit = AI_LIMITS[key]
        if density > limit:
            level = "必修" if density > limit * 1.6 else "提示"
            msg = f"{label}密度 {density:.1f}/千字（{cnt} 处），上限 {limit:.1f} —— AI 味信号，见 STYLE §2.10"
            (issues if level == "必修" else warns).append(msg)

    # 段落节奏：句数标准差过小 = 每段都切得一样齐
    if len(prose) >= 6:
        counts = [len(re.findall(r"[。！？]", p)) for p in prose]
        mean = sum(counts) / len(counts)
        var = sum((c - mean) ** 2 for c in counts) / len(counts)
        sd = var ** 0.5
        if sd < 0.8:
            warns.append(
                f"段落节奏过匀：句数标准差 {sd:.2f}（建议 ≥0.8），每段都像切好的片。"
                "穿插单句段与长段试试"
            )

    # 节间模板：连续 3 节都用「数量型」开场 = 流水线产出
    # （这里只抓数字开场。非数字开场千变万化，不构成同构，不告警。）
    sections = []
    cur_lines: list[str] = []
    for ln in src_zone.split("\n"):
        s = ln.strip()
        if s.startswith("## "):
            if cur_lines:
                sections.append(cur_lines)
            cur_lines = []
        elif s:
            cur_lines.append(s)
    if cur_lines:
        sections.append(cur_lines)

    def numeric_open(lines: list[str]) -> bool:
        first = re.sub(r"[*`_ ]", "", lines[0])
        opening = re.split(r"[。！？]", first)[0]
        return bool(re.search(r"\d", opening))

    opens = [numeric_open(s) for s in sections]
    run = 0
    start = 0
    for i, flag in enumerate(opens):
        if flag:
            run = run + 1 if run else 1
            if run == 1:
                start = i
            if run >= 3:
                warns.append(
                    f"连续 {run} 节都用数量开场（自第 {start + 1} 节起），像同一个模子倒出来的。"
                    "换几种开法：有的先抛结论，有的先讲用途，有的用一个例子带进去"
                )
                break
        else:
            run = 0

    ai_line = (
        f"去 AI 味：加粗 {n_bold} / 破折号 {n_dash} / 自问自答 {n_ques} / 元话语 {n_meta}"
    )

    # --- 门3 图占比（粗估）---
    n_fig = len(figs)
    n_mermaid = raw.count("```mermaid")
    total_fig = n_fig + n_mermaid
    chars = len(re.sub(r"\s+", "", body))
    density = chars / max(1, total_fig)
    if total_fig == 0 and not is_index:
        issues.append("没有图，违反「图优先」")
    elif total_fig and density > 1200:
        warns.append(f"图文比偏高：每图约 {density:.0f} 字，建议 ≤800–1200 字/图")

    # --- 输出 ---
    name = path.name
    print(f"\n=== {name} ===")
    print(f"字符数 {chars} · 图 {total_fig} 张（图注 {n_fig} / mermaid {n_mermaid}） · 图文比 {density:.0f} 字/图")
    print(f"  {ai_line}")
    print(f"  {ste_line}")
    if not issues and not warns:
        print("通过：无问题")
        return 0
    for w in warns:
        print(f"  [提示] {w}")
    for i in issues:
        print(f"  [必修] {i}")
    return 1 if issues else 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    code = 0
    for p in sys.argv[1:]:
        path = Path(p)
        if not path.exists():
            print(f"找不到文件：{p}")
            code = 1
            continue
        code |= check(path)
    sys.exit(code)


if __name__ == "__main__":
    main()
