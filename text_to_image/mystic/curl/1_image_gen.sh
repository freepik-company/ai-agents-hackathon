#!/usr/bin/env bash
[ -z "${BASH_VERSION:-}" ] && exec bash "$0" "$@"
set -euo pipefail
[ "${DEBUG:-0}" = "1" ] && set -x

# Basic Mystic image generation using curl
# Requirements:
# - FREEPIK_API_KEY exported in the shell or present in project .env
# - jq installed for JSON parsing (brew install jq)

# Dependency checks
command -v curl >/dev/null 2>&1 || { echo "curl is required"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "jq is required. Install it: brew install jq"; exit 1; }

API_URL="https://api.freepik.com/v1/ai/mystic"

# Resolve API key (env var or project .env)
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

# Build the JSON payload
read -r -d '' PAYLOAD <<'JSON'
{
  "prompt": "a car in the forest",
  "resolution": "2k",
  "aspect_ratio": "square_1_1",
  "model": "realism",
  "creative_detailing": 33,
  "engine": "automatic",
  "fixed_generation": false,
  "filter_nsfw": true
}
JSON

echo "Submitting generation request..."
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

echo "Task ID: $TASK_ID"

# Polling until COMPLETED (timeout 300s)
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

# Download the first generated image
IMG_URL=$(echo "$FINAL_RESP" | jq -r '.data.generated[0]')
OUT_DIR=$(cd "$(dirname "$0")" && pwd)
OUT_FILE="$OUT_DIR/generated_image.jpg"

curl -sS -L "$IMG_URL" -o "$OUT_FILE"
echo "Image successfully downloaded as $OUT_FILE"


