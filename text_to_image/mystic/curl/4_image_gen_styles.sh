#!/usr/bin/env bash
[ -z "${BASH_VERSION:-}" ] && exec bash "$0" "$@"
set -euo pipefail
[ "${DEBUG:-0}" = "1" ] && set -x

# Mystic generation with styling block (styles and colors)
# Also demonstrates fetching available styles from /v1/ai/loras and choosing one randomly
# Requirements: FREEPIK_API_KEY, jq

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

# 1) Fetch available styles
LORAS_URL="https://api.freepik.com/v1/ai/loras"
echo "Fetching available styles..."
STYLES_RESP=$(curl -sS -H "x-freepik-api-key: $API_KEY" "$LORAS_URL")
STYLE_NAME=$(echo "$STYLES_RESP" | jq -r '.data.default | .[0].name')
if [ -z "$STYLE_NAME" ] || [ "$STYLE_NAME" = "null" ]; then
  echo "Could not fetch a style name. Full response:" >&2
  echo "$STYLES_RESP" >&2
  exit 1
fi
echo "Selected style: $STYLE_NAME"

# 2) Generate with styling
MYSTIC_URL="https://api.freepik.com/v1/ai/mystic"

read -r -d '' PAYLOAD <<JSON
{
  "prompt": "a car in the forest",
  "resolution": "2k",
  "aspect_ratio": "square_1_1",
  "model": "zen",
  "creative_detailing": 33,
  "engine": "automatic",
  "fixed_generation": false,
  "filter_nsfw": true,
  "styling": {
    "styles": [
      { "name": "$STYLE_NAME", "strength": 100 }
    ],
    "colors": [
      { "color": "#F58727", "weight": 0.5 },
      { "color": "#2727F5", "weight": 0.5 }
    ]
  }
}
JSON

echo "Submitting generation request with styling..."
RESP=$(curl -sS -X POST "$MYSTIC_URL" \
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
  STATUS_RESP=$(curl -sS -H "x-freepik-api-key: $API_KEY" "$MYSTIC_URL/$TASK_ID")
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


