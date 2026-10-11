# 蓝宝书 · DeepSeek Harness 执笔指南（v3.1 全书重写用）

> 这份文件是写每一节之前必须读完的东西。写完一节，拿末尾的自检清单过一遍。

---

## 一、这本书是什么

讲 DeepSeek Harness（DSH）这套 agent 外壳的**设计理念**，不是源码导读。
读者不写代码。目标：合上书，读者能带走「下次自己设计时该怎么切这一刀」。

判据：**把一段里的包名全删掉，还有没有东西剩下。** 有，是设计；没了，是流水账。

## 二、双层解释法（每节固定骨架，STYLE.md §十一）

```
N.1 小白版    用师傅队伍的故事讲完这节的设计，一个术语都不许出现
N.2 专业版    同一回事上术语：正式名字、核心机制（分条）、适用边界、代价
N.3 对照表    本节新说法的「小白说法 ↔ 专业术语」表（小章可砍）
N.4 易错点    2–4 处，每处先给错的理解再给对的
N.5 能搬去哪  一到两个读者能自己动手的自查动作
```

参考样章：`fragments/07-kernel-is-empty.md`（全书唯一已达标的节，照它的语感写）。

- 小白版一个术语都不许出现；术语在 N.2 才准登场。
- 专业版必须给出小白版给不了的东西，不是把故事换个词重讲。
- 官方引文（`>` 引用）只放专业版。

## 三、师傅队伍：全书固定类比（不许换说法）

| 技术词 | 全书统一的说法 |
|---|---|
| 模型（model） | 师傅的脑子（只会想，不会动手） |
| 外壳（harness） | 一整套人马 |
| 工具（读/写文件、跑命令） | 拧螺丝的 |
| 会话记录（session log） | 记笔记的 |
| 权限与沙箱 | 把门的 |
| agent 循环 | 领班的（看情况、决定、动手、看结果、再决定） |
| 装配清单（assembly manifest） | 排班表（今天雇了谁） |
| 插件（plugin） | 临时工 |
| 内核（kernel） | 公司最里面那一层 / 总部 |
| 消费方直连实现 | 直接点名找那个小张 |
| 改动半径 | 换掉他要动几个人 |
| 事件总线 / 发布订阅 | 公告栏（谁都能贴，谁都能看，不私下喊话） |
| 配置三层覆盖 | 公司规矩、部门规矩、工位上贴的纸条，小的压大的 |
| 四种 preset 形态 | 四套编制（满编 / 带徒弟 / 轻装 / 招新） |
| 接缝（有第二个实现的位子） | 备了替补的位子 |
| 会话 fork / resume | 笔记复印一份，从那一页接着写 |
| 子代理 | 领班叫来的外援小队 |
| 上下文压缩 | 把厚笔记誊成一页纸 |

新类比可以造，但必须：① 生活里人人都见过；② 一个词能说完；③ 登记进本表。

## 四、文风红线（机器会查）

- 每节 1,400–2,200 中文字，图 2–4 张
- 加粗 ≤2 处/千字（图注行的 `**图 N：…**` 也算）
- 破折号「——」≤2 处/千字
- 「你」全节 ≤4 次，最好 0
- 禁用词：综上所述、值得注意的是、首先/其次/最后、强大的、革命性、赋能、
  众所周知、不得不说、简而言之
- 段落 2–6 句，长短段交错；不许连续三节同一套开场
- 包名、文件路径、代码、统计数字（N 个包、N 行）一律不许进正文，要去附录 C
- 每节落点必须回答「为什么这么设计」和「这条能搬去哪」，不许收在陈述上

## 五、图的规矩

- 图号是全书流水号（图 1、图 2……），**节内从 1 起编即可**，成书时脚本统一重排
- 图片文件名是唯一权威源。写法：
  ```
  ![图 1：一句话说图](../figures/fig-XX-Y-name.svg)

  **图 1：一句结论，不是主题**〔本书〕
  ```
  图片行和图注行之间空一行；图注写结论不写主题；末尾 `〔本书〕` 不许丢。
- 图后必须有一段解读，把图里的东西落回这节的论点。
- **不许新画 SVG 文件**（图由工具链统一生成）。本节约不到合适的旧图，
  在文末 `<!-- FIG-REQUEST: 一句话描述需要的图 -->` 里登记，由总装阶段补。

## 六、现有图怎么挑（按旧节号归组）

图文件名里的旧节号对照（fragments-v2 时代的归属）：

