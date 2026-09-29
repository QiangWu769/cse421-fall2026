#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
image_name="${PINTOS_IMAGE:-cse421-fall2026-pintos}"
submission_dir="$repo_root/assignments/pa1/submissions/phase1"
mkdir -p "$submission_dir"
docker run --rm --platform linux/amd64 \
  --mount "type=bind,source=$repo_root/assignments/pa1/pintos,target=/home/pintos" \
  --mount "type=bind,source=$submission_dir,target=/submission" \
  --workdir /home/pintos "$image_name" bash -c '
set -euo pipefail
make -C src clean
tar -czf /submission/pa1-phase1.tar.gz src/
cd /submission
sha256sum pa1-phase1.tar.gz > SHA256SUMS
'
printf '%s\n' "Submission package: $submission_dir/pa1-phase1.tar.gz"
