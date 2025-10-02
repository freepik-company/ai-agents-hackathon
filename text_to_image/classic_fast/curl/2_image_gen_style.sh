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

API_URL="https://api.freepik.com/v1/ai/text-to-image"

echo "[INFO] Requesting image generation (with styling)..."
curl --request POST \
  --url "$API_URL" \
  --header "x-freepik-api-key: ${FREEPIK_API_KEY}" \
  --header "Content-Type: application/json" \
  --output "${OUTPUT_DIR}/response.json" \
  --data '{
  "prompt": "a car in the forest",
  "negative_prompt": "b&w, earth, cartoon, ugly",
  "guidance_scale": 2,
  "seed": 42,
  "num_images": 1,
  "image": {
    "size": "square_1_1"
  },
  "styling": {
    "style": "anime",
    "effects": {
      "color": "pastel",
      "lightning": "warm",
      "framing": "portrait"
    },
    "colors": [
      { "color": "#FF5733", "weight": 1 },
      { "color": "#33FF57", "weight": 1 }
    ]
  },
  "filter_nsfw": true
}'

# Check for jq
if ! command -v jq >/dev/null 2>&1; then
  echo "[ERROR] jq is not installed. Please install it to continue (brew install jq)" >&2
  exit 1
fi

IMG_B64="$(jq -r '.data[0].base64 // empty' "${OUTPUT_DIR}/response.json")"
if [[ -z "${IMG_B64}" || "${IMG_B64}" == "null" ]]; then
  echo "[ERROR] Could not get data[0].base64 from response.json" >&2
  jq -r '.' "${OUTPUT_DIR}/response.json" >/dev/null || true
  exit 1
fi

OUTPUT_IMAGE_PATH="${OUTPUT_DIR}/generated_image.jpg"
echo "[INFO] Saving image to ${OUTPUT_IMAGE_PATH}"
# macOS uses -D; GNU coreutils uses --decode
printf "%s" "${IMG_B64}" | base64 -D > "${OUTPUT_DIR}/generated_image.jpg" 2>/dev/null || printf "%s" "${IMG_B64}" | base64 --decode > "${OUTPUT_DIR}/generated_image.jpg"

rm "${OUTPUT_DIR}/response.json"
echo "[OK] Image saved as: ${OUTPUT_IMAGE_PATH}"


