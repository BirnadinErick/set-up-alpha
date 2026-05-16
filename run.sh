#!/usr/bin/env bash
set -euo pipefail

# List the files to run here, in order.
files=(
  "file1.sh"
  "file2.sh"
  "file3.sh"
)

for file in "${files[@]}"; do
  if [ ! -e "$file" ]; then
    echo "Error: file '$file' does not exist." >&2
    exit 1
  fi

  echo "Running: $file"
  if [ -x "$file" ]; then
    "$file"
  else
    source "$file"
  fi

done
