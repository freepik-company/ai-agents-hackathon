#!/usr/bin/env bash
[ -z "${BASH_VERSION:-}" ] && exec bash "$0" "$@"
set -euo pipefail
[ "${DEBUG:-0}" = "1" ] && set -x

# Mystic generation using style_reference (image provided as base64)
# Requirements: FREEPIK_API_KEY, jq, base64

API_URL="https://api.freepik.com/v1/ai/mystic"
STYLE_URL="https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"

# Resolve API key
API_KEY="${FREEPIK_API_KEY:-}"
if [ -z "$API_KEY" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
  if [ -f "$PROJECT_ROOT/.env" ]; then
    API_KEY=$(grep -E '^FREEPIK_API_KEY=' "$PROJECT_ROOT/.env" | sed -E 's/^FREEPIK_API_KEY="?([^"\r\n]*)"?/\1/')
  fi
fi
if [ -z "$API_KEY" ]; then
  echo "FREEPIK_API_KEY is not set. Export it or add it to .env at project root."
  exit 1
fi

echo "Downloading style reference image..."
STYLE_B64=$(curl -sS "$STYLE_URL" | base64 | tr -d '\n')

read -r -d '' PAYLOAD <<JSON
{
  "prompt": "a car in the forest",
  "style_reference": "$STYLE_B64",
  "adherence": 50,
  "hdr": 50,
  "resolution": "1k",
  "aspect_ratio": "square_1_1",
  "model": "realism",
  "creative_detailing": 33,
  "engine": "automatic",
  "fixed_generation": false,
  "filter_nsfw": true
}
JSON

echo "Submitting generation request with style reference..."
RESP=$(curl -sS -X POST "$API_URL" \
  -H "x-freepik-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

TASK_ID=$(echo "$RESP" | jq -r '.data.task_id')
STATUS=$(echo "$RESP" | jq -r '.data.status')

if [ "$TASK_ID" = "null" ] || [ -z "$TASK_ID" ]; then
  echo "Request failed or invalid response:" >&2
  echo "$RESP" >&2
  exit 1
fi

TIMEOUT=300
START=$(date +%s)
FINAL_RESP="$RESP"
while [ "$STATUS" != "COMPLETED" ]; do
  echo "Waiting for the task to complete... (current status: $STATUS)"
  sleep 2
  STATUS_RESP=$(curl -sS -H "x-freepik-api-key: $API_KEY" "$API_URL/$TASK_ID")
  STATUS=$(echo "$STATUS_RESP" | jq -r '.data.status')
  FINAL_RESP="$STATUS_RESP"
  NOW=$(date +%s)
  if [ $((NOW-START)) -gt $TIMEOUT ]; then
    echo "Timeout reached"
    exit 1
  fi
done

echo "COMPLETED"

IMG_URL=$(echo "$FINAL_RESP" | jq -r '.data.generated[0]')
OUT_DIR=$(cd "$(dirname "$0")" && pwd)
OUT_FILE="$OUT_DIR/generated_image.jpg"

curl -sS -L "$IMG_URL" -o "$OUT_FILE"
echo "Image successfully downloaded as $OUT_FILE"


