# 中医（TCM）开源资源地图

> **检索时间**：2026-11-09 CST（初版 2026-10-23；10-30 二次；11-01 hf-mirror 补遗；11-04 论文与范式；11-09 复核社区提名模型 + 灵丹-V2 发布状态；**11-09 晚新增第 11 节缺口分析**）· **检索方式**：GitHub Search API + HuggingFace API（经 hf-mirror 镜像，含 tag 过滤）+ ModelScope 文件树核对 + arXiv API + Crossref + **Zenodo API** + 逐仓库 README 核对 + **数据集下载解包实测字段** + Awesome-TCM-LLM 交叉验证
> **覆盖**：Agent Skill / 大模型 / 应用工具 / 古籍教材 / 数据语料 / 综述专利 / 评测基准 / 论文范式 / **缺口与行业信息（监管、标准、真流队列）**
> **口径**：⭐ 与更新日期为检索当时快照；已剔除 funNLP、awesome-go 这类"泛中文大杂烩"噪音项
> **性质**：不是链接清单，是**带判断的选型地图** —— 每条都标了"值不值得用、什么场景用、有什么坑"
> **硬件基线**：按 **DGX Spark（GB10 / 128G 统一内存）** 为主要跑测机，兼容消费级显卡与笔记本（见 3.8）

---

## 目录

