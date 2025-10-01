#!/usr/bin/env bash
set -euo pipefail

# Output directory (this script's directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR"
mkdir -p "$OUTPUT_DIR"

# API Key from environment variable
: "${FREEPIK_API_KEY:=}"
if [[ -z "${FREEPIK_API_KEY}" ]]; then
  echo "[ERROR] FREEPIK_API_KEY is not set in the environment" >&2
  exit 1
fi

ICONS_SEARCH_URL="https://api.freepik.com/v1/icons"

# Perform icon search to obtain an icon ID
echo "[INFO] Performing icon search..."
curl -sS -G "$ICONS_SEARCH_URL" \
  -H "x-freepik-api-key: ${FREEPIK_API_KEY}" \
  --data-urlencode "term=a mechanic taller" \
  --data-urlencode "slug=repair" \
  --data-urlencode "page=1" \
  --data-urlencode "per_page=1" \
  --data-urlencode "order=relevance" \
  --data-urlencode "thumbnail_size=256" \
  --data-urlencode "filters[color]=green" \
  --data-urlencode "filters[color]=orange" \
  --data-urlencode "filters[shape]=outline" \
  --data-urlencode "filters[shape]=fill" \
  >"${OUTPUT_DIR}/search.json"

if ! command -v jq >/dev/null 2>&1; then
  echo "[ERROR] jq is not installed. Please install it to continue (brew install jq)" >&2
  exit 1
fi

ICON_ID="$(jq -r '.data[0].id // empty' "${OUTPUT_DIR}/search.json")"
if [[ -z "${ICON_ID}" || "${ICON_ID}" == "null" ]]; then
  echo "[ERROR] Could not get icon id from search.json" >&2
  jq -r '.' "${OUTPUT_DIR}/search.json" >/dev/null || true
  exit 1
fi

echo "[INFO] Icon found: ID=${ICON_ID}"

DOWNLOAD_URL="https://api.freepik.com/v1/icons/${ICON_ID}/download"
echo "[INFO] Requesting icon download URL..."
curl -sS -G "$DOWNLOAD_URL" \
  -H "x-freepik-api-key: ${FREEPIK_API_KEY}" \
  --data-urlencode "format=png" \
  --data-urlencode "png_size=64" \
  >"${OUTPUT_DIR}/download.json"

ICON_URL="$(jq -r '.data.url // empty' "${OUTPUT_DIR}/download.json")"
if [[ -z "${ICON_URL}" || "${ICON_URL}" == "null" ]]; then
  echo "[ERROR] data.url not found in download.json" >&2
  exit 1
fi

OUTPUT_ICON_PATH="${OUTPUT_DIR}/${ICON_ID}.png"
echo "[INFO] Downloading icon to ${OUTPUT_ICON_PATH}"
curl -sS -L "${ICON_URL}" -o "${OUTPUT_DIR}/${ICON_ID}.png"

rm "${OUTPUT_DIR}/download.json"
rm "${OUTPUT_DIR}/search.json"
echo "[OK] search.json, download.json and ${ICON_ID}.png saved in: ${OUTPUT_DIR}"


