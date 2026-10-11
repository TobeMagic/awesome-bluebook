#!/usr/bin/env python3
"""蓝宝书系列 · 起一本新书的骨架

用法:
    python tools/init_book.py deepseek-harness
    python tools/init_book.py my-topic --title "书名" --subtitle "副标题"
    python tools/init_book.py my-topic --dir books/my-topic

生成后先填 PROJECT.md，再按 TEMPLATE.md 走流程。
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

VERSION_STAMP = "v" + datetime.now().strftime("%y%m%d")
TODAY = datetime.now().strftime("%Y-%m-%d")

MIT = """MIT License

Copyright (c) {year} Blue Book series contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

PROJECT = """# {title} — 项目计划

> **目标**：{goal_placeholder}
> **规格**：中文为主 · 约 __ 节 + __ 附录 · 目标 __ 页 · 图占比 ≥40% · PDF / EPUB / HTML
> **状态**：立项
> **当前版本**：{ver}
> **溯源基准**：commit `________` · {today} · `上游版本______`
> **License**：MIT

---

## 一、差异化定位（不可动摇）

- [ ] 花叔橙皮书是否写过同主题？写的是什么角度？我们怎么错位？
- [ ] 一句话定位：
- [ ] 读者读完能「照着造」什么？

## 二、章节大纲

| Part | 节 | 标题 | 核心内容 | 信息来源 |
|---|---|---|---|---|
| 1 | §01 | | | |
| 2 | §02 | | | |

## 三、核心图清单（本书必须有哪几张图）

| 图 | 说明什么结论 | 原创/改绘 |
|---|---|---|
| 图 1-1 | | |

## 四、调研资料索引

| # | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | | | 待补 |

## 五、待办

- [ ] 阶段 1 调研（6–10 维度）
- [ ] 阶段 2 大纲定稿
- [ ] 阶段 3 图先行写作
- [ ] 阶段 4 过 6 道质量门
- [ ] 阶段 5 构建 + 拆独立仓库
"""

README_ZH = """**中文** | [English](README.md)

<p align="center">
  <!-- 封面：cover/cover-zh.png -->
</p>

# {title}

> 蓝宝书系列 · {ver} · 溯源：commit `{commit}` · {today}

{subtitle}

## 下载

| 格式 | 文件 | 大小 |
|---|---|---|
| PDF | | |
| EPUB | | |
| HTML | | |

## 这本书回答什么

- 
- 
- 

## 内容结构

| Part | 节 | 主题 |
|---|---|---|
| | | |

## 谁该读

- 

## 这套方法能迁到哪

- 

## 不粉饰：本书的边界

- 本书基于 commit `{commit}` 的快照，上游仍在开发者预览期，会有破坏性变更
- 

## 蓝宝书系列

- **{title}** ← 你在这里

## License

[MIT](LICENSE)
"""

README_EN = """**English** | [中文](README_zh.md)

# {title}

> Blue Book series · {ver} · Source: commit `{commit}` · {today}

{subtitle}

## Download

| Format | File | Size |
|---|---|---|
| PDF | | |
| EPUB | | |
| HTML | | |

## What this book answers

- 
- 

## Structure

| Part | Sections | Topics |
|---|---|---|
| | | |

## Who should read

- 

## Where this transfers

- 

## Honest limits

- Snapshot at commit `{commit}`; upstream is in developer preview and will break compatibility
- 

## Blue Book series

- **{title}** ← you are here

## License

[MIT](LICENSE)
"""

TERMS = """# 术语表 · {title}

写作时对照，同一事物全书只能有一个名字。
包名、ctx 键、事件名必须与官方源码**逐字一致**。

| 中文 | 原文 | 首次出现 | 说明 |
|---|---|---|---|
| | | § | |
"""


def build(args):
    slug = args.slug
    title = args.title or slug.replace("-", " ").title()
    subtitle = args.subtitle or "（一句话副标题：读完能做什么）"
    base = Path(args.dir) if args.dir else Path("books") / slug

    dirs = ["research", "fragments", "output", "cover", "screenshots", "assets", "tools"]
    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)
        keep = base / d / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")

    commit = args.commit or "________"

    files = {
        base / "PROJECT.md": PROJECT.format(
            title=title,
            goal_placeholder="（目标读者 + 解决什么问题，一句话）",
            ver=VERSION_STAMP,
            today=TODAY,
        ),
        base / "README.md": README_EN.format(
            title=title, ver=VERSION_STAMP, commit=commit, today=TODAY, subtitle=subtitle
        ),
        base / "README_zh.md": README_ZH.format(
            title=title, ver=VERSION_STAMP, commit=commit, today=TODAY, subtitle=subtitle
        ),
        base / "TERMS.md": TERMS.format(title=title),
        base / "LICENSE": MIT.format(year=datetime.now().year),
    }

    for path, content in files.items():
        if path.exists() and not args.force:
            print(f"  跳过（已存在）: {path}")
            continue
        path.write_text(content, encoding="utf-8")
        print(f"  生成: {path}")

    print(f"\n完成：{base}")
    print(f"版本戳：{VERSION_STAMP}")
    print(f"\n下一步：")
    print(f"  1. 填 {base}/PROJECT.md 的差异化定位与章节大纲")
    print(f"  2. 按 TEMPLATE.md 走阶段 1 调研")
    print(f"  3. 每张图先定草图，再动笔写文字")


def main():
    ap = argparse.ArgumentParser(description="蓝宝书系列 · 起一本新书的骨架")
    ap.add_argument("slug", help="主题 slug，如 deepseek-harness")
    ap.add_argument("--title", help="书名")
    ap.add_argument("--subtitle", help="副标题")
    ap.add_argument("--dir", help="输出目录，默认 books/<slug>")
    ap.add_argument("--commit", help="溯源 commit")
    ap.add_argument("--force", action="store_true", help="覆盖已存在文件")
    args = ap.parse_args()
    try:
        build(args)
    except Exception as e:
        print(f"失败：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
