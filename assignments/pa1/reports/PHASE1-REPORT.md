# Phase 1 Implementation and Verification Report

Verification date: September 25, 2026.

**Status: Phase 1 completed. The full Design Document PDF, Phase 2, and Phase 3 are not started.**

## Implementation

`src/devices/timer.c` uses a queue ordered by wake-up time and a separate semaphore for each sleep request. A sleeping thread blocks in `sema_down()`. The timer interrupt removes all expired entries and calls `sema_up()` to wake them.

- Removed polling and repeated calls to `thread_yield()` from `timer_sleep()`.
- Zero and negative durations return immediately.
- Sleepers with the same deadline are all signaled during the same timer interrupt.
- The semaphore retains an early signal, avoiding a lost wake-up between queue registration and blocking.
- Interrupts are disabled only while accessing shared queue state; the semaphore performs the actual wait.
- An unsigned 64-bit deadline avoids signed addition overflow for very large positive durations.
- No fields were added to `struct thread`, no heap allocation was introduced, and no course tests or later scheduling components were changed.

The Alarm Clock A1-A6 notes in `src/threads/DESIGNDOC` describe the Phase 1 data structures, algorithm, synchronization, and design choices. These are Phase 1 implementation notes, not a completed or started full Design Document PDF deliverable. Group identities and the other design sections remain to be filled in when that deliverable is started.

## Course tests

After cleaning the previous build, the implementation was rebuilt in the course Docker environment and tested with the default Bochs configuration:

| Test | Result |
|---|---|
| alarm-single | PASS |
| alarm-multiple | PASS |
| alarm-simultaneous | PASS |
| alarm-zero | PASS |
| alarm-negative | PASS |

No compiler warnings originated from the Phase 1 changes. Existing framework warnings in files such as init.c, debug.c, and string.c remained.

## Additional checks

Behavioral checks were added to an independent temporary source copy and were not included in the submission:

- Observed a sleeping thread from another thread and verified `THREAD_BLOCKED`, followed by a normal return at or after its deadline.
- Tested an `INT64_MAX` positive duration and confirmed it did not return early because of deadline overflow.
- Ran eight threads with 100 one-tick sleeps each: all 800 sleeps completed without an early return.
- Independently reviewed the lifetime of stack-local wait records, lost wake-ups, interrupt context, and simultaneous deadlines.

These additional checks passed. The course-test exit statistics also showed that the CPU could become idle during sleep: 250 idle ticks for alarm-single and 550 idle ticks for alarm-multiple.

## Submission archive

`pa1-phase1.tar.gz` contains the complete, cleaned `src/` tree for Autolab Phase 1. It excludes Docker images, temporary behavioral tests, and build output.

The 625 regular files in the archive were checked byte-for-byte against the source tree, and the final archive was extracted into a separate directory and successfully rebuilt. The Bochs source download supplied by the course environment remains in `src/misc/`.

- Archive size: 5,490,858 bytes.
- SHA-256: `e914a0456dc7b8c7c34f822bc7971870b49a5dbb0c7c6c030187273d890b6dad`.

Phase 1 implementation and local verification are complete. Course-platform submission and server grading are unconfirmed. The other three deliverables are not started.
