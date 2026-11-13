# Project 2: User Programs

CSE 421/521 Operating Systems, Fall 2026.

| Deliverable | Deadline, America/New_York | Weight | Status |
|---|---|---|---|
| Design document PDF | November 23, 2026, 23:59 EST | 10% | Proposal prepared; group review and UBLearns submission pending |
| Complete source tree | December 11, 2026, 23:59 EST | 90% | Clean source prepared; implementation not started |

The supplied assignment's explicit November 23 date is used for the design
deadline. Its description of that date as three weeks before December 11 is
inconsistent. No revised deadline or submission confirmation has been supplied.

## Design proposal

Use the [original-template PDF](design/PA2-DESIGNDOC.pdf), prepared November 13.
It answers all **15 required questions**, A1-A4 and B1-B11. The editable
[DESIGNDOC](pintos/src/threads/DESIGNDOC) is in the location specified by the
course assignment. The original [userprog.tmpl](pintos/doc/userprog.tmpl)
remains available for comparison.

The proposal describes single-page argument setup, checked user-memory copies,
per-process file descriptors, filesystem serialization, load/exit signaling,
reference-counted child status, and executable write denial. Proposed declarations
are design choices; they have not yet been added to the kernel.

To rebuild the PDF with ReportLab installed:

```bash
python3 scripts/build-pa2-design-pdf.py
```

Review every rendered page after changing the source document. The PDF is for
UBLearns; keeping a copy on GitHub does not submit it to the course.

## Source baseline

`pintos/` is a separate export of the exact commit required by the course Dockerfile:

```text
9f013d0930202eea99c21083b71098a0df64be0d
```

All 778 upstream files were verified against that commit's Git blob IDs. The
only added file in this source tree is the course-path `src/threads/DESIGNDOC`.
See [BASELINE.txt](BASELINE.txt) for the source and tree identity. Project 1
source and submission archives are maintained separately.

The source is the starter implementation. No Project 2 kernel implementation,
successful build, test pass, or submission is claimed. The original Pintos
[LICENSE](pintos/LICENSE) and [AUTHORS](pintos/AUTHORS) are retained.

## Implementation checklist

- [ ] Build arguments and `argv` on a bounded 4 KiB user stack.
- [ ] Safely copy syscall words, strings, and cross-page buffers; check destination permissions.
- [ ] Implement all 13 calls: `halt`, `exit`, `exec`, `wait`, `create`, `remove`,
      `open`, `filesize`, `read`, `write`, `seek`, `tell`, and `close`.
- [ ] Synchronize executable loading, direct-child waiting, and all exit orders.
- [ ] Close descriptors and executables and free partial-load resources on every failure.
- [ ] Serialize filesystem access and deny writes to running executables.
- [ ] Run all 76 tests and verify the final extracted submission archive.
- [ ] Complete group review and submit the design PDF and source through their respective platforms.

The existing rubric contains 28 functionality tests, 34 robustness tests,
one no-VM test (`multi-oom`), and 13 base-filesystem tests. No tests have been
run for Project 2 yet. The rubric's internal percentages are separate from
the course's 90% implementation component.

## Development environment

Reuse the course image from the [original Docker setup](../pa1/environment/).
Start Docker Desktop, then open this independent source tree from the repository root:

```bash
./scripts/enter-pa2.sh
```

This selects `linux/amd64`, mounts this Project 2 tree at `/home/pintos`, and
starts in `/home/pintos/src/userprog`. `PINTOS_IMAGE` can select an existing
course-compatible image. Build in `src/userprog`; after implementation is ready,
run `make check` and `make grade` from its `build/` directory.

The design review record is [reports/DESIGN-REVIEW.md](reports/DESIGN-REVIEW.md).
