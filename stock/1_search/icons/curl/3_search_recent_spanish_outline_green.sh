#!/usr/bin/env bash
set -euo pipefail

# Check if FREEPIK_API_KEY is set
: "${FREEPIK_API_KEY:=}"
if [[ -z "${FREEPIK_API_KEY}" ]]; then
  echo "[ERROR] FREEPIK_API_KEY is not set in the environment" >&2
  exit 1
fi

API_URL="https://api.freepik.com/v1/icons"

curl --silent --show-error --get "$API_URL" \
  -H "x-freepik-api-key: $FREEPIK_API_KEY" \
  -H "Accept-Language: es-ES" \
  --data-urlencode "term=herramientas de mecánico" \
  --data-urlencode "slug=mechanic" \
  --data-urlencode "page=1" \
  --data-urlencode "per_page=5" \
  --data-urlencode "order=recent" \
  --data-urlencode "thumbnail_size=256" \
  --data-urlencode "filters[color]=green" \
  --data-urlencode "filters[shape]=outline"


