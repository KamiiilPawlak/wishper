#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
scripts_dir="$script_dir/scripts"

usage() {
    echo "Usage: $0 {quality-backend|quality-frontend|quality|cleanup-backend|cleanup-frontend|cleanup|dev-backend|dev-frontend|docker-up}"
    exit 1
}

[ $# -eq 1 ] || usage

case "$1" in
    quality-backend)
        "$scripts_dir/quality-tools-backend.sh"
        ;;
    quality-frontend)
        "$scripts_dir/quality-tools-frontend.sh"
        ;;
    quality)
        "$scripts_dir/quality-tools-backend.sh"
        "$scripts_dir/quality-tools-frontend.sh"
        ;;
    cleanup-backend)
        "$scripts_dir/cleanup-backend.sh"
        ;;
    cleanup-frontend)
        "$scripts_dir/cleanup-frontend.sh"
        ;;
    cleanup)
        "$scripts_dir/cleanup-backend.sh"
        "$scripts_dir/cleanup-frontend.sh"
        ;;
    dev-backend)
        "$scripts_dir/dev-backend.sh"
        ;;
    dev-frontend)
        "$scripts_dir/dev-frontend.sh"
        ;;
    docker-up)
        "$scripts_dir/docker-up.sh"
        ;;
    *)
        usage
        ;;
esac
