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

curl --silent --show-error --get "$API_URL" \
  -H "x-freepik-api-key: $FREEPIK_API_KEY" \
  --data-urlencode "term=beautiful landscape" \
  --data-urlencode "page=1" \
  --data-urlencode "order=relevance" \
  --data-urlencode "filters[category]=footage" \
  --data-urlencode "filters[resolution][720]=1" \
  --data-urlencode "filters[resolution][1080]=1" \
  --data-urlencode "filters[resolution][2K]=0" \
  --data-urlencode "filters[resolution][4K]=0" \
  --data-urlencode "filters[ai-generated][excluded]=1" \
  --data-urlencode "filters[ai-generated][only]=0"


