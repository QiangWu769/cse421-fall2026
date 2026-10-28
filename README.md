# CSE 421/521 - Fall 2026

Course assignments, source code, submission archives, and deadlines. This repository currently contains **Project 1: Pintos Threads**.

**All three Project 1 components are implemented. Phase 3 passed all 27 official tests locally on October 27: nine MLFQS tests and 18 earlier-phase regressions. Phase 1 has confirmed full credit. The user confirmed Phase 2 submission on October 14; its grade is unconfirmed. Phase 3 submission is pending.**

## Deadlines and status

All deadlines below are in **2026 at 23:59**. The Phase 1 Autolab screenshot confirms EDT (UTC-04:00). Remaining deadlines use Buffalo's **America/New_York** local time; official course announcements take precedence.

| Deliverable | Deadline | Points | Platform | Status |
|---|---|---:|---|---|
| Phase 1: Alarm Clock | September 30, 23:59 | 14 | [Autolab](https://autolab.cse.buffalo.edu/) | Submitted and graded: 100/100 |
| Formal Design Document | October 8, 23:59 | 12 | UBLearns, PDF | Eight-page template PDF selected as final; submission unconfirmed |
| Phase 2: Priority Scheduler | October 14, 23:59 | 42 | [Autolab](https://autolab.cse.buffalo.edu/) | Submitted October 14, user confirmed; grade unconfirmed |
| Phase 3: MLFQ Scheduler | October 27, 23:59 | 37 | [Autolab](https://autolab.cse.buffalo.edu/) | Implemented; 27/27 local tests passed; submission pending |

Implementation is worth **93 points**, plus **12 points** for the formal design document, for a total of **105 points**. The 4-point `alarm-priority` test belongs to Phase 2, giving phase totals of 14, 42, and 37.

See [DEADLINES.md](DEADLINES.md) for requirements and checklists, and [deadlines.json](deadlines.json) for structured dates. Dates for other semester projects and exams have not been provided.

## Phase 1 progress

The following work was completed and locally verified on **2026-09-25**:

- `timer_sleep()` blocks using an ordered sleep queue and a semaphore, without busy waiting.
- All five Phase 1 course tests passed. Additional checks passed for actual `THREAD_BLOCKED` state, an `INT64_MAX` delay, and 800 concurrent short sleeps.
- The complete source archive was generated, extracted into a separate directory, and compiled successfully.
- Alarm Clock A1-A6 notes are included in the source [DESIGNDOC](assignments/pa1/pintos/src/threads/DESIGNDOC). Group identities are filled in. The working document covers all 19 questions and is maintained separately from the retained Phase 1 archive.

**The user-provided Autolab screenshot confirms 100/100, all five tests passed, and 14/14 rubric points.** See the [Phase 1 report](assignments/pa1/reports/PHASE1-REPORT.md) for the local verification record.

## Phase 2 progress

Priority scheduling, immediate preemption, priority-aware synchronization, and multiple/nested lock donation are implemented. The final clean build passed all **18 course tests** covering Phase 2 and Phase 1, using the course image and **Bochs 2.6.11**. Six supplemental edge cases passed in a disposable source copy; course tests were not modified.

The 13 Phase 2 tests cover its **42-point rubric locally**. This is not an Autolab score. The [Phase 2 archive](assignments/pa1/submissions/phase2/pa1-phase2.tar.gz) was extracted into an isolated container, rebuilt, and passed all 18 course and regression tests again. Its 625 source files matched the October 9 source snapshot byte-for-byte. See the dated [Phase 2 report](assignments/pa1/reports/PHASE2-REPORT.md) for individual results and the checksum. The user subsequently confirmed submission on **October 14**; the platform grade has not been supplied.

## Phase 3 progress

The 4.4BSD-style scheduler is implemented with signed 17.14 fixed-point arithmetic, inherited `nice`/`recent_cpu` state, periodic load and priority updates, idle exclusion, and the `-mlfqs` startup option. The final clean build passed **all 27 official tests** on Bochs 2.6.11. Each test uses the scheduler mode selected by the course Makefile.

The nine MLFQS tests cover **37 rubric points locally**; this is not an Autolab grade. Seven supplemental scheduler groups passed, as did 31 targeted arithmetic assertions, 53,930 helper comparisons against a rational-arithmetic oracle, and 70,050 scheduler-method comparisons. These are supplemental checks, not additional course tests. The verified [Phase 3 archive](assignments/pa1/submissions/phase3/pa1-phase3.tar.gz) contains 626 regular files that matched the cleaned source tree at packaging time. It was independently extracted and rebuilt, and all **27 official tests passed again**. See [PHASE3-REPORT.md](assignments/pa1/reports/PHASE3-REPORT.md).

## Start here

1. **Develop and test:** read the [PA1 guide](assignments/pa1/README.md). Course environment files are in [environment/](assignments/pa1/environment/).
2. **Use the final design submission:** the [eight-page template PDF](assignments/pa1/design/PA1-DESIGNDOC-TEMPLATE.pdf) is the selected final submission version. It contains all 19 answers from the completed source [DESIGNDOC](assignments/pa1/pintos/src/threads/DESIGNDOC), covering all three implemented components. The instructor confirmed on [Piazza @135](https://piazza.com/class/mr5d91n9mi73f/post/135): "Use the same template with your updated implementation." The [nine-page formatted version](assignments/pa1/design/PA1-DESIGNDOC-FINAL.pdf) is an alternate, and the [earlier proposal](assignments/pa1/design/PA1-DESIGNDOC.pdf) remains historical. UBLearns submission is unconfirmed.
3. **Finish the Phase 3 submission:** confirm the Phase 3 group, upload the verified archive to Autolab by **October 27 at 23:59**, and retain the grading result. Implementation and local/archive verification are complete. Record the Phase 2 grade and design-PDF submission confirmation when available.

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
├── design/                           # Final design PDF, earlier proposal, implementation notes
├── reports/                          # Verification records for all three phases
└── submissions/
    ├── phase1/pa1-phase1.tar.gz       # Retained Phase 1 source archive
    ├── phase2/pa1-phase2.tar.gz       # Retained Phase 2 source archive
    └── phase3/pa1-phase3.tar.gz       # Verified complete Project 1 source archive
scripts/                              # Repository helper scripts
deadlines.json                        # Structured deadlines
DEADLINES.md                          # Requirements and checklists
```

The [selected final PDF](assignments/pa1/design/PA1-DESIGNDOC-TEMPLATE.pdf) follows the original text-template format: monospaced text, `>>` question labels, section dividers, an ASCII nested-donation diagram, and the C2 text table. It was prepared on October 27 from the updated `DESIGNDOC`. The nine-page formatted PDF and original proposal are retained as separate versions. This selection does not change the verified Phase 3 source archive. The original design-PDF deadline was October 8; no separate revision deadline or UBLearns submission confirmation has been supplied.

To regenerate the selected template PDF, run `python3 scripts/build-template-design-pdf.py` with ReportLab installed, then render and inspect every page before submission.
