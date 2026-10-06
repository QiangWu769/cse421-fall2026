# CSE 421/521 - Fall 2026

Course assignments, source code, submission archives, and deadlines. This repository currently contains **Project 1: Pintos Threads**.

**Phase 1 is completed and graded: 100/100 on Autolab (14/14 rubric points, five tests passed). The complete English design PDF is prepared for group review and submission. Phase 2 and Phase 3 implementations are not started.**

## Deadlines and status

All deadlines below are in **2026 at 23:59**. The Phase 1 Autolab screenshot confirms EDT (UTC-04:00). Remaining deadlines use Buffalo's **America/New_York** local time; official course announcements take precedence.

| Deliverable | Deadline | Points | Platform | Status |
|---|---|---:|---|---|
| Phase 1: Alarm Clock | September 30, 23:59 | 14 | [Autolab](https://autolab.cse.buffalo.edu/) | Submitted and graded: 100/100 |
| Formal Design Document | October 8, 23:59 | 12 | UBLearns, PDF | PDF prepared; not submitted |
| Phase 2: Priority Scheduler | October 14, 23:59 | 42 | [Autolab](https://autolab.cse.buffalo.edu/) | Not started |
| Phase 3: MLFQ Scheduler | October 27, 23:59 | 37 | [Autolab](https://autolab.cse.buffalo.edu/) | Not started |

Implementation is worth **93 points**, plus **12 points** for the formal design document, for a total of **105 points**. The 4-point `alarm-priority` test belongs to Phase 2, giving phase totals of 14, 42, and 37.

See [DEADLINES.md](DEADLINES.md) for requirements and checklists, and [deadlines.json](deadlines.json) for structured dates. Dates for other semester projects and exams have not been provided.

## Phase 1 progress

The following work was completed and locally verified on **2026-09-25**:

- `timer_sleep()` blocks using an ordered sleep queue and a semaphore, without busy waiting.
- All five Phase 1 course tests passed. Additional checks passed for actual `THREAD_BLOCKED` state, an `INT64_MAX` delay, and 800 concurrent short sleeps.
- The complete source archive was generated, extracted into a separate directory, and compiled successfully.
- Alarm Clock A1-A6 notes are included in the source [DESIGNDOC](assignments/pa1/pintos/src/threads/DESIGNDOC). Group identities are filled in. The complete document now covers A1-A6, B1-B7, and C1-C6, with the later implementations described as plans.

**The user-provided Autolab screenshot confirms 100/100, all five tests passed, and 14/14 rubric points.** See the [Phase 1 report](assignments/pa1/reports/PHASE1-REPORT.md) for the local verification record.

## Start here

1. **Develop and test:** read the [PA1 guide](assignments/pa1/README.md). Course environment files are in [environment/](assignments/pa1/environment/).
2. **Review the design:** read the [complete English PDF](assignments/pa1/design/PA1-DESIGNDOC.pdf), its editable [DESIGNDOC](assignments/pa1/pintos/src/threads/DESIGNDOC), and [IMPLEMENTATION-PLAN.txt](assignments/pa1/design/IMPLEMENTATION-PLAN.txt). The existing Phase 1 archive is retained as the earlier submission package.
3. **Plan remaining work:** use [DEADLINES.md](DEADLINES.md) and the GitHub tracking links below. The design PDF is **Prepared, not submitted**; Phase 2 and Phase 3 implementations remain **Not started**.

## GitHub tracking

| Deliverable | Milestone | Issue |
|---|---|---|
| Phase 1: Alarm Clock | [Milestone 1](https://github.com/QiangWu769/cse421-fall2026/milestone/1) | [Issue #1](https://github.com/QiangWu769/cse421-fall2026/issues/1) |
| Formal Design Document | [Milestone 2](https://github.com/QiangWu769/cse421-fall2026/milestone/2) | [Issue #2](https://github.com/QiangWu769/cse421-fall2026/issues/2) |
| Phase 2: Priority Scheduler | [Milestone 3](https://github.com/QiangWu769/cse421-fall2026/milestone/3) | [Issue #3](https://github.com/QiangWu769/cse421-fall2026/issues/3) |
| Phase 3: MLFQ Scheduler | [Milestone 4](https://github.com/QiangWu769/cse421-fall2026/milestone/4) | [Issue #4](https://github.com/QiangWu769/cse421-fall2026/issues/4) |

Milestones display the due dates. The exact local deadline is 23:59 on each date above, using the stated America/New_York assumption.

## Repository layout

```text
assignments/pa1/
├── README.md                         # PA1 development and submission guide
├── pintos/                           # Complete Pintos project
├── environment/                      # Course Dockerfile and setup guide
├── design/                          # Complete design PDF and implementation plan
├── reports/PHASE1-REPORT.md           # Implementation and verification
└── submissions/phase1/
    └── pa1-phase1.tar.gz              # Phase 1 source archive
scripts/                              # Repository helper scripts
deadlines.json                        # Structured deadlines
DEADLINES.md                          # Requirements and checklists
```

The source `DESIGNDOC` contains all 19 required answers. The nine-page English PDF includes three plain black-and-white vector figures for sleep/wakeup, nested donation, and MLFQS update order, plus the verified C2 scheduling table. It still needs group review and submission to UBLearns. To regenerate it after editing, run `python3 scripts/build-design-pdf.py` in an environment with ReportLab installed.
