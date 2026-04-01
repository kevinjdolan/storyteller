#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "${ROOT_DIR}"

git config core.hooksPath .githooks

printf 'Configured repo-local Git hooks at %s/.githooks\n' "${ROOT_DIR}"
