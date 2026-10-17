#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
frontend_dir="$script_dir/../frontend"

if [ ! -f "$frontend_dir/package.json" ]; then
    echo "Frontend nie jest jeszcze zainicjalizowany (brak frontend/package.json) - pomijam."
    exit 0
fi

cd "$frontend_dir"

echo "== Lint =="
npm run lint

echo "== Type check =="
npm run typecheck

echo "== Test =="
npm run test

echo "Frontend quality gate: OK"
