# ALuSkills

一组面向软件开发工作流的 Agent Skills，覆盖需求澄清、技术方案设计、代码审查、长任务检查点和代码库手册维护。

这些 skills 遵循 [Agent Skills 规范](https://agentskills.io/specification)，可以通过 [`skills`](https://github.com/vercel-labs/skills) CLI 安装到兼容的 Agent。

## 1. 安装

安装由 [`skills`](https://github.com/vercel-labs/skills) CLI 完成，需要本机已经安装 Node.js 和 `npx`。

### 1.1 查看可用 Skills

以下命令只查看，不会安装：

```bash
npx skills add ChengsongLu/ALuSkills --list
```

确认来源为 `ChengsongLu/ALuSkills`，并显示 5 个 skills。

### 1.2 全局安装全部 Skills

推荐首次安装使用交互模式：

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global
```

安装时只需关注以下步骤：

1. **选择 Agent**

   使用 `↑`、`↓` 移动，`Space` 选择，`Enter` 确认。

   - Codex、Cursor：包含在 `Universal (.agents/skills)` 中，无需额外选择；
   - Claude Code：在 `Additional agents` 中额外选择 `Claude Code`；
   - 不要选择自己不用的 Agent，避免创建无关目录或链接。

2. **检查安装摘要**

   应看到 5 个 skills 安装到 `~/.agents/skills/`。摘要中的 `copy → Codex ...` 表示这些 Agent 可以读取通用副本，是正常结果。

   如果需要 Claude Code，还应确认摘要中包含 `Claude Code`；如果没有，选择 `No` 并重新运行安装。

3. **确认安装**

   在 `Proceed with installation?` 处选择 `Yes`，按 `Enter` 完成安装。

安装完成后重新启动 Agent，或新建一个会话。

### 1.3 直接指定 Agent

跳过交互，安装给 Codex：

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global --agent codex --yes
```

安装给 Claude Code：

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global --agent claude-code --yes
```

安装给 Cursor：

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global --agent cursor --yes
```

同时安装给三者：

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global \
  --agent codex --agent claude-code --agent cursor --yes
```

### 1.4 安装位置

| Agent | 项目级目录 | 全局目录 |
| --- | --- | --- |
| Codex | `.agents/skills/` | `~/.codex/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |

CLI 可能将公共副本放在 `~/.agents/skills/`，再由 Agent 直接读取或建立链接；以 `Installation Summary` 显示的路径为准。

### 1.5 验证

```bash
npx skills list --global
```

输出中应能看到本仓库的 5 个 skills。

## 2. Skills

| Skill | 用途 |
| --- | --- |
| [`clarify-development-request`](skills/clarify-development-request/) | 在非简单开发开始前澄清目标、范围、行为、契约、风险和验收标准 |
| [`write-technical-spec`](skills/write-technical-spec/) | 基于仓库事实编写并审查流程、设计和实施方案 |
| [`review-code-changes`](skills/review-code-changes/) | 审查工作区、提交、分支或 PR 的具体正确性与可靠性风险 |
| [`maintain-task-checkpoints`](skills/maintain-task-checkpoints/) | 为长时间、多阶段或高恢复成本的任务保存可恢复状态 |
| [`codebase-handbook`](skills/codebase-handbook/) | 创建和维护面向人类与 Agent 的代码库技术手册 |

### 2.1 clarify-development-request

在需求会影响产品行为、技术边界或验收方式时，先调查仓库事实，再逐项澄清真正会改变实现方向的问题，最终形成可确认、可交接的开发简报。

适合：

- 将模糊需求整理成实现就绪的 brief；
- 明确目标、范围、非目标和验收标准；
- 澄清状态、失败语义、兼容性、安全和副作用边界；
- 在进入技术设计前消除会改变方案的未决问题。

不适合普通咨询、纯诊断、纯审查、机械修改，或已经足够明确的低风险任务。

安装：

```bash
npx skills add ChengsongLu/ALuSkills --skill clarify-development-request --global
```

### 2.2 write-technical-spec

根据已经确认的需求和当前仓库证据，编写并审查技术规格。根据任务需要生成流程、设计和分阶段实施文档，并保持不同文档的抽象层级清晰。

适合：

- 编写技术方案或设计文档；
- 绘制核心处理流程；
- 规划模块、接口、数据、状态和兼容性变化；
- 制定分阶段实施计划和验证策略；
- 审查已有设计是否完整且与仓库一致。

安装：

```bash
npx skills add ChengsongLu/ALuSkills --skill write-technical-spec --global
```

### 2.3 review-code-changes

针对工作区 diff、暂存修改、提交、分支比较或 PR 进行证据驱动的代码审查，重点检查正确性、可靠性、安全性、兼容性、测试和文档风险。

适合：

- 审查当前未提交修改；
- 审查指定 commit 或分支差异；
- 检查状态、并发、持久化、重试和失败恢复路径；
- 输出带证据、影响级别和修复方向的审查结果；
- 在用户明确授权后修复已确认的问题。

默认只审查、不修改实现文件。

安装：

```bash
npx skills add ChengsongLu/ALuSkills --skill review-code-changes --global
```

### 2.4 maintain-task-checkpoints

为长时间、多阶段或高恢复成本的开发任务维护紧凑的恢复状态，帮助任务在中断、上下文压缩或 Agent 交接后安全继续。

适合：

- 跨多个模块和阶段的复杂开发；
- 包含迁移、状态机、并发或外部副作用的任务；
- 需要在不同 Agent 之间交接的工作；
- 容易因中断而重复危险操作的任务；
- 用户明确要求保存检查点的任务。

短小、低风险、单次即可完成的任务不应创建检查点。

安装：

```bash
npx skills add ChengsongLu/ALuSkills --skill maintain-task-checkpoints --global
```

### 2.5 codebase-handbook

在仓库中创建和维护 `.codebase-handbook/` 技术手册，用稳定的概念、职责、流程、状态、失败行为和源码证据解释系统，而不是生成逐文件 API 清单。

适合：

- 初始化代码库技术手册；
- 导航和理解已有手册；
- 在代码变更前后同步架构与行为说明；
- 校验手册结构、引用和覆盖范围；
- 生成自包含的 HTML 阅读视图；
- 拆分、合并或演进手册章节。

该 skill 不会因为普通编码任务而自动初始化手册；初始化需要用户明确提出。

安装：

```bash
npx skills add ChengsongLu/ALuSkills --skill codebase-handbook --global
```

## 3. 目录结构

每个 skill 都是一个独立目录，并至少包含一个带 YAML frontmatter 的 `SKILL.md`：

```text
skills/
├── clarify-development-request/
├── codebase-handbook/
├── maintain-task-checkpoints/
├── review-code-changes/
└── write-technical-spec/
```

部分 skills 还包含 `scripts/`、`references/`、`assets/` 或 `agents/openai.yaml`。安装时这些依赖会和对应的 `SKILL.md` 一起复制或链接到目标 Agent 的 skills 目录。

## 4. 开源协议

本项目采用 [Apache License 2.0](LICENSE) 开源。

Copyright 2026 Chengsong Lu.
