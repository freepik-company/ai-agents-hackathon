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

curl --silent --show-error --get "$API_URL" \
  -H "x-freepik-api-key: $FREEPIK_API_KEY" \
  --data-urlencode "term=old person driving a car" \
  --data-urlencode "page=1" \
  --data-urlencode "limit=5" \
  --data-urlencode "order=relevance" \
  --data-urlencode "filters[orientation][landscape]=1" \
  --data-urlencode "filters[orientation][portrait]=0" \
  --data-urlencode "filters[orientation][square]=1" \
  --data-urlencode "filters[orientation][panoramic]=1" \
  --data-urlencode "filters[content_type][photo]=1" \
  --data-urlencode "filters[people][include]=1" \
  --data-urlencode "filters[people][number]=1" \
  --data-urlencode "filters[people][age]=senior" \
  --data-urlencode "filters[people][age]=elder" \
  --data-urlencode "filters[people][gender]=female" \
  --data-urlencode "filters[color]=gray" \
  --data-urlencode "filters[color]=blue"


