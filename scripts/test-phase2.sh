#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
image_name="${PINTOS_IMAGE:-cse421-fall2026-pintos}"

# Thirteen Phase 2 tests (42 points), plus five Phase 1 regressions.
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
)

docker run --rm --platform linux/amd64 \
  --mount "type=bind,source=$repo_root/assignments/pa1/pintos,target=/home/pintos" \
  --workdir /home/pintos/src/threads "$image_name" bash -c '
set -euo pipefail
command -v bochs >/dev/null
make clean
make -j2
cd build

targets=()
for name in "$@"; do
  targets+=("tests/threads/${name}.result")
done

# The course launcher defaults to QEMU; select Bochs explicitly.
make_failed=0
make -k SIMULATOR=--bochs "${targets[@]}" || make_failed=1
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
printf "Phase 2 and Phase 1 regression tests: %s/%s passed.\n" "$passed" "$#"
test "$make_failed" -eq 0 && test "$failed" -eq 0
' phase2-tests "${tests[@]}"
