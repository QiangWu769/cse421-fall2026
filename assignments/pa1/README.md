# Project 1：Pintos Threads

课程：CSE 421/521 Operating Systems，Fall 2026。各阶段日期见根目录 [DEADLINES.md](../../DEADLINES.md)。

## Phase 1 当前成果

- [完整源码](pintos/src/)：`timer_sleep()` 已改为通过信号量阻塞，定时器中断唤醒到期线程。
- [提交包](submissions/phase1/pa1-phase1.tar.gz)：包含清理后的完整 `src/`；五项测试通过，压缩包重新解压编译成功。
- [SHA-256 校验值](submissions/phase1/SHA256SUMS)。
- [测试与实现报告](reports/PHASE1-REPORT.md)：记录 2026-09-25 的本地验证结果。
- [设计记录](pintos/src/threads/DESIGNDOC)：Alarm Clock A1-A6 已填，组员姓名/邮箱待补充，后续阶段和完整设计 PDF 尚待完成。

GitHub 存储不等同于课程平台提交。Phase 1 需要由一名组员上传到 Autolab，并确认最终评分。当前课程平台提交状态待确认。

## 在新的电脑或克隆目录中开发

先安装并启动 Docker Desktop。课程原始 [Dockerfile](environment/Dockerfile) 与 [Fall 2026 安装指南](environment/Docker_Setup_Guide.pdf) 保存在 `environment/`。

在仓库根目录运行：

```bash
./scripts/build-env.sh
./scripts/enter-pintos.sh
```

脚本指定 `linux/amd64`，支持在 Apple Silicon 上运行课程镜像。代码目录绑定到容器 `/home/pintos`，本地编辑会直接反映到容器。

运行 Phase 1 五项测试：

```bash
./scripts/test-phase1.sh
```

修改代码或设计记录后，先测试，再重新打包：

```bash
./scripts/package-phase1.sh
```

压缩包写入 `assignments/pa1/submissions/phase1/pa1-phase1.tar.gz`，同时更新校验值。脚本本身不会上传到 Autolab。

如果本机已有完全匹配课程 Dockerfile 的镜像，可以通过 `PINTOS_IMAGE` 指定其名字或 ID，而不重新构建。例如在原开发机已验证的镜像：

```bash
PINTOS_IMAGE=sha256:fd28c381bdb9f830d5d45eafa3d2878eae302ba08296a3152f110688c495e68d ./scripts/enter-pintos.sh
```

课程 Dockerfile 原样保留，首次构建需要联网下载依赖。Pintos 的源代码版本固定为 `9f013d0930202eea99c21083b71098a0df64be0d`。

## 各阶段工作范围

- Phase 1：Alarm Clock，消除 `timer_sleep()` 的忙等待，通过五项测试。
- Phase 2：Priority Scheduler、锁的多重/嵌套优先级捐赠，以及 `alarm-priority` 测试。
- Phase 3：MLFQ / 4.4BSD 调度器，使用 `-mlfqs` 选择。
- 设计文档：按 [课程模板](pintos/doc/threads.tmpl) 完善全部设计，10 月 8 日单独交 PDF 到 UBLearns。

`pintos/LICENSE` 与 `pintos/AUTHORS` 保留原始项目授权及作者信息。
