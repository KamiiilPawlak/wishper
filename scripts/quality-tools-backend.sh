#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
backend_dir="$script_dir/../backend"

cd "$backend_dir"

echo "== Ruff lint =="
uv run ruff check .

echo "== Ruff format check =="
uv run ruff format --check .

echo "== mypy =="
uv run mypy

echo "== pytest =="
uv run pytest

echo "Backend quality gate: OK"
