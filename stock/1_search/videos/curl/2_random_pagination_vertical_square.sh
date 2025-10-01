#!/usr/bin/env bash
set -euo pipefail

# Check if FREEPIK_API_KEY is set
: "${FREEPIK_API_KEY:=}"
if [[ -z "${FREEPIK_API_KEY}" ]]; then
  echo "[ERROR] FREEPIK_API_KEY is not set in the environment" >&2
  exit 1
fi

# API usage example
API_URL="https://api.freepik.com/v1/videos"

for page in 1 2; do
  echo "\n=== Page $page ==="
  curl --silent --show-error --get "$API_URL" \
    -H "x-freepik-api-key: $FREEPIK_API_KEY" \
    --data-urlencode "term=city street portrait" \
    --data-urlencode "page=$page" \
    --data-urlencode "order=relevance" \
    --data-urlencode "per_page=5" \
    --data-urlencode "filters[ai-generated][excluded]=0" \
    --data-urlencode "filters[ai-generated][only]=1"
done


