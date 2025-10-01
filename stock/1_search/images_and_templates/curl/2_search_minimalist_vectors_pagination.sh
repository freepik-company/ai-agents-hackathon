#!/usr/bin/env bash
set -euo pipefail

# Check if FREEPIK_API_KEY is set
: "${FREEPIK_API_KEY:=}"
if [[ -z "${FREEPIK_API_KEY}" ]]; then
  echo "[ERROR] FREEPIK_API_KEY is not set in the environment" >&2
  exit 1
fi

# API usage example
API_URL="https://api.freepik.com/v1/resources"

for page in 1 2; do
  echo "\n=== Page $page ==="
  curl --silent --show-error --get "$API_URL" \
    -H "x-freepik-api-key: $FREEPIK_API_KEY" \
    -H "Accept-Language: en-US" \
    --data-urlencode "term=minimalist bicicle logo" \
    --data-urlencode "order=relevance" \
    --data-urlencode "limit=3" \
    --data-urlencode "page=$page" \
    --data-urlencode "filters[content_type][vector]=1" \
    --data-urlencode "filters[color]=black" \
    --data-urlencode "filters[color]=white"
done


