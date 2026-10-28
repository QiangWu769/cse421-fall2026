# Project 1: Pintos Threads

CSE 421/521 Operating Systems, Fall 2026. See [DEADLINES.md](../../DEADLINES.md) for the complete schedule.

| Deliverable | Status |
|---|---|
| Phase 1: Alarm Clock | **Completed** - Autolab 100/100; 14/14 points |
| Full Design Document PDF | **Prepared** - eight-page template version selected as final; alternate and proposal retained; submission unconfirmed |
| Phase 2: Priority Scheduler | **Submitted October 14, user confirmed** - grade unconfirmed |
| Phase 3: MLFQ Scheduler | **Implemented and locally verified** - 27/27 official tests passed; submission pending |

The user-provided Autolab result confirms five Phase 1 tests passed and a score of 100/100. The user confirmed Phase 2 submission on October 14, but its grade has not been supplied. Phase 3 has not been submitted. The actual UBLearns submission status of the design PDF is unknown.

## Completed Phase 1 work

- [Full source tree](pintos/src/): `timer_sleep()` blocks using a semaphore; the timer interrupt wakes expired sleepers.
- [Submission archive](submissions/phase1/pa1-phase1.tar.gz): the complete, cleaned `src/` tree. All five Phase 1 tests passed, and the extracted archive was rebuilt successfully.
- [SHA-256 checksum](submissions/phase1/SHA256SUMS).
- [Implementation and verification report](reports/PHASE1-REPORT.md): records the local checks performed on September 25, 2026.
- [Phase 1 implementation notes](pintos/src/threads/DESIGNDOC): Alarm Clock A1-A6 describe the completed code. The editable document now covers all 19 required questions.

The Phase 1 archive is retained as the earlier submission package. The working DESIGNDOC continues separately and records the current source design.

## Implemented Phase 2 work

- Highest-effective-priority dispatch, prompt preemption when a higher-priority thread becomes ready, and FIFO order among equal priorities.
- Semaphore and condition-variable wakeups use current effective priorities, including donations received after joining a wait queue.
- Lock donation supports multiple donors, nested chains up to eight holders, and removal of the donations associated with a released lock. Pending contenders remain registered until they actually acquire the lock.
- Safe preemption after creation, synchronization updates, priority changes, and interrupt-queue wakeups; interrupt handlers defer switches until return.
- The final clean build passed **13 Phase 2 tests plus all five Phase 1 regressions** using Bochs 2.6.11. Six additional cases passed in a disposable source copy.

See the dated [PHASE2-REPORT.md](reports/PHASE2-REPORT.md) for the October 9 verification record. The 13 Phase 2 tests cover **42 rubric points locally**, not an Autolab score. The retained [Phase 2 archive](submissions/phase2/pa1-phase2.tar.gz) contains 625 source files matching that source snapshot; an isolated extraction, rebuild, and repeat of all 18 course tests passed. Its [SHA256SUMS](submissions/phase2/SHA256SUMS) is recorded separately. The user subsequently confirmed submission on October 14.

## Implemented Phase 3 work

- Signed 17.14 arithmetic with 64-bit intermediates, complete-expression rounding for priority, and rounded-times-100 reporting interfaces.
- Inherited `nice` and `recent_cpu`, system-wide `load_avg`, and explicit exclusion of idle from accounting.
- Timer updates account the running thread, wake due alarms, perform second-boundary CPU/load updates, recompute priorities every four ticks, and only then consider preemption.
- The `-mlfqs` option selects the advanced scheduler, bypasses lock donation, and ignores manually supplied thread priorities. Default-mode priority scheduling and the alarm clock remain covered by regression tests.
- All **27 official tests** passed locally on October 27: nine Phase 3 tests and 18 earlier-phase regressions, using the course Makefile's per-test scheduler modes and Bochs 2.6.11.

See [PHASE3-REPORT.md](reports/PHASE3-REPORT.md) for individual results, seven successful supplemental scheduler groups, and independent arithmetic checks. The nine MLFQS tests cover **37 rubric points locally**; no Autolab grade is claimed. The verified [Phase 3 archive](submissions/phase3/pa1-phase3.tar.gz) contains 626 regular files that matched the cleaned source tree at packaging time, with [SHA256SUMS](submissions/phase3/SHA256SUMS) recorded beside it. An isolated extraction and rebuild passed all **27 official tests again**.

## Develop from a new clone

Install and start Docker Desktop. The original course [Dockerfile](environment/Dockerfile) and [Fall 2026 setup guide](environment/Docker_Setup_Guide.pdf) are in `environment/`.

From the repository root:

```bash
./scripts/build-env.sh
./scripts/enter-pintos.sh
```

The scripts select `linux/amd64`, including on Apple Silicon. The local Pintos directory is mounted at `/home/pintos`, so local edits are visible inside the container.

Run the full Phase 3 suite and all earlier-phase regression tests:

```bash
./scripts/test-phase3.sh
```

The script cleans and rebuilds the kernel, explicitly selects Bochs, runs `make check`, and checks all 27 `.result` files for `PASS`. The official Makefile enables `-mlfqs` only for the nine advanced-scheduler tests. After code and design notes are ready, create the complete Phase 3 source archive:

```bash
./scripts/package-phase3.sh
```

The archive is written to `assignments/pa1/submissions/phase3/pa1-phase3.tar.gz`, with `SHA256SUMS` in the same directory. The packaging script cleans the source tree and rejects leftover build or temporary files. It does not upload anything to Autolab. Preserve `submissions/phase1/` and `submissions/phase2/` as the earlier submission records.

`./scripts/test-phase1.sh` and `./scripts/test-phase2.sh` remain available for their narrower suites. The Phase 3 script includes all of those tests as regressions.

If an existing local image exactly matches the course Dockerfile, select its name or ID with `PINTOS_IMAGE`. For example, the original development machine used:

```bash
PINTOS_IMAGE=sha256:fd28c381bdb9f830d5d45eafa3d2878eae302ba08296a3152f110688c495e68d ./scripts/enter-pintos.sh
```

The course Dockerfile is preserved unchanged. Building it for the first time requires network access to download dependencies. The Pintos source revision is `9f013d0930202eea99c21083b71098a0df64be0d`.

## Remaining work

- **Phase 3 submission:** confirm the Phase 3 group and upload the verified archive to Autolab by October 27 at 23:59. Retain the grading result; implementation, local testing, and extracted-archive verification are complete.
- **Phase 2 grade:** submission on October 14 is user-confirmed; record the platform grade when available.
- **Final design PDF and submission confirmation:** use the [eight-page template PDF](design/PA1-DESIGNDOC-TEMPLATE.pdf), selected as the final submission version. Prepared October 27 from the updated [DESIGNDOC](pintos/src/threads/DESIGNDOC), it contains all 19 answers, the ASCII nested-donation diagram, and the C2 text table. This follows the instructor's [Piazza @135 reply](https://piazza.com/class/mr5d91n9mi73f/post/135): "Use the same template with your updated implementation." The [nine-page formatted alternate](design/PA1-DESIGNDOC-FINAL.pdf) and [earlier proposal](design/PA1-DESIGNDOC.pdf) remain separate. The original PDF deadline was October 8 at 23:59; no separate revision deadline has been supplied. Actual UBLearns submission is unconfirmed. The verified Phase 3 archive is unchanged; [implementation notes](design/IMPLEMENTATION-PLAN.txt) provide the code and verification record.

The original project license and author information are retained in `pintos/LICENSE` and `pintos/AUTHORS`.
