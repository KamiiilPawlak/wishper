#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
frontend_dir="$script_dir/../frontend"

if [ ! -f "$frontend_dir/package.json" ]; then
    echo "Frontend nie jest jeszcze zainicjalizowany (brak frontend/package.json)."
    exit 1
fi

cd "$frontend_dir"
npm run dev
