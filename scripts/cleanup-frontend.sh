#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
frontend_dir="$script_dir/../frontend"

targets=(
    "$frontend_dir/node_modules"
    "$frontend_dir/dist"
    "$frontend_dir/build"
    "$frontend_dir/.next"
    "$frontend_dir/coverage"
)

for target in "${targets[@]}"; do
    if [ -e "$target" ]; then
        echo "Usuwam $target"
        rm -rf "$target"
    fi
done

echo "Frontend cleanup: OK"
