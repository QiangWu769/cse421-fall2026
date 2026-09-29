#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
image_name="${PINTOS_IMAGE:-cse421-fall2026-pintos}"
docker build --platform linux/amd64 -t "$image_name" "$repo_root/assignments/pa1/environment"
