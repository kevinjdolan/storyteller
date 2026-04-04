#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_VENV_DIR="${ROOT_DIR}/backend/.venv"
BACKEND_VENV_PYTHON="${BACKEND_VENV_DIR}/bin/python"
SECRETS_FILE="${ROOT_DIR}/secrets.yaml"
SECRETS_EXAMPLE_FILE="${ROOT_DIR}/secrets.example.yaml"

python_supports_backend() {
  local python_cmd="$1"
  "${python_cmd}" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1
}

if ! command -v npm >/dev/null 2>&1; then
  printf 'npm is required to bootstrap the frontend dependencies.\n' >&2
  exit 1
fi

SYSTEM_PYTHON=""
for candidate_name in python python3.13 python3.12 python3.11 python3.10 python3; do
  if ! command -v "${candidate_name}" >/dev/null 2>&1; then
    continue
  fi

  candidate_path="$(command -v "${candidate_name}")"
  if python_supports_backend "${candidate_path}"; then
    SYSTEM_PYTHON="${candidate_path}"
    break
  fi
done

if [[ -z "${SYSTEM_PYTHON}" ]]; then
  printf 'Storyteller backend bootstrap requires Python 3.10 or newer.\n' >&2
  exit 1
fi

created_secrets_file=false
if [[ ! -f "${SECRETS_FILE}" ]]; then
  cp "${SECRETS_EXAMPLE_FILE}" "${SECRETS_FILE}"
  created_secrets_file=true
fi

"${ROOT_DIR}/scripts/install-git-hooks.sh"

if [[ -x "${BACKEND_VENV_PYTHON}" ]] && ! python_supports_backend "${BACKEND_VENV_PYTHON}"; then
  rm -rf "${BACKEND_VENV_DIR}"
fi

if [[ ! -x "${BACKEND_VENV_PYTHON}" ]]; then
  "${SYSTEM_PYTHON}" -m venv "${BACKEND_VENV_DIR}"
fi

"${BACKEND_VENV_PYTHON}" -m pip install --requirement "${ROOT_DIR}/backend/requirements.txt"

if [[ -d "${ROOT_DIR}/frontend/node_modules" ]]; then
  npm --prefix "${ROOT_DIR}/frontend" install --no-fund --no-audit
else
  npm --prefix "${ROOT_DIR}/frontend" ci --no-fund --no-audit
fi

printf 'Backend virtualenv ready at %s\n' "${BACKEND_VENV_DIR}"
printf 'Frontend dependencies synced in %s/frontend\n' "${ROOT_DIR}"

if [[ "${created_secrets_file}" == true ]]; then
  printf 'Created %s from %s\n' "${SECRETS_FILE}" "${SECRETS_EXAMPLE_FILE}"
fi

if grep -q 'your-gemini-api-key-here' "${SECRETS_FILE}"; then
  printf 'Reminder: replace the placeholder Gemini API key in %s before using AI-backed workflows.\n' "${SECRETS_FILE}"
fi
