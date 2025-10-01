#!/usr/bin/env bash
set -euo pipefail

# Check if FREEPIK_API_KEY is set
: "${FREEPIK_API_KEY:=}"
if [[ -z "${FREEPIK_API_KEY}" ]]; then
  echo "[ERROR] FREEPIK_API_KEY is not set in the environment" >&2
  exit 1
fi

# API usage example
API_URL="https://api.freepik.com/v1/icons"

for page in 1 2; do
  echo "\n=== Page $page ==="
  curl --silent --show-error --get "$API_URL" \
    -H "x-freepik-api-key: $FREEPIK_API_KEY" \
    --data-urlencode "term=family" \
    --data-urlencode "page=$page" \
    --data-urlencode "per_page=5" \
    --data-urlencode "order=relevance" \
    --data-urlencode "thumbnail_size=128"
done


