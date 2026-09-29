# 截止时间与提交清单

依据本次提供的 CSE 421/521 Fall 2026 Project 1 作业说明及提交说明整理。最近整理日期：**2026-09-29**。

**时区说明：** 原始截图未注明时区；本仓库按 Buffalo 的 **America/New_York** 记录。所有日期均为 2026 年，截止时刻均为 **23:59**。如后续课程公告、老师通知或提交平台的信息有变化，应据此更新本文件与 [deadlines.json](deadlines.json)。

## 总览

| 交付项 | 截止时间 | 分值 | 交付格式与平台 |
|---|---|---:|---|
| Phase 1：Alarm Clock | 2026-09-30 23:59 | 14 | 完整源码树的 `.tar.gz`，Autolab |
| Project 1 完整设计文档 | 2026-10-08 23:59 | 12 | PDF，UBLearns；源码中保留 `src/threads/DESIGNDOC` |
| Phase 2：Priority Scheduler | 2026-10-14 23:59 | 42 | 完整源码树的 `.tar.gz`，Autolab |
| Phase 3：MLFQ Scheduler | 2026-10-27 23:59 | 37 | 完整源码树的 `.tar.gz`，Autolab |

实现：14 + 42 + 37 = **93 分**。设计文档：**12 分**。总计：**105 分**。

早前按组件划分的 18 分 Alarm Clock、38 分 Priority Scheduler，与分阶段提交的 14 分、42 分并不冲突：`alarm-priority` 的 **4 分在 Phase 2 提交**。

## Phase 1：Alarm Clock

**截止：9 月 30 日 23:59 · 14 分 · Autolab**

重写 `devices/timer.c` 中的 `timer_sleep()`，让调用线程阻塞，等待至少指定数量的 timer ticks 后进入就绪队列。参数单位是 ticks；不要求线程在到期时立刻得到 CPU。零和负延时应立即返回。

实现要求：

- 不能通过循环检查时间、反复调用 `thread_yield()` 来忙等待。
- 使用合适的同步原语；中断处理程序不能获取会阻塞的锁。
- 可以短暂关闭中断，保护线程与中断处理程序共享的数据；不能把关闭中断作为唯一同步机制。
- 保留课程默认 `TIMER_FREQ`，不需要改动毫秒、微秒、纳秒睡眠包装函数。
- 作业说明分别列出忙等待、仅以关中断作为同步机制的 **14 分扣分项**；功能测试通过仍须检查实现本身。

| 课程测试 | 分值 | 已有本地结果 |
|---|---:|---|
| `alarm-single` | 4 | PASS |
| `alarm-multiple` | 4 | PASS |
| `alarm-simultaneous` | 4 | PASS |
| `alarm-zero` | 1 | PASS |
| `alarm-negative` | 1 | PASS |

`alarm-priority` 不属于本阶段要求。

完成与待办：

- [x] 实现有序睡眠队列与信号量阻塞。
- [x] 五项 Phase 1 课程测试通过（2026-09-25）。
- [x] 额外验证通过：实际 `THREAD_BLOCKED` 状态、`INT64_MAX` 延时、8 个线程共 800 次短睡眠。
- [x] 生成完整源码包，并从最终包中重新解压、编译成功。
- [x] 填写 DESIGNDOC 的 Alarm Clock A1–A6。
- [ ] 填写实际组员姓名、邮箱并共同审阅代码及设计说明。
- [ ] 在 Autolab 的 Phase 1 页面核对小组成员已确认加入。
- [ ] 由一名成员上传最终版本，并记录平台提交时间和评分反馈；当前平台提交状态待用户确认。

提交包：[pa1-phase1.tar.gz](assignments/pa1/submissions/phase1/pa1-phase1.tar.gz)。验证详情：[PHASE1-REPORT.md](assignments/pa1/reports/PHASE1-REPORT.md)。若修改文件，重新测试并生成包含最新修改的包。

## 完整设计文档

**截止：10 月 8 日 23:59 · 12 分 · PDF 提交到 UBLearns**

按课程的 `threads.tmpl` 模板填写设计文档，并在源码中保留 [src/threads/DESIGNDOC](assignments/pa1/pintos/src/threads/DESIGNDOC)。内容应覆盖各组件的数据结构、算法、同步方式和设计取舍。

这个截止时间早于 Phase 2 和 Phase 3 的代码截止时间，因此不能等后续代码全部完成后才准备文档。根据课程说明，文档需要描述已经采用或计划采用的设计。

- [x] Alarm Clock A1–A6 已填写。
- [ ] 填入所有组员的真实姓名及 UB 邮箱。
- [ ] 审阅 Alarm Clock 答案，确认与最终提交源码一致。
- [ ] 完成 Priority Scheduling 部分 B1–B7，包括多重和嵌套优先级捐赠的设计。
- [ ] 完成 Advanced Scheduler 部分 C1–C6，包括调度示例表格及定点数方案。
- [ ] 核对引用与协助来源记录，补充组员实际使用的其他来源。
- [ ] 生成并检查完整 PDF 的内容与排版。
- [ ] 在 UBLearns 提交 PDF，保存平台确认信息。

