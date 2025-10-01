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

VIDEOS_SEARCH_URL="https://api.freepik.com/v1/videos"

# Perform video search to obtain a video ID
echo "[INFO] Performing video search..."
curl -sS -G "$VIDEOS_SEARCH_URL" \
  -H "x-freepik-api-key: ${FREEPIK_API_KEY}" \
  --data-urlencode "term=beautiful landscape" \
  --data-urlencode "page=1" \
  --data-urlencode "order=relevance" \
  --data-urlencode "filters[category]=footage" \
  --data-urlencode "filters[resolution][720]=1" \
  --data-urlencode "filters[resolution][1080]=1" \
  --data-urlencode "filters[resolution][2K]=0" \
  --data-urlencode "filters[resolution][4K]=0" \
  --data-urlencode "filters[ai-generated][excluded]=1" \
  --data-urlencode "filters[ai-generated][only]=0" \
  >"${OUTPUT_DIR}/search.json"

if ! command -v jq >/dev/null 2>&1; then
  echo "[ERROR] jq is not installed. Please install it to continue (brew install jq)" >&2
  exit 1
fi

VIDEO_ID="$(jq -r '.data[1].id // empty' "${OUTPUT_DIR}/search.json")"
if [[ -z "${VIDEO_ID}" || "${VIDEO_ID}" == "null" ]]; then
  echo "[ERROR] Could not get video id from search.json" >&2
  jq -r '.' "${OUTPUT_DIR}/search.json" >/dev/null || true
  exit 1
fi

echo "[INFO] Video found: ID=${VIDEO_ID}"

DOWNLOAD_URL="https://api.freepik.com/v1/videos/${VIDEO_ID}/download"
echo "[INFO] Requesting video download URL..."
curl -sS -G "$DOWNLOAD_URL" \
  -H "x-freepik-api-key: ${FREEPIK_API_KEY}" \
  >"${OUTPUT_DIR}/download.json"

VIDEO_URL="$(jq -r '.data.url // empty' "${OUTPUT_DIR}/download.json")"
if [[ -z "${VIDEO_URL}" || "${VIDEO_URL}" == "null" ]]; then
  echo "[ERROR] data.url not found in download.json" >&2
  exit 1
fi

OUTPUT_VIDEO_PATH="${OUTPUT_DIR}/${VIDEO_ID}.mp4"
echo "[INFO] Downloading video to ${OUTPUT_VIDEO_PATH}"
curl -sS -L "${VIDEO_URL}" -o "${OUTPUT_DIR}/${VIDEO_ID}.mp4"

rm "${OUTPUT_DIR}/download.json"
rm "${OUTPUT_DIR}/search.json"
echo "[OK] search.json, download.json and ${VIDEO_ID}.mp4 saved in: ${OUTPUT_DIR}"