| 旧归属 | 图文件 |
|---|---|
| 背景 §0 | fig-0-1-one-call-vs-agent（一次调用 vs 能干活的）、fig-0-2-harness-in-between（外壳站在模型和世界之间）、fig-0-3-four-problems（四道难题↔四条应对）、fig-0-4-what-changes（会变的 vs 不该动的） |
| 主张·拼装 | fig-1-1-loop-dependents、fig-2-1-group-code-share、fig-2-2-code-vs-dependence、fig-2-3-depth-layers |
| 六层/装配 | fig-3-1-six-layers、fig-3-2-config-overlay、fig-3-3-host-entry、fig-3-4-core-four、fig-3-5-capability-hands、fig-3-7-load-order、fig-10-3-base-vs-modes |
| 按名查找 | fig-4-1-key-lookup、fig-4-2-swap-backend |
| 事件 | fig-5-1-inject-derived-order、fig-5-3-two-graphs |
| 可撤回 | fig-6-1-three-switches、fig-7-1-load-unload-symmetry、fig-7-2-ghost-state、fig-7-3-fiber-states |
| 单一事实/日志 | fig-14-1-log-is-truth、fig-14-2-derivation-cost、fig-14-3-log-broadcast-persistence、fig-8-2-delegate-or-veto、fig-8-3-decision-owner |
| 走一遍 | fig-12-1-turn-skeleton、fig-12-2-turn-sequence、fig-12-3-three-decisions、fig-13-1-five-stages、fig-13-2-who-can-abort、fig-13-3-trace-lands |
| 接缝 | fig-15-1-four-roles、fig-15-2-seam-fanout、fig-15-3-seam-second-impl、fig-9-1-three-roles、fig-9-3-replace-not-merge |
| 三道闸 | fig-16-1-three-layers、fig-16-2-approval-outcomes、fig-16-3-sandbox-modes |
| 事故 | fig-17-1-four-signals、fig-17-2-signal-path、fig-17-3-log-is-evidence |
| 判据/收 | fig-18-1-five-checks、fig-18-2-decision-tree、fig-18-3-score-ladder、fig-19-1-two-axes、fig-19-3-mapping、fig-20-1-migration-order |
| §07 专用 | fig-07-a-seven-needs、fig-07-b-empty-center、fig-07-c-swap-radius（不许挪去别节） |

挑图原则：图的结论要跟这节论点一致；图里有包名/统计数字的，尽量别用，
非用不可时在 FIG-REQUEST 里登记重画。

## 七、旧稿在哪（改写素材，不是照抄）

旧版全文在 `fragments-v2/`（v2 结构 16 节 + 4 附录）。v3.1 的对应：

| v3.1 | 素材来源（v2） |
|---|---|
| §00 序章 | 新写 |
| §01 模型明明会写代码 | 01-beyond-one-call.md |
| §02 harness 是什么 | 新写（用 01 的 1.2/1.4 + 行业通说） |
| §03 三家三种做法 | 新写（调研素材见下） |
| §04 难在哪 | 02-four-hard-problems.md |
| §05 六层 | 08-six-layer-panorama.md |
| §06 怎么装上去 | 09-overlay-and-profiles.md + 12-seams.md |
| §07 内核是空的 | **已完成，别动** |
| §08 只写名字 | 04-claim-lookup-by-name.md |
| §09 公告栏 | 05-claim-events-only.md |
| §10 能拆下来 | 06-claim-reversible.md |
| §11 只存一份 | 07-claim-single-truth.md（注意不是 07-kernel-is-empty） |
| §12 一句问话 | 10-dialog-lifecycle.md |
| §13 五道工序 | 11-tool-pipeline.md |
| §14 三道闸 | 13-three-gates.md |
| §15 出过什么事 | 14-four-lessons.md |
| §16 不看代码怎么知道 | 15-five-criteria.md |
| §17 在赌什么 | 16-spatiotemporal.md |

## 八、§03 三家对比的调研素材（新写那节用）

- 行业公式：`Agent = 模型 + 外壳`；调侃「如果你不是模型，你就是外壳」；
  核心不变式「模型提议，外壳授权、执行、记录、恢复」。
- 外壳 vs 框架：框架给材料自己盖房（谦让）；外壳是有主见的成品房，
  不问你「要不要权限校验」，直接「不校验门都别想进」。
- 三家已收敛到同一形态：记忆/指令文件、分层配置、MCP、沙箱+审批、
  headless、企业托管。比的不再是功能有无。
- 八维度对比：开源（MIT / 闭源 / 开源）、架构（插件内核 / 垂直集成 / 垂直集成）、
  哲学（一切皆插件 / 开箱即用 / Protocol-first）、模型（任意 OpenAI 兼容端点 /
  仅 Anthropic / 仅 OpenAI）、会话日志（仅追加明文本地可 fork/replay / 托管 / 托管）、
  运行时自扩展（热加载 / 不支持 / 不支持）、默认沙箱（read-only 故障安全 /
  权限提示 / 权限提示）。
- 落点：Claude Code 卖成品，Codex CLI 卖接口，DSH 卖插座。
  必答题三家都做（循环、上下文、工具接入、会话持久、权限沙箱）；
  选答题只有 DSH 这么选（内核空置、模型插件化、日志可重放）。
  选答题不是更好，是把复杂度从实现方转移给了使用者。

## 九、交稿自检（写完一节逐项过）

- [ ] 五层骨架齐（N.1–N.5），顺序对
- [ ] 小白版全文零术语（逐句查：模型/插件/内核/循环/装配/事件……出现一个算失败）
- [ ] 专业版有正式名字 + 分条机制 + 边界/代价
- [ ] 对照表只收新词
- [ ] 易错点每处都是「先错后对」
- [ ] 图 2–4 张，图注写结论、带〔本书〕、图后有解读
- [ ] 无包名/路径/代码/统计数字
- [ ] 字数 1,400–2,200，「你」≤4，破折号 ≤2/千字，加粗 ≤2/千字
- [ ] 文末 `<!-- FIGURES 图号 文件名 -->` 清单 + 需要的 FIG-REQUEST
