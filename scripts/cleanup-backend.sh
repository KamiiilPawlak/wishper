#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$script_dir/.."
backend_dir="$repo_root/backend"

targets=(
    "$backend_dir/.pytest_cache"
    "$backend_dir/.mypy_cache"
    "$backend_dir/.ruff_cache"
    "$repo_root/.mypy_cache"
    "$repo_root/.ruff_cache"
)

for target in "${targets[@]}"; do
    if [ -e "$target" ]; then
        echo "Usuwam $target"
        rm -rf "$target"
    fi
done

find "$backend_dir" -type d -name "__pycache__" -not -path "*/.venv/*" -print -exec rm -rf {} + | sed 's/^/Usuwam /'

echo "Backend cleanup: OK"
