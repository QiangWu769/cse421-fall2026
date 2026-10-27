# Phase 3 Implementation and Verification Report

Verification date: **October 27, 2026**.

**Phase 3 is implemented and verified. All 27 official tests and seven supplemental scheduler groups passed. The actual source archive was independently extracted and rebuilt, then passed all 27 official tests again. The nine MLFQS tests cover 37 rubric points locally; this is not an Autolab grade. Phase 3 submission is pending.**

## Implemented behavior

- Each thread stores `nice` and signed 17.14 `recent_cpu`; `load_avg` is global. Ordinary MLFQS threads inherit both per-thread values from their creator before publication. The initial thread starts at zero, while idle is identified explicitly and excluded from CPU and ready-thread accounting.
- The scheduler computes priorities from the full integer expression before conversion and clamping. Load average is updated with one combined numerator and one division; `recent_cpu` preserves negative values. Arithmetic helpers use 64-bit intermediates without floating point.
- `thread_tick()` accounts the running thread, the timer interrupt wakes due alarm requests, and `thread_tick_end()` performs periodic updates. Load average and every non-idle thread's `recent_cpu` update once per second; all non-idle priorities update every fourth global tick, including blocked threads.
- The timer's `tick_in_progress` and `ready_changed` flags defer MLFQS wakeup-related preemption decisions until periodic calculations finish, so decisions use current priorities. Context switches occur after interrupt return.
- The `-mlfqs` option selects the advanced scheduler, ignores manually supplied priorities, and bypasses lock donation. Default-mode priority scheduling and donation remain available. `thread_set_nice()` recomputes priority and checks preemption; the CPU/load getters return values multiplied by 100 and rounded to nearest, with halves away from zero.
- Ready-list selection continues to choose the first entry with the greatest current priority, retaining FIFO order among equal priorities and round-robin behavior with the four-tick quantum.

| Changed source file | Purpose |
|---|---|
| `src/threads/fixed-point.h` | New signed 17.14 helper functions with 64-bit intermediates |
| `src/threads/thread.h` | Per-thread MLFQS fields and end-of-tick interface |
| `src/threads/thread.c` | Initialization, inheritance, accounting, formulas, getters/setters, and final preemption decisions |
| `src/devices/timer.c` | Invoke end-of-tick updates after expired alarm requests are signaled |

The source `src/threads/DESIGNDOC` separately records all implemented components. Official course tests were not modified.

## Integer formulas and update order

Let `F = 16384`, and let `L` and `R` denote the stored fixed-point integers for `load_avg` and `recent_cpu`. The implementation uses 64-bit intermediates:

```text
priority = ((PRI_MAX - 2 * nice) * 4 * F - R) / (4 * F)
L = (59 * L + ready_threads * F) / 60
coefficient = (2 * L * F) / (2 * L + F)
R = (coefficient * R) / F + nice * F
```

Integer division truncates toward zero. Priority is clamped to `PRI_MIN..PRI_MAX`; positive in-range values therefore round down as required. The code does not discard the fractional part of `recent_cpu / 4` before evaluating the complete priority expression. The reporting getters scale by 100 in 64 bits before applying signed nearest-integer rounding.

The timer increments ticks, accounts CPU use, wakes due alarms, updates load average and `recent_cpu` at second boundaries, recomputes priorities at four-tick boundaries, and then performs preemption/time-slice checks. When both boundaries coincide, priority uses the newly updated CPU/load state. Ready-thread counting includes threads whose alarms expire at that boundary and excludes idle.

## Official course tests

The full suite ran in the course `linux/amd64` Docker environment with **GCC 7.5.0** and **Bochs 2.6.11**. The [compiler record](phase3/compiler.txt) reports `gcc (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0`. The image used for this project is:

```text
sha256:fd28c381bdb9f830d5d45eafa3d2878eae302ba08296a3152f110688c495e68d
```

From the repository root:

```bash
PINTOS_IMAGE=sha256:fd28c381bdb9f830d5d45eafa3d2878eae302ba08296a3152f110688c495e68d \
./scripts/test-phase3.sh
```

The script cleans and rebuilds, runs `make check` with `SIMULATOR=--bochs`, and checks every expected `.result` for `PASS`. The official `Make.tests` enables `-mlfqs` and a 480-second timeout only for the nine advanced-scheduler tests. The other 18 tests use default priority scheduling. The final log reports both `All 27 tests passed.` and `Phase 3 and earlier regression tests: 27/27 passed.`

