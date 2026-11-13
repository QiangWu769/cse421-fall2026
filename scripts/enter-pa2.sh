#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
image_name="${PINTOS_IMAGE:-cse421-fall2026-pintos}"
exec docker run --rm -it --platform linux/amd64 \
  --mount "type=bind,source=$repo_root/assignments/pa2/pintos,target=/home/pintos" \
  --workdir /home/pintos/src/userprog "$image_name" bash
