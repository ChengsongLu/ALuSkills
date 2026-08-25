# ALuSkills

[English](README.md) | **简体中文**

ALuSkills 是一组面向真实代码库的软件开发 Agent Skills：

```text
需求 → 技术规格 → TDD 实现 → 代码审查 → 任务恢复 → 代码库手册
```

这些 Skills 基于仓库证据工作，重点覆盖复杂行为和失败路径，同时避免给
简单任务增加不必要的流程。每个 Skill 都是自包含的，可以独立安装，不依赖
其他 Skill。

## Skills

| Skill | 适用场景 | 产物 |
| --- | --- | --- |
| [`clarify-development-request`](skills/clarify-development-request/) | 在实现前解决会影响需求结果的实质决策 | `brief.md` |
| [`write-technical-spec`](skills/write-technical-spec/) | 创建、更新或审查与仓库一致的技术设计 | 可选 `flow.md`、`design.md`、`implement.md` |
| [`develop-with-tdd`](skills/develop-with-tdd/) | 使用聚焦 TDD 实现选定的高风险行为 | 源码与测试 |
| [`review-code-changes`](skills/review-code-changes/) | 审查变更，并安全修复已授权的问题 | 可选 `review.md`、`coverage.md`、`remediation.md` |
| [`maintain-task-checkpoints`](skills/maintain-task-checkpoints/) | 为长期或容易中断的任务保存可恢复状态 | `STATE.md`、`CHECKPOINTS.md` |
| [`codebase-handbook`](skills/codebase-handbook/) | 建立和维护带源码证据的技术手册 | Markdown 章节、`manifest.yaml`、`handbook.html` |

### clarify-development-request

当开发需求仍有会改变行为、契约、范围或验收标准的未决问题时使用。它会先
调查仓库，再逐个确认真正影响决策的问题，最终形成已确认的 `brief.md`。
普通咨询、机械修改和已经明确的低风险任务不会进入该流程。

### write-technical-spec

用于创建、更新或审查技术规格。它会基于仓库检查需求，明确适用的流程、
边界、契约、失败行为和验证方式，并生成 `design.md`、`implement.md` 和可选的
`flow.md`。审查模式只读，不修改文档或代码。

### develop-with-tdd

当用户明确要求 TDD，或需要保护回归缺陷、复杂规则、状态流转、并发行为、
安全边界、外部契约或副作用时使用。它将测试映射到已确认行为，选择稳定的
测试接缝，并执行小步红—绿—重构循环。它不会创建独立流程产物，也不会把
TDD 强加给低风险修改。

### review-code-changes

用于审查工作区差异、commit、分支比较或 Pull Request。它检查正确性、
可靠性、安全性、兼容性、测试和文档。默认只读；只有用户明确授权后才修复
问题，修复完成后还会重新验证和审查。

### maintain-task-checkpoints

用于长期、多阶段、恢复成本高、容易中断或明确需要交接的任务。它记录当前
状态和已完成的检查点，但不保存凭据，也不替代 Git。隐式触发时，写入文件前
必须先获得用户确认。

### codebase-handbook

用于初始化、查阅、同步、验证或渲染代码库技术手册。它结合源码证据说明稳定
架构、运行行为、状态、失败处理和系统关系。所有写入都限制在
`.codebase-handbook/` 下，源码和普通仓库文件始终只作为只读证据。

## 安装与更新

安装需要 Node.js 和 `npx`。

查看可用 Skills：

```bash
npx skills add ChengsongLu/ALuSkills --list
```

全局安装全部 Skills：

```bash
npx skills add ChengsongLu/ALuSkills --skill '*' --global
```

为指定 Agent 安装一个 Skill：

```bash
npx skills add ChengsongLu/ALuSkills \
  --skill develop-with-tdd --global --agent codex --yes
```

按需替换 Skill 名称和 Agent。常用 Agent 值包括 `codex`、`claude-code` 和
`cursor`。

更新已全局安装的 ALuSkills：

```bash
npx skills update --global \
  clarify-development-request \
  write-technical-spec \
  develop-with-tdd \
  review-code-changes \
  maintain-task-checkpoints \
  codebase-handbook
```

验证安装：

```bash
npx skills list --global
```

安装或更新后，请重新启动 Agent 或新建会话。

## 目录结构

```text
skills/
├── clarify-development-request/
├── codebase-handbook/
├── develop-with-tdd/
├── maintain-task-checkpoints/
├── review-code-changes/
└── write-technical-spec/
```

每个 Skill 都包含 `SKILL.md` 和 `agents/openai.yaml`；只有工作流确实需要时，
才会增加 `references/`、`scripts/` 或 `assets/`。

## 开源协议

[Apache License 2.0](LICENSE) © 2026 Chengsong Lu
