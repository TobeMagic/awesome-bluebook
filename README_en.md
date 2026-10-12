**English** | [中文](README.md)

<p align="center">
  <img src="books/deepseek-harness/assets/social-preview.png" width="88%" alt="Blue Book 01 · DeepSeek Harness: Everything is a plugin — how an agent harness grows" />
</p>

# Blue Book 01 · DeepSeek Harness

> Book one of the **Blue Book** series, a Chinese book series on design reading · finished draft
> Preface + 17 chapters + 3 appendices · ~34k characters · **42 hand-drawn diagrams**

A free book about **why a system is built the way it is**.

**It won't teach you how to install things. It teaches you how they work — and how to build one yourself.**

DeepSeek Harness is taken apart and rebuilt in plain language, using one running story — a repair crew fixing a lamp — and then questioned layer by layer: why is it cut this way, what does that cost, and which parts can you carry into your own project.

---

## 📖 Read & Download

| Format | File | Notes |
|------|------|------|
| **HTML (single file, recommended)** | [deepseek-harness-bluebook.html](books/deepseek-harness/deepseek-harness-bluebook.html) | Cover, 6 part frontispieces, TOC, all chapters; 42 diagrams inlined; works offline |
| **PDF** | [deepseek-harness-bluebook.pdf](books/deepseek-harness/deepseek-harness-bluebook.pdf) | 111 pages, WYSIWYG, good for printing and sharing |
| **EPUB** | [deepseek-harness-bluebook.epub](books/deepseek-harness/deepseek-harness-bluebook.epub) | 21 chapters with a navigation TOC; diagrams rasterized; works in Kindle / Apple Books |
| Source | [fragments/](books/deepseek-harness/fragments) | Chapter sources in Markdown; rebuild with `tools/build_book.py` |

> 💡 Grab the HTML for a quick look; grab the EPUB for reading on a phone or e-reader.

## What this book covers

***Everything is a plugin: how an agent harness grows.***

DeepSeek Harness is an open-source agent harness: the model does the thinking, the harness lets the model reach the real world. Its most counter-intuitive property — **the innermost layer can be removed in one piece without changing a line elsewhere**. Even the agent loop itself is a plugin.

The book moves through six parts — *in the door → one look around → take the kernel apart → walk it once → hit the edges → bring it home*. It starts with coordinates (how this harness compares with Claude Code and Codex CLI), then a map (the six layers), then unpacks each trade-off, and closes with checks you can run yourself.

| Part | Sections | Theme |
|------|------|------|
| **Preface** | §00 | The innermost layer can be pulled out in one piece |
| **1 · In the door** | §01–§04 | Why a model alone can't do the job · harness vs framework vs scaffolding · three harnesses, three sales pitches · four old problems |
| **2 · One look around** | §05–§06 | Six layers · three-tier config overlay and four shapes |
| **3 · Take the kernel apart** | §07–§11 | Empty kernel · lookup by name · event-only communication · load/unload symmetry · single source of truth |
| **4 · Walk it once** | §12–§13 | A full turn of dialogue · five stages of one tool call |
| **5 · Hit the edges** | §14–§15 | Three gates · real incidents (including a CVSS 9.4 sandbox escape) |
| **6 · Bring it home** | §16–§17 | Five checks · what it is betting on, and what that costs |

## Every section has two layers

The same thing is said twice, without repeating or skipping steps:

1. **Plain version** — the design told through the repair-crew story, with no terminology at all
2. **Professional version** — the same content with the real terms: formal names, core mechanisms, boundaries, costs
3. **Mapping table** — the plain-term ↔ technical-term pairs introduced in that section
4. **Where readers get it wrong** — the wrong reading first, then the right one
5. **Where to carry it** — one or two checks you can run on your own project

**You don't need to read code.** No code, no package names, no statistics in the main text — anything a reader cannot perceive stays out.

## How it differs from the Orange Books

The Orange Books by [Huashu](https://github.com/alchaincyf) are excellent. Blue Book doesn't repeat them; it covers the other half.

| | Orange Book | Blue Book |
|---|---|---|
| Question answered | What happens after I install it | Why it was designed this way |
| Material | Hands-on testing | Public sources and documentation |
| Medium | Prose + screenshots | **Diagram-driven** — figures are the skeleton, not decoration |
| Direction of depth | Vertical: master the product | Horizontal: abstract a general pattern |
| Shelf life | Short (follows releases) | Long (architectural patterns age slowly) |

An Orange Book leaves you able to *use* it. A Blue Book leaves you able to *build* it.

## Repo layout

```
deepseek-harness-bluebook/
├── README.md / README_en.md       this file (Chinese first)
├── STYLE.md                       writing rules (two-layer method, self-contained, macro-first)
├── CONVENTIONS.md                 figure rules, terminology, palette
├── PIPELINE.md                    production pipeline + quality gates
├── TEMPLATE.md                    checklist for starting a new book
├── tools/
│   ├── build_book.py              assemble the HTML book
│   ├── build_epub.py              export EPUB
│   ├── build_figures.py           builds all 42 SVG figures
│   ├── renumber_figures.py        renumbers figures (running numbers, not section-bound)
│   ├── preview.py                 single-section preview
│   └── check_style.py             style quality gate
└── books/deepseek-harness/
    ├── deepseek-harness-bluebook.html / .pdf / .epub
    ├── OUTLINE.md  WRITING-GUIDE.md
    ├── fragments/                 chapter sources (Markdown)
    ├── figures/                   the 42 SVG figures
    └── assets/                    cover, part frontispieces, social preview
```

Rebuild:

```bash
python tools/build_book.py     # HTML
python tools/build_epub.py     # EPUB
# PDF: open the HTML in a browser and print to PDF, or use headless Chrome --print-to-pdf
```

## Three principles underneath

1. **The book is the only deliverable** — nothing a reader can't perceive enters the text: citation lists, commits, package names, statistical caveats. Caveats are settled on the spot; details sink into the appendices.
2. **Figures are the skeleton** — prose serves the figures. Every figure carries a conclusion-style caption and a paragraph of explanation.
3. **Portable means understood** — every section ends in "where to carry this". An abstraction that can't be reused in a second domain is just a restatement.

## About Blue Book

Blue Book is a Chinese technical book series on **design reading** — *one book per repo, one system per book*. Every title follows the same rules: two-layer explanation, diagram-driven, self-contained, no code detail.

## License

[MIT](LICENSE) — use, adapt and distribute freely, commercially included. Attribution is not required, but welcome.

Author: **计算机魔术师 (The Computer Magician)**
