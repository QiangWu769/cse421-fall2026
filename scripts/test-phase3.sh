#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
image_name="${PINTOS_IMAGE:-cse421-fall2026-pintos}"

# Nine Phase 3 tests (37 points), plus eighteen earlier-phase regressions.
tests=(
  alarm-single
  alarm-multiple
  alarm-simultaneous
  alarm-zero
  alarm-negative
  alarm-priority
  priority-change
  priority-preempt
  priority-fifo
  priority-sema
  priority-condvar
  priority-donate-one
  priority-donate-multiple
  priority-donate-multiple2
  priority-donate-nest
  priority-donate-chain
  priority-donate-sema
  priority-donate-lower
  mlfqs-load-1
  mlfqs-load-60
  mlfqs-load-avg
  mlfqs-recent-1
  mlfqs-fair-2
  mlfqs-fair-20
  mlfqs-nice-2
  mlfqs-nice-10
  mlfqs-block
)

docker run --rm --platform linux/amd64 \
  --mount "type=bind,source=$repo_root/assignments/pa1/pintos,target=/home/pintos" \
  --workdir /home/pintos/src/threads "$image_name" bash -c '
set -euo pipefail
command -v bochs >/dev/null
make clean
make -j2
cd build

# Make.tests enables -mlfqs only for the nine MLFQS tests.
# Earlier phases run in the default priority-scheduling mode.
make_failed=0
make -k check SIMULATOR=--bochs || make_failed=1
passed=0
failed=0
for name in "$@"; do
  if grep -qx PASS "tests/threads/${name}.result"; then
    printf "PASS %s\n" "$name"
    passed=$((passed + 1))
  else
    printf "FAIL %s (see tests/threads/%s.output and .errors)\n" "$name" "$name"
    failed=$((failed + 1))
  fi
done
printf "Phase 3 and earlier regression tests: %s/%s passed.\n" "$passed" "$#"
test "$make_failed" -eq 0 && test "$failed" -eq 0 && test "$passed" -eq 27
' phase3-tests "${tests[@]}"