- [0. 怎么读这份文档](#0-怎么读这份文档)
- [1. 情报源：从哪开始](#1-情报源从哪开始)
- [2. Agent Skill（当前最热赛道）](#2-agent-skill当前最热赛道)
- [3. 大模型](#3-大模型)
- [4. 应用 / 系统 / 工具](#4-应用--系统--工具)
- [5. 古籍 / 教材 / 视频](#5-古籍--教材--视频)
- [6. 数据与知识库](#6-数据与知识库)
- [7. 综述 / 专利 / 行业动态](#7-综述--专利--行业动态)
- [8. 场景选型（决策路径）](#8-场景选型决策路径)
- [9. 避坑清单](#9-避坑清单)
- [10. 论文与范式（2026-11）](#10-论文与范式2026-11)
- [11. 还缺什么：资源与信息缺口](#11-还缺什么资源与信息缺口2026-11-09)
- [附录 A 检索方法](#附录-a-检索方法可复现)
- [附录 B 术语表](#附录-b-术语表)
- [附录 C 变更日志](#附录-c-变更日志)

---

## 0. 怎么读这份文档

### 0.1 分层标准

本文档用 S / A / B / C 标注**实用性**（不是学术水平，也不是 star 数）：

| 档位 | 定义 | 典型特征 |
|:--:|---|---|
| **S** | 可开箱即用，工程完整，边界诚实 | 有安全契约 / 许可明确 / 版本化 / 多平台分发 |
| **A** | 专业性强，但生态小或需二次加工 | 质量高于热度，往往 star 很少 |
| **B** | 可用，但场景窄、同质化或信息密度低 | 能用，但别当主力 |
| **C** | 参考价值 > 实用价值 | 面广而浅，或定位不是给你用的 |
| **⚠️** | 有坑 | fork 刷星、许可不明、争议内容、无权重 |

### 0.2 六个判断（结论先行）

1. **能真下载复现的中医权重约 20+ 个**（2026-11-01 补遗后；Awesome-TCM-LLM 在 2026-10 的统计是 16 个），其余 100+ 条目是论文模型、医院产品、碎片 LoRA。所以选型的真实问题不是"哪个模型最强"，而是"哪个模型你能跑起来并验证"。
2. **底座已经统一到 Qwen 系**。2026 年的新权重几乎全部站在 Qwen2.5 / Qwen3 / Qwen3.5 上；Ziya-LLaMA、Baichuan、ChatGLM 时代的自研底座基本停更。做新东西直接拿 Qwen3 + 领域 CPT，比用 2023 年的"首个中医大模型"划算得多。
3. **中医模型的真正分水岭是评测可信度，不是知识量**。所有模型都能背教材，差别在于敢不敢做患者分组切分、给 Oracle 上界、分初诊/复诊报口径。目前做到全套的只有 `man_medical` 一家，其余多数用同源数据自测，**分数不可跨表比较**。
4. **Skill 赛道已从"堆语料"进入"工程化"**。分层索引、渐进披露、`POLICY.md` 安全契约成为区分度；3.5M 字全量塞入的做法正在被 2.3k token 按需加载取代。
5. **名医 Skill 是一家之言，教材型 Skill 才是底座**。多派共存时必须有仲裁机制，否则模型会在互斥结论之间自由发挥。
6. **缺的不再是模型，是数据终点、评测框架和行业信息**（2026-11-09 补充，详见第 11 节）。能下载的权重已 20+ 个，但：脉象公开数据集**实测为零**；舌象只有齿痕/苔色这类属性标签，**没有一个带辨证证型**；所有真实病历都**没有疗效终点字段**，所以"超过医师"永远证明不了有效；评测有基准但**几乎没有能跑的框架**。另有监管口径（中医辨证 AI 未查到三类证）、现行国标（GB/T 16751 系列已换版，全文只能在线预览）这类**不在 GitHub 上的信息**，拿不到会让整个方案作废。

### 0.3 一页速览

| 用途 | 首选 | 一句话 |
|---|---|---|
| 总入口 | **[tyang816/Awesome-TCM-LLM](https://github.com/tyang816/Awesome-TCM-LLM)** | 模型/数据/论文/专利/新闻全覆盖，113 模型 186 数据集 |
| Agent Skill（经方） | **[jangviktor-web/nihaixia](https://github.com/jangviktor-web/nihaixia)** ⭐3898 | 生态最成熟，多平台分发 |
| Agent Skill（通识） | **[YuanZHAO321/TCM.Skill](https://github.com/YuanZHAO321/TCM.Skill)** ⭐163 | 教材通识 + 安全硬约束，工程质量最高 |
| 能跑的模型 | **[QLU-NLP/BianCang](https://github.com/QLU-NLP/BianCang)** ⭐86 / **[TCMAI-BJTU/Lingdan-V2](https://github.com/TCMAI-BJTU/Lingdan-V2)** | 论文+权重+许可最规整 |
| 古籍语料 | [xiaopangxia/TCM-Ancient-Books](https://github.com/xiaopangxia/TCM-Ancient-Books) ⭐1507 | 近 700 部古籍纯文本 |
| 多模态四诊 | [FreedomIntelligence/ShizhenGPT](https://github.com/FreedomIntelligence/ShizhenGPT) ⭐154 | 舌/脉/面，数据+权重全开。⚠️ **"四诊开源"不等于四样都有数据**：公开侧脉象数据集实测为零，见 11.1 |
| 评测基准 | [TCM-Ladder](https://github.com/orangeshushu/TCM-Ladder) / [LingLan](https://github.com/TCMAI-BJTU/LingLan) | 任务定义清楚，见 3.6 |
| **评测跑分框架** | [pariskang/Med-Bench-Arena](https://github.com/pariskang/Med-Bench-Arena) | 40+ 基准 × 任意后端，中医指标一等公民，见 11.3 |
| 症状→国际编码映射 | [TCM-SO v4.10](https://github.com/Pinellia7ternata/TCM-Symptom-Ontology-v4.10) | ICD-11 / SNOMED / HPO 三向映射，见 6.3 |

---

## 1. 情报源：从哪开始

### 1.1 入口清单

| 仓库 | ⭐ | 最近推送 | 说明 |
|---|---:|---|---|
| [tyang816/Awesome-TCM-LLM](https://github.com/tyang816/Awesome-TCM-LLM) | 127 | 2026-10-22 | **最强入口**。开源中医模型、数据集、论文、专利、行业新闻合集；README 按"你想做什么→先看哪个"组织，并附综述与专利条线 |
| [GanjinZero/awesome_Chinese_medical_NLP](https://github.com/GanjinZero/awesome_Chinese_medical_NLP) | 2654 | 2024-01 | 中文医学 NLP 公开资源：术语集 / 语料库 / 词向量 / 预训练 / 知识图谱 / NER / QA，含 CBLUE 挑战榜 |
| [gexiaoxin11/nihaixia-unified](https://github.com/gexiaoxin11/nihaixia-unified) | 19 | 2026-07 | 倪海厦数字遗产「总目录」，git submodule 整合 GitHub 上 10 个倪师项目（Skill / APP / 教材 / 命理 / 面相 / 知识库） |
| [AiHubCN/Awesome-Chinese-LLM](https://github.com/AiHubCN/Awesome-Chinese-LLM) | 22.8k | 2026-05 | 中文开源 LLM 总表，含垂直领域分支，可横向看中医模型的生态位 |

### 1.2 判断

- **只用 Awesome-TCM-LLM 一个入口就够了**：它是目前唯一同时维护"模型 + 数据 + 论文 + 专利 + 新闻"五条线、且逐条核过链接的清单。它自己都写明「真能下载复现的权重约 16 个」（2026-10 快照；11 月灵丹-V2 权重开放后已不止）——这个数字比任何宣传都可信。
- `awesome_Chinese_medical_NLP` 停在 2024-01，价值在**历史语料索引**（术语集、词向量、CBLUE），不是最新模型。
- `nihaixia-unified` 是 submodule 索引，适合一次性 clone 全家桶，但**别指望它帮你筛质量**。

---

## 2. Agent Skill（当前最热赛道）

> **本节结论**：真正值得装的只有 4 个（`nihaixia` / `TCM.Skill` / `nihaisha-nishi-tcm` / `nihaisha-skill`）。其余 8 个是流派补充或素材库，star 数在这里几乎不代表质量。

### 2.1 核心 Skill（分层评价）

| 仓库 | ⭐ | 更新 | 档 | 内容要点 | 我的判断 |
|---|---:|---|:--:|---|---|
| [jangviktor-web/nihaixia](https://github.com/jangviktor-web/nihaixia) | **3898** | 2026-10-28 | **S** | 倪海厦视角中医 Agent Skill v2.3.1，MulanPSL-2.0。蒸馏《伤寒论》129 条、《金匮要略》23 篇、《黄帝内经》72 篇、《神农本草经》374 种（上137/中110/下127）、针灸篇；1257 例结构化医案 + 243 例叙事医案、2452 页讲义、约 3.5M 字；六经辨证 + 八纲辨证，8 个诊断公式 + 快速诊断流程图；附天纪（紫微斗数、易经、八字、风水） | 唯一做到"多平台分发（Claude Code / Codex / 腾讯 IMA / SkillHub）+ 版本化 + 免责声明"的，开箱即用度最高。**代价是 3.5M 字，触发后吃大量上下文**，长会话要留意 |
| [YuanZHAO321/TCM.Skill](https://github.com/YuanZHAO321/TCM.Skill) | 163 | 2026-07-07 | **S** | **家庭中医参谋** v3.0（终版）：16 部著作逐字通读整编，三层知识（6 部规划教材 → 5 部经典 → 3 部温病 + 2 部医家专著）；`SKILL.md` 只放流程与索引，事实全在 `references/`（50 文件）**渐进披露**；内嵌 42 部原书全文可"现场翻书"；安全表为**硬约束**（十八反十九畏 / 妊娠禁忌分级 / 101 味毒性药剂量上限 / 马兜铃酸）；建议分 A（可自行）/ A⁻（艾灸耳穴，须带禁忌）/ B（须医师）/ C（立即就医） | **知识库型天花板**。工程结构最规范，边界写得最诚实（专门列出"不能做什么"）。只覆盖教材级通识，不含各派发挥 —— 这恰好是它作为"底座"的优点 |
| [JuneYaooo/nihaisha-nishi-tcm](https://github.com/JuneYaooo/nihaisha-nishi-tcm) | 2213 | 2026-09-16 | **A** | 倪海厦课程资料 Skill：课程检索、**方证 / 穴位辨析**、学习笔记整理、**板书截图证据索引**（可回溯到原始板书） | **溯源最好**。要回答"这句话出自哪一页板书"就用它。适合当 nihaixia 的证据补充层，而非替代 |
| [Tespera/nihaisha-skill](https://github.com/Tespera/nihaisha-skill) | 8 | 2026-08-06 | **A** | 倪海厦讲义 Skill：伤寒论 129 条、金匮 23 篇、内经 53 篇、本草 345 种、医案 321 例；**分层索引按需加载，触发仅 2.3k token**；带 `POLICY.md` 安全契约，强制"转述争议观点必须标注这是倪海厦的观点" | **工程最克制**。星最少但最专业：上下文预算（2.3k vs 3.5M）和争议内容处理都做到位。**适合作为二次开发基底**，可惜社区关注度不足 |
| [jangviktor-web/likeskill](https://github.com/jangviktor-web/likeskill) | 139 | 2026-08-23 | **B+** | 李可（1930-2013）思维操作系统。13 个来源（11 本著作 + 2 篇访谈）蒸馏，423 个医案、120+ 首方剂、92 种症状路由、24 种假证识别；主打急危重症（心衰/中风/休克）、经方剂量体系、六经辨证 | 同模板产物，质量稳定。**急危重症场景最全**，但剂量体系必须人工把关，不能直接采信 |
| [jangviktor-web/huxishu](https://github.com/jangviktor-web/huxishu) | 48 | 2026-08-23 | **B+** | 胡希恕（1898-1984）经方临床 Skill。基于 38 万字中日录音增补版讲稿（伤寒论 398 条 + 金匮要略 22 篇），蒸馏为 16 个六经辨证 IF-THEN 公式、9 组方证鉴别速查表、4 大核心心智模型 | **六经方证最严谨**，结构最"公式化"，适合做规则引擎。但 38 万字只蒸馏出 16 条公式，信息密度偏低 |
| [jangviktor-web/huangyuanyu](https://github.com/jangviktor-web/huangyuanyu) | 21 | 2026-08-23 | **B** | 黄元御视角 Skill v4.0.0：土枢四象·一气周流，15 个诊断公式 + 10 棵决策树 + 10 问诊协议 + 273 条关键词索引 + 11 部医书全文（2326 条行号索引） | 体系完整，但临床面窄，**与伤寒派结论常冲突**。装之前想清楚主从 |
| [jangviktor-web/wujutong](https://github.com/jangviktor-web/wujutong) | 24 | 2026-08-23 | **B** | 吴鞠通（1758-1836）温病派 Skill。基于《温病条辨》《医医病书》《吴鞠通医案》359 案、《温热经纬》吴氏按语；三焦辨证、卫气营血、22 温病方剂、9 诊断公式、凉开三宝、白虎四禁、湿温三禁 | **温病专用**。与 nihaixia 合参互补，单用场景窄 |
| [jonhnsonzz/nihaisha-renji](https://github.com/jonhnsonzz/nihaisha-renji) | 12 | 2026-08-23 | **B** | 倪海厦人纪辨证知识系统，12 门课程知识库，支持 **Skill + MCP + API** 三种调用方式 | 星少但形态最实用：**唯一提供 MCP/API 的**，要做产品后端就它 |
| [xiaojian94xiaojian/nihaixia-tcm-wiki](https://github.com/xiaojian94xiaojian/nihaixia-tcm-wiki) | 36 | 2026-06-12 | **B−** | 倪海厦人纪经方知识库，按 karpathy 知识库方法论构建，封装为 Claude Code Skill；针灸大成 / 内经 / 本草 / 伤寒 / 金匮同步文稿 + 医案 + 文章 + 梁冬访谈 | **素材全、加工少**。接近原始语料库，适合自己再蒸馏 |
| [Lyuyaowei/chinese-medicine](https://github.com/Lyuyaowei/chinese-medicine) | 7 | 2026-04-20 | **C** | AI 中医健康咨询 Skill：体质辨证 / 食疗养生 / 经络穴位 / 方剂参考 / 体检解读（轻量日常向，OpenClaw Skill） | 面广但浅，**无安全表**。只适合非医疗场景的科普 |

> ⚠️ [3150214587/niehaixia](https://github.com/3150214587/niehaixia) ⭐83 是 **nihaixia 的旧版 fork**（v2.1.0，README 徽章都还指向上游仓库）。star 数会误导人，别当独立项目引用。

### 2.2 流派地图（选 Skill 前先想清楚要哪一派）

| 流派 | 代表医家 | 对应 Skill | 适用场景 | 互斥风险 |
|---|---|---|---|---|
| **伤寒 / 经方** | 倪海厦、胡希恕 | `nihaixia`、`huxishu` | 六经辨证、方证对应 | 与温病派在"伤寒温病是否分家"上对立 |
| **温病** | 吴鞠通、叶天士 | `wujutong`、`ye-tianshi-skill` | 外感热病、卫气营血 / 三焦辨证 | 与伤寒派在辛温/辛凉上对立 |
| **扶阳** | 李可 | `likeskill` | 急危重症、大剂量附子类 | 与温病派用药方向完全相反 |
| **一气周流** | 黄元御 | `huangyuanyu` | 脾胃中气、升降浮沉 | 与六经体系框架不同，难混用 |
| **教材通识** | — | `TCM.Skill` | 概念解释、病种直达、用药安全 | 无（刻意不选边） |

> **关键认知**：前四行都是"一家之言"，结论会互相矛盾。`TCM.Skill` 是唯一刻意不选边的通识层。

### 2.3 造 Skill 的工具与证据层

| 仓库 | ⭐ | 档 | 说明 |
|---|---:|---|:--:|
| [jangviktor-web/tcm-distiller](https://github.com/jangviktor-web/tcm-distiller) | 49 | **A** | **中医·国学思维蒸馏器 v4.4.0**。不是堆典籍素材，而是标准化流水线：15 个维度拆解医者心智模型与用药逻辑，把胡希恕、黄元御、吴鞠通等人的著作/讲稿/医案提炼成可还原真人辨证思路的专属 Skill。上面 `huxishu` / `wujutong` / `likeskill` / `huangyuanyu` **全是它的产物** —— 想造自己的名医 Skill 从这里起 |
| [Renhuai123/nihai-renji-corpus](https://github.com/Renhuai123/nihai-renji-corpus) | 19 | **A** | 倪海厦《人纪》**结构化语料库**：全量 19,294 条判语，六部（伤寒论/金匮/本草/内经/仲景心法/针灸大成）117 集约 178 小时讲课，**每条带精确到秒的视频出处可回放溯源** —— 做 Skill 的"证据层"极佳 |
| [skyfiredao/oh-my-tcmpowers](https://github.com/skyfiredao/oh-my-tcmpowers) | 16 | **B+** | **中医之心**：5 agents（扁鹊/陶弘景/彭子益/陈士铎/皇甫谧）+ 18 skills 的**编排层**，三支辨证（五行诀方剂 / 圆运动 / 辨证录）+ 针灸四路**并行推导后交叉验证**，脉诊做独立反向验证，每次分析落盘归档。架构最"重"，但理论偏彭子益/陈士铎一家 |
| [jangviktor-web/ye-tianshi-skill](https://github.com/jangviktor-web/ye-tianshi-skill) | 7 | **B** | 叶天士 · 温病卫气营血辨证 persona（同作者 2026-10 新作） |
| [dhicoc/dsh-chinese-traditional-wisdom-skill](https://github.com/dhicoc/dsh-chinese-traditional-wisdom-skill) | 61 | ⚠️ | 中华传统智慧「玄枢」技能包：八字 / 紫微 / 六爻 / 梅花 / 奇门 / 风水 / 五运六气 / 体质，本地确定性引擎 + Dashboard。**中医只占一小块，主体是命理，别混用** |

### 2.4 怎么挑（三条硬标准）

1. **看上下文预算，不只看字数**
   `nihaixia` 3.5M 字是"重武器"，每次触发都吃 token；`TCM.Skill` 的"SKILL.md 只放流程 + references 按需加载"和 `nihaisha-skill` 的 2.3k token 触发开销才是可持续做法。**判断方法**：看仓库里 `SKILL.md` 有多长、事实是否外置到 `references/`。

2. **看有没有安全契约**
   合格的标志：`POLICY.md`（Tespera）、硬约束安全表（TCM.Skill：十八反十九畏 / 妊娠 / 毒性药剂量上限 / 马兜铃酸）、A·A⁻·B·C 分级（TCM.Skill）。只有一句免责声明的，**别接进面向用户的链路**。

3. **看是一派还是通识**
   名医 Skill 本质是一家之言。**正确用法：教材型打底 + 名医 Skill 做视角切换**，而不是装一堆名医让模型自由发挥。

**推荐组合**

| 用途 | 组合 |
|---|---|
| 学习 / 查典 | `TCM.Skill`（教材通识）+ `nihaisha-nishi-tcm`（板书溯源） |
| 经方辨证练习 | `nihaixia`（主）+ `huxishu`（六经方证校验）+ `wujutong`（温病反证） |
| 做产品后端 | `jonhnsonzz/nihaisha-renji`（MCP/API）+ `Tespera/nihaisha-skill`（低 token 触发） |
| 自己造 Skill | `tcm-distiller` + `nihai-renji-corpus`（证据层） |

### 2.5 安装方式（以 nihaixia 为例）

```bash
# 方式一：手动（最简）
git clone https://github.com/jangviktor-web/nihaixia.git
cp -r nihaixia ~/.claude/skills/nihaixia/
# pi / Codex / OpenClaw 同理，放进各自的 skills 目录即可

# 方式二：腾讯云 SkillHub（已更新至 v2.3.1）
# 把这句话发给你的 agent：
#   请根据 https://skillhub.cn/install/skillhub.md，安装 @user_ff4d9420/nihaixia-pro

# 方式三：腾讯 IMA APP 内置 Skill 商店直接更新
```

激活词：`倪海厦` / `海厦视角` / `倪师` / `经方思维` / `倪海厦会怎么看`

### 2.6 本节风险提示

1. **star 与质量弱相关**：`nihaixia` 3898⭐ 但上下文最重；`nihaisha-skill` 8⭐ 却是工程质量最高的。
2. **同模板复制**：`jangviktor-web` 一家贡献了 6 个中医 Skill（nihaixia / likeskill / huxishu / wujutong / huangyuanyu / ye-tianshi），star 受母体带动，**不代表各自都被验证过**。
3. **授权参差**：主仓多为 MulanPSL-2.0（可商用需保留声明），但教材/视频类仓库常常没有 LICENSE。

---

## 3. 大模型

> **本节结论**：能用的是 3.2 / 3.3 / 3.3.1 三张表（约 20+ 个权重）。3.4 那张表全是"有论文没权重"，只用于看方向；3.5 是通用医疗底座，做对照实验必备。

### 3.1 全景：三类模型，别混用

```
真能下载的权重（~20+）  ──►  直接跑 / 微调 / 复现      → 3.2 + 3.3 + 3.3.1
只有论文的垂类模型      ──►  看方法论、写相关工作      → 3.4
医院 / 厂商产品         ──►  了解行业方向，拿不到权重  → 3.4 末
通用中文医疗底座        ──►  中医微调上游 + 论文对照    → 3.5
```

**最常见的错误**：把 3.4 里的"天医""数智岐黄"当成可选模型写进方案 —— 它们没有公开权重，只能引用论文。

### 3.2 代码 + 权重齐备（首选池）

| 模型 | 仓库 | ⭐ | 机构 / 年份 | 档 | 特色与判断 |
|---|---|---:|---|:--:|---|
| 本草 Huatuo | [SCIR-HI/Huatuo-Llama-Med-Chinese](https://github.com/SCIR-HI/Huatuo-Llama-Med-Chinese) | 5001 | 中科院 / 2023 | B | 医疗指令微调 LLaMA，中医语料。**星最多但最老**，2026 年只适合当历史基线，别当生产底座 |
| 仲景 CMLM-ZhongJing | [pariskang/CMLM-ZhongJing](https://github.com/pariskang/CMLM-ZhongJing) | 533 | 福耀科技大学 / 2025 | A | 首个中医专用 LLM，专家知识引导微调，权重 ZhongjingGPT1-13B（gated）。另有 1.5B / 1.8B / 7B 小模型系列，端侧可跑 |
| 神农 ShenNong | [michael-wzhu/ShenNong-TCM-LLM](https://github.com/michael-wzhu/ShenNong-TCM-LLM) | 513 | 华东师大 / 2023 | B+ | 首个中医药中文大模型，配套 ShenNong_TCM_Dataset。**价值在数据开源**，模型本身已过时 |
| TCMLLM / 灵丹 v1 | [2020MEAI/TCMLLM](https://github.com/2020MEAI/TCMLLM) | 273 | 北交大 / 2024 | B | 中医药大模型 + 处方推荐，Lingdan-13B-Base。**已被 v2 取代**，只作历史引用 |
| **灵丹-V2 Lingdan-V2** | [TCMAI-BJTU/Lingdan-V2](https://github.com/TCMAI-BJTU/Lingdan-V2) | 3 | 北交大 / 2026 | **S** | **当前最完整的开源中医训练管线**：Qwen3 4B/8B/14B × Base（CPT 16.62B token）/ SFT（773 万样本）/ **R1（处方 GRPO）**，Apache-2.0，有在线 demo [lingdan.chat](https://lingdan.chat/)、[HF 官方组织](https://huggingface.co/TCMLLM)、ModelScope 镜像与 [arXiv 2610.14705](https://arxiv.org/abs/2610.14705)。**星只有 3 个但质量最高** —— 本文档里 star 与质量反差最大的一条。<br>**⚠️ 2026-11-09 复核**：HF 实际可下载的是 **8 个** checkpoint（4B/8B 各 Base/SFT/R1 + 14B Base/SFT，全部 Apache-2.0 非 gated）；README Model Zoo 里列的 **`Lingdan-14B-R1` 权重并未发布** —— `resolve/main/README.md` 与 `config.json` 都是 404（gated 会是 403，见 9.5），组织仓库列表里没有它，ModelScope 的文件树也返回 404 只有占位页。所以论文里最强的那档（Overall 67.1 / 处方 F1 37.0）**现在拿不到**，实际可用的处方旗舰是 **8B-R1**（Overall 63.7 / 处方 F1 34.5，私有临床 Herb F1 50.7） |
| 黄帝 HuangDI | [Zlasejd/HuangDI](https://github.com/Zlasejd/HuangDI) | 163 | 2024 | C | 基于 Ziya-LLaMA-13B-V1 的中医古籍知识问答。底座已停更，只适合古籍问答对照 |
| 时珍 ShizhenGPT | [FreedomIntelligence/ShizhenGPT](https://github.com/FreedomIntelligence/ShizhenGPT) | 154 | 港中深等 / 2025 | **A+** | **多模态四诊**（舌/脉/面/声），ShizhenGPT-7B-Omni，数据与权重都开源。**做四诊多模态的唯一现成起点**，另有 32B-VL 大号（gated） |
| MedChatZH | [tyang816/MedChatZH](https://github.com/tyang816/MedChatZH) | 111 | 华东理工 / 2024 | A | 中西医**问诊对话**微调（Computers in Biology and Medicine 2024），开源问诊数据集。做问诊产品的现成数据源 |
| 扁仓 BianCang | [QLU-NLP/BianCang](https://github.com/QLU-NLP/BianCang) | 86 | 齐鲁工大 / 2025 | **A+** | JBHI 正式发表，7B / 14B 系列，论文+权重+代码齐，有社区 GGUF。**综合性价比最高的"本机跑通"选择** |
| TCMChat | [ZJUFanLab/TCMChat](https://github.com/ZJUFanLab/TCMChat) | 81 | 浙大 / 2025 | A | 预训练 + SFT，配套 **60 万条中药知识对话数据集**。模型一般，**数据集是宝藏** |
| **中医男科 MiMo-9B-LoRA** | [GitHub](https://github.com/johnson7788/man_medical) · [HF](https://huggingface.co/johnson/MiMo-9B-TCM-Andrology-LoRA) | 1 | 2026-10 | **A+** | 唯一「专科 + 完整评测协议」开源中医模型：基座 `XiaomiMiMo/MiMo-V2.6-Distill-Qwen-9B`（9.41B），bf16 LoRA r=16 仅 43.3M 参数；21,484 条真实男科门诊病历（四诊→诊断+处方）；冻结测试集 2,764 条、**按患者分组切分无泄漏**，处方 Jaccard 0.429（初诊 0.301 **超过检索 Oracle 0.254**，复诊 0.501 不如直接照抄）；**代码 Apache-2.0 / 数据与权重 CC BY-NC 4.0（禁商用）**。**价值不在模型大小，而在评测范式** |
| RenShu-AI | [yanlinPeng-code/RenShu-AI](https://github.com/yanlinPeng-code/RenShu-AI) | 93 | 2026 | B | 多 Agent 中医问诊系统，前后端分离。**应用层，不是模型层**，做产品架构参考 |

### 3.3 仅 HuggingFace 权重（GitHub 侧无独立仓库）

| 模型 | 年份 | 规模 / 底座 | 档 | 特色与判断 | 链接 |
|---|:--:|---|:--:|---|---|
| **杏核 Xinghe 1.2** | 2026 | 9B | A | 推理 + 古籍；**有 GGUF，普通笔记本可跑**（下载量最高的小模型之一） | [权重](https://huggingface.co/zsyjsld/Xinghe1.2-9B) · [GGUF](https://huggingface.co/zsyjsld/Xinghe1.2-9B-GGUF) · [数据](https://huggingface.co/datasets/zsyjsld/neijing-sft-v1.2) |
| **白泽 Baize-TCM** | 2025 | Qwen3 0.6B / 8B | A | 中国中医科学院中药所，V1/V2/V3 各有 16bit / 4bit 版本，**语料库同步开源**（见 6.1）。**0.6B 是当前能跑的最小可用中医模型** | [权重](https://huggingface.co/DigitalIntelligenceCenter-of-ICMM/Baize-Traditional-Chinese-Medicine-Large-Language-Model) · [V3-16bit](https://huggingface.co/DigitalIntelligenceCenter-of-ICMM/Baize-Traditional-Chinese-Medicine-Large-Language-Model-V3-16bit) · [GGUF](https://huggingface.co/mradermacher/Baize-Traditional-Chinese-Medicine-Large-Language-Model-GGUF) |
| **知方丹台 ZhiFangDanTai** | 2025 论文 / 2026 权重 | — | B+ | 首师大，RAG + 知识图谱。**⚠️ 2026-11-09 复核：原权重链接已失效** —— `resolve/main/config.json` 与 `README.md` 都返回 404（不是 gated 的 403），`search=ZhiFangDanTai` 命中 0 条，作者 `tczzx6` 名下现在只有 `LLM-SAGE`。原先记的"gated / API 401"是误判，**现在当作"有论文无权重"看**（见 3.4） | [论文](https://arxiv.org/abs/2509.05867) · [原权重链接（已 404）](https://huggingface.co/tczzx6/ZhiFangDanTai1.0) |
| **仲景小模型系列** | 2026 | 1.5B / 1.8B / 7B | A | 与 13B 同门，主打端侧/手机可跑 | HF `CMLM/Zhongjing-1-7b` · `CMLM/ZhongJing-2-1_8b` · `CMLL/ZhongJing-3-1_5b_V2`（+GGUF） |
| **石真 32B** | 2025 | 32B-VL | A | ShizhenGPT 大号多模态版，**gated**；**Spark 上 bf16 可跑（64G）**，是多模态四诊的上限选择 | [权重](https://huggingface.co/FreedomIntelligence/ShizhenGPT-32B-VL) |
| ChatTCM | 2025 | Qwen2-7B | B+ | 继续预训练权重，**适合自己接着训** | [权重](https://huggingface.co/SylvanL/ChatTCM-7B-Pretrain) |
| ViTCM-LLM | 2025 | 多模态 | B | 清华 SIGS，多模态 + RAG（IEEE BIBM 2025） | [代码](https://github.com/jw-chae/ViTCM_LLM) · [权重](https://huggingface.co/Mark-CHAE/ViTCM-LLM) |
| TCM-VisResolve (TCM-VR) | 2025 | 多模态 | C | 云南民族大学，视觉问答（IEEE BIBM 2025）。文档少，慎用 | HF `dylanyang963/TCM-VR` |
| TCMConverse 系列 | 2026 | 14B / 4B | B+ | 中医问诊 SFT + DPO 对齐；同门 `cduoduo/TCM-Rerank-v2-m3` 是**中医检索/重排模型，做 RAG 时很有用** | HF `cduoduo/TCMConverse-14B-SFT` |
| TCM-Qwen2.5-7B-SFT | 2026 | 7B | B | 社区全量 SFT 权重，另有 mradermacher GGUF。无评测，慎作基线 | [权重](https://huggingface.co/Xxiao2023/TCM-Qwen2.5-7B-SFT-V1) |
| Qwen3.5-9B 中医 CPT | 2026 | 9B | B+ | Qwen3.5-9B 中医继续预训练全量权重（约 17.9G）。**做底座很新，但无配套评测** | HF `arthur789/qwen3.5-9b-tcm-cpt` |
| 中医体质 Qwen3-8B | 2026 | 8B | B | **体质辨识**方向量化权重（q4/q5/q8），场景专一 | [GGUF](https://huggingface.co/chenhaodev/tcm-constitution-qwen3-8b-gguf) |
| DeepSeek-R1-Distill-Qwen-7B-TCM | 2025 | 7B | C | R1 蒸馏 + 中医 SFT，推理链路；有 GGUF。**社区实验性微调** | HF `jasonXT/DeepSeek-R1-Qwen-7B-TCM` |
| 神农权重 | 2023 | 7B | B | 首个中医药中文大模型 | [HF](https://huggingface.co/michaelwzhu/ShenNong-TCM-LLM) · [数据集](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset) |

> **口径提示**：Awesome-TCM-LLM 统计「真能下载复现的中医权重约 16 个」（2026-10 快照）；2026-11-01 按 tag 重扫 hf-mirror 又补了 7 个可直接下载的权重，见 3.3.1。2026-11-09 复核把已失效的知方丹台移出可下载口径（净 -1，仍是 20+），并确认灵丹-V2 实际发布 8 个而非 9 个。其余多为 gated、LoRA 片段或社区实验性微调。

### 3.3.1 2026-11-01 hf-mirror 补遗：中西医结合专项

> **本节结论**：按 tag 重扫 hf-mirror 后，补到 7 个有模型卡、可直接下载的权重；其中**明确"中西医兼通"的只有 3 个**（`medical-v5-8b` / Qwen3-4B 医疗微调 / 中药学 Qwen3-8B），其余仍是中医专用。灵丹-V2 官方 HF 权重也已开放（见 3.2 行），是比新增社区模型更重要的变化。

| 模型 | 规模 / 底座 | 许可 | 档 | 判断 | 链接 |
|---|---|---|---|---|---|
| **medical-v5-8b** | Qwen3-8B（8.19B） | 权重 Apache-2.0；训练数据含 M2 蒸馏，仅研究/教育 | **A-** | 卡片直接写"中医西医兼通临床助手"：37,353 条临床数据 + Baichuan-M2-32B 蒸馏 thinking 链，自评 210 题 CMB 70% / C-Eval 92%（open 题有 judge 天花板）。**把"MCQ + thinking 需先剥 `<think>`"这类坑写得很清楚**；有 Q5_K_M GGUF | [权重](https://huggingface.co/shdkahjkda/medical-v5-8b) · [GGUF](https://huggingface.co/shdkahjkda/medical-v5-8b-gguf) |
| **中药学 Qwen3-8B** | Qwen3-8B LoRA / GGUF | Apache-2.0 | B+ | 按《中药学（新世纪第四版）》883 页教材蒸馏：410 味药、4,172 知识点、约 13k 样本；除中药问答外专门做了**中西药联用**（阿司匹林/华法林/二甲双胍等）与"幻觉审查官"。q4/q5/q8 GGUF 齐全；**教材级知识，无临床评测** | [GGUF](https://huggingface.co/chenhaodev/tcm-qwen3-8b-gguf) · [LoRA](https://huggingface.co/chenhaodev/tcm-qwen3-8b-lora) |
| **Qwen3-4B 医疗微调** | Qwen3-4B | Apache-2.0 | B | 卡片自述 80% 中医 + 20% 西医/通用推理的 QLoRA 合并权重；无评测，自己也列了"可能混淆中西医概念、编造处方"等限制。适合端侧或小参数对照，不适合当主基线 | [权重](https://huggingface.co/ronan7878/qwen3-4b-medical-finetune) |
| **TraceMed** | Qwen3-4B | 未标（待补） | B+ | 甘草医生 AI；辨证/方剂对比/考试题，回答逐句带引用、可定位到教材原文段落；32k 上下文、bf16 约 8.8GB。**训练数据、评测、许可都未公布**，先当 citation 型试用基线 | [权重](https://huggingface.co/GancaoDoctorAI/TraceMed) |
| **TCM-Qwen3.5-9B-SFT-R2** | Qwen3.5-9B | 未标 | B+ | 与 3.3 的 `qwen3.5-9b-tcm-cpt` 同底座：CPT 6.16 亿 token + SFT 21,586 条后的**全量 BF16 合并权重**，thinking/non-thinking 双模式；保留视觉组件但未做舌诊训练。**可直接跑，许可待补**（2026-11-09 复核：`cardData.license` 仍为空，作者 Xxiao2023 名下只有这一个 + TCM-Qwen2.5-7B-SFT-V1，无新增） | [权重](https://huggingface.co/Xxiao2023/TCM-Qwen3.5-9B-SFT-R2) |
| **YIAN-4B** | Qwen3-4B LoRA（66MB） | CC BY-NC 4.0 | **A-** | 中医医案**结构化抽取**专用：从带理论铺陈/按语的整篇医案中定位病历，输出 7 字段 JSON（患者/主症/舌/脉/证/治法/方药剂量）；12,500 条 TCM-YIAN 指令。抽取场景很实用，**禁商用**；数据集 DOI 仍是占位符 | [权重](https://huggingface.co/mark1111222/YIAN-4B) |
| **TCM-m3** | bge-m3（2.27GB） | Apache-2.0 | A- | 中医 RAG **嵌入模型**，与 `cduoduo/TCM-Rerank-v2-m3` 配套；无评测、模型卡只有一句，但比通用 embedding 更贴中医术语，做知识库检索可直接替 | [权重](https://huggingface.co/cduoduo/TCM-m3) |

**判断**

1. **"中西医兼通"不是标签，是训练配比**：本轮新增里，只有 `medical-v5-8b`（真实临床数据 + M2 蒸馏）、`ronan7878` 4B（80/20 配比）、`中药学 Qwen3-8B`（中西药联用专项）明确混合中西数据；`MedChatZH`（3.2 行）仍是最早的"中西医问诊"开源模型/数据，但底座停在 2024。其余新增一律是中医专用，不要在方案里写成"中西医结合"。
2. **灵丹-V2 官方权重是这轮最大的增量**：`TCMLLM/Lingdan-{4B,8B,14B}-{Base,SFT,R1}`，**2026-11-09 复核：实际公开可下载 8 个**（4B/8B 全 6 个 + 14B Base/SFT），全部 Apache-2.0 且非 gated；**`Lingdan-14B-R1` 只有 README 链接没有权重** —— `resolve/main/README.md` 直接 404（gated 应该是 403），组织仓库列表里没有它，ModelScope 文件树也 404。11-01 那轮记的"14B-R1 仍 401 gated"是错的，它从来没被上传过。社区 GGUF 有 6 个（`mradermacher/` 下的 Lingdan-4B-Base / 4B-R1 / 8B-Base / 8B-R1 / 14B-Base / 14B-SFT-GGUF，下载量 479–807，比官方 safetensors 还高），SFT 缺 4B/8B、R1 同样缺 14B。Apache-2.0 + arXiv 2610.14705 + LingLan 榜。做新项目从 8B-R1 起，别再拿 2024 年的 Lingdan-13B。
3. **"能下载"≠"能信"**：TraceMed / TCM-Qwen3.5 未标许可，YIAN / MiMo 是 CC BY-NC，medical-v5 权重 Apache-2.0 但训练数据受 Baichuan-M2 条款限制，中药学 Qwen3 不随权重发布教材原文。商用前逐项核，别只看 license 字段。
4. **本轮不采信的**：`NYCU-CGI-LLM/*-TCM-SD`、`Capmaomao/TCM_8B`、`ElonYi/Qwen2.5-7B-zhongyi`、`Huanghaonan88/*-ShangHanLun`、`wq528/tongue_vl_8B` 等要么无模型卡、要么只有 Unsloth 模板卡，没有训练/评测信息，只适合当"存在性"记录。
5. **方法**：hf-mirror 的 `search=` 对中文关键词（中医/中西医/仲景）返回 0；按 tag 扫才全：`filter=tcm`（28）、`filter=traditional-chinese-medicine`（29）、`filter=chinese-medicine`（9）。检索时间 2026-11-01。

### 3.3.2 2026-11-09 复核：社区再次提名的 4 个模型

> **本节结论**：Issue #10 里点名的 4 个 HF 模型，**3 个早已收录且信息仍然准确，无需改动**；真正的更新不在"补新模型"，而在**灵丹-V2 的 14B-R1 权重始终没发布** —— 而它正是本文档此前推荐的处方首选。

| 被点名的模型 | 之前是否已收录 | 本次核对结果 | 处理 |
|---|:--:|---|---|
| `Xxiao2023/TCM-Qwen3.5-9B-SFT-R2` | ✅ 3.3.1 | 存在、非 gated、可下载；**`license` 字段仍为空**；作者名下无新作（只有它 + `TCM-Qwen2.5-7B-SFT-V1`） | 保留，许可待补的提醒再确认一次 |
| `TCMLLM/Lingdan-14B-SFT` | ✅ 3.2（灵丹-V2 行内） | 存在、Apache-2.0、14.77B、非 gated，**14B 档目前能下到的就是它和 Base** | 行内补"14B-R1 未发布"的事实 |
| `johnson/MiMo-9B-TCM-Andrology-LoRA` | ✅ 3.2 + 3.8 专段 | CC BY-NC 4.0、LoRA 适配器、评测协议与本文所述一致 | 无需改动 |
| `chenhaodev/tcm-qwen3-8b-gguf` | ✅ 3.3.1（中药学 Qwen3-8B） | Apache-2.0、q4/q5/q8 齐全、410 味药教材向 | 无需改动 |

**核对方法**（比上一轮多了一步）：除了 HF 的 `api/models/<id>`，还查了 `api/models?author=TCMLLM`（组织实际发布了什么）和 ModelScope 的 `repo/files?Recursive=true`（仓库页存在 ≠ 权重上传）。三者不一致时，**以文件树为准**。

**这条更新为什么值得单独写**：`Lingdan-14B-R1` 是论文里打败 DeepSeek-R1 的那个 checkpoint，README、arXiv、Model Zoo 表都列着它，但 HF 的 `resolve/main/README.md` 直接 404、ModelScope 文件树也 404。**任何按 14B-R1 写的方案现在都跑不起来**，改用 8B-R1（私有临床 Herb F1 50.7，与 14B-R1 的 52.8 差 2.1）或等权重发布。

**顺带查出来的第二个问题**：3.3 里标"权重与数据 gated（API 401）"的 **`tczzx6/ZhiFangDanTai1.0`（知方丹台）其实仓库已经不存在**（`README.md` 404、`search=ZhiFangDanTai` 命中 0 条、作者 `tczzx6` 名下只剩 `LLM-SAGE`），不是 gated。它已从"可选权重"退回 3.4 的"有论文无权重"。两处一起修，是因为**上一轮的 401/404 判据本身就不成立**（见 9.5）—— 判据错了，按它得出的每一条"gated"标注都需要重验。

### 3.4 有论文、**无公开权重**（看方向可以，别当底座）

| 模型 | 机构 / 年份 | 档 | 一句话 |
|---|---|:--:|---|
| **天医 Tianyi** | 南京中医药大学 / 2026（Information Fusion） | A | 7.6B，「读书—临证—跟师」多阶段训练 + TCMEval + 真实世界验证。**目前最像样的中医训练方法论**，写论文必读 |
| **岐伯 Qibo** | 天大 + 天中医 / 2025（ESWA） | B+ | 继续预训练 + SFT，配套 Qibo Benchmark |
| **智明堂 ZMT-M1** | 北航 / 2025 | B+ | 中医大模型 + TCM-Eval 动态评测平台（[tcmeval](https://tcmeval.bamaidical.com)） |
| **青囊 QingNangTCM** | 河北北方学院 / 2026 | B | GLM-4-9B-Chat + P-Tuning v2，10 万条 QnTCM_Dataset |
| **悬壶 XuanHuGPT** | 河北北方学院 / 2025 | C | ChatGLM2-6B + LoRA/P-Tuning v2，参数高效微调的常规做法 |
| **TCM-R1** | 西南大学 / 2025 | B | GRPO 增强中医推理；同路线还有 **Ladder-base(GRPO-TCM)**（TCM-Ladder 团队） |
| **Med-Shicheng 师承** | 南中医 / 2026 | B | Qwen2.5-1.5B，CPT+SFT+KTO 学 5 位名医经验，[代码开源](https://github.com/NJUCM-BJUCM-TCM-AI/Med-Shicheng) 权重未放 |
| **知方丹台 ZhiFangDanTai** | 首师大 / 2025 论文 | B+ | RAG + 知识图谱（[arXiv 2509.05867](https://arxiv.org/abs/2509.05867)）。**原 HF 权重仓库已消失**（2026-11-09 复核 404，见 3.3），从"可选权重"退回"只能引论文" |
| TCM-DS / GastroTCM / TCM-KLLaMA / RACE-Align / DoPI | 澳科大 / 清华+中日友好 / 浙工商 / 上科大 / 天大 | C | 分别是食疗推荐、消化内科 RAG、KG+方剂生成、1.7B 轻量对齐、主动问诊 |
| **医院/厂商产品** | — | ⚠️ | 数智岐黄、大医金匮、天河·灵枢、仲思、广医·岐智、固生堂中医大脑、任度·素问、中医横琴 Hengqin-R1、华族本草、薪火中国药、伊尹、张仲景中医药大模型…**全部无公开权重**，只能引用新闻 |

### 3.5 通用中文医疗底座（微调上游 + 论文最常用对照）

| 仓库 | ⭐ | 档 | 说明 |
|---|---:|---|:--:|
| [FreedomIntelligence/HuatuoGPT-3](https://github.com/FreedomIntelligence/HuatuoGPT-3) | 29 | **A+** | **2026 最新**：9B / 27B（底座 Qwen3.5-9B / Qwen3.8-27B），OnePO 单阶段 RL **免 SFT** 的领域适配；HealthBench Professional 68.3 / 71.4，另放 Grader-8B 与 20K RL 数据。**通用医疗目前最强的开源基线**；Spark 上 bf16 可跑（54G），适合本地做同口径对照 |
| [FreedomIntelligence/HuatuoGPT-o1](https://github.com/FreedomIntelligence/HuatuoGPT-o1) | 1364 | A | 医疗复杂推理 7B/8B/70B。中医推理类论文最常用对照 |
| [baichuan-inc/Baichuan-M2-32B](https://github.com/baichuan-inc/Baichuan-M2-32B) | — | A | 百川医疗推理 32B（M3-235B 更大），HealthBench 开源前列，主动问诊 + 抑幻觉 |
| [DUTIR-BioNLP/Taiyi-LLM](https://github.com/DUTIR-BioNLP/Taiyi-LLM) | — | B+ | 太一，Taiyi-2 换 GLM4-9B 底座，中英双语生物医学 |
| [winninghealth/WiNGPT3](https://github.com/winninghealth/WiNGPT3) | — | B | 卫宁 32B 医疗推理，对接医院流程（权重未核验） |
| [scutcyr/BianQue](https://github.com/scutcyr/BianQue) | — | B+ | 扁鹊 2，多轮追问式问诊，CMB 常见对照 |
| [X-D-Lab/Sunsimiao](https://github.com/X-D-Lab/Sunsimiao) | — | B+ | 孙思邈，Qwen2-7B + 高质量医疗数据，CMB-Exam 上性价比高 |
| [MediaBrain-SJTU/MING](https://github.com/MediaBrain-SJTU/MING) | 1188 | B | 明医，中文医疗问诊大模型，MoE-LoRA 多任务 |
| [CMKRG/QiZhenGPT](https://github.com/CMKRG/QiZhenGPT) | 783 | B | 启真医学，中文医疗 LLM |
| [shibing624/MedicalGPT](https://github.com/shibing624/MedicalGPT) / [WangRongsheng/CareGPT](https://github.com/WangRongsheng/CareGPT) | — | A | 中文医疗 LLM 全流程训练框架（PT→SFT→RLHF/DPO），**中医微调实验常直接拿来改** |
| [liuhuanyong/QASystemOnMedicalKG](https://github.com/liuhuanyong/QASystemOnMedicalKG) | 7400 | B+ | 以疾病为中心的医疗知识图谱 + QA 教程，**KG 入门首选** |
| [honeyandme/RAGQnASystem](https://github.com/honeyandme/RAGQnASystem) | 1488 | B+ | Neo4j KG-RAG（4.4 万实体 / 31 万关系）+ BERT NER + 32B 意图识别 |
| [wangle1218/KBQA-for-Diagnosis](https://github.com/wangle1218/KBQA-for-Diagnosis) | 1489 | B | KG + 向量检索的诊疗问答 |
| [WangRongsheng/XrayGLM](https://github.com/WangRongsheng/XrayGLM) | 1087 | C | 中文胸部 X 光多模态医学模型（非中医，仅作多模态对照） |

### 3.6 评测基准（选型必须一起看）

> **铁律**：不同论文的中医 benchmark 分数**不可跨表比较**。要么用同一套基准重跑，要么只比"有没有做患者分组切分"。

| 基准 | 覆盖 | 档 | 入口 |
|---|---|:--:|---|
| **TCM-Ladder** | 首个中医多模态 QA 基准，任务定义清楚 | A | [orangeshushu/TCM-Ladder](https://github.com/orangeshushu/TCM-Ladder) ⭐25 |
| **LingLan / LingLanMedBench（灵兰）** | 灵丹团队配套基准，与 Lingdan-V2 对齐 | A | [TCMAI-BJTU/LingLan](https://github.com/TCMAI-BJTU/LingLan) ⭐7 · [arXiv 2602.01779](https://arxiv.org/abs/2602.01779) |
| **MTCMB** | 多任务中医评测（知识 / 辨证 / 处方） | B+ | [Wayyuanyuan/MTCMB](https://github.com/Wayyuanyuan/MTCMB) ⭐27 |
| **TCMBench** | 中医 LLM 综合评测 | B | [ywjawmw/TCMBench_v1](https://github.com/ywjawmw/TCMBench_v1) |
| **TCMEval** | 动态可扩展评测平台（智明堂配套） | B | [tcmeval.bamaidical.com](https://tcmeval.bamaidical.com) |
| **ShizhenGPT TCM Benchmarks** | 文本 + 视觉两套，**多模态唯一现成口径** | A | [TCM-Text-Exams](https://huggingface.co/datasets/FreedomIntelligence/TCM-Text-Exams) · [TCM-Vision-Benchmark](https://huggingface.co/datasets/FreedomIntelligence/TCM-Vision-Benchmark) |
| **Med-Bench-Arena** | **不是基准，是跑分框架**：40+ 基准 × 任意后端 × 12 指标，中医（辨证证型链 / 方剂君臣佐使 / 经络 / 舌脉）与伦理安全都是一等公民；结果自带 `split_type` 区分可比较与不可比较 | **A** | [pariskang/Med-Bench-Arena](https://github.com/pariskang/Med-Bench-Arena) ⭐4 · MIT。已 clone 实测可跑，详见 11.3 |
| CMB / CMExam | 通用中文医疗考试题，非中医专用但常一起报 | B | — |
| **man_medical 评测协议** | 不是数据集，是**方法论**：患者分组切分 + Oracle 上界 + 初/复诊分口径 + 显著性检验 | **S** | [johnson7788/man_medical](https://github.com/johnson7788/man_medical) |

### 3.7 横向选型矩阵（我的判断）

> 下表按「消费级显卡 / 笔记本」场景写；**DGX Spark 用户直接看 3.8**（几乎所有条目都升级为 bf16 全精度可跑）。

| 你的处境 | 选它 | 别选 | 理由 |
|---|---|---|---|
| 24G 单卡，要能跑 + 有论文背书 | **BianCang-7B-Instruct** | Huatuo-LLaMA（2023） | 底座差两代，且扁仓有 JBHI 正刊 + 权重 + GGUF |
| 12G / 笔记本，纯推理 | **Xinghe1.2-9B-GGUF** 或 **Baize-0.6B** | 13B 级中医模型 | 量化后 9B 约 6G，0.6B 约 0.5G |
| 要辨证 / 开方质量 | **Lingdan-8B-R1**（14B-R1 权重未发布，见 3.2） | 通用医疗模型直接问中医 | R1 阶段专门做处方 GRPO，是唯一有处方专项对齐的开源权重 |
| 要舌象 / 面象 / 声音 | **ShizhenGPT-7B-Omni** | 纯文本模型 + 图片 OCR | 目前唯一开源中医多模态（6B token 对齐语料）。⚠️ 但**脉象没有可复用的公开数据集**（11.1 实测），脉这一路要么用厂商数据要么自己采 |
| 要自己 CPT | **ChatTCM-7B-Pretrain** / **qwen3.5-9b-tcm-cpt** | 从零训练 | 有现成 CPT 权重 + 6B token 语料（ShizhenGPT） |
| 做论文对比实验 | 中医侧：扁仓 + 灵丹 + 神农 + 时珍；通用侧：HuatuoGPT-3-27B | 只跑自己模型 | 审稿人要看到强基线 |
| 要商用 | **BianCang**（查许可）/ **Lingdan-V2**（Apache-2.0） | `man_medical`、TCM-Qwen2.5-SFT | 后两者 CC BY-NC，禁商用 |
| **有 DGX Spark** | **Lingdan-14B-SFT bf16 + ShizhenGPT-32B-VL + HuatuoGPT-3-27B**（处方专项对齐用 Lingdan-8B-R1，14B-R1 未发布权重） | 8B 级量化模型 | 128G 统一内存足以全精度跑 32B，量化纯属浪费（见 3.8） |

---

### 3.8 硬件适配：DGX Spark（GB10）能跑什么

> **本节结论**：Spark 让 3.2 / 3.3 里几乎所有模型都变成"能跑"，连 32B 多模态和 70B 都能塞下。但**容量不是瓶颈，带宽才是** —— 32B 以上交互体验会明显变差。

**公开规格**（nvidia.com 产品页 + DGX Spark User Guide，2026-10 核对；本机未实测，下表数值为文档数据 + 带宽推算）

| 项 | 值 | 对选型的影响 |
|---|---|---|
| GPU | Blackwell GB10，5th-gen Tensor Cores，**1 PFLOP FP4** | 算力只在 prefill（长文本首 token）和训练时有用 |
| 内存 | 64GB 或 **128GB** LPDDR5X，统一内存（UMA），256-bit，**273 GB/s** | 容量大但带宽只有消费级显卡的 1/3 —— **逐字生成慢** |
| CPU | 20 核 Arm（10× Cortex-X925 + 10× A725） | 部分 x86 轮子需自己编，优先用 NGC 容器 |
| 软件栈 | DGX OS 7.6.0 / 驱动 580.178.04 / **CUDA 13.0.3** / TensorRT 10.14.1 | 需 sm_121 支持，老版本 torch/vLLM 装不上 |
| 显示预留 | 默认 2GB（BIOS 可调 4GB） | 128G 版实际约 **126GB** 可用 |
| 网络 | ConnectX-7 200Gb/s | 两台可串联跑更大模型 |

**三条关键认知**

1. **容量不是瓶颈，带宽是。** 128GB 让你"装得下"70B，但 273GB/s 决定了 32B 以上交互会卡。
   估算公式：`tok/s ≈ 0.65 × 273 ÷ 每 token 需读取的 GB`（0.65 为有效带宽系数）
2. **算力只在 prefill 有用。** 1 PFLOP FP4 让 RAG 灌长文档很快，但逐字生成受带宽限制 —— 所以**长上下文 RAG 比长对话更适合 Spark**。
3. **统一内存 = 可以同时跑多个模型。** 这是 Spark 相对 24G 显卡最大的优势：TCM 全栈（生成 + 重排 + 嵌入）能塞进一台机器，不用来回换模型。

**显存占用与速度估算**

| 模型 | 参数量 | bf16 | q8 | q4 | bf16 tok/s | q4 tok/s | Spark 判定 |
|---|---:|---:|---:|---:|---:|---:|:--:|
| Baize-TCM 0.6B | 0.6B | 1.2G | 0.6G | 0.3G | ~148 | ~526 | ✅ 随便跑 |
| ZhongJing-1.5B | 1.5B | 3.0G | 1.6G | 0.8G | ~59 | ~210 | ✅ 随便跑 |
| Lingdan-4B | 4B | 8.0G | 4.2G | 2.2G | ~22 | ~79 | ✅ 流畅 |
| BianCang-7B / Lingdan-8B | 7.6–8.2B | 15–16G | 8–9G | 4.3–4.6G | ~11 | ~40 | ✅ 流畅 |
| Xinghe-9B / **MiMo-9B** | 9–9.41B | 18–19G | 9.5–10G | 5.1–5.3G | ~9.5 | ~34 | ✅ 流畅（见下节） |
| ZhongJing-13B | 13B | 26G | 14G | 7.3G | ~7 | ~24 | ✅ 可用 |
| Lingdan-14B / BianCang-14B | 14B | 28G | 15G | 7.9G | ~6.3 | ~22 | ✅ 可用（**不必量化**） |
| HuatuoGPT-3-27B | 27B | 54G | 29G | 15G | ~3.3 | ~12 | ⚠️ bf16 偏慢，q8 更实用 |
| **ShizhenGPT-32B-VL** / Baichuan-M2-32B | 32B | 64G | 34G | 18G | ~2.8 | ~10 | ⚠️ bf16 能装但慢，q8 平衡 |
| HuatuoGPT-o1-70B | 70B | 140G ❌ | 74G | 39G | — | ~4.5 | ⚠️ 只能 q4 + 离线批量 |
| Baichuan-M3-235B | 235B | ❌ | ❌ | 132G | — | ~1.3 | ❌ 装不下（要留 KV cache） |

> 速度为**带宽上限估算**，实际受 KV cache、batch、内核实现影响；prefill（读长文档）远快于这些数字。

**原来跑不了的，现在能跑了（4 个实质升级）**

| 升级 | 之前 | 现在 | 意义 |
|---|---|---|---|
| 多模态四诊 | 只能用 ShizhenGPT-7B-Omni | **ShizhenGPT-32B-VL bf16（64G）** | 舌/面/声理解精度直接上一个台阶 |
| 论文对照基线 | 只能引别人数字 | **HuatuoGPT-3-27B / Baichuan-M2-32B 本地跑** | 自己做同口径对比，不用信别人的表 |
| 处方评测 | 14B 要量化，精度受损 | **Lingdan-14B-SFT bf16 全精度**（R1 档只有 8B 有权重） | 评测结论更可信 |
| 推理范式 | 8B 级 | **HuatuoGPT-o1-70B q4** | 能跑但 4.5 tok/s，只适合离线批量 |

**仍然不实用**：235B 级（Baichuan-M3）q4 就 132GB，加 KV cache 装不下；即便 FP4 硬塞也只有 ~1.3 tok/s。

**MiMo-9B-TCM-Andrology-LoRA 在 Spark 上**

结论：**完全能跑，而且很轻松** —— 9.41B × 2 = 18.8GB，占 128G 的 15%；LoRA 适配器只有 43.3M（0.17GB）。

真正的门槛不是显存，而是**软件版本**：

| 要求 | 说明 |
|---|---|
| `transformers >= 5.12` | 基座是 `qwen3_5` 混合注意力架构，旧版直接报未知模型 |
| `trust_remote_code=True` | 必须 |
| `AutoModelForImageTextToText` | 带视觉塔，用 AutoModelForCausalLM 会缺模块 |
| `padding_side='left'` | decoder-only 批量生成必须，否则输出错乱 |
| LoRA 目标模块 | **不能照抄 Qwen3 名单**：32 层里只有 8 层有 `q/k/v/o_proj`，另 24 层用 `in_proj_qkv/z/b/a/out_proj` |

```python
from transformers import AutoModelForImageTextToText, AutoTokenizer
from peft import PeftModel
import torch

BASE = "XiaomiMiMo/MiMo-V2.6-Distill-Qwen-9B"
ADAPTER = "johnson/MiMo-9B-TCM-Andrology-LoRA"

tok = AutoTokenizer.from_pretrained(BASE, trust_remote_code=True)
tok.padding_side = "left"
model = AutoModelForImageTextToText.from_pretrained(
    BASE, dtype=torch.bfloat16, device_map={"": 0}, trust_remote_code=True)
model = PeftModel.from_pretrained(model, ADAPTER).eval()
# 单条 9 tok/s 级；批量跑评测用 batch 提升吞吐
```

- **别去找 GGUF**：官方没有；`qwen3_5` 混合注意力在 llama.cpp 的支持通常滞后，自己 merge + convert 容易踩坑。Spark 上显存富裕，直接 bf16 最省事。
- **要上 vLLM**：先 merge LoRA（`merge_and_unload()`）再导出，vLLM 对 PEFT 适配器的支持版本敏感。
- **顺带能做的**：这台机器可以同时挂 9B 生成 + `cduoduo/TCM-Rerank-v2-m3` 重排 + 一个 embedding 模型，组成完整中医 RAG，不用切换。

**Spark 上的栈要点（避坑）**

1. **优先用 NGC 容器**（PyTorch / vLLM / TensorRT-LLM）。官方明确写「最新特性与性能优化通过 NGC 容器提供」—— pip 直装的 CUDA 13 + sm_121 轮子经常不全。
2. **自己编 llama.cpp 要指定架构**：`-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=121`，否则默认架构跑不出性能。
3. **`nvidia-smi` 会显示 `Memory-Usage: Not Supported`** —— 这是 UMA/iGPU 的预期行为，不是故障。别写脚本依赖这个字段做显存判断，用 `nvidia-smi --query-gpu=memory.total` 或直接看进程占用。
4. **64GB 版注意**：32B bf16（64G）跑不动；14B bf16（28G）没问题，正好是 3.2 里的主力。
5. **微调可行**：`man_medical` 那种 bf16 LoRA（43.3M 参数、21.5k 样本、2 epoch）在原卡 H20 上 2h50m，Spark 估计慢 2–4 倍（约 6–10 小时），完全可接受。

---

## 4. 应用 / 系统 / 工具

> **本节结论**：应用层能直接用的是 `OpenTCM`（可溯源 RAG 架构）和 `my-TCM-textbook-website`（当 wiki）；科研工具按"网络药理学 / 处方推荐 / NER"三条线各挑一个就够。

### 4.1 应用与客户端

| 仓库 | ⭐ | 更新 | 档 | 说明 |
|---|---:|---|:--:|---|
| [jangviktor-web/nihaixia-app](https://github.com/jangviktor-web/nihaixia-app) | 254 | 2026-10-19 | A | Flutter 安卓客户端：六经辨证、伤寒论、**子午流注取穴、灵龟八法、五运六气**、小六壬、梅花易数、紫微斗数、八字四柱排盘、周公解梦、小儿关煞、每日黄历、节气养生、玉匣记身体占；**完全离线**。功能极全，但"中医 + 命理"混装，面向专业用户要裁剪 |
| [OpenTCM01/OpenTCM](https://github.com/OpenTCM01/OpenTCM) | 49 | 2026-10-08 | **A+** | **可溯源**中医问答：GraphRAG + 经典文本 + 现代文献 + 多语言。**做中医 RAG 最值得抄架构的一个** |
| [ChiryuhLii/my-TCM-textbook-website](https://github.com/ChiryuhLii/my-TCM-textbook-website) | 91 | 2026-08 | A | 基于 Obsidian 的**互链中医教材网站**，当个人 wiki 用很顺手 |
| [yanlinPeng-code/RenShu-AI](https://github.com/yanlinPeng-code/RenShu-AI) | 93 | 2026-03 | B | 多 Agent 中医问诊系统，前后端分离。看架构可以，模型层需替换 |
| [llyang21/TCM-Acupoint-Massage-Robot-MultiAgent](https://github.com/llyang21/TCM-Acupoint-Massage-Robot-MultiAgent) | 7 | 2026-05 | B | 多 Agent 穴位按摩机器人：YOLOv8 毫米级穴位识别 + SMPL-X 人体建模 + 灵巧手力控 + 肌电闭环。具身智能方向参考 |
| [JICio/tcm-3d](https://github.com/JICio/tcm-3d) | 6 | 2026-09 | B | 开源 3D 穴位人体，6 类工具 + 疼痛关联教学模拟 |
| [galaxy-hzy/meridian-atlas](https://github.com/galaxy-hzy/meridian-atlas) | 6 | 2026-09 | B | 3D 经络系统，419 个穴位可交互探索 |
| [mac20777/aijiu-mpvue](https://github.com/mac20777/aijiu-mpvue) | 26 | 2023 | C | 经络 / 穴位查询微信小程序（PLpgSQL 数据 + mpvue） |
| [10969Rainy/Acupuncture](https://github.com/10969Rainy/Acupuncture) | 6 | 2019 | C | C# 针灸学习辅助：穴位说明 + 模拟针灸 |
| [suixufeng/lingguibafa](https://github.com/suixufeng/lingguibafa) | 6 | 2023 | C | C# 针灸灵龟八法推算 |

### 4.2 科研 / 计算工具

| 仓库 | ⭐ | 档 | 说明 |
|---|---:|---|:--:|
| [z814081807/DeepNER](https://github.com/z814081807/DeepNER) | 966 | **A+** | 天池**中药说明书实体识别**冠军方案（BERT-CRF / SPAN / MRC）。中医 NER 的经典工程实现，直接可复用 |
| [yao8839836/PTM](https://github.com/yao8839836/PTM) | 97 | A | 处方主题模型（TKDE 2018），处方数据挖掘的基准方法 |
| [chentao1999/MedicalRelationExtraction](https://github.com/chentao1999/MedicalRelationExtraction) | 74 | B | 医疗关系抽取 BERT-CNN |
| [tcmlab/TCMNP](https://github.com/tcmlab/TCMNP) | 68 | A | R 包，中医**网络药理学**分析（R 生态首选） |
| [MLi-lab-Bioinformatics-NJUCM/HerbiV](https://github.com/MLi-lab-Bioinformatics-NJUCM/HerbiV) | 64 | A | 中药网络药理学多功能工具，支持经典与**反向**网络药理学 |
| [yao8839836/tcm_bert](https://github.com/yao8839836/tcm_bert) | 51 | B+ | 中医病历分类 BERT（JAMIA 2019） |
| [yao8839836/CEMRClass](https://github.com/yao8839836/CEMRClass) | 44 | B | 中医临床记录分类（BIBM 2016） |
| [ZENGJingqi/GraphAI-for-TCM](https://github.com/ZENGJingqi/GraphAI-for-TCM) | 43 | B | 图 AI 量化评估中药配伍兼容性 |
| [S0mbraD/OpenTCM_Discovery](https://github.com/S0mbraD/OpenTCM_Discovery) | 31 | B | 中药小分子发现：疾病通路 + 成分检索、多库交叉核对、条件性分子对接 |
| [2020MEAI/PresRecST](https://github.com/2020MEAI/PresRecST) | 20 | B+ | 处方推荐（JAMIA），含数据集 |
| [2020MEAI/PresRecRF](https://github.com/2020MEAI/PresRecRF) | 13 | B | 处方推荐（Phytomedicine） |
| [hellowangqian/TCMDI](https://github.com/hellowangqian/TCMDI) | 2 | B | 中药—西药禁忌相互作用预测基准。星少但方向独特（中西药联用安全） |

---

## 5. 古籍 / 教材 / 视频

> **本节结论**：语料层只有 `TCM-Ancient-Books`（公有领域古籍）可以放心用；倪海厦系教材/视频仓库**授权不明**，自用可以，对外服务有风险。

| 仓库 | ⭐ | 更新 | 授权风险 | 内容 |
|---|---:|---|:--:|---|
| [xiaopangxia/TCM-Ancient-Books](https://github.com/xiaopangxia/TCM-Ancient-Books) | **1507** | 2023-09 | 低（古籍公有领域） | **中医药古籍文本近 700 项**，做 RAG / 预训练语料首选原始素材 |
| [9527qingfeng/hantang-nihaixia-follower](https://github.com/9527qingfeng/hantang-nihaixia-follower) | 504 | 2026-10-23 | **高（无 LICENSE）** | 汉唐倪海厦教材库：人纪五部（**倪师自编教材课本讲义**，非语音转文字）+ 天纪，另含李可、胡希恕等。作者给出自学顺序：**针灸 → 黄帝内经 → 神农本草经 → 伤寒论 → 金匮要略** |
| [Lance-myk/Traditional-Chinese-Medicine-nihaisha](https://github.com/Lance-myk/Traditional-Chinese-Medicine-nihaisha) | 93 | 2026-07 | **高（视频版权）** | 倪海厦**全套高清教学视频 + 原版 PDF 讲义课件**，人纪 / 天纪完整体系 |
| [siriuscc/TCM-Note](https://github.com/siriuscc/TCM-Note) | 73 | 2019 | 中 | 中医笔记与相关书籍合集 |
| [PanckooAI/TCM_Datasets](https://github.com/PanckooAI/TCM_Datasets) | 24 | 2025-04 | 中 | 中医书籍、文献等**高质量文本数据** |
| [xiaogege6697/tcm-db](https://github.com/xiaogege6697/tcm-db) | 14 | 2026-09 | 中 | 倪海厦中医知识数据库：**3,867 条 SQLite 结构化记录**（中药/方剂/医案/经典/针灸/天纪）+ 2,987 页 OCR 讲稿。**结构化程度最高，适合直接入库** |
| [Lance-myk/NiHaisha-Agent](https://github.com/Lance-myk/NiHaisha-Agent) | 11 | 2026-06 | 中 | 基于人纪六部构建的、有中医诊疗逻辑的 AI 顾问 |
| [l756302098/zhongyi_books](https://github.com/l756302098/zhongyi_books) | 3 | 2025-10 | 低 | 伤寒派及符合伤寒观点的后世医学著作 |
| [TCMExposed/SiteSource](https://github.com/TCMExposed/SiteSource) | 86 | 2019 | 低 | 「揭穿中医」网站源文件 —— **反方视角**，建知识库时建议正反都收 |
| 泛书源 | — | — | 中 | [Dujltqzv/Some-Many-Books](https://github.com/Dujltqzv/Some-Many-Books) ⭐25k、[jbiaojerry/ebook-treasure-chest](https://github.com/jbiaojerry/ebook-treasure-chest) ⭐22k、[kska32/ebooks](https://github.com/kska32/ebooks) ⭐7.3k（约 10 万本，含文史哲，需自行筛中医） |

---

## 6. 数据与知识库

> **本节结论**：预训练语料首选 **ShizhenGPT 6B token**；指令/对话数据首选 **TCMChat-600k**；真实病历只有 **TCM-Andrology-EMR** 一家（且非商用）；数据库权威性排序 **TCMSSD > HERB 2.0 > BATMAN-TCM 2.0**。

### 6.1 NLP 语料

| 资源 | 规模 / 说明 | 档 | 链接 |
|---|---|:--:|---|
| [Toyhom/Chinese-medical-dialogue-data](https://github.com/Toyhom/Chinese-medical-dialogue-data) ⭐1776 | 中文医疗对话数据集（非中医专用，但最常用） | B+ | GitHub |
| **ShizhenGPT 预训练语料** | **约 6B token**，含视觉/听觉对齐，目前最大开源中医预训练集 | **S** | [HF datasets](https://huggingface.co/datasets/FreedomIntelligence/TCM-Pretrain-Data-ShizhenGPT) |
| ShizhenGPT 指令数据 | 27K 条中医多模态指令微调数据 | A | [HF datasets](https://huggingface.co/datasets/FreedomIntelligence/TCM-Instruction-Tuning-ShizhenGPT) |
| **TCMChat-dataset-600k** | **60 万条**中药知识对话 | **S** | [HF datasets](https://huggingface.co/datasets/ZJUFanLab/TCMChat-dataset-600k) |
| TCM-Andrology-EMR | **中医男科真实门诊病历**：67,073 条原始记录 / 25,103 患者（2023-01～2026-09），其中 26,923 条四诊+诊断+处方齐全；462 味药、263 病名、499 证型、320 治法；患者 ID 已哈希脱敏。**CC BY-NC 4.0**（未做伦理审查与知情同意） | A | [HF datasets](https://huggingface.co/datasets/johnson/TCM-Andrology-EMR) |
| ShenNong_TCM_Dataset | 中医古籍 + 百科 + 医案混编预训练语料 | B+ | [HF datasets](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset) |
| Baize-TCM-Corpus V1–V3 | 中国中医科学院中药所中医问答语料，V3 与白泽模型配套 | A | [HF datasets](https://huggingface.co/datasets/DigitalIntelligenceCenter-of-ICMM/Baize-TCM-Corpus-for-Large-Language-Models-V3) |
| MedChatZH 问诊数据集 | 中西医问诊对话 | B+ | [HF datasets](https://huggingface.co/datasets/tyang816/MedChatZH) |
| neijing-sft-v1.2 | 杏核配套《内经》向 SFT 数据 | B | [HF datasets](https://huggingface.co/datasets/zsyjsld/neijing-sft-v1.2) |
| OnePO-Medical-20K | 华佗GPT-3 的医疗 RL 数据（10,191 选择题 + 10,147 开放题带 rubric） | A | [HF datasets](https://huggingface.co/datasets/FreedomIntelligence/OnePO-Medical-20K) |
| 传统方剂—疾病关系标注语料 | 生物医学文献标注的方剂↔疾病关系 | B+ | [Scientific Data](https://doi.org/10.1038/s41597-025-04377-2) |
| 针灸临床实践指南数据集 | 指南结构化后可直接临床用 | A | [Scientific Data](https://doi.org/10.1038/s41597-026-08112-3) |
| 中医药中英术语数据集 | 中英术语对照 | B | [DOI](https://doi.org/10.11922/csdata.2021.0009.zh) |
| Cross-linguistic TCM Formula Names | 方剂名**跨语言对照**（中文 / 日本汉方 / 韩国韩医 / 英文），xlsx | B+ | [Zenodo](https://zenodo.org/records/18724305) |
| 赵汉青门诊处方集（2025） | **单名医门诊处方，但许可与剂量字段最干净**：122 患者 / 335 首方 / **5,951 条药味记录，实测 100% 带 `dose_g` 克剂量**，另带 102 个证型、91 个病名、初诊 1,189 + 复诊 4,762、季节与节气、给药途径。**CC BY 4.0** | A- | [Zenodo 10.5281/zenodo.21947836](https://zenodo.org/records/21947836) |
| TCMCPD 中医病案 + 药理库 | 4,895 患者 / 12,900 就诊 / 703 味药，就诊-证候关联 11,879 条；**直接给 Neo4j 图文件**，省掉建库环节。**CC BY 4.0**（实测 Zenodo 200，11.7 MB）。同样**无疗效终点字段** | A- | [Zenodo 10.5281/zenodo.20929034](https://zenodo.org/records/20929034) |
| 古代经典名方关键信息表 | 官方三批（2020 年 7 首、2023 年 25 首、2025 年 43 首），逐味给基原、炮制规格、**折算剂量**与煎服法 | **A+** | 国家中医药管理局通知 |

### 6.2 图像 / 植物 / 药材

| 资源 | 说明 | 档 |
|---|---|:--:|
| **CHM-315** | 315 类常用中药材，126,000 张图（每类 400 张） [DOI](https://doi.org/10.6084/m9.figshare.32745123) | A |
| [winycg/TCMP-300](https://github.com/winycg/TCMP-300) ⭐13 | 中药材植物识别综合图像集（Scientific Data） | B+ |
| **Baize TCM Botanical Origin Images** | 药用植物**基原鉴定**图像（生境 / 原植物 / 药用部位 + 中英拉丁鉴定，依据中国药典、中国植物志、恩格勒系统） | A |
| [CS688/Acupuncture_points_datasets_face_and_ear](https://github.com/CS688/Acupuncture_points_datasets_face_and_ear) | 面 / 耳穴位关键点，labelme 格式 | B |
| [Ye-ChunZhe/DMDBAK](https://github.com/Ye-ChunZhe/DMDBAK) ⭐24 | 人体**背部穴位检测**算法评测基准 | B+ |
| **TongueBench** | 舌象 2,694 张 / 22 个标签，**CC BY 4.0**（Zenodo API 实测 200，670 MB）。⚠️ 标签是齿痕/裂纹/苔色**属性**，不是辨证证型 | A- |
| **TongueAtlas-4K** | 4,000 张临床舌象，中专家 22 类标注，**CC BY 4.0**（Zenodo API 实测 200） | A- |
| [Mark-CHAE/SM-Tongue-Public-Original512](https://huggingface.co/datasets/Mark-CHAE/SM-Tongue-Public-Original512) | 舌象**分割**数据集（512，1K–10K 张），ViTCM 团队配套。**CC BY-NC 4.0**，禁商用 | B+ |

> ⚠️ **舌象数据的关键限制**：以上公开集**全部是属性/分割标签，没有一个带"舌象 → 辨证证型"监督对**。想做"看舌辨证"只能自己标（见 11.1）。另外 `DUTC-TongueDatabase`、`TongueQC` 这两个常被论文引用的集子，在 GitHub / HuggingFace **均检索不到公开仓库实体**，引用前先确认拿得到。

### 6.3 成分–靶点–证候–毒性（数据库型）

| 库 | 内容 | 档 | 入口 |
|---|---|:--:|---|
| **TCM 症状本体 TCM-SO v4.10** | 中英双语 OWL 2 症状本体（8.3 MB），**带专家确认的三向国际术语映射**：ICD-11 974 行 / SNOMED CT 708 行 / HPO 650 行（实测行数）。是本文档里**唯一把中医症状对到国际编码**的公开资源。0 star 但工程完整（CITATION.cff + Zenodo DOI + BioPortal 提交指南）。⚠️ 仓库许可字段是 `NOASSERTION`，README 声明 CC-BY 4.0，商用前需确认 | **A** | [Pinellia7ternata/TCM-Symptom-Ontology-v4.10](https://github.com/Pinellia7ternata/TCM-Symptom-Ontology-v4.10) |
| **中医证候标准化数据库 TCMSSD** | **624 证候 / 133,518 首方剂 / 8,073 种疾病 / 8,259 味中药 / 43,413 个成分 / 17,602 个靶点**。⚠️ 只有站内浏览，**未找到整库下载入口**（2026-11-09 复核） | **S** | [tcmssd.ratcm.cn](http://tcmssd.ratcm.cn/) |
| **HERB 2.0 本草组鉴** | 整合临床试验、荟萃分析、高通量实验与文献的中药证据库 + 实体关系图谱 | **A+** | [herb.ac.cn/v2](http://herb.ac.cn/v2) · [NAR](https://doi.org/10.1093/nar/gkae1037) |
| **BATMAN-TCM 2.0** | 已知+预测中药成分–靶蛋白相互作用，支持由靶反查成分 | A | [batman-tcm](http://bionet.ncpsb.org.cn/batman-tcm/) · [NAR](https://doi.org/10.1093/nar/gkad926) |
| **TCMToxDB** | 中药毒性与安全使用，区分方剂/饮片/成分毒性，集成 5 种药-靶预测算法 | A | [TCMToxDB](https://www.sdu-idea.cn/TCMToxDB) |
| **CMAUP** | 有用植物（含中药）多靶点活性、通路与疾病景观 | B+ | [bidd.group/CMAUP](https://www.bidd.group/CMAUP/) |
| **中药植物基因组库 TCMPG 2.0** | 274 种植物 / 324 基因组 / 414 味药材 / 13,809 成分，含 BLAST、JBrowse | B+ | [TCMPG2](https://cbcb.cdutcm.edu.cn/TCMPG2/) |
| **中成药公开数据集 RAG-CPMF** | 持续更新的大规模中成药数据 | B+ | [gitee.com/tcmdoc/cpm](https://gitee.com/tcmdoc/cpm) |
| 中药扰动转录组图谱 | 中药处理转录组汇总，用于机制解释 | B | [Sci Data](https://doi.org/10.1038/s41597-026-06988-9) |
| 中药化学成分毒性实验库 | 体内/体外毒性实验记录（闹羊花、斑蝥、巴豆、洋金花、附子、轻粉等），含 LD50、靶器官、病理表现、PMID | A | [ScienceDB](https://doi.org/10.57760/sciencedb.015ml) |
| TCM-QM | 3,196 个中药相关分子的气相 DFT 描述符 + 16,918 条草药–分子来源关系 | B | [Zenodo](https://zenodo.org/records/22173180) |
| TCM-MS2Link | 中药–化合物知识层 + 质谱数据的统一可建模数据集 | B | [ScienceDB](https://doi.org/10.57760/sciencedb.31921) |
| 内蒙古民族药目录 | 医保收载民族药目录（蒙医成方为主，乙类） | C | 内蒙古医保局 PDF |

### 6.4 判断：哪些数据能直接用

| 用途 | 直接用 | 需处理 | 别用 |
|---|---|---|---|
| 预训练 | ShizhenGPT 6B / TCM-Ancient-Books | ShenNong（古籍+百科混编，需去重） | 泛书源（噪音太大） |
| 指令微调 | TCMChat-600k / ShizhenGPT-27K | Baize Corpus（需按 V1/V2/V3 对齐模型） | 社区未标注的 SFT |
| 真实临床 | TCM-Andrology-EMR（**仅非商用**） | 官方经典名方关键信息表（需结构化） | 医院产品宣传里的"数据集" |
| RAG 知识层 | TCMSSD / HERB 2.0 | BATMAN-TCM（需转成实体关系） | 未经核对的百科条目 |

---

## 7. 综述 / 专利 / 行业动态

> **本节结论**：写相关工作先读 7.1 的 8 篇综述，别从单篇模型论文起手；专利看的是"别人在占什么坑"；行业动态只看方向，别当可用资源。

### 7.1 综述（先读这些）

> 📥 **下载情况**：8 篇中 2 篇已抓到本地（`/tcm-reviews/`，含 PDF 与 OSF 全文导出），其余 6 篇为 CNKI 登录墙 / 出版社反爬，详见该目录 `README.md` 的逐篇获取途径。

| 综述 | 出处 | 我的判断 |
|---|---|---|
| 从大语言模型到智能体 —— 中医临床辅助诊疗中文系统综述 | 兰州大学学报医学版 2026;52(4):49-57 · [DOI](https://doi.org/10.13885/j.issn.2097-681X.T20260032) | **最贴合当前 Agent 方向**，中文写作可直接引用 |
| 中医大模型关键技术综述 | IJPRAI · [DOI](https://doi.org/10.1142/s0218001426590263) | 知识组织 / 辅助诊断 / 临床决策支持三条线梳理清楚 |
| AI 驱动中医诊断智能化综述 | JTCMS · [DOI](https://doi.org/10.1016/j.jtcms.2026.05.002) | 多模态融合 + 四诊智能化，做四诊必引 |
| 人工智能驱动下的中医智能诊疗研究进展与挑战 | 上海中医药杂志 2026;60(1) · [DOI](https://doi.org/10.16305/j.1007-1334.2026.z20250609004) | 以辨治六步程式为骨架，方法论视角 |
| 多模态大模型驱动舌脉面诊智能化综述 | Springer CCIS 书章 · [DOI](https://doi.org/10.1007/978-981-95-7299-1_15) | **唯一以「多模态 LLM × 四诊感知」为题** |
| AI 赋能中医数字化诊断：现状与挑战 | 中华中医药学刊（北大核心）· [DOI](https://doi.org/10.13193/j.issn.1673-7717.2026.01.004) | 现状盘点型，适合引言 |
| 面向临床的中西药联用安全性数智评价 | 中国科学通报 · [DOI](https://doi.org/10.1360/csb-2026-0084) | 中西药联用安全，少见的切入角度 |
| Agentic and Knowledge-Grounded LLMs in TCM | OSF 预注册方案 · [DOI](https://doi.org/10.17605/osf.io/kq8jx) | ⚠️ **非完成版综述**，只是研究方案，别当文献引用 |

### 7.2 专利（都在公开未授权阶段）

- CN122531762A 基于生成式模拟医案构建的定制化中医处方推荐大模型（北京中医药大学）
- CN122529089A 基于大语言模型的中医对话生成方法（杭州旺柴科技，长期记忆库 + 用户画像）
- CN122508432A 面向中医药知识图谱的综合质量评估方法（湖北省标准化与质量研究院）
- CN122436154A 张锡纯中医理法方药数字化传承与智能分析系统（辨病辨证规则 + 三路检索 + LLM）
- CN122436116A 基于知识图谱与 LLM 的脾胃学派理法方药分析系统（选方验证 + 安全校验 + 处方生成）

### 7.3 行业 / 机构动态（多数**未开源**）

- 2026.10 徐桂华团队「灵素·艾护」中医护理大模型，27 所加盟医院首批应用
- 2026.09 广安门医院「广医·岐智 2.0」，AI 医生「安安」覆盖六大场景
- 2026.09 北京中医药大学发布中医体质辨识体系 + 具身智能推拿机器人
- 2026.09 「方证大模型」开放接入，计划部署龙华医院及医联体
- 2026.08 广州中医药大学「杏林智慧教学大模型」（约 20 亿词元中医药数据）
- 2026.07 国家人工智能应用中试基地（医疗）集中发布中医经络辅诊模型、中医药高质量数据集、中药研发大模型、名中医数字智能体

### 7.4 判断

- **专利的用法是"避坑"而不是"学习"**：上面 5 件覆盖了处方推荐、对话生成、图谱质检、名家传承、学派分析 —— 恰好是创业最常见的 5 个方向。动手前先查一遍。
- 行业动态里的模型**一个权重都拿不到**，价值在于判断"哪家医院/学校在做哪个方向"，找合作或找数据时有用。

---

## 8. 场景选型（决策路径）

### 8.1 先问三个问题

```
Q1 你要的是「能力」还是「知识」？
   ├─ 能力（会辨证、会开方）→ 走模型路线 → 3.2 / 3.3
   └─ 知识（查得到、说得清）→ 走 Skill / RAG 路线 → 2.1 / 6.3

Q2 什么机器？
   ├─ DGX Spark（128G）→ 直接上 32B bf16 / 70B q4，见 3.8
   ├─ DGX Spark（64G）→ 14B bf16 / 27B q8，见 3.8
   ├─ 独显 ≥24G → BianCang-7B / Lingdan-8B / ShizhenGPT-7B
   ├─ 独显 12-16G → Xinghe-9B-GGUF / Lingdan-4B
   └─ 无独显 → Baize-0.6B / ZhongJing-1.5B（或直接上 API）

Q3 要商用吗？
   ├─ 要 → 只碰 Apache-2.0 / MulanPSL-2.0（BianCang、Lingdan-V2、nihaixia）
   └─ 不要 → 可用 CC BY-NC（man_medical、TCM-Andrology-EMR）
```

### 8.2 场景 → 路线

| 你的目标 | 建议路线 | 备选 |
|---|---|---|
| **笔记本 / 单机跑一个中医模型** | Xinghe 1.2-9B（GGUF）→ 再小上 ZhongJing-1.5B/1.8B 或 Baize-0.6B | 追求论文可复现选 BianCang 7B / Lingdan-8B |
| **有 DGX Spark，想跑满** | Lingdan-14B-SFT bf16 + ShizhenGPT-32B-VL（多模态）+ HuatuoGPT-3-27B（对照），见 3.8 | 8B 量化模型（浪费统一内存） |
| **要辨证 / 开方推理质量** | Lingdan-8B-R1（处方 GRPO；14B-R1 权重尚未发布） | HuatuoGPT-o1-8B（推理范式） |
| **做单科室 / 专科辨证开方** | 抄 [man_medical](https://github.com/johnson7788/man_medical) 的评测协议 | — |
| **给 Agent 加中医能力，不想训模型** | `TCM.Skill`（通识底座）+ `nihaixia`（经方视角） | 温病补 `wujutong`，扶阳补 `likeskill` |
| **做中医问诊对话产品** | MedChatZH（问诊数据 + 模型） | ShizhenGPT（要舌面脉多模态）+ RenShu-AI（多 Agent 编排） |
| **自己继续预训练 / SFT** | ChatTCM-7B-Pretrain 接着训 | 语料：TCM-Ancient-Books + ShizhenGPT 6B + TCMChat-600k |
| **搭 RAG / 知识图谱** | 架构抄 OpenTCM 的 GraphRAG | 数据：TCMSSD + HERB 2.0 + BATMAN-TCM 2.0；骨架：QASystemOnMedicalKG |
| **做科研（网络药理学）** | TCMNP(R) / HerbiV + TCMToxDB + CMAUP | — |
| **做辨证思维研究 / 写论文** | 先读 7.1 的 8 篇综述 | 基准用 TCM-Ladder + LingLan + MTCMB |
| **做多模态四诊** | ShizhenGPT-7B-Omni + 其 TCM Vision Benchmark | ViTCM-LLM（RAG 路线） |

### 8.3 三套开箱组合

| 组合 | 组成 | 适合 |
|---|---|---|
| **A. 学习型**（零训练） | `TCM.Skill` + `nihaisha-nishi-tcm` + `my-TCM-textbook-website` | 个人学习、临床参考、教学 |
| **B. 实验型**（单卡） | BianCang-7B + TCM-Ladder + TCM-Ancient-Books | 论文复现、毕业设计 |
| **C. 产品型**（要上线） | Lingdan-V2（Apache-2.0）+ OpenTCM 架构 + TCMSSD/HERB 数据 + `nihaisha-renji`(MCP) | 商用落地 |

---

## 9. 避坑清单

### 9.1 许可与合规

1. **代码许可 ≠ 权重许可**。中医模型常见「代码 Apache-2.0 / 数据与权重 CC BY-NC 4.0」混搭（`man_medical`、`TCM-Andrology-EMR`、`TCM-Qwen2.5-7B-SFT`）—— 代码能用不等于权重能商用。
2. **教材/视频仓库多数没有 LICENSE**（`hantang-nihaixia-follower`、`Traditional-Chinese-Medicine-nihaisha`）。自用可以，对外服务前逐仓确认。
3. **真实病历数据集可能未过伦理**：`TCM-Andrology-EMR` 明确写了"伦理审查与患者知情同意未做"。
4. 可商用的安全选择：`nihaixia`（MulanPSL-2.0，需保留声明）、`Lingdan-V2`（Apache-2.0）。

### 9.2 医学与安全

1. **Skill 输出是"某医家的辨证思路"，不是诊断结论**。经方剂量、附子细辛类有毒药物尤其要人工把关。
2. **模型自己生成的剂量不可信**：`man_medical` 明确不生成剂量，并警告"任何剂量输出都应丢弃"。补充 2026-11-09 核实：这**不是因为没有带剂量的数据**，而是量太少 —— 赵汉青处方集 5,951 条药味实测 100% 带 `dose_g`（见 6.1），但只有 335 首方，撑不起剂量学习；公开侧**没有**汉代度量衡折算数据，经方 Skill 各自的换算口径互不相同。
3. **争议内容要标注来源**：倪海厦对现代医学的批评属"一家之言"，`nihaisha-skill` 的 `POLICY.md` 强制标注，这是正确做法。
4. **急症一律转诊**，任何 Skill 都不该给"家庭解毒方案"。

### 9.3 评测与方法论

1. **分数不可跨表比较**：各家中医 benchmark 口径不一。
2. **同源数据自测 = 分数虚高**：多数中医 LLM 用古籍 + 百科 + 医案混编预训练，评测集若同源就失真。
3. **看有没有做患者分组切分**：这是区分"能发论文"和"能上线"的关键指标，目前只有 `man_medical` 做全了。
4. **复诊任务别用模型**：`man_medical` 实测复诊 Jaccard 0.501 < 直接照抄上次处方 0.542 —— 结构性事实，不是训练不足。

### 9.4 星标与热度陷阱

| 陷阱 | 实例 |
|---|---|
| **fork 刷星** | `3150214587/niehaixia` ⭐83，实为 nihaixia 旧版 fork |
| **同模板连带** | `jangviktor-web` 6 个中医 Skill 共享 star 势能，不代表各自被验证 |
| **老项目惯性** | `Huatuo-Llama-Med-Chinese` ⭐5001 但停在 2023，底座已落后两代 |
| **低星高质量** | `Lingdan-V2` ⭐3、`man_medical` ⭐1、`nihaisha-skill` ⭐8 —— 都是本文档里质量最高的 |

> **结论**：中医开源圈里，star 与实际质量**弱相关**。判断依据应该是"有没有权重 / 有没有评测协议 / 有没有许可"。

### 9.5 网络与工具链

1. **`raw.githubusercontent.com` 直连超时**（Fastly 185.199.x）。抓 README 用 API：

   ```bash
   curl -s -H "Accept: application/vnd.github.raw" \
     https://api.github.com/repos/<owner>/<repo>/readme
   ```

   拉整包用 codeload tarball 比 `git clone` 稳。

2. **HuggingFace 需走镜像**：`huggingface.co` 直连不通（curl 返回 000），`hf-mirror.com` 正常。

   ```bash
   export HF_ENDPOINT=https://hf-mirror.com
   curl -s "$HF_ENDPOINT/api/models?search=TCM&limit=20&sort=downloads&direction=-1"
   ```

3. **分辨 gated 与"仓库不存在"，别信 `api/models` 的状态码**：镜像对 gated 的 `meta-llama/Llama-3.1-8B-Instruct` 返回 **200**，对已消失的 `tczzx6/ZhiFangDanTai1.0` 返回 **404**，而对任何仓库都会随机吐 429 —— 单看这个接口分不出"gated"和"没了"。两条可靠判据：

   ```bash
   # 判据一：下载仓库里的文件。README.md 404 = 仓库不存在；config.json 403 = gated；302/307/200 = 可下载
   curl -s -o /dev/null -w '%{http_code}\n' -L "$HF_ENDPOINT/<owner>/<repo>/resolve/main/README.md"
   curl -s -o /dev/null -w '%{http_code}\n' -L "$HF_ENDPOINT/<owner>/<repo>/resolve/main/config.json"

   # 判据二：列组织下的仓库。gated 仓库照常出现在列表里（meta-llama 实测如此），
   #         所以"列表里没有"就是真没发布，比 README 的 Model Zoo 表可信
   curl -s "$HF_ENDPOINT/api/models?author=TCMLLM&limit=100" | jq -r '.[].id'
   ```

   实测对照（2026-11-09）：`CMLM/ZhongjingGPT1_13B` → cfg 403 = gated（与本文档一致）；`meta-llama/Llama-3.1-8B-Instruct` → cfg 403 = gated；`TCMLLM/Lingdan-14B-SFT` → 302/307 = 可下载；`TCMLLM/Lingdan-14B-R1` → **README 404 = 权重从未发布**（见 3.2）。按同一判据，原先标"gated / API 401"的 **`tczzx6/ZhiFangDanTai1.0` 也是 404**（`search=ZhiFangDanTai` 命中 0 条、作者名下只剩 `LLM-SAGE`），仓库已失效，见 3.3 / 3.4。

4. **GitHub 搜索噪音大**：直接搜「中医」前 15 名基本被 funNLP / awesome-* 占据。用 `topic:tcm`、`中医 in:name,description` 收窄。
5. **DGX Spark 的 CUDA 版本坑**：当前栈是 DGX OS 7.6.0 / 驱动 580 / **CUDA 13.0.3**，需 sm_121 支持。pip 直装的 torch / vLLM 常常没有对应轮子，**优先用 NGC 容器**；自己编 llama.cpp 要加 `-DCMAKE_CUDA_ARCHITECTURES=121`。另外 `nvidia-smi` 会显示 `Memory-Usage: Not Supported`（UMA 预期行为，不是故障），别写脚本依赖它。细节见 3.8。

---

## 10. 论文与范式（2026-11）

> **本节结论**：截至 2026-11-04 的公开检索，中医大模型论文与 Agent Skill 论文基本是两条平行线：模型侧已覆盖 CPT/SFT/RL、RAG/KG、多模态四诊、评测与真实临床对比；Skill 侧在 2025-10 出现 SKILL.md 格式后，2026 年迅速形成技能库 / 技能评测的独立文献，但都不针对中医。公开检索里最接近交叉的是 **TCM-SEA**（让 agent 在失败病案后改写自己的「临床 skill 文档」）；从摘要看它把 skill 写成自然语言文档，未提 SKILL.md 规范，论文重点是病案 benchmark 与自我修订，不是技能库/安全审计。

### 10.1 先回答：结合了吗？

| 层次 | 现状 | 代表 |
|---|---|---|
| 论文层 | 两边几乎没有交集：本轮检索未发现 TCM 模型论文把 Agent Skill 作为变量，也未发现 Skill 评测论文包含中医任务 | 2602.12430、2607.10113、2608.10906 vs 2610.14705、2610.38333、2610.40663 |
| 模型层 | 已 agent 化，但 skill 多以 tool / memory / workflow 实现，不是可复用技能包 | Jingfang（2502.04345）、DeepTCM1.0（2608.18103）、TCMScience（2610.24601） |
| 工程层 | nihaixia / TCM.Skill 等 skill 仓库目前没看到对应论文与量化评测；模型论文也不把 skill 作为评测项 | 本文档 §2 |

**判断**：按上述渠道检索，没有一篇同行评议论文系统回答「TCM LLM + Agent Skills」的效用、安全与成本。三个空白：① 没有 TCM 版 skill 评测；② 没有 TCM skill 数据集；③ 没有 skill + model + KG/RAG 的消融。TCM-SEA 是目前最接近的尝试，但从摘要看它把 skill 写成自然语言文档，未提 SKILL.md 规范，也未给出技能级评测协议。

**检索边界**：arXiv、Crossref、PubMed 可机器检索；CNKI / 万方有登录墙，本轮只按题录与摘要核对，不保证穷尽中文期刊与硕博论文。

### 10.2 论文从哪来：渠道矩阵

| 渠道 | 看什么 | 适合 | 注意 |
|---|---|---|---|
| arXiv | cs.CL / cs.AI / cs.LG / cs.CV / q-bio.QM 预印本 | 追最新（TCM 论文大多先上 arXiv） | 未同行评议；以 v1 日期为准 |
| OpenReview | ICLR / NeurIPS / TMLR 投稿、评审、rebuttal | 看方法争议与审稿意见 | 不是所有会议都用 |
| ACL Anthology | ACL / EMNLP / NAACL / COLING | NLP 主会与 Findings | 页码稳定，适合引用 |
| ML 会议 | NeurIPS / ICLR / ICML / AAAI / IJCAI / KDD / WWW | 方法创新 | 医学落地论文少 |
| 医学 / 生信 | IEEE BIBM、AMIA、ACM BCB、MICCAI；JBI、JAMIA、npj Digital Medicine、Lancet Digital Health | 临床、评测、真实世界 | 周期长、门槛高 |
| 中医期刊 | Chinese Medicine、JTCMS、中华中医药杂志、中国中医药信息杂志、上海中医药杂志、南京/北京中医药大学学报 | 中文临床与理论 | 多在 CNKI / 万方，需机构权限 |
| 索引 / 追踪 | PubMed、Semantic Scholar、Google Scholar、dblp、Papers with Code、HF Papers、alphaXiv、Connected Papers | 引文追溯、找同作者 | Google Scholar 噪音大；注意预印本与正式版混排 |
| 其他 | medRxiv / bioRxiv、SSRN / Research Square、CNIPA 专利、会议 accepted lists、实验室 blog、X/Twitter、机器之心/量子位、GitHub awesome lists | 灰色文献与行业动态 | 只作线索，回到原文核对 |

**检索模板**

```bash
# arXiv API：标题/摘要里同时出现 TCM 与 LLM/agent/skill
curl -s "https://export.arxiv.org/api/query?search_query=all:%22traditional%20Chinese%20medicine%22%20AND%20all:%22large%20language%20model%22&sortBy=submittedDate&sortOrder=descending&max_results=50"
# 其他组合
# all:"TCM" AND all:"agent"
# all:"agent skills" AND all:"medical"
```

- Google Scholar：`"traditional Chinese medicine" "large language model" after:2024`、`"agent skills" "clinical" after:2025`
- PubMed：`("Medicine, Chinese Traditional"[Mesh]) AND ("Large Language Models"[Mesh])`
- ACL Anthology：`https://aclanthology.org/search/?q=TCM`
- 中文：CNKI / 万方 / 维普检索 `中医 大模型`、`中医 智能体`、`辨证论治 大语言模型`；硕博论文的综述章节往往比期刊更全

### 10.3 基本范式：八条路线

| 范式 | 代表工作 | 做法 | 强项 | 主要坑 |
|---|---|---|---|---|
| **① 领域 CPT + SFT + RL** | Qibo（2403.16056）、BianCang（2411.11027）、Tianyi（2505.13156）、Lingdan-V2（2610.14705）、GRPO-TCM（2510.17402）、TianHui（2509.19834） | 2GB~16.6B token 领域 CPT → SFT → RLAIF / GRPO / 处方 RL | 知识注入、术语与风格、处方对齐 | 数据质量与许可、灾难遗忘、评测不同源 |
| **② 结构化推理 / 方证链** | Syndrome/Synergy/Safety（2609.25755）、CORE-Acu（2603.08321）、DoPI（2507.04877）、TCM-DiffRAG（2602.22828） | PG-CoT / S-CoT、KG 约束、规则 DPO、多轮问诊 | 可审计、可解释、能编码禁忌 | schema 与标注成本高、覆盖不全 |
| **③ RAG / KG grounding** | ZhiFangDanTai（2509.05867）、DiagnosGraph（2504.07724）、LingShu（2608.20402）、MMIR-TCM（2607.01814） | GraphRAG、多轮检索、症状中心 KG、引用溯源 | 知识新鲜、可溯源、训练成本低 | 检索质量、KB 覆盖、延迟 |
| **④ 多模态四诊** | ShizhenGPT（2508.14706）、LingLan（2609.25715）、Fu-TCM（2610.38333） | 舌/面/脉/声 + 文本对齐、视觉指令、BGPO | 接近真实四诊流程 | 数据/设备/隐私、模态对齐、评测难 |
| **⑤ Agent / Skill / tool** | Jingfang（2502.04345）、DeepTCM1.0（2608.18103）、TCMScience（2610.24601）、TCM-SEA（2610.40663）、Med-Shicheng（2603.23520）；通用侧见 2602.12430、2603.28815、2606.20659、2604.20441 | 多 agent 角色、工具注册、技能库、记忆、自我修订 | 模块化、可复用、可审计 | skill 质量与安全无标准、缺 TCM 基准 |
| **⑥ 评测基准** | TCM-Ladder（2505.24063）、LingLanMedBench（2602.01779）、MTCMB（2506.01252）、TCMBench（2406.01126）、TCM-3CEval（2503.07041）/5CEval（2511.13169）、TCM-Eval（2511.07148）、TCMClinicalReason-Bench（2610.04215） | 考试题 → 临床推理 → 患者分组 / Oracle / 安全 | 可比、可复现 | 污染、同源数据、分数不可跨表 |
| **⑦ 数据 / 合成 / 蒸馏** | ShizhenGPT（100GB 文本 + 200GB 多模态）、Lingdan（16.6B CPT token）、ChiMed 2.0（2507.15275）、TCM-Eval SI-CoTE、TCM-FTP DigestDS（2407.10510） | 古籍/教材/EMR/合成/教师蒸馏 | 规模与覆盖 | 版权、隐私、去重、蒸馏污染 |
| **⑧ 真实世界临床验证** | Tianyi（2505.13156）、LLMs vs Physicians（2609.17544）、TCMClinicalReason-Bench（2610.04215） | 多中心病例、医生盲评、处方级指标 | 接近临床 | 样本量、伦理、缺前瞻试验 |

**读法**：①—④ 是「模型怎么做」，⑤ 是「系统怎么组织」，⑥—⑧ 是「怎么证明有用」。目前论文集中在 ①③④⑥，⑤ 最热但最不成熟，⑧ 最缺。

### 10.4 必读论文清单

> 综述先看 §7.1；这里只列 primary papers，链接以 arXiv 为准，已发表版本在备注里标 DOI。

**TCM 侧（按时间倒序）**

| 论文 | 时间 | 类型 | 一句话 | 链接 |
|---|---|---|---|---|
| Fu-TCM | 2026-10 | 多模态 + BGPO | 7.12M 样本、27B，六个 TCM benchmark 领先 | [2610.38333](https://arxiv.org/abs/2610.38333) |
| Lingdan-V2 | 2026-10 | 模型 + RL | 4B/8B/14B，CPT + 推理监督 + 处方 RL | [2610.14705](https://arxiv.org/abs/2610.14705) |
| TCM-SEA / TCM-MisDx | 2026-10 | Agent + skill | 失败病案后自我改写临床 skill 文档；820 例 benchmark | [2610.40663](https://arxiv.org/abs/2610.40663) |
| TCMScience | 2026-10 | Agent | 117 个公共数据源连接器、444 个类型化操作 | [2610.24601](https://arxiv.org/abs/2610.24601) |
| TCMClinicalReason-Bench | 2026-10 | 评测 | 2,000 例多中心 EHR；七段推理 + 临床医生盲评 | [2610.04215](https://arxiv.org/abs/2610.04215) |
| Syndrome, Synergy, Safety | 2026-09 | 处方 + RL | SFT → PG-CoT → Dynamic → K-RL，编码十八反等禁忌 | [2609.25755](https://arxiv.org/abs/2609.25755) |
| LingLan | 2026-09 | 多模态 | 舌/脉图像转结构化四诊记录，LingLan-14B | [2609.25715](https://arxiv.org/abs/2609.25715) |
| LLMs vs Physicians | 2026-07 | 临床对比 | 349 例、16 个 LLM vs 60 位中医师；处方与安全仍有差距 | [2609.17544](https://arxiv.org/abs/2609.17544) |
| LingShu | 2026-07 | KG | 症状中心 KG，连接中医与现代生物医学 | [2608.20402](https://arxiv.org/abs/2608.20402) |
| DeepTCM1.0 | 2026-06 | 多专家 Agent | 用通用 LLM 做方剂机制解析 | [2608.18103](https://arxiv.org/abs/2608.18103) |
| MMIR-TCM | 2026-07 | 多模态 + RAG | Memory-SAM 舌象 + Qwen3-VL + RAG | [2607.01814](https://arxiv.org/abs/2607.01814) |
| DongYuan | 2026-03 | 中西医结合 | 脾胃病 ICWM 数据集 + SSDF-Core | [2603.28191](https://arxiv.org/abs/2603.28191) |
| CORE-Acu | 2026-03 | 针灸 + KG | 结构化推理链 + KG 安全校验 | [2603.08321](https://arxiv.org/abs/2603.08321) |
| TCM-DiffRAG | 2026-02 | RAG | KG + CoT 的个性化辨证 | [2602.22828](https://arxiv.org/abs/2602.22828) |
| LingLanMedBench | 2026-02 | 评测 | 25,620 题、13 子任务、5 领域 | [2602.01779](https://arxiv.org/abs/2602.01779) |
| TCM-5CEval | 2025-11 | 评测 | 知识 / 经典 / 临床 / 本草 / 非药物五维 | [2511.13169](https://arxiv.org/abs/2511.13169) |
| TCM-Eval | 2025-11 | 评测 + 数据 | 动态题库 + SI-CoTE + ZMT | [2511.07148](https://arxiv.org/abs/2511.07148) |
| ShizhenGPT | 2025-08 | 多模态 | 100GB 文本 + 200GB 多模态（舌/脉/面/声） | [2508.14706](https://arxiv.org/abs/2508.14706) |
| TCM-Ladder | 2025-05 | 评测 | 首个中医多模态 QA 基准 | [2505.24063](https://arxiv.org/abs/2505.24063) |
| Tianyi | 2025-05 | 模型 + 临床 | 7.6B，读书—临证—跟师 + 真实世界验证；Information Fusion 2026 | [2505.13156](https://arxiv.org/abs/2505.13156) · [DOI](https://doi.org/10.1016/j.inffus.2025.103663) |
| Jingfang | 2025-02 | 多智能体 | 专科 agent 协作 + 辨证 | [2502.04345](https://arxiv.org/abs/2502.04345) |
| BianCang | 2024-11 | 模型 | 两阶段 CPT + SFT；JBHI 2025 | [2411.11027](https://arxiv.org/abs/2411.11027) |
| Qibo | 2024-03 | 模型 | 2GB 语料 CPT + SFT；ESWA 2025 | [2403.16056](https://arxiv.org/abs/2403.16056) · [DOI](https://doi.org/10.1016/j.eswa.2025.127672) |
| MedChatZH | 2023-09 | 问诊 | 中医书籍预训练 + 问诊指令微调 | [2309.01114](https://arxiv.org/abs/2309.01114) |

**AI / Skill 侧（按主题）**

| 论文 / 资源 | 时间 | 主题 | 一句话 | 链接 |
|---|---|---|---|---|
| Agent Skills for LLMs | 2026-02 | 综述 | SKILL.md、渐进披露、MCP、技能获取与安全 | [2602.12430](https://arxiv.org/abs/2602.12430) |
| Dynamic Agent Skills | 2026-07 | 综述 | 124 篇 2023-2026 的技能库生命周期与分类；TMLR 2026 | [2607.10113](https://arxiv.org/abs/2607.10113) |
| GitSkills | 2026-08 | 数据集 | 282,200 个仓库、3,797,117 个 SKILL.md（2026-07） | [2608.10906](https://arxiv.org/abs/2608.10906) |
| SkillTester | 2026-03 | 评测 | 技能效用 + 安全评分 | [2603.28815](https://arxiv.org/abs/2603.28815) |
| Skill Coverage | 2026-06 | 评测 | 用轨迹覆盖约束衡量技能是否被真正执行 | [2606.20659](https://arxiv.org/abs/2606.20659) |
| MedSkillAudit | 2026-04 | 医学技能审计 | 75 个医学研究 skill 的发布前审计 | [2604.20441](https://arxiv.org/abs/2604.20441) |
| SAGE | 2025-12 | RL + 技能库 | 用 GRPO 让 agent 在任务链中积累技能 | [2512.17102](https://arxiv.org/abs/2512.17102) |
| SkeMex | 2026-06 | 医学技能记忆 | 把交互轨迹蒸馏为可复用技能，不更新权重 | [2606.09365](https://arxiv.org/abs/2606.09365) |
| MCP medical | 2025-09 | 工具协议 | 用 MCP 做医学概念标准化，零训练 | [2509.03828](https://arxiv.org/abs/2509.03828) |
| ClinVerse | 2026-10 | 多 agent 环境 | 150k 真实 EHR 病例的诊断训练/评测环境 | [2610.34878](https://arxiv.org/abs/2610.34878) |
| Baichuan-M4 | 2026-06 | 临床 agent 系统 | 连续照护、工具层、患者记忆、多 agent | [2606.08982](https://arxiv.org/abs/2606.08982) |
| ReflecTool | 2024-10 | 工具增强临床 agent | 长记忆 + 工具经验；ACL 2025 | [2410.17657](https://arxiv.org/abs/2410.17657) |
| Learning to Be A Doctor | 2025-04 | Agent 架构搜索 | 自动设计医疗 agent 工作流；ACM MM 2025 | [2504.11301](https://arxiv.org/abs/2504.11301) |
| LongMedBench | 2026-07 | 长程评测 | 335 患者、19.72 次就诊/人 | [2607.09322](https://arxiv.org/abs/2607.09322) |
| Agent Hospital | 2024-05 | 模拟环境 | 可演化医疗 agent 的医院模拟器 | [2405.02957](https://arxiv.org/abs/2405.02957) |

**基础三篇**（只补 AI 背景时看）：ReAct（[2210.03629](https://arxiv.org/abs/2210.03629)）、Toolformer（[2302.04761](https://arxiv.org/abs/2302.04761)）、Voyager（[2305.16291](https://arxiv.org/abs/2305.16291)）；RAG 侧加 GraphRAG（[2404.16130](https://arxiv.org/abs/2404.16130)）、MedRAG（[2402.13178](https://arxiv.org/abs/2402.13178)）。

### 10.5 缺口与可做的题

| 缺口 | 具体表现 | 可做的题 |
|---|---|---|
| 没有 TCM 版 skill 评测 | SkillTester / Skill Coverage / MedSkillAudit 都不含辨证、方证、禁忌 | **TCM-SkillBench**：50-100 个 SKILL.md（六经辨证、方证鉴别、四诊采集、十八反十九畏、妊娠禁忌、毒性药剂量），比较 no-skill / RAG / skill / skill+RAG；指标 accuracy、citation、safety、token、latency |
| 没有 TCM skill 数据集 | GitSkills 379 万条里中医占比未知；nihaixia / TCM.Skill 未进论文 | **TCM skill 审计**：把 MedSkillAudit + SkillTester 迁到中医，加入法规/毒性/剂量红线与红队测试 |
| 没有 skill + model + KG 的消融 | 模型论文不比 skill，skill 仓库不比模型 | **Skill + KG + agent**：把 LingShu KG、TCM-DiffRAG 与 SKILL.md 组合，在 TCM-Ladder / LingLanMedBench + 真实病案上做消融 |

**投稿方向**：ACL / EMNLP / ACL Findings、AMIA、JBI、IEEE BIBM、JAMIA、npj Digital Medicine；技能方向可投 Agent Skills '26 workshop。**注意**：临床安全、数据许可、患者隐私、预注册；预印本不能当临床证据。

---

## 11. 还缺什么：资源与信息缺口（2026-11-09）

> **本节结论**：前 10 节回答"有什么"，本节回答"还缺什么"。缺的**不是模型数量**——能跑的权重已经 20+ 个。真正卡住三件事：① **证候级标注的四诊数据**（有图像没标签）；② **带疗效终点的队列**（有病历没结局）；③ **能一键跑分的评测 harness**（有基准没框架）。另有一层**行业标准与监管文本**根本不在 GitHub / HuggingFace 上，拿不到就只能人工誊录。
>
> 与前面各节一样，下面每条都标了**实测方式**。"真空缺"= 我用列出的关键词在列出的平台检索过且为空，不是"我没找到"。

### 11.1 真空缺（实测为空）

| 缺口 | 实测方式与结果 | 为什么关键 | 能不能自己补 |
|---|---|---|---|
| **脉象数据集**（脉波信号 + 浮沉迟数标签） | HF datasets 搜 `pulse` / `pulse diagnosis` / `sphygm` / `pulsiology`：0 条中医结果；GitHub `脉象` 只命中仪器 demo 仓库（`PulseInstrument` 无数据、`tcm-pulse-kit` 是工具包）。Awesome-TCM-LLM 的 71 条数据集里也没有脉象 | 3.7 把"舌/脉/面"当成一个整体推荐，但**脉这一路其实无数据可复用**；脉诊仪数据全在道生、依脉等厂商手里 | **不能**，只能谈采购或合作。写方案时别把"四诊开源"当成四样都有 |
| **舌象 → 证候标签** | 属性级数据集有：[TongueBench](https://zenodo.org/records/20701289)（Zenodo API 实测 200，**CC BY 4.0**，2,694 图 / 22 标签）、[TongueAtlas-4K](https://zenodo.org/records/17557646)（实测 200，CC BY 4.0，4,000 张）；HF `Mark-CHAE/SM-Tongue-Public-Original512`（265 下载，CC BY-NC 4.0，分割任务）。**但标签全是齿痕/裂纹/苔色属性，没有一个带辨证证型** | ShizhenGPT 是唯一开源四诊多模态，但要做"看舌→辨证"的训练，公开集喂不出来 | **半能**：属性图现成，缺的是中医标注预算，不是图 |
| **疗效 / 结局终点** | 多就诊序列有（见 6.1 赵汉青处方集、TCMCPD、`TCM-Andrology-EMR` 初/复诊切分），但三个都**没有疗效字段** | 这是本文档最重的一条缺口：没有结局数据，模型只能证明"开得像一个医生"，**永远证明不了"有效"**。所有"超过医师"的说法都卡在这 | **不能**，要队列。见 11.5 RWE |
| **经方剂量折算标准数据**（汉代一两 = ? 克） | GitHub `经方 剂量` 只命中 Skill 提示词仓库（`likeskill`、`huxishu`），**零数据集零工具**；英文 `han dynasty dosage chinese medicine` 0 命中 | 经方派绕不开换算，3 家 skill 各有各的口径，AI 只能"挑一个信仰"而不是"查一个标准" | **能**：这是文献整理活，做出来就是全行业引用点 |
| **证候/方剂 → 标准编码映射表**（ICD-11 TM2） | HF `ICD-11` 命中的全是西医资源；GitHub `ICD-11 traditional chinese medicine` 0 命中；TCMSSD 只有站内浏览无整库下载。**但见 6.3 的 TCM-SO，已把 ICD-11 / SNOMED / HPO 映射做出来了** | 要和 HIS / 科研数据库对接、要发国际期刊的可复现标签体系，都需要编码映射 | **已部分解决**，见 11.2 |
| **多轮真实问诊对话** | HF datasets 搜 `tcm-dialogue` / `tcm-inquiry` / `TCM-consult`：**全部 0 条** | 中医问诊是"问→答→追问→改判"，单轮 QA 训不出主动追问能力；而 Agent 化产品恰恰需要这个 | **能**：可在既有病历上构造，但需医生复核 |

### 11.2 本轮挖出来、已并入前文的可用资源

这几条之前不在文档里，是这一轮检索的实际增量，已分别加进 3.6 / 6.1 / 6.2 / 6.3：

1. **Med-Bench-Arena**（评测 harness，见 3.6）—— 补齐"缺框架"这条最关键的缺口。**我 clone 下来实际跑通了**，`python -m medeval run configs/example_smoke.yaml` 在无 GPU、无 API key、无网络下出了 leaderboard。
2. **TCM-Symptom-Ontology v4.10**（见 6.3）—— 0 star 但带 ICD-11 / SNOMED CT / HPO 三向映射（实测 974 / 708 / 650 行），正是 11.1 那条"标准编码映射"缺口的答案。
3. **赵汉青处方集**（见 6.1）—— 我下载解开验证过：**5,951 行药味记录 100% 带 `dose_g` 克剂量**，且带证型（102 个）、病名（91 个）、初诊/复诊标记，CC BY 4.0。规模小（122 患者 / 335 方），但它是本轮实测里**唯一"许可干净 + 每味药都有克数"**的公开处方集（我没有穷举全部数据集，所以这是"没找到第二个"而不是"确定只有一个"）。
4. **TCMCPD**（见 6.1）—— Zenodo 实测 200，CC BY 4.0，11.7 MB，直接给 Neo4j 图文件。

### 11.3 评测层：缺的是跑分框架，不是题目

3.6 收了 8 个基准，但按"能不能跑"重新核一遍，结论比文档里更严峻：

| 基准 | 实测维护状态 | 能不能直接跑分 |
|---|---|---|
| TCM-Ladder | 最后实质提交 **2025-05-23**（2025-10 只改过 README） | 脚本 + 数据级，非统一框架 |
| TCM-Eval（`Zescy1/TCM-Eval`） | OpenCompass 改版，1⭐，最后提交 2026-01-24 | 是唯一"真框架"，但近乎弃坑 |
| LingLan | 最活跃（2026-10-19），但近期 commit 全是 README；**默认分支是 `master` 不是 `main`**（用 `main` 取树会 404） | 数据在仓库里（实测 32 个 jsonl / 34 MB，`data/LICENSE` = CC-BY-4.0），**打分代码弱** |

**补上缺口的是 [pariskang/Med-Bench-Arena](https://github.com/pariskang/Med-Bench-Arena)**（MIT，2026-06 创建）——同一作者 pariskang 就是 3.2 仲景 CMLM-ZhongJing 的作者：

- 40+ 基准接任意后端，**中医是一等公民**：辨证证型链（症状→病机→证型，带同病异治部分给分）、方剂君臣佐使结构匹配、经络腧穴、舌象/脉象、名老中医医案，评分方式各不相同，不是统一塞给 LLM-judge 打总分。
- 正面回应了本文档的铁律（0.2 判断 #3「分数不可跨表比较」）：结果行带 `split_type`（`official` / `validation` / `demo` / `sample` / `gated` / `approximated`），榜单把"官方可比较"和"内部不可比较"分开渲染；headline 基准钉死 revision commit。
- **诚实度是同类里最高的**：自己文档写明 `TCMEval-SDT` 只有 Train 的 200 条有 gold（Test/Val 是空的）、`TCMBench` 全库 gated 只有 14 条 demo、`MTCMB` 无医生标签所以开放题只算辅助分。也给了 `medeval calibrate` 让 judge 先对医生标签校准（κ ≥ 0.40 才有资格当主分）。
- **别高估的部分**：README 宣传的"可下载古籍知识图谱"实测只有 **116 节点 / 157 边**，是示例文件不是可用资产；4⭐ 说明社区还没验证过它。

**还差的最后一环**：所有中医开放题都需要医生标签来校准 judge，而公开数据里**没有中医医生标注的 meta-eval 集**（`data/calibration/` 用的是 HealthBench 西医医生标签）。攒一套 200 条中医开放题的医生评分，是投入产出比最高的自建资产。

### 11.4 Skill 层：零质量信号，但通用工具刚好出现了

第 2 节收了 40+ 个中医 Skill，第 10 节自己也指出"没有 TCM 版 skill 评测"。到现在，**中医 Skill 依然没有任何一个提供质量信号**（3898⭐ 的 nihaixia 也只有下载量，没有准确率）。

但通用侧的 Skill 评测工具刚好补齐了，可以直接拿来测中医 Skill，不必从零造轮子：

| 工具 | ⭐ | 许可 | 实测 |
|---|---:|---|---|
| [edonadei/caliper](https://github.com/edonadei/caliper) | 229 | **MIT** | 专测 skill 是否真的有用：`false-success` / `tool-misuse` / `runaway-loops` / `prompt-regression` / `context-boundary` 六类样例；最近提交 **2026-11-09（当天）**，已发 PyPI（`caliper-eval`） |
| [huggingface/upskill](https://github.com/huggingface/upskill) | 763 | **Apache-2.0** | 生成 + 评测 agent skill |
| [DeadHead04/skillEd](https://github.com/DeadHead04/skillEd) | 70 | Apache-2.0 | skill 评测 CLI + MCP |

**可执行的最小动作**：用 caliper 给 nihaixia 和 TCM.Skill 各跑一轮 `false-success` + `prompt-regression`，把结果贴回各自 README。这是本清单里唯一"今天就能做、且立刻改变选型依据"的一条。

### 11.5 行业侧信息缺口：GitHub 上根本没有的三层

这三层不在仓库里，**拿不到不会让代码报错，但会让方案和论文整体作废**，且第 1 / 7 / 9 节均未覆盖：

| 层 | 现状（核实结论） | 拿不到的后果 |
|---|---|---|
| **监管口径** | 中医 AI **未查到任何"国械注准"三类证**；已获证的全是省局二类（如苏械注准 20252211492 南京大经"中医舌面图像处理分析软件"，适用范围明示**"不含自动诊断"**）。依据是 NMPA 2021 年第 47 号《人工智能医用软件产品分类界定指导原则》（辅助诊断/治疗决策→三类）；《医疗器械分类目录》子目录 20"中医器械"虽列脉诊/望诊设备（Ⅱ类），但明文**"不包括中医独立软件"**。华为神农大脑、问止中医大脑、脉景黄煌经方 AI 均查无注册证 | 只要产品说"辅助辨证/开方"并按此进医院收费，二类证不够用，三类要 2-3 年临床验证。**现阶段所有中医大模型实际都是以"非医疗器械"身份落地**，商业计划里别写"三类证已打通" |
| **标准文本** | 现行国标：GB/T 16751.1-2023（疾病）、.2-2021（证候）、.3-2023（治法）、GB/T 15657-2021（病证分类与代码），1997 版已废止；著录在 std.samr.gov.cn 免费，全文在 openstd.samr.gov.cn **只能在线预览不可下载**（无机器可读版）。"中医病证诊断疗效标准"是 **ZY 号**行业标准（ZY/T 001.x-1994，国家中医药管理局主管，**不是 NY/T**），**无免费全文需购买** | 做辨证标签体系 / HIS 术语映射，GB/T 只能人工誊录；判分口径要对表 ZY/T 就得留采购预算。**论文里再写"GB/T 16751.1-1997"是引用废止标准** |
| **真实世界队列（RWE）** | 公开的是**注册和文件**，不是数据：ITMCTR 国际传统医学临床试验注册平台（中国中医科学院主办，WHO ICTRP 一级机构）只有试验元数据；NMPA 2020 年第 77 号真实世界数据指导原则免费。**没有任何公开可下载或可申请获取的中医专病真流队列**（北京 2026-10 报道的"跨院数据调阅破百万次"是调阅不是导出） | 直接对应 11.1 的"疗效终点"缺口。想做病历级评测集或发 RWE 论文，唯一路径是与中医院（广安门 / 省中医体系）签科研合作 + 过伦理，周期和不确定性都要预留。**不存在"中医版 CVM"** |

另外两条容易踩的信息坑：

- **古籍底本**：没有"开放获取 + API"的权威校勘全文库。《中华医典》（裘沛然/邓铁涛/王永炎编审）是个人付费产品（定价 799 / 直销 599 元，无 API）；国图"中华古籍资源库"read.nlc.cn 影像免费在线看但无 OCR 无 API；《新编中国中医古籍总目》（2023-12，8,650 种）是书目不是全文。**所以 5 节的社区文本仍是唯一机器可读来源，用它就必须注明"未对校底本"**。
- **资助语汇**：国家重点研发计划"中医药现代化"专项 2025 年度起主责单位改为国家中医药管理局；国自然医学科学部 2026 年度专项是"人工智能驱动的中药复方药效物质基础与作用原理研究"（H31/H32）。官方语汇是**名中医经验智能化传承、复方药效物质解析、智能装备**——"对话大模型"不在指南词表里，写本子要换词。

### 11.6 顺带发现：两个值得盯的新仓库

| 仓库 | 为什么值得记 |
|---|---|
| [cxu7524-dotcom/TCM-OCR-Knowledge-Graph](https://github.com/cxu7524-dotcom/TCM-OCR-Knowledge-Graph)（⭐2，2026-11-**07** 新建） | 中医古籍 OCR + 知识图谱构建系统，`ocr/ extract/ graph/ qa/ eval/` 目录齐全。第 5 节只有古籍**文本**、没有可用 OCR 工具，这是第一个成体系的 |
| [Zhuyuyangyy/TCM-SD42-Public-Reproducibility](https://github.com/Zhuyuyangyy/TCM-SD42-Public-Reproducibility)（⭐1，持续更新到 2026-11-09） | 9.3 / 10 节反复讲"证据诚实度"，这个仓库是**正面样本**：明确声明"不是官方 148 类 TCM-SD 基准"、"故意不发布原始病历/逐例预测/权重"、并单独写了 S2 归一化定义的复核记录（数字删除复现 22/45/23、N=4,195；`#` 哨兵模式复现不了计数）。找"可复现范例"时给它，别找 5000⭐ 的 |

### 11.7 如果只做三件事

1. **跑一轮 Skill 评测**（1-2 天，零成本）：caliper 测 nihaixia + TCM.Skill。第 2 节现在完全没有选型依据，这是唯一能立刻补上的。
2. **搭 Med-Bench-Arena 做自有模型基线**（3-5 天）：中医指标是一等公民且许可 MIT，直接解决"分数不可跨表比较"。注意先把它自带的 116 节点示例 KG 换掉。
3. **攒一批疗效结局数据**（长期，只有医院能给）：疗效终点是本文档所有"超过医师"说法的共同上游缺口，绕不过去。前两条做完了才有意义——没有可信评测，拿到结局数据也不会用。

---

## 附录 A 检索方法（可复现）

```bash
# 1. 仓库搜索（未认证 10 次/分钟，注意限速）
curl -s -G "https://api.github.com/search/repositories" \
  --data-urlencode "q=topic:tcm" \
  --data-urlencode "sort=stars" --data-urlencode "per_page=20" \
| jq -r '.items[] | "\(.stargazers_count)⭐ \(.full_name) upd:\(.pushed_at[:10]) :: \(.description)"'

# 2. 读 README（绕开 raw.githubusercontent 超时）
curl -s -H "Accept: application/vnd.github.raw" \
  https://api.github.com/repos/tyang816/Awesome-TCM-LLM/readme > awesome-tcm.md

# 3. 单仓详情（含许可）
curl -s https://api.github.com/repos/jangviktor-web/nihaixia \
| jq '{stars:.stargazers_count, pushed:.pushed_at, license:.license.spdx_id}'

# 4. HuggingFace 侧（必须走镜像）
export HF_ENDPOINT=https://hf-mirror.com
for q in TCM ShenNong BianCang Huatuo Zhongjing traditional-chinese-medicine; do
  curl -s "$HF_ENDPOINT/api/models?search=$q&limit=30&sort=downloads&direction=-1" \
  | jq -r '.[] | "\(.downloads)↓ \(.likes)♥ \(.id)"'
done

# 4b. 中文关键词在镜像 search= 返回 0（2026-11-01 实测），改用 tag 过滤才全
for t in tcm traditional-chinese-medicine chinese-medicine; do
  curl -s "$HF_ENDPOINT/api/models?filter=$t&limit=100&sort=createdAt&direction=-1" \
  | jq -r '.[] | "\(.createdAt[:10]) \(.id) dl=\(.downloads)"'
done

# 5. 判断权重到底能不能下（别只看 api/models，镜像会随机 429/525，且把 gated 与不存在都报成 401/404）
#    判据：README.md 404 = 仓库不存在；config.json 403 = gated（要网页同意许可）；302/307/200 = 可下载
for p in TCMLLM/Lingdan-14B-SFT CMLM/ZhongjingGPT1_13B TCMLLM/Lingdan-14B-R1; do
  printf "%-32s readme=%s cfg=%s\n" "$p" \
    "$(curl -s -o /dev/null -w '%{http_code}' -L "$HF_ENDPOINT/$p/resolve/main/README.md")" \
    "$(curl -s -o /dev/null -w '%{http_code}' -L "$HF_ENDPOINT/$p/resolve/main/config.json")"
  sleep 3   # 镜像限流很凶，连续请求务必留间隔
done
# 实测（2026-11-09）：14B-SFT → 可下载；ZhongjingGPT1_13B → 403 gated；14B-R1 → README 404 仓库不存在
# 注意 GGUF 仓库本身没有 config.json，只查 config.json 会误判成"不存在"，一定先看 README.md

# 6. 官方组织下实际发布了哪些 checkpoint（比 README 的 Model Zoo 表可信；gated 仓库照常出现在列表里，
#    所以"列表里没有"就是真没发布 —— Lingdan-14B-R1 就是这样暴露的）
curl -s "$HF_ENDPOINT/api/models?author=TCMLLM&limit=100" | jq -r '.[].id'

# 7. ModelScope 侧核对权重是否真的上传了（有仓库页 ≠ 有文件）
curl -s -o /dev/null -w "%{http_code}\n" \
  "https://modelscope.cn/api/v1/models/TCMAIBJTU/Lingdan-14B-R1/repo/files?Recursive=true"          # 404 = 无文件

# 8. 证实"某类资源不存在"（第 11 节缺口分析的判据，2026-11-09）
#    说"缺"之前必须多关键词交叉：单个关键词 0 命中很可能只是用词不对。
#    脉象一例：pulse / pulse diagnosis / sphygm / pulsiology / pulse wave chinese 在 HF datasets
#    全部为空，GitHub 脉象 只命中仪器 demo 仓库，且 Awesome-TCM-LLM 的 71 条数据集里没有脉象
#    —— 三方都为空，才敢写"真空缺"。
for q in pulse "pulse diagnosis" sphygm pulsiology; do
  printf "%-20s " "$q"
  curl -s -G "$HF_ENDPOINT/api/datasets" --data-urlencode "search=$q" --data-urlencode "limit=12" \
    | jq -r '[.[] | .id] | "count=\(length) \(.[0:4])"'
  sleep 3
done

# 9. Zenodo 数据集核对（DOI 会 302 跳到真正的 record，要跟着跳）
curl -sL "https://zenodo.org/api/records/21947836" \
  | jq -r '.metadata.title, .metadata.license.id, ([.files[].size] | add)'
# 实测：赵汉青处方集 → cc-by-4.0；下载解包后 dose_g 列 5951/5951 非空
```

**用过的查询词**

- GitHub：`中医`、`traditional chinese medicine`、`tcm`、`针灸 OR acupuncture`、`topic:tcm`、`topic:traditional-chinese-medicine`、`中医 in:name,description`、`中医 书籍`、`中医古籍`、`中草药`、`穴位`、`TCM-LLM`、`伤寒论/金匮/经方`、`中药/本草/方剂`、`traditional chinese medicine language model`、`中医 skill`、`TCM agent skill`、`伤寒论 skill`、`中医 agent`、`TCM-Andrology-EMR`、`MiMo TCM Andrology`、`中医男科 大模型`、`TCM-Ladder`、`LingLan benchmark`、`MTCMB`
- HuggingFace：`TCM`、`中医`、`中医药`、`traditional-chinese-medicine`、`chinese-medical`、`ShenNong`、`BianCang`、`Huatuo`、`Zhongjing`、`acupuncture`、`herb`；2026-11-01 补遗改用 tag：`filter=tcm`、`filter=traditional-chinese-medicine`、`filter=chinese-medicine`（中文 `search=` 无结果）

---

## 附录 B 术语表

| 术语 | 含义 |
|---|---|
| **CPT** | Continued Pre-Training，继续预训练。在领域语料上再训一轮，让底座"懂行话" |
| **SFT** | Supervised Fine-Tuning，监督微调。用指令-回答对训练 |
| **LoRA** | 低秩适配，只训练少量参数（如 43.3M / 9.41B = 0.458%） |
| **GRPO** | Group Relative Policy Optimization，一种 RL 方法；中医模型常用它做"处方"这类难验证任务的专项对齐 |
| **DPO / KTO** | 偏好对齐方法，DPO 用成对偏好，KTO 用单条好/坏标签 |
| **R1 阶段** | 指灵丹-V2 的第三阶段（处方 GRPO），不是 DeepSeek-R1 |
| **Jaccard** | 集合相似度，处方评测常用：预测药味 ∩ 真实药味 / 并集 |
| **Oracle 上界** | 用"真实答案"做检索能达到的天花板，用来判断模型是否真的在读自由文本 |
| **患者分组切分** | 按患者而非按样本切 train/test，避免同一患者泄漏到测试集 |
| **gated** | HF 上需同意许可才能下载的仓库，API 返回 401 |
| **四诊** | 望（舌/面）、闻（声/气）、问、切（脉） |
| **六经辨证** | 伤寒论体系：太阳/阳明/少阳/太阴/少阴/厥阴 |
| **卫气营血 / 三焦** | 温病学两套辨证框架 |
| **渐进披露** | Skill 设计模式：主文件只放流程，事实按需从 `references/` 加载，省 token |

---

## 附录 C 变更日志

| 日期 | 变更 |
|---|---|
| 2026-10-23 | 初版：GitHub 侧全量检索（Agent Skill / 大模型 / 应用 / 古籍 / 数据 / 综述专利） |
| 2026-10-30（二次） | 新增 **3.8 硬件适配：DGX Spark（GB10）** —— 公开规格核对（273 GB/s / 128G UMA / CUDA 13.0.3）+ 16 个模型的显存与 tok/s 估算表 + MiMo-9B 跑法 + Spark 栈避坑；同步更新 3.7 矩阵、8.1 决策树、8.2 场景表、9.5 工具链 |
| 2026-10-30 | ① 修复文档误存两份的问题；② 合并 HuggingFace 权重盘点（3.3）、2026 新模型（灵丹-V2、HuatuoGPT-3、man_medical 等）、评测基准（3.6）；③ 第 2 节重写为分层评价 + 流派地图 + 挑选标准；④ 全文重排：加目录、分层标准、五个判断、决策路径、避坑清单、术语表 |
| 2026-11-01 | hf-mirror 补遗（tag 重扫）：新增 **3.3.1 中西医结合专项**，收 7 个可下载权重（medical-v5-8b、中药学 Qwen3-8B、Qwen3-4B 医疗微调、TraceMed、TCM-Qwen3.5-9B-SFT-R2、YIAN-4B、TCM-m3）；补灵丹-V2 官方 HF 链接/arXiv、Baize GGUF、MiMo HF；"真能下载权重"口径由 16 改为 20+；附录 A 增加 tag 过滤方法 |
| 2026-11-04 | 新增 **10. 论文与范式（2026-11）**：回答「中医大模型是否与 Agent Skill 论文结合」——结论是两条平行线，最接近的是 TCM-SEA；收 8 条基本范式、8 类论文渠道与检索模板、24 篇 TCM + 15 篇 AI/Skill 论文清单、3 个可做的题 |
| 2026-11-09（晚） | 新增 **11. 还缺什么：资源与信息缺口**（回应"还需要哪些资源和信息"）。核心是**实测出的六个真空缺**：脉象公开数据集为零（HF 6 个关键词 + GitHub 全空）、舌象公开集全是属性标签无一带辨证证型、**所有真实病历均无疗效终点字段**、经方度量衡折算无公开数据/工具、证候→ICD-11 TM2 映射缺、多轮问诊对话集为零。同时纠正两处本文档的口径误导：① "多模态四诊开源"被读成四样都有数据（脉其实没有）；② "剂量不可信"被读成没有剂量数据（赵汉青处方集实测 5,951 行 100% 带 `dose_g`，问题在量太小）。新收 6 项可用资源：Med-Bench-Arena（评测框架，**已 clone 实跑通**）、TCM-SO v4.10（ICD-11/SNOMED/HPO 三向映射）、赵汉青处方集、TCMCPD、TongueBench、TongueAtlas-4K。另补 GitHub 之外的三层行业信息：中医辨证 AI **未查到三类证**、现行国标 GB/T 16751.1-2023/.2-2021/.3-2023 + GB/T 15657-2021（1997 版已废止，全文仅可在线预览）、**不存在公开的中医真流队列**。0.2 判断由五条扩到六条，0.3 速览加评测框架与编码映射两行，3.6 / 6.1 / 6.2 / 6.3 / 9.2 同步补录 |
| 2026-11-09 | 复核社区再次提名的 4 个 HF 模型（Issue #10）：`TCM-Qwen3.5-9B-SFT-R2` / `Lingdan-14B-SFT` / `MiMo-9B-TCM-Andrology-LoRA` / `chenhaodev/tcm-qwen3-8b-gguf` —— **3 个早已收录，信息准确无需改动**。真正的增量是两处**旧事实错误**：① **`TCMLLM/Lingdan-14B-R1` 权重从未发布**（此前记为"401 gated"），故新增 **3.3.2 复核小节**，并把 3.2 / 3.3.1 / 3.7 / 3.8 / 8.2 的处方首选改为**实际可下载的 `Lingdan-8B-R1`**、Spark 组合改用 `Lingdan-14B-SFT` bf16；② **`tczzx6/ZhiFangDanTai1.0`（知方丹台）仓库已消失**（此前也记为"401 gated"），从 3.3 移入 3.4。**根因是上一轮的"API 401 = gated"判据不成立**：镜像会把 gated 和不存在都报成 401/404，还会随机 429。本轮改用**下载 `resolve/main/README.md` + `config.json` 的组合判据**（403 = gated、404 = 不存在、302/200 = 可下载），并用 `api/models?author=` 与 ModelScope 文件树交叉验证；判据与实测对照写进 9.5 与附录 A |

---

初版 2026-10-23 · 重构 2026-10-30 · 补遗 2026-11-01 · 论文范式 2026-11-04 · 复核 2026-11-09 · 缺口分析 2026-11-09 CST*