**当前只有 Phase 1 设计记录已完成；完整设计 PDF 尚未完成。** 把 DESIGNDOC 放入 GitHub 或源码压缩包，不能代替 UBLearns 的 PDF 提交。

## Phase 2：Priority Scheduler

**截止：10 月 14 日 23:59 · 42 分 · Autolab**

要求：

- 就绪线程中选择最高优先级线程；更高优先级线程就绪时及时让出 CPU。
- 锁、信号量和条件变量应优先唤醒最高优先级等待线程。
- 正确处理相同优先级线程的公平轮转与测试要求。
- 为锁实现优先级捐赠，处理多重和嵌套捐赠；释放锁后正确撤销相关捐赠。
- 实现 `thread_set_priority()` 和 `thread_get_priority()` 的要求，包括有效优先级及降优先级后的让出 CPU。
- 保持既有 Alarm Clock 行为，并完成 `alarm-priority` 测试。

| 测试 | 分值 |
|---|---:|
| `alarm-priority` | 4 |
| `priority-change` | 3 |
| `priority-preempt` | 3 |
| `priority-fifo` | 3 |
| `priority-sema` | 3 |
| `priority-condvar` | 3 |
| `priority-donate-one` | 3 |
| `priority-donate-multiple` | 3 |
| `priority-donate-multiple2` | 3 |
| `priority-donate-nest` | 3 |
| `priority-donate-chain` | 5 |
| `priority-donate-sema` | 3 |
| `priority-donate-lower` | 3 |

- [ ] 完成优先级调度及同步等待队列的优先级处理。
- [ ] 完成锁的多重、嵌套优先级捐赠及撤销。
- [ ] 通过上表 13 项测试，并检查 Phase 1 回归测试。
- [ ] 更新 DESIGNDOC，使其与最终实现一致。
- [ ] 清理构建输出、打包完整源码、验证压缩包可编译。
- [ ] 在 Autolab 对应 Phase 页面核对组员、上传并检查评分反馈。

## Phase 3：MLFQ Scheduler

**截止：10 月 27 日 23:59 · 37 分 · Autolab**

实现符合 Pintos 4.4BSD 调度器要求的多级反馈队列调度。默认启用优先级调度器，使用 `-mlfqs` 内核选项切换到高级调度器。

要求：

- 实现调度器计算优先级所需的 `nice`、`recent_cpu`、`load_avg` 及相应更新规则。
- 按 Pintos Appendix B 的公式、更新时机和舍入规则实现定点运算。
- MLFQS 模式不进行优先级捐赠。
- MLFQS 模式忽略 `thread_create()` 的优先级参数及 `thread_set_priority()`；`thread_get_priority()` 返回调度器计算的当前优先级。
- 保持默认调度模式及 Alarm Clock 正常工作。

| 测试 | 分值 |
|---|---:|
| `mlfqs-load-1` | 5 |
| `mlfqs-load-60` | 5 |
| `mlfqs-load-avg` | 3 |
| `mlfqs-recent-1` | 5 |
| `mlfqs-fair-2` | 5 |
| `mlfqs-fair-20` | 3 |
| `mlfqs-nice-2` | 4 |
| `mlfqs-nice-10` | 2 |
| `mlfqs-block` | 5 |

- [ ] 阅读 Appendix B，完成定点数与调度状态设计。
- [ ] 实现 MLFQS 计算、更新时间点及启动选项切换。
- [ ] 通过上表九项测试，并检查其他阶段的回归测试。
- [ ] 更新 DESIGNDOC，使其与最终实现一致。
- [ ] 清理构建输出、打包完整源码、验证压缩包可编译。
- [ ] 在 Autolab 对应 Phase 页面核对组员、上传并检查评分反馈。

## 每次代码提交都要核对

1. 提交完整 `src/` 源码树，不能只提交改动过的单个文件。清理后应可正常 `make` 编译。
2. 确认对应 Phase 的小组成员均已接受邀请；由一名成员提交后，成绩会应用到全组。
3. 提前上传到 [Autolab](https://autolab.cse.buffalo.edu/) 并检查任务结果。课程说明指出，**最后一次提交决定成绩**；后续重交仍需检查反馈。
4. 把平台确认信息记录到仓库任务中，区分“本地测试完成”“GitHub 已保存”和“课程平台已提交”。

任务入口：[milestones](https://github.com/QiangWu769/cse421-fall2026/milestones) · [issues](https://github.com/QiangWu769/cse421-fall2026/issues)。

## 尚未提供的日期

其他本学期项目、测验、期中和期末考试的日期尚未提供，暂不列出。收到课程正式安排后，再补充相应要求和截止时间。
