# Deadlines and Submission Checklists

Based on the supplied CSE 421/521 Fall 2026 Project 1 assignment and submission instructions. Last updated: **2026-10-09**.

**Time zone:** the Phase 1 Autolab screenshot confirms EDT (UTC-04:00). Remaining deadlines use Buffalo's **America/New_York** local time. Every deadline below is in 2026 at **23:59**. Official course announcements and platform instructions take precedence; update this file and [deadlines.json](deadlines.json) if the course publishes changes.

## Overview

| Deliverable | Deadline | Points | Format and platform | Status |
|---|---|---:|---|---|
| Phase 1: Alarm Clock | 2026-09-30 23:59 | 14 | Complete source tree in `.tar.gz`, Autolab | Submitted and graded: 100/100 |
| Formal Design Document | 2026-10-08 23:59 | 12 | PDF, UBLearns; retain `src/threads/DESIGNDOC` in the source tree | PDF prepared; submission unconfirmed |
| Phase 2: Priority Scheduler | 2026-10-14 23:59 | 42 | Complete source tree in `.tar.gz`, Autolab | Implemented; locally verified; not submitted |
| Phase 3: MLFQ Scheduler | 2026-10-27 23:59 | 37 | Complete source tree in `.tar.gz`, Autolab | Not started |

Implementation: 14 + 42 + 37 = **93 points**. Formal design document: **12 points**. Total: **105 points**.

The assignment also lists component totals of 18 points for Alarm Clock and 38 for Priority Scheduler. The phase totals differ because the **4-point `alarm-priority` test is submitted with Phase 2**.

## Phase 1: Alarm Clock

**Due September 30 at 23:59 | 14 points | Autolab**

**Status: Submitted and graded. Autolab 100/100; five tests passed; 14/14 rubric points.**