| Phase 3 test | Rubric points | Local result |
|---|---:|---|
| `mlfqs-load-1` | 5 | PASS |
| `mlfqs-load-60` | 5 | PASS |
| `mlfqs-load-avg` | 3 | PASS |
| `mlfqs-recent-1` | 5 | PASS |
| `mlfqs-fair-2` | 5 | PASS |
| `mlfqs-fair-20` | 3 | PASS |
| `mlfqs-nice-2` | 4 | PASS |
| `mlfqs-nice-10` | 2 | PASS |
| `mlfqs-block` | 5 | PASS |

The following 18 earlier-phase regressions also passed:

- Alarm tests: `alarm-single`, `alarm-multiple`, `alarm-simultaneous`, `alarm-zero`, `alarm-negative`, and `alarm-priority`.
- Priority tests: `priority-change`, `priority-preempt`, `priority-fifo`, `priority-sema`, `priority-condvar`, `priority-donate-one`, `priority-donate-multiple`, `priority-donate-multiple2`, `priority-donate-nest`, `priority-donate-chain`, `priority-donate-sema`, and `priority-donate-lower`.

The [course-test summary](phase3/course-tests.txt) records all 27 results; the original local log is `tmp/phase3/course-tests.log`. These results establish local test success, not a platform submission or grade.

## Independent arithmetic validation

The implementation also passed:

- **31 targeted arithmetic assertions**.
- **53,930 fixed-point helper comparisons** against an independent rational-arithmetic oracle.
- **70,050 scheduler-method comparisons** covering the integer calculation methods.

These checks are independent validation, not additional official tests or rubric points. The local validation sources are retained under `tmp/phase3/`; they are not part of the submitted `src/` tree.

## Supplemental scheduler checks

A separate MLFQS harness ran only in a disposable source copy, with the production source mounted read-only. The final run passed all seven groups:

1. Niceness bounds, ignored manual priorities, and signed rounding.
2. Child inheritance of `nice` and `recent_cpu` before its first run.
3. FIFO dispatch among equal computed priorities.
4. Lock donation remains disabled in MLFQS mode.
5. Priority updates occur on the fourth global tick.
6. Priority-zero wakeup and idle exclusion from CPU accounting.
7. Second-boundary alarm wakeups are counted before the load-average update.

The [supplemental test log](phase3/edge-tests.log) contains all seven success messages, `(mlfqs-edge-cases) PASS`, `(mlfqs-edge-cases) end`, and the runner's explicit all-seven-passed summary. The original final log is `tmp/phase3/edge-verified.log`.

An initial FIFO check failed because a timer tick could lower a newly dispatched thread's priority before its entry function ran. The corrected setup uses inherited `nice=-20` to keep the tested priorities equal at 63. The runner also isolates emulator stdin so the remaining verification commands execute. These changes affected only the temporary harness; the production implementation was unchanged.

## Source archive and submission

The verified [Phase 3 archive](../submissions/phase3/pa1-phase3.tar.gz) has its [SHA256SUMS](../submissions/phase3/SHA256SUMS) beside it.

- Size: **5,496,294 bytes**.
- Contents: **626 regular files** in the complete cleaned `src/` tree.
- SHA-256: `283560a63b1a8080bd2b5a80f45b75ddcf92a671c4d988d04dff9a45b7ef7b57`.
- Every archived file matches the cleaned production source byte-for-byte. No build output or supplemental harness is included.
- The actual archive was extracted into an isolated course-image container and rebuilt using GCC 7.5.0. All **27 official tests passed again** on Bochs 2.6.11; see the [archive-test summary](phase3/archive-tests.txt). The original full runner log is `tmp/phase3/archive-verification.log`.

The packaging script cleans the complete `src/` tree, rejects leftover build and temporary files, and writes only the Phase 3 submission directory. Earlier Phase 1 and Phase 2 archives are retained unchanged.

Implementation and local/archive verification are complete. Confirm the Phase 3 group and upload the verified archive to Autolab by **October 27, 2026 at 23:59 America/New_York**. Retain the platform result. GitHub storage and local tests do not replace the submission.

## Earlier submissions and design-document status

- **Phase 1:** the user-provided Autolab result confirms 100/100 and 14/14 rubric points.
- **Phase 2:** the user confirmed submission on October 14. Its platform grade is unconfirmed; the October 9 report remains the historical local-verification record.
- **Design PDF:** the existing eight-page PDF remains the historical proposal from before Phase 2 and Phase 3 implementation. It has not been regenerated for the completed code. Its UBLearns submission status is unconfirmed.
- **Current source design document:** `src/threads/DESIGNDOC` describes all three implemented components, including the final timer-update order and full integer formulas.
