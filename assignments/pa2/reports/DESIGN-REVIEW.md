# Project 2 design proposal review

Prepared November 13, 2026; wording revised November 21, 2026. This is a review
of the planned design, not an implementation test report.

- All 15 original questions from `doc/userprog.tmpl` are preserved in full and
  answered in the course-path `src/threads/DESIGNDOC`.
- The eight-page PDF uses the original monospaced template layout. Every source
  line is included, and all rendered pages were inspected for clipping and
  incomplete question headings.
- The stack-size formula includes all argument strings, padding, argument
  pointers, sentinel, `argv`, `argc`, and the fake return address.
- Parent and child status references cover both semaphore waits and signals.
  Load failure cleanup precedes reporting failure; a failed thread creation
  frees the unshared status record directly.
- The combined page-translation helper is proposed, rather than presented as
  an existing Pintos API. B4 distinguishes a single copy pass from the planned
  prevalidation-plus-copy path and counts their page inspections separately.
- File-descriptor ownership, signed `off_t` limits, read-only user mappings,
  executable write denial, and temporary-buffer cleanup are included.
- The November 21 revision shortens the answers and clarifies syscall return
  values and status-record ownership. The proposed architecture is unchanged.

The clean baseline's 778 original files match the course commit's Git blob IDs.
Only `src/threads/DESIGNDOC` was added inside that source export. No Project 2
build or kernel tests were run, and no platform submission was performed.

The assignment lists 76 tests: 28 functionality, 34 robustness, one no-VM,
and 13 filesystem tests. These remain implementation targets.
