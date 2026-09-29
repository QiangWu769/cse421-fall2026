# Phase 1 完成与验证记录

日期：2026-09-25。

## 实现

`src/devices/timer.c` 使用按唤醒时间排序的等待队列和每次睡眠独立的信号量。等待线程通过 `sema_down()` 阻塞；定时器中断移除全部到期记录并调用 `sema_up()`。

- 消除了 `timer_sleep()` 中的轮询和反复 `thread_yield()`。
- 零、负参数直接返回。
- 相同到期时间的记录在同次中断内全部唤醒。
- 信号量保留提前到达的唤醒，避免登记与阻塞之间丢失通知。
- 中断保护只覆盖共享队列访问，等待本身由信号量完成。
- 无符号 64 位截止时间避免超大正延时的有符号加法溢出。
- 没有扩大 `struct thread`，没有堆分配，也没有修改课程测试或后续调度功能。

`src/threads/DESIGNDOC` 已完成 Alarm Clock A1-A6，记录了数据结构、算法、同步和设计取舍。组员姓名与邮箱仍须填写；Phase 2/3 部分明确标为后续任务。

## 课程测试

清理旧构建后，在课程 Docker 环境中重新编译，并使用默认 Bochs 配置运行：

| 测试 | 结果 |
|---|---|
| alarm-single | PASS |
| alarm-multiple | PASS |
| alarm-simultaneous | PASS |
| alarm-zero | PASS |
| alarm-negative | PASS |

编译未出现来自本次修改的警告。原始框架仍有 init.c、debug.c、string.c 等处的既有编译警告。

## 额外验证

在独立临时源码副本中增加行为检查，未将其加入提交源码：

- 从另一个线程观察睡眠线程，确认其状态是 `THREAD_BLOCKED`，并确认到期后正常返回。
- 使用 `INT64_MAX` 正延时，确认不会发生截止时间溢出造成的提前返回。
- 8 个线程各执行 100 次单 tick 睡眠，共 800 次，全部完成且没有提前返回。
- 代码独立审查覆盖了局部等待记录生命周期、丢唤醒、中断上下文和同截止时间唤醒。

上述额外行为检查通过。课程测试的退出统计也显示睡眠期间 CPU 可以进入 idle 状态：alarm-single 为 250 idle ticks，alarm-multiple 为 550 idle ticks。

## 提交范围

`pa1-phase1.tar.gz` 包含完整且已清理的 `src/` 源码树，供 Autolab Phase 1 使用。它不包含 Docker 镜像、临时额外测试或构建输出。

已核对包内 625 个普通文件与当前源码逐字节一致，并从最终压缩包解压到独立临时目录后重新编译成功。课程环境附带的 Bochs 源码下载包保留在 `src/misc/` 中。

- 压缩包大小：5,490,858 字节。
- SHA-256：`e914a0456dc7b8c7c34f822bc7971870b49a5dbb0c7c6c030187273d890b6dad`。

当前完成的是 Phase 1 实现与本地验证；没有上传到 Autolab，没有服务器评分结果，也没有完成 Phase 2/3 或另交的完整设计文档 PDF。
