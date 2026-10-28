# ALuSkills

[English](README.md) | **简体中文**

面向软件开发的 Agent Skills，覆盖方案判断、需求澄清、技术设计、测试、审查和
代码库维护。每个 Skill 都可独立使用，基于依据开展与任务复杂度相称的工作。
按需选择，无须按固定顺序使用。

## Skills

点击 Skill 链接查看详情。下表描述各 Skill 声明的使用条件，实际选择由宿主
Agent 决定；目前没有覆盖所有任务的常驻规则。用户可用自然语言提出请求，
无须点名 Skill；已有授权在原范围内持续有效。

| Skill | 适用场景 | 产物 | 触发与确认 |
| --- | --- | --- | --- |
| [`reason-from-evidence`](skills/reason-from-evidence/SKILL.md) | 评价方案，避免盲目赞同与刻意反对 | 判断与依据 | 按场景：方案讨论或结论受到质疑时使用，无须进入确认 |
| [`codebase-handbook`](skills/codebase-handbook/SKILL.md) | 导航代码库，维护技术手册 | Markdown 手册与 HTML 阅读页 | 按场景：查阅已有手册或评估变更影响；初始化须主动请求，其他写入须有授权 |
| [`clarify-development-request`](skills/clarify-development-request/SKILL.md) | 解决会影响结果的需求歧义 | 明确的决策；可选 `brief.md` | 按场景：出现实质歧义直接提问；生成简报须用户要求或同意 |
| [`write-technical-spec`](skills/write-technical-spec/SKILL.md) | 评估设计风险，编写、更新和审查技术规格 | `design.md`；按需补充配套文档 | 按场景：自动评估重要设计风险；主动建议生成文档须确认，明确请求则直接开展 |
| [`maintain-task-checkpoints`](skills/maintain-task-checkpoints/SKILL.md) | 保存难以重建的任务状态，恢复中断工作 | `STATE.md` | 自动评估恢复需要，必要时提议并经确认创建；明确请求直接创建，授权后持续维护，恢复时核查已有记录 |
| [`develop-with-tdd`](skills/develop-with-tdd/SKILL.md) | 用聚焦 TDD 处理回归缺陷、复杂逻辑和契约变化 | 代码与测试 | 按场景或明确请求：回归缺陷、复杂逻辑、契约变更；大幅扩展工作范围须确认 |
| [`review-code-changes`](skills/review-code-changes/SKILL.md) | 审查代码差异，修复已授权的问题 | 审查结论；授权后的修复 | 用户请求审查变更；修复须明确授权，报告落盘须要求或同意 |
| [`commit-changes`](skills/commit-changes/SKILL.md) | 用信息完整的提交说明提交已授权变更 | Git 提交 | 用户主动要求提交；遵循仓库审批规则，已满足的确认不重复询问 |
| [`write-weekly-report`](skills/write-weekly-report/SKILL.md) | 汇总一周 Git 提交 | 周报 | 用户主动要求周报或一周提交总结 |

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
  reason-from-evidence \
  codebase-handbook \
  clarify-development-request \
  write-technical-spec \
  maintain-task-checkpoints \
  develop-with-tdd \
  review-code-changes \
  commit-changes \
  write-weekly-report
```

验证安装：

```bash
npx skills list --global
```

安装或更新后，请重新启动 Agent 或新建会话。

## 额外依赖

`codebase-handbook` 的 Python 辅助脚本需要 Python 3.9+ 和 PyYAML。将以下路径
替换为该 Skill 的实际安装目录：

```bash
python3 -m pip install -r /path/to/codebase-handbook/scripts/requirements.txt
```

使用同一 Python 环境运行辅助脚本。

## 参与贡献

目录与验证要求见 [CONTRIBUTING.md](CONTRIBUTING.md)；漏洞报告方式见
[SECURITY.md](SECURITY.md)。

## 开源协议

[Apache License 2.0](LICENSE) © 2026 Chengsong Lu
