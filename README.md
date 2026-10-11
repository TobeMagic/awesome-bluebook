**English** | [中文](README_zh.md)

<p align="center">
  <img src="books/deepseek-harness/assets/cover.jpg" width="46%" alt="Blue Book 01 · DeepSeek Harness cover illustration: a plugin tree with a slender trunk and detachable blocks on its branches" />
</p>

# Blue Book · 蓝宝书

> A Chinese book series on **design reading** — why systems are built the way they are
> Book 01 · *DeepSeek Harness* — finished draft: preface + 17 chapters + 3 appendices · ~34k characters · **42 SVG diagrams**

A series of free, diagram-driven books. Each book takes one system, maps its structure with flowcharts, and distills the parts you can carry somewhere else.

**It won't teach you how to install things. It teaches you how they work — and how to build one yourself.**

---

## 📖 Read & Download

| Format | File | Notes |
|------|------|------|
| **HTML (single file, recommended)** | [books/deepseek-harness/deepseek-harness-bluebook.html](books/deepseek-harness/deepseek-harness-bluebook.html) | Cover, 6 part frontispieces, TOC, all chapters; 42 diagrams inlined; works offline |
| PDF | Open the HTML in a browser → "Print to PDF" | WYSIWYG |

## What Book 01 covers

***Everything is a plugin: how an agent harness grows.***

DeepSeek Harness is an open-source agent harness: the model does the thinking, the harness lets the model reach the real world. Its most counter-intuitive property — **the innermost layer can be removed in one piece without changing a line elsewhere**. Even the agent loop itself is a plugin.

Six parts: *Getting In → A First Look → The Kernel → A Full Pass → Hitting the Limits → Takeaways*. It opens with coordinates (a three-way comparison of DSH vs Claude Code vs Codex CLI), gives the map (six layers), then walks the trade-offs layer by layer, and closes with checkable criteria.

| Part | Chapters | Topic |
|------|------|------|
| **Preface** | §00 | The innermost layer can be removed in one piece |
| **1 · Getting In** | §01–§04 | Why models alone can't work · harness vs framework vs scaffold · three vendors, three takes · four hard problems |
| **2 · A First Look** | §05–§06 | Six layers · three-tier config overlay and four presets |
| **3 · The Kernel** | §07–§11 | Empty kernel · lookup by name · events, not calls · symmetric load/unload · single source of truth |
| **4 · A Full Pass** | §12–§13 | Life of a turn · five stages of a tool call |
| **5 · Limits** | §14–§15 | Three gates · five real incidents (incl. the CVSS 9.4 sandbox escape) |
| **6 · Takeaways** | §16–§17 | Five criteria · the bet and its price |

## How it differs from the Orange Books

The Orange Books (by [Huashu](https://github.com/alchaincyf)) are excellent. Blue Book doesn't repeat them; it covers the other half.

| | Orange Book | Blue Book |
|---|---|---|
| Answers | What happens after I install it | Why it was designed this way |
| Sources | Hands-on testing | Source structure + first-party docs + papers |
| Medium | Text + screenshots | **Diagram-driven** — figures are the skeleton |
| Depth | Vertical: master the product | Horizontal: extract a reusable pattern |
| Shelf life | Short (follows versions) | Long (architecture patterns age slowly) |

## Who it's for

- **Non-programmers**: every chapter opens with the "repair crew" story — technical terms only appear in the second layer
- **Engineers & architects**: every chapter lands on "why this cut" and "how to reuse this rule in your own project"
- **Agent builders**: §03 gives an 8-dimension comparison of three harnesses; §16 gives five acceptance criteria that need no code reading

## Repository layout

```
bluebook/
├── STYLE.md / CONVENTIONS.md / PIPELINE.md / TEMPLATE.md   specs
├── tools/                          build, figure, style-check scripts
└── books/
    └── deepseek-harness/           01 · DeepSeek Harness (finished)
        ├── deepseek-harness-bluebook.html   ← the book
        ├── fragments/    chapter sources (Markdown)
        ├── figures/      42 SVG diagrams
        └── assets/       cover & frontispieces
```

## Three ground rules

1. **The book is the only deliverable** — nothing the reader can't perceive goes into the text: no reference lists, commits, package names, or counting methodology. Details sink into appendices
2. **Figures are the skeleton** — text serves the figures. Every figure carries a conclusion-style caption and a reading paragraph
3. **It transfers, or it doesn't count** — every chapter ends at "where to carry this". What you abstract must survive in a second domain, otherwise it's just retelling

## License

[MIT](LICENSE) — free to use, adapt, and redistribute, including commercially.
