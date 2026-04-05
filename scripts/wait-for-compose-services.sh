#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE=(docker compose -f "${ROOT_DIR}/infra/compose/docker-compose.yml")
POLL_INTERVAL_SECONDS="${POLL_INTERVAL_SECONDS:-2}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-120}"

if [[ "$#" -eq 0 ]]; then
  echo "usage: $0 <service> [<service> ...]" >&2
  exit 1
fi

deadline=$((SECONDS + TIMEOUT_SECONDS))

for service in "$@"; do
  echo "Waiting for ${service} to become healthy..."

  while true; do
    container_id="$("${COMPOSE[@]}" ps -q "${service}")"

    if [[ -z "${container_id}" ]]; then
      echo "Service ${service} is not running yet." >&2
    else
      status="$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "${container_id}")"

      if [[ "${status}" == "healthy" || "${status}" == "running" ]]; then
        echo "Service ${service} is ${status}."
        break
      fi

      if [[ "${status}" == "unhealthy" || "${status}" == "exited" || "${status}" == "dead" ]]; then
        echo "Service ${service} entered terminal status: ${status}" >&2
        "${COMPOSE[@]}" logs --no-color "${service}" >&2 || true
        exit 1
      fi

      echo "Service ${service} status: ${status}"
    fi

    if (( SECONDS >= deadline )); then
      echo "Timed out waiting for ${service} after ${TIMEOUT_SECONDS} seconds." >&2
      "${COMPOSE[@]}" logs --no-color "${service}" >&2 || true
      exit 1
    fi

    sleep "${POLL_INTERVAL_SECONDS}"
  done
done
