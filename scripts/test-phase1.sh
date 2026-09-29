#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
image_name="${PINTOS_IMAGE:-cse421-fall2026-pintos}"
docker run --rm --platform linux/amd64 \
  --mount "type=bind,source=$repo_root/assignments/pa1/pintos,target=/home/pintos" \
  --workdir /home/pintos/src/threads "$image_name" bash -c '
set -euo pipefail
make clean
make -j2
cd build
make tests/threads/alarm-single.result \
     tests/threads/alarm-multiple.result \
     tests/threads/alarm-simultaneous.result \
     tests/threads/alarm-zero.result \
     tests/threads/alarm-negative.result
for name in single multiple simultaneous zero negative; do
  grep -qx PASS "tests/threads/alarm-${name}.result"
done
'
