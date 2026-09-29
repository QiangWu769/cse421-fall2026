# CSE 421/521 · Fall 2026

课程作业、源码、提交包与截止时间记录。当前收录 **Project 1：Pintos Threads**。课程平台的提交和评分需要单独确认；将文件上传到 GitHub 不代表已提交作业。

## 截止时间

以下均为 **2026 年 23:59**。原始截图未注明时区，本仓库暂按 Buffalo 的 **America/New_York** 整理；课程公告、老师通知及平台显示的最新要求优先。

| 交付项 | 截止日期 | 分值 | 提交平台 | 当前状态 |
|---|---|---:|---|---|
| Phase 1：Alarm Clock | 9 月 30 日 | 14 | [Autolab](https://autolab.cse.buffalo.edu/) | 代码与本地验证完成，平台提交待确认 |
| 完整设计文档 PDF | 10 月 8 日 | 12 | UBLearns | Alarm Clock A1–A6 已填；身份信息及完整 PDF 待完成 |
| Phase 2：Priority Scheduler | 10 月 14 日 | 42 | [Autolab](https://autolab.cse.buffalo.edu/) | 待实现 |
| Phase 3：MLFQ Scheduler | 10 月 27 日 | 37 | [Autolab](https://autolab.cse.buffalo.edu/) | 待实现 |

实现共 **93 分**，设计文档 **12 分**，总计 **105 分**。`alarm-priority` 的 4 分属于 Phase 2，因此各阶段分值为 14、42、37。

完整要求见 [DEADLINES.md](DEADLINES.md)；结构化日期见 [deadlines.json](deadlines.json)。其他本学期项目和考试日期尚未提供。

## 当前进度

截至 2026-09-29，已保存 9 月 25 日完成的 Phase 1 工作：

- `timer_sleep()` 使用有序等待队列和信号量阻塞，消除了忙等待。
- 五项 Phase 1 课程测试通过；额外的 `THREAD_BLOCKED` 状态、`INT64_MAX` 延时和 800 次并发短睡眠检查也通过。
- 已生成完整源码提交包，并从包中重新解压、编译验证。
- [DESIGNDOC](assignments/pa1/pintos/src/threads/DESIGNDOC) 的 Alarm Clock A1–A6 已填写。组员姓名与邮箱、后续设计内容和另交的完整 PDF 尚待完成。
- **是否已上传 Autolab、服务器评分是多少，仍待组员确认。** 本地验证记录见 [Phase 1 报告](assignments/pa1/reports/PHASE1-REPORT.md)。

## 使用入口

1. 开发、编译和测试：阅读 [PA1 使用说明](assignments/pa1/README.md)，课程环境文件在 [environment/](assignments/pa1/environment/)。
2. Phase 1 提交：使用 [pa1-phase1.tar.gz](assignments/pa1/submissions/phase1/pa1-phase1.tar.gz)，在 Autolab 对应 Phase 页面核对小组后，由一名成员上传并检查反馈。若修改源码或 DESIGNDOC，须重新打包最新版本。
3. 规划后续工作：查看 [截止时间与待办](DEADLINES.md)、[GitHub milestones](https://github.com/QiangWu769/cse421-fall2026/milestones) 和 [issues](https://github.com/QiangWu769/cse421-fall2026/issues)。

## GitHub 跟进

| 项目 | 截止日期 | 待办 |
|---|---|---|
| PA1 Phase 1 - Alarm Clock | [里程碑 1](https://github.com/QiangWu769/cse421-fall2026/milestone/1) | [待办 #1](https://github.com/QiangWu769/cse421-fall2026/issues/1) |
| PA1 - Design Document | [里程碑 2](https://github.com/QiangWu769/cse421-fall2026/milestone/2) | [待办 #2](https://github.com/QiangWu769/cse421-fall2026/issues/2) |
| PA1 Phase 2 - Priority Scheduler | [里程碑 3](https://github.com/QiangWu769/cse421-fall2026/milestone/3) | [待办 #3](https://github.com/QiangWu769/cse421-fall2026/issues/3) |
| PA1 Phase 3 - MLFQ Scheduler | [里程碑 4](https://github.com/QiangWu769/cse421-fall2026/milestone/4) | [待办 #4](https://github.com/QiangWu769/cse421-fall2026/issues/4) |

里程碑用于显示截止日期；精确截止时间为上表的 23:59，采用 America/New_York。

## 目录

```text
assignments/pa1/
├── README.md                         # PA1 开发与提交说明
├── pintos/                           # 完整 Pintos 工程
├── environment/                      # 课程 Dockerfile 与环境指南
├── reports/PHASE1-REPORT.md           # 实现与本地验证记录
└── submissions/phase1/
    └── pa1-phase1.tar.gz              # Phase 1 源码提交包
scripts/                              # 仓库辅助脚本
deadlines.json                        # 结构化截止时间
DEADLINES.md                          # 分阶段要求和待办
```

代码中的 `DESIGNDOC` 保留了实现及文档的协助来源记录。小组成员应审阅代码和设计说明，并补齐实际身份信息。