Track: [Milestone 1](https://github.com/QiangWu769/cse421-fall2026/milestone/1) | [Issue #1](https://github.com/QiangWu769/cse421-fall2026/issues/1).

Reimplement `timer_sleep()` in `devices/timer.c` so the caller blocks until at least the requested number of timer ticks has elapsed, then becomes ready. The argument is in ticks; the thread does not need to receive the CPU immediately at its deadline. Zero and negative delays return immediately.

Requirements:

- Do not busy-wait by polling the clock or repeatedly calling `thread_yield()`.
- Use appropriate synchronization primitives. Interrupt handlers cannot acquire locks that may block.
- Briefly disabling interrupts is permitted to protect data shared with an interrupt handler; it must not be the sole synchronization mechanism.
- Keep the default `TIMER_FREQ`. The millisecond, microsecond, and nanosecond sleep wrappers do not need to change.
- The assignment lists a **14-point deduction** for a busy-waiting alarm and a separate **14-point deduction** for using interrupt disabling as the sole synchronization mechanism. Passing timing tests alone does not establish compliance.

The following course tests passed locally on **2026-09-25**:

| Test | Points | Local result |
|---|---:|---|
| `alarm-single` | 4 | PASS |
| `alarm-multiple` | 4 | PASS |
| `alarm-simultaneous` | 4 | PASS |
| `alarm-zero` | 1 | PASS |
| `alarm-negative` | 1 | PASS |

`alarm-priority` is a Phase 2 requirement.

Implementation and verification record:

- [x] Implement the ordered sleep queue and semaphore-based blocking.
- [x] Pass the five Phase 1 course tests on 2026-09-25.
- [x] Verify actual `THREAD_BLOCKED` state, an `INT64_MAX` delay, and 800 short sleeps across eight threads.
- [x] Generate the complete source archive, extract the final archive, and compile it successfully.
- [x] Include Alarm Clock A1-A6 implementation notes with the Phase 1 source. These answers have now been reviewed for the formal design draft.

Submission follow-up:

- [x] Enter actual group names and email addresses.
- [ ] Review the design together before the PDF submission.
- [x] Complete the Phase 1 group submission.
- [x] Confirm grading from the user-provided screenshot: 100/100, five tests passed, 14/14 points. The screenshot does not show the exact submission time.

Archive: [pa1-phase1.tar.gz](assignments/pa1/submissions/phase1/pa1-phase1.tar.gz). Verification details: [PHASE1-REPORT.md](assignments/pa1/reports/PHASE1-REPORT.md). If files change, test again and produce an archive containing the latest version.

## Formal Design Document

**Due October 8 at 23:59 | 12 points | PDF submitted to UBLearns**

**Status: Complete eight-page English PDF prepared. UBLearns submission is unconfirmed.**

Track: [Milestone 2](https://github.com/QiangWu769/cse421-fall2026/milestone/2) | [Issue #2](https://github.com/QiangWu769/cse421-fall2026/issues/2).

Prepare the formal document using the course `threads.tmpl` template and retain [src/threads/DESIGNDOC](assignments/pa1/pintos/src/threads/DESIGNDOC) in the source tree. Cover the data structures, algorithms, synchronization, and design rationale for **all project components**, including completed and planned designs.

This deadline precedes the Phase 2 and Phase 3 implementation deadlines. The formal document must therefore describe the planned designs for components whose code is not yet complete; it cannot wait until all later implementations are finished.

The [complete English PDF](assignments/pa1/design/PA1-DESIGNDOC.pdf) covers all 19 required questions. It is the earlier proposal, prepared before the Phase 2 code was implemented, and has not been regenerated for the October 9 changes. The Alarm Clock answers, nested donation diagram, and C2 scheduling table were reviewed. The source `DESIGNDOC` and [implementation plan](assignments/pa1/design/IMPLEMENTATION-PLAN.txt) track the current implementation and remaining Phase 3 plan.

- [x] Begin the formal draft and enter every group member's name and UB email address.
- [x] Review the Alarm Clock design against the completed implementation.
- [x] Complete Priority Scheduling questions B1-B7, including multiple and nested priority donation.
- [x] Complete Advanced Scheduler questions C1-C6, including the scheduling example table and fixed-point arithmetic design.
- [x] Include checked technical references.
- [x] Produce the complete eight-page PDF and inspect every rendered page.
- [ ] Confirm group review of the document.
- [ ] Record UBLearns submission confirmation; actual submission status is currently unknown.

Saving source notes on GitHub or including `DESIGNDOC` in a source archive does not replace the separate PDF submission to UBLearns.

## Phase 2: Priority Scheduler

**Due October 14 at 23:59 | 42 points | Autolab**

**Status: Implemented and locally verified on October 9. All 13 Phase 2 tests, five Phase 1 regressions, and six supplemental edge cases passed. Not submitted to or graded by Autolab.**

Track: [Milestone 3](https://github.com/QiangWu769/cse421-fall2026/milestone/3) | [Issue #3](https://github.com/QiangWu769/cse421-fall2026/issues/3).

Requirements:

- Select the highest-priority ready thread and promptly yield when a higher-priority thread becomes ready.
- Wake the highest-priority thread waiting on a lock, semaphore, or condition variable first.
- Handle equal-priority scheduling and the FIFO test requirements correctly.
- Implement priority donation for locks, including multiple and nested donations; revoke the relevant donations when a lock is released.
- Implement `thread_set_priority()` and `thread_get_priority()`, including effective priority and yielding after a priority decrease when required.
- Preserve Alarm Clock behavior and pass `alarm-priority`.

| Test | Points |
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

- [x] Implement priority scheduling and priority-aware synchronization wait queues.
- [x] Implement multiple and nested lock donation and its removal.
- [x] Pass all 13 tests above and all five Phase 1 regression tests on real Bochs.
- [x] Pass six supplemental cases in a disposable source copy: early condition signal, runnable lock contender/retake, semaphore FIFO, condition waiter donation after enqueue, direct interrupt-queue wakeup, and priority-zero wakeup from idle.
- [x] Keep the source `DESIGNDOC` consistent with the final Phase 2 implementation.
- [x] Clean and archive the complete source tree, verify all 625 source files against the working tree, rebuild from the extracted archive, and pass all 18 course and regression tests again.
- [ ] Confirm group membership for the corresponding Autolab phase, upload, and review grading feedback.

See [PHASE2-REPORT.md](assignments/pa1/reports/PHASE2-REPORT.md) for the individual local results. Local success covers the 42-point Phase 2 rubric; it does not establish an Autolab grade. The verified [Phase 2 archive](assignments/pa1/submissions/phase2/pa1-phase2.tar.gz) has a separate [SHA256SUMS](assignments/pa1/submissions/phase2/SHA256SUMS). The original Phase 1 archive is retained unchanged.

## Phase 3: MLFQ Scheduler

**Due October 27 at 23:59 | 37 points | Autolab**

**Status: Not started.**

Track: [Milestone 4](https://github.com/QiangWu769/cse421-fall2026/milestone/4) | [Issue #4](https://github.com/QiangWu769/cse421-fall2026/issues/4).

Implement the multilevel feedback queue scheduler specified by the Pintos 4.4BSD scheduler requirements. Use the priority scheduler by default and select the advanced scheduler with the `-mlfqs` kernel option.

Requirements:

- Implement `nice`, `recent_cpu`, `load_avg`, and their update rules for computed priorities.
- Follow Pintos Appendix B for formulas, update timing, and fixed-point rounding behavior.
- Do not perform priority donation in MLFQS mode.
- In MLFQS mode, ignore the priority argument to `thread_create()` and calls to `thread_set_priority()`; return the scheduler-computed priority from `thread_get_priority()`.
- Preserve the default scheduling mode and Alarm Clock behavior.

| Test | Points |
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

- [ ] Read Appendix B and design the fixed-point operations and scheduler state.
- [ ] Implement MLFQS calculations, update timing, and selection through the kernel option.
- [ ] Pass all nine tests above and run regression tests for the earlier phases.
- [ ] Keep the source `DESIGNDOC` consistent with the final implementation.
- [ ] Clean build outputs, archive the complete source tree, and verify that the archive builds.
- [ ] Confirm group membership for the corresponding Autolab phase, upload, and review grading feedback.

## Check every source submission

1. Submit the complete `src/` tree, not only changed files. It must compile with `make` after cleaning.
2. Confirm that every member has accepted the group invitation for the relevant phase. One member's submission applies to the whole group.
3. Upload early to [Autolab](https://autolab.cse.buffalo.edu/) and inspect the result. The course instructions state that **the latest submission determines the score**; check the feedback after each resubmission.
4. Record platform confirmation in the relevant issue. Keep local verification, GitHub storage, and confirmed course-platform submission as separate facts.

Tracking: [milestones](https://github.com/QiangWu769/cse421-fall2026/milestones) | [issues](https://github.com/QiangWu769/cse421-fall2026/issues).

## Dates not yet provided

Dates for other semester projects, quizzes, midterms, and final exams have not been supplied. Add them only after the official course schedule is available.
