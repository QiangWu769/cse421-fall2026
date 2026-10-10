# Phase 2 Implementation and Verification Report

Verification date: **October 9, 2026**.

**Phase 2 is implemented and locally verified. All 13 Phase 2 course tests, all five Phase 1 regression tests, and six supplemental edge cases passed. The source archive was extracted, rebuilt, and passed all 18 course tests again. Phase 2 has not been submitted to or graded by Autolab.**

## Implemented behavior

- The scheduler selects the first ready thread with the greatest current effective priority. New and yielding threads join the tail, retaining FIFO order among equal priorities.
- Higher-priority ready threads preempt after creation, semaphore updates, priority changes, and direct interrupt-queue wakeups. Interrupt handlers request a switch on interrupt return. A ready thread also displaces idle when both priorities are zero.
- Semaphore and condition-variable wakeups select by current effective priority. This accounts for donations received after a thread joined a wait queue.
- Each thread records its base priority, held locks, and pending lock acquisition. Each lock records pending contenders. Effective priority is recomputed from the base priority and contenders for all held locks; nested donation follows at most eight holders and stops on a cycle.
- Releasing a lock removes only that lock's contribution to donation. An unblocked lock contender remains registered until acquisition succeeds, including if another thread retakes the lock. Successful `lock_try_acquire()` calls update the same ownership records.
- Condition wait records store a thread pointer, allowing a signal before the waiter enters its private semaphore wait and preserving visibility of later priority changes.
- `thread_set_priority()` updates the base priority and recomputes effective priority. `thread_get_priority()` returns effective priority. The existing semaphore-based Alarm Clock remains intact.

Production code changes are limited to these five files:

| File under `src/` | Purpose |
|---|---|
| `threads/thread.h` | Priority and lock state; shared helper declarations |
| `threads/thread.c` | Ready selection, donation propagation, priority updates, and preemption |
| `threads/synch.h` | Lock contender and ownership links |
| `threads/synch.c` | Priority-aware wakeups and lock donation bookkeeping |
| `devices/intq.c` | Check preemption after clearing the direct-unblock waiter pointer |

The code does not busy-wait. Blocking still uses Pintos semaphores and locks. Interrupt protection is used for the scheduler and synchronization metadata while preserving the original interrupt state. The existing Phase 1 `devices/timer.c` and official course tests were not changed.

## Environment and reproducible course tests

Tests ran in the course Docker image on `linux/amd64`, using **Bochs 2.6.11** and the supplied Pintos build system. The image ID was:

```text
sha256:fd28c381bdb9f830d5d45eafa3d2878eae302ba08296a3152f110688c495e68d
```

The source is based on course revision `9f013d0930202eea99c21083b71098a0df64be0d`. The compiler was **GCC 7.5.0**, specifically `gcc (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0`; see the [compiler record](phase2/compiler.txt).

From the repository root, with the course image installed:

```bash
PINTOS_IMAGE=sha256:fd28c381bdb9f830d5d45eafa3d2878eae302ba08296a3152f110688c495e68d \
./scripts/test-phase2.sh
```

The script cleans and rebuilds the kernel, requests the 18 exact `.result` targets with `SIMULATOR=--bochs`, and requires `PASS` in every result file. The final log states `Phase 2 and Phase 1 regression tests: 18/18 passed.` Existing framework compiler warnings remain; they are not test failures.

| Course test | Scope | Rubric points | Local result |
|---|---|---:|---|
| `alarm-priority` | Phase 2 | 4 | PASS |
| `priority-change` | Phase 2 | 3 | PASS |
| `priority-preempt` | Phase 2 | 3 | PASS |
| `priority-fifo` | Phase 2 | 3 | PASS |
| `priority-sema` | Phase 2 | 3 | PASS |
| `priority-condvar` | Phase 2 | 3 | PASS |
| `priority-donate-one` | Phase 2 | 3 | PASS |
| `priority-donate-multiple` | Phase 2 | 3 | PASS |
| `priority-donate-multiple2` | Phase 2 | 3 | PASS |
| `priority-donate-nest` | Phase 2 | 3 | PASS |
| `priority-donate-chain` | Phase 2 | 5 | PASS |
| `priority-donate-sema` | Phase 2 | 3 | PASS |
| `priority-donate-lower` | Phase 2 | 3 | PASS |
| `alarm-single` | Phase 1 regression | 4 | PASS |
| `alarm-multiple` | Phase 1 regression | 4 | PASS |
| `alarm-simultaneous` | Phase 1 regression | 4 | PASS |
| `alarm-zero` | Phase 1 regression | 1 | PASS |
| `alarm-negative` | Phase 1 regression | 1 | PASS |

The 12 priority tests account for 38 points; `alarm-priority` adds 4, covering **42 Phase 2 points locally**. The five Phase 1 regressions cover its earlier 14-point rubric. These local results are not an Autolab grade.

## Supplemental edge cases

A separate harness was compiled only in a disposable source copy inside a fresh course-image container. The production source was mounted read-only. Temporary registration changes were confined to that copy; neither the harness nor its registrations were added to the production source or official tests.

All six checks emitted their success messages, followed by `(priority-edge-cases) PASS` and `(priority-edge-cases) end`, with no `PANIC` or `FAIL`:

1. A condition signal arrives after releasing the monitor lock but before entering the waiter's private semaphore wait.
2. A lock contender becomes ready, another thread retakes the lock, and the pending contender continues to contribute donation.
3. Equal-priority semaphore waiters wake in FIFO order.
4. A condition waiter receives a donation after joining the condition queue, and selection uses its updated priority.
5. Interrupt-queue readers and writers preempt only after the corresponding waiter pointer is cleared.
6. A priority-zero sleeper wakes correctly while the idle thread is running.

The [course-test summary](phase2/course-tests.txt), [supplemental test log](phase2/edge-tests.log), and [archive-test summary](phase2/archive-tests.txt) retain the results. The original full local logs are `tmp/phase2/standard-tests-final.log` and `tmp/phase2/edge-test.log`. The supplemental checks are development evidence, not additional course rubric tests.

## Source archive and submission

The verified [Phase 2 archive](../submissions/phase2/pa1-phase2.tar.gz) has its [SHA256SUMS](../submissions/phase2/SHA256SUMS) beside it.

- Size: **5,494,793 bytes**.
- Contents: **625 regular files** in the complete cleaned `src/` tree.
- SHA-256: `0471d8fc579f12c8fda694a19d279cc2a9a909d849596c2b85a3bb2be533a7ea`.
- Every archived source file matches the working source tree byte-for-byte. No build directory, temporary output, or supplemental harness is included.
- The actual archive was extracted into an isolated container and rebuilt with GCC 7.5.0. All **18 course and regression tests passed again** on Bochs; see the [extracted-archive test summary](phase2/archive-tests.txt).

The packaging script runs `make -C src clean`, rejects residual build or temporary files, and packages the complete `src/` tree. It writes only the Phase 2 submission directory. The original Phase 1 archive and its verified submission history are retained unchanged.

Confirm group membership for Phase 2, upload the verified archive to Autolab by **October 14, 2026 at 23:59 America/New_York**, and retain the grading result. GitHub storage and local testing do not replace this submission.

## Design documents and remaining scope

The working `src/threads/DESIGNDOC` is maintained with the source implementation. The existing **eight-page PDF** is the proposal prepared before Phase 2 code completion and has not been regenerated for these changes. Its UBLearns deadline was October 8; actual submission status is unconfirmed.

**Phase 3 remains not started.** No MLFQS calculation implementation or Phase 3 test result is claimed. Its planned design remains in the source design document and implementation plan.
