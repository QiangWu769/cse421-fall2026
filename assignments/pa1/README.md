# Project 1: Pintos Threads

CSE 421/521 Operating Systems, Fall 2026. See [DEADLINES.md](../../DEADLINES.md) for the complete schedule.

| Deliverable | Status |
|---|---|
| Phase 1: Alarm Clock | **Completed** - Autolab 100/100; 14/14 points |
| Full Design Document PDF | **Prepared** - earlier eight-page proposal; UBLearns submission unconfirmed |
| Phase 2: Priority Scheduler | **Implemented and locally verified** - 18 course tests and six edge cases passed; not submitted |
| Phase 3: MLFQ Scheduler | **Not started** |

The user-provided Autolab result confirms five Phase 1 tests passed and a score of 100/100. No Phase 2 Autolab submission or grade is claimed. The actual UBLearns submission status of the design PDF is unknown.

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

See [PHASE2-REPORT.md](reports/PHASE2-REPORT.md) for individual results. The 13 Phase 2 tests cover **42 rubric points locally**, not an Autolab score. The verified [Phase 2 archive](submissions/phase2/pa1-phase2.tar.gz) contains 625 source files matching the current tree; an isolated extraction, rebuild, and repeat of all 18 course tests passed. Its [SHA256SUMS](submissions/phase2/SHA256SUMS) is recorded separately.

## Develop from a new clone

Install and start Docker Desktop. The original course [Dockerfile](environment/Dockerfile) and [Fall 2026 setup guide](environment/Docker_Setup_Guide.pdf) are in `environment/`.

From the repository root:

```bash
./scripts/build-env.sh
./scripts/enter-pintos.sh
```

The scripts select `linux/amd64`, including on Apple Silicon. The local Pintos directory is mounted at `/home/pintos`, so local edits are visible inside the container.

Run the Phase 2 suite and all five Phase 1 regression tests:

```bash
./scripts/test-phase2.sh
```

The script cleans and rebuilds the kernel, explicitly selects Bochs, and checks all 18 `.result` files for `PASS`. After code and design notes are ready, create the complete Phase 2 source archive:

```bash
./scripts/package-phase2.sh
```

The archive is written to `assignments/pa1/submissions/phase2/pa1-phase2.tar.gz`, with `SHA256SUMS` in the same directory. The packaging script cleans the source tree and rejects leftover build or temporary files. It does not upload anything to Autolab. Preserve `submissions/phase1/` as the earlier submission record; do not overwrite it when preparing Phase 2.

`./scripts/test-phase1.sh` remains available to run only the five original alarm tests. The Phase 2 script includes those same tests as regressions.

If an existing local image exactly matches the course Dockerfile, select its name or ID with `PINTOS_IMAGE`. For example, the original development machine used:

```bash
PINTOS_IMAGE=sha256:fd28c381bdb9f830d5d45eafa3d2878eae302ba08296a3152f110688c495e68d ./scripts/enter-pintos.sh
```

The course Dockerfile is preserved unchanged. Building it for the first time requires network access to download dependencies. The Pintos source revision is `9f013d0930202eea99c21083b71098a0df64be0d`.

## Remaining work

- **Design document submission confirmation:** the [eight-page English PDF](design/PA1-DESIGNDOC.pdf) was prepared before Phase 2 implementation and has not been regenerated for these code changes. It includes every required answer, three diagrams, and the C2 table. Its deadline was October 8 at 23:59; actual UBLearns submission is unconfirmed. The current [DESIGNDOC](pintos/src/threads/DESIGNDOC) and [implementation notes and plan](design/IMPLEMENTATION-PLAN.txt) are maintained separately from that historical PDF.
- **Phase 2 submission:** confirm group membership for Phase 2, upload the verified archive to Autolab by October 14 at 23:59, and record the grading result. Local testing and package verification are complete; Autolab submission and grading remain outstanding.
- **Phase 3:** the MLFQ / 4.4BSD scheduler selected with `-mlfqs`.

The original project license and author information are retained in `pintos/LICENSE` and `pintos/AUTHORS`.
