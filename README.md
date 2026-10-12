**中文** | [English](README_en.md)

<p align="center">
  <img src="books/deepseek-harness/assets/social-preview.png" width="88%" alt="蓝宝书 01 · DeepSeek Harness：一切皆插件——一个 AI 外壳是怎么长起来的" />
</p>

# 蓝宝书 01 · DeepSeek Harness

> 中文技术丛书「蓝宝书」的第一本 · 已完稿
> 序章 + 17 节 + 3 附录 · 约 3.4 万字 · **42 张手绘图**

一本免费的设计解读书。**不教你怎么装，教你怎么看懂——以及怎么照着造。**

把 DeepSeek Harness 拆开，用「修灯的师傅队伍」这个故事讲完它的全部设计，然后一层层追问：为什么切成这样，代价是什么，哪些能搬到自己的项目里。

---

## 📖 阅读与下载

| 格式 | 文件 | 说明 |
|------|------|------|
| **HTML（单文件，推荐）** | [deepseek-harness-bluebook.html](books/deepseek-harness/deepseek-harness-bluebook.html) | 封面 + 6 部题图 + 目录 + 全部章节，42 张图全内联，双击即看，离线可用 |
| **PDF** | [deepseek-harness-bluebook.pdf](books/deepseek-harness/deepseek-harness-bluebook.pdf) | 111 页，版式即所见，适合打印与分享 |
| **EPUB** | [deepseek-harness-bluebook.epub](books/deepseek-harness/deepseek-harness-bluebook.epub) | 21 章带导航目录，图已转位图，Kindle / Apple Books / 微信读书可读 |
| 源稿 | [fragments/](books/deepseek-harness/fragments) | 各章节 Markdown，改完跑 `tools/build_book.py` 重新成书 |

> 💡 想快速看效果就下 HTML；想在手机或墨水屏上读就下 EPUB。

## 本书讲什么

**《一切皆插件：一个 agent harness 是怎么长出来的》**

DeepSeek Harness 是一个开源的 agent 外壳：模型负责想，它负责让模型够得着真实世界。它最反常识的一件事是——**最中间的那一层可以整块抽走，别处一行都不用改**。连 agent 循环本身都是插件。

全书按「进门 → 先看一眼 → 拆内核 → 走一遍 → 碰边界 → 收」六部推进：先给坐标（它与 Claude Code、Codex CLI 三家外壳的对比），再给地图（六层结构），然后一层层拆开讲取舍，最后给几条能自查的判据。

| 部分 | 章节 | 主题 |
|------|------|------|
| **序章** | §00 | 最中间的那一层，可以整块抽走 |
| **第 1 部 · 进门** | §01–§04 | 模型为什么干不成活 · harness 与框架/脚手架的分界 · 三家外壳三种卖法 · 四道老难题 |
| **第 2 部 · 先看一眼** | §05–§06 | 六层结构 · 三层配置覆盖与四种形态 |
| **第 3 部 · 拆内核** | §07–§11 | 内核空置 · 按名查找 · 事件通信 · 装拆对称 · 单一事实来源 |
| **第 4 部 · 走一遍** | §12–§13 | 一次对话的完整周期 · 一次工具调用的五道工序 |
| **第 5 部 · 碰边界** | §14–§15 | 三道闸 · 真实事故（含 CVSS 9.4 沙箱逃逸） |
| **第 6 部 · 收** | §16–§17 | 五条判据 · 它在赌什么、代价是什么 |

## 每节都是两层

同一件事讲两遍，不重复也不跳步：

1. **小白版** —— 用师傅修灯的故事把设计讲完，一个术语都不出现
2. **专业版** —— 同样的内容上术语：正式名字、核心机制、适用边界、代价
3. **对照表** —— 这一节新说法的「人话 ↔ 术语」对应
4. **最容易理解错的地方** —— 先给错的，再给对的
5. **这条能搬去哪** —— 一两个能对自己项目动手的自查

**不用会写代码。** 全书零代码、零包名、零统计口径——读者感知不到的东西不进正文。

## 它和橙皮书的区别

橙皮书（[花叔](https://github.com/alchaincyf)）已经做得很好，蓝宝书不重复它，而是补它没做的那一半。

| | 橙皮书 | 蓝宝书 |
|---|---|---|
| 回答什么 | 我装上之后会发生什么 | 它为什么被设计成这样 |
| 素材来源 | 亲手实测 | 公开资料与文档 |
| 载体 | 文字 + 截图 | **流程图驱动**，图是骨架不是配图 |
| 深度方向 | 竖向：用透这个产品 | 横向：抽象出通用范式 |
| 保质期 | 短（跟着版本走） | 长（架构范式不易过时） |

读完你能「上手用」的是橙皮书，读完你能「照着造」的是蓝宝书。

## 仓库结构

```
deepseek-harness-bluebook/
├── README.md / README_en.md       本文件（中文优先）
├── STYLE.md                       写作规范（双层解释法、自包含、宏观优先）
├── CONVENTIONS.md                 图规范、术语统一、配色
├── PIPELINE.md                    生产流水线 + 质量门
├── TEMPLATE.md                    开一本新书的 checklist
├── tools/
│   ├── build_book.py              装书（HTML 单文件）
│   ├── build_epub.py              导出 EPUB
│   ├── build_figures.py           42 张 SVG 的总装入口
│   ├── renumber_figures.py        图号重排（流水号，不绑节号）
│   ├── preview.py                 单节预览
│   └── check_style.py             风格质量门
└── books/deepseek-harness/
    ├── deepseek-harness-bluebook.html / .pdf / .epub
    ├── OUTLINE.md  WRITING-GUIDE.md
    ├── fragments/                 各章节源稿（Markdown）
    ├── figures/                   42 张 SVG 图
    └── assets/                    封面、部题图、社交预览图
```

重新出书：

```bash
python tools/build_book.py     # HTML
python tools/build_epub.py     # EPUB
# PDF：浏览器打开 HTML → 打印为 PDF，或用无头 Chrome --print-to-pdf
```

## 三条底层原则

1. **书是唯一交付物** —— 读者感知不到的东西不进正文：引用清单、commit、包名、统计口径。口径当场讲完，细节沉到附录
2. **图是主骨架** —— 文字服务于图。每张图必有结论式图注和一段解读
3. **可迁移才算懂** —— 每一节收在「这条能搬去哪」。抽象出来的东西必须能在第二个领域复用，否则只是复述

## 关于蓝宝书

蓝宝书是一套中文技术丛书，讲「设计解读」——**一本书一个仓库，一本讲透一个系统**。每本都按同一套规范写：双层解释法、图驱动、自包含、不写代码细节。

## License

[MIT](LICENSE) —— 自由使用、改编、分发，含商用。署名不必需，但欢迎。

作者：**计算机魔术师**
