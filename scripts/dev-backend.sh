#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
backend_dir="$script_dir/../backend"

cd "$backend_dir"
uv run uvicorn app.main:app --reload
