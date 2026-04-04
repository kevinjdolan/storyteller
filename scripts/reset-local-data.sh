#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_SCRIPT="${ROOT_DIR}/scripts/dev-compose.sh"
DATA_VOLUMES=(
  storyteller_postgres_data
  storyteller_gcs_data
)

"${COMPOSE_SCRIPT}" down --remove-orphans

volumes_to_remove=()
for volume_name in "${DATA_VOLUMES[@]}"; do
  if docker volume inspect "${volume_name}" >/dev/null 2>&1; then
    volumes_to_remove+=("${volume_name}")
  fi
done

if [[ "${#volumes_to_remove[@]}" -eq 0 ]]; then
  printf 'No Postgres or fake GCS data volumes were present.\n'
  exit 0
fi

docker volume rm "${volumes_to_remove[@]}"

printf 'Removed local data volumes:\n'
printf '  %s\n' "${volumes_to_remove[@]}"
printf 'Dependency cache volumes were left in place. Run make up to recreate the stack with a clean database and object store.\n'
