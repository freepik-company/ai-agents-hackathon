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

# Perform search
SEARCH_URL="https://api.freepik.com/v1/resources"

echo "[INFO] Performing search..."
curl -sS -G "$SEARCH_URL" \
  -H "x-freepik-api-key: ${FREEPIK_API_KEY}" \
  --data-urlencode "term=old person driving a car" \
  --data-urlencode "page=1" \
  --data-urlencode "limit=1" \
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
  --data-urlencode "filters[color]=blue" \
  --data-urlencode "filters[license][freemium]=1" \
  >"${OUTPUT_DIR}/search.json"

# Check if jq is installed to save the results in a json file to get the RESOURCE_ID
if ! command -v jq >/dev/null 2>&1; then
  echo "[ERROR] jq is not installed. Please install it to continue (brew install jq)" >&2
  exit 1
fi

# Get the RESOURCE_ID from the search.json file
RESOURCE_ID="$(jq -r '.data[0].id // empty' "${OUTPUT_DIR}/search.json")"
if [[ -z "${RESOURCE_ID}" || "${RESOURCE_ID}" == "null" ]]; then
  echo "[ERROR] Could not get RESOURCE_ID from search.json" >&2
  jq -r '.' "${OUTPUT_DIR}/search.json" >/dev/null || true
  exit 1
fi

echo "[INFO] Resource found: ID=${RESOURCE_ID}"

DOWNLOAD_URL="https://api.freepik.com/v1/resources/${RESOURCE_ID}/download"
echo "[INFO] Requesting download URL..."
curl -sS -G "$DOWNLOAD_URL" \
  -H "x-freepik-api-key: ${FREEPIK_API_KEY}" \
  --data-urlencode "image_size=small" \
  >"${OUTPUT_DIR}/download.json"

IMAGE_URL="$(jq -r '.data.url // empty' "${OUTPUT_DIR}/download.json")"
if [[ -z "${IMAGE_URL}" || "${IMAGE_URL}" == "null" ]]; then
  echo "[ERROR] data.url not found in download.json" >&2
  exit 1
fi

OUTPUT_IMAGE_PATH="${OUTPUT_DIR}/${RESOURCE_ID}.jpg"
echo "[INFO] Downloading image to ${OUTPUT_IMAGE_PATH}"
curl -sS -L "${IMAGE_URL}" -o "${OUTPUT_IMAGE_PATH}"

rm "${OUTPUT_DIR}/download.json"
rm "${OUTPUT_DIR}/search.json"
echo "[OK] search.json, download.json and ${RESOURCE_ID}.jpg saved in: ${OUTPUT_DIR}"
