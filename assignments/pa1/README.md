# Project 1: Pintos Threads

CSE 421/521 Operating Systems, Fall 2026. See [DEADLINES.md](../../DEADLINES.md) for the complete schedule.

| Deliverable | Status |
|---|---|
| Phase 1: Alarm Clock | **Completed** - implementation and local verification |
| Full Design Document PDF | **Not started** |
| Phase 2: Priority Scheduler | **Not started** |
| Phase 3: MLFQ Scheduler | **Not started** |

Course-platform submission and grading are tracked separately. No Autolab submission or server score has been confirmed.

## Completed Phase 1 work

- [Full source tree](pintos/src/): `timer_sleep()` blocks using a semaphore; the timer interrupt wakes expired sleepers.
- [Submission archive](submissions/phase1/pa1-phase1.tar.gz): the complete, cleaned `src/` tree. All five Phase 1 tests passed, and the extracted archive was rebuilt successfully.
- [SHA-256 checksum](submissions/phase1/SHA256SUMS).
- [Implementation and verification report](reports/PHASE1-REPORT.md): records the local checks performed on September 25, 2026.
- [Phase 1 implementation notes](pintos/src/threads/DESIGNDOC): Alarm Clock A1-A6 describe the completed code. These notes accompany Phase 1; the separate full Design Document PDF remains **Not started**.

One group member must submit the final archive to Autolab Phase 1 and check the grading feedback. Uploading files to GitHub does not submit them to the course platform.

## Develop from a new clone

Install and start Docker Desktop. The original course [Dockerfile](environment/Dockerfile) and [Fall 2026 setup guide](environment/Docker_Setup_Guide.pdf) are in `environment/`.

From the repository root:

```bash
./scripts/build-env.sh
./scripts/enter-pintos.sh
```

The scripts select `linux/amd64`, including on Apple Silicon. The local Pintos directory is mounted at `/home/pintos`, so local edits are visible inside the container.

Run the five Phase 1 tests:

```bash
./scripts/test-phase1.sh
```

After changing the code or implementation notes, run the tests and rebuild the archive:

```bash
./scripts/package-phase1.sh
```

The archive is written to `assignments/pa1/submissions/phase1/pa1-phase1.tar.gz`, and its checksum is updated. The script does not upload anything to Autolab.

If an existing local image exactly matches the course Dockerfile, select its name or ID with `PINTOS_IMAGE`. For example, the original development machine used:

```bash
PINTOS_IMAGE=sha256:fd28c381bdb9f830d5d45eafa3d2878eae302ba08296a3152f110688c495e68d ./scripts/enter-pintos.sh
```

The course Dockerfile is preserved unchanged. Building it for the first time requires network access to download dependencies. The Pintos source revision is `9f013d0930202eea99c21083b71098a0df64be0d`.

## Work not started

- **Full Design Document PDF:** complete the [course template](pintos/doc/threads.tmpl), including the adopted or planned designs for every component, and submit the PDF to UBLearns by October 8 at 23:59.
- **Phase 2:** priority scheduling, multiple and nested priority donation for locks, and the `alarm-priority` test.
- **Phase 3:** the MLFQ / 4.4BSD scheduler selected with `-mlfqs`.

The original project license and author information are retained in `pintos/LICENSE` and `pintos/AUTHORS`.
