#!/usr/bin/env bash
set -euo pipefail

BASE=${GITHUB_BASE_REF:-main}
PATTERN='(PASSWORD=|SECRET_KEY=|postgres://|BEGIN PRIVATE KEY)'

if git rev-parse --verify origin/$BASE >/dev/null 2>&1; then
  git fetch origin "$BASE" --depth=1 >/dev/null 2>&1 || true
  diffs=$(git diff --unified=0 origin/$BASE...HEAD -- . ':(exclude).env.example' ':(exclude)docs/' ':(exclude)README.md')
else
  diffs=$(git diff --unified=0 HEAD -- . ':(exclude).env.example' ':(exclude)docs/' ':(exclude)README.md')
fi
if echo "$diffs" | grep -nE "$PATTERN"; then
  echo "Possible secret detected above."
  exit 1
fi

echo "No secrets detected."
