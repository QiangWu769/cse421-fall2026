#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
image_name="${PINTOS_IMAGE:-cse421-fall2026-pintos}"
submission_dir="$repo_root/assignments/pa1/submissions/phase2"
mkdir -p "$submission_dir"

docker run --rm --platform linux/amd64 \
  --mount "type=bind,source=$repo_root/assignments/pa1/pintos,target=/home/pintos" \
  --mount "type=bind,source=$submission_dir,target=/submission" \
  --workdir /home/pintos "$image_name" bash -c '
set -euo pipefail
make -C src clean

# Refuse to package leftover build output or editor temporary files.
# Keep all source files, including the course-provided source archives.
leftovers="$(find src \
  \( -type d \( -name build -o -name .git -o -name __pycache__ -o -name tmp \) \) -o \
  \( -type f \( -name "*.o" -o -name "*.d" -o -name "*.output" \
    -o -name "*.result" -o -name "*.errors" -o -name "*.pyc" \
    -o -name "*.swp" -o -name "*.swo" -o -name "*.tmp" -o -name "*~" \
    -o -name bochsout.txt -o -name bochsrc.txt \) \))"
if test -n "$leftovers"; then
  printf "Remove these generated or temporary files before packaging:\n%s\n" "$leftovers" >&2
  exit 1
fi

archive_tmp="$(mktemp /submission/.pa1-phase2.tar.gz.XXXXXX)"
checksum_tmp="$(mktemp /submission/.SHA256SUMS.XXXXXX)"
trap '\''rm -f "$archive_tmp" "$checksum_tmp"'\'' EXIT
tar --exclude=.DS_Store --exclude="._*" -czf "$archive_tmp" src/
tar -tzf "$archive_tmp" >/dev/null
checksum="$(sha256sum "$archive_tmp")"
printf "%s  pa1-phase2.tar.gz\n" "${checksum%% *}" > "$checksum_tmp"
chmod 644 "$archive_tmp" "$checksum_tmp"
mv "$archive_tmp" /submission/pa1-phase2.tar.gz
mv "$checksum_tmp" /submission/SHA256SUMS
cd /submission
sha256sum -c SHA256SUMS
'
printf '%s\n' "Submission package: $submission_dir/pa1-phase2.tar.gz"
printf '%s\n' "Checksum file: $submission_dir/SHA256SUMS"
