#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "${ROOT_DIR}"

staged_paths=()
while IFS= read -r path; do
  staged_paths+=("${path}")
done < <(git diff --cached --name-only --diff-filter=ACMR)

if [[ "${#staged_paths[@]}" -eq 0 ]]; then
  exit 0
fi

blocked_paths=()

for path in "${staged_paths[@]}"; do
  case "${path}" in
    secrets.yaml|*/secrets.yaml)
      blocked_paths+=("${path}")
      ;;
    .env|*/.env|.env.*|*/.env.*|.envrc|*/.envrc)
      case "${path}" in
        .env.example|*/.env.example|.env.sample|*/.env.sample|.env.template|*/.env.template|.env.*.example|*/.env.*.example|.env.*.sample|*/.env.*.sample|.env.*.template|*/.env.*.template)
          ;;
        *)
          blocked_paths+=("${path}")
          ;;
      esac
      ;;
  esac
done

if [[ "${#blocked_paths[@]}" -gt 0 ]]; then
  printf 'Secret hygiene check failed.\n' >&2
  printf 'Refusing to commit local-only config files:\n' >&2
  printf '  %s\n' "${blocked_paths[@]}" >&2
  printf '\nUse tracked example files such as secrets.example.yaml or .env.example for placeholders.\n' >&2
  exit 1
fi

staged_patch="$(git diff --cached --unified=0 --no-color -- .)"
added_lines="$(printf '%s\n' "${staged_patch}" | rg '^\+' | rg -v '^\+\+\+' || true)"

if [[ -z "${added_lines}" ]]; then
  exit 0
fi

if private_key_hits="$(printf '%s\n' "${added_lines}" | rg -n 'BEGIN [A-Z ]*PRIVATE KEY' || true)"; [[ -n "${private_key_hits}" ]]; then
  printf 'Secret hygiene check failed.\n' >&2
  printf 'Detected staged private key material:\n%s\n' "${private_key_hits}" >&2
  exit 1
fi

if gemini_key_hits="$(printf '%s\n' "${added_lines}" | rg -n 'AIza[0-9A-Za-z_-]{20,}' || true)"; [[ -n "${gemini_key_hits}" ]]; then
  printf 'Secret hygiene check failed.\n' >&2
  printf 'Detected staged Gemini or Google API key material:\n%s\n' "${gemini_key_hits}" >&2
  exit 1
fi

if assigned_secret_hits="$(
  printf '%s\n' "${added_lines}" \
    | rg -n '^\+.*(STORYTELLER_GEMINI_API_KEY|GEMINI_API_KEY|api_key)[[:space:]]*[:=][[:space:]]*.+$' \
    | rg -vi '(example|sample|template|placeholder|changeme|replace|dummy|test-key|your-|<your)' \
    || true
)"; [[ -n "${assigned_secret_hits}" ]]; then
  printf 'Secret hygiene check failed.\n' >&2
  printf 'Detected staged secret assignment lines:\n%s\n' "${assigned_secret_hits}" >&2
  printf '\nMove live credentials into secrets.yaml or local environment variables instead.\n' >&2
  exit 1
fi
