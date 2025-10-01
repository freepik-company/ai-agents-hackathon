#!/usr/bin/env bash
[ -z "${BASH_VERSION:-}" ] && exec bash "$0" "$@"
set -euo pipefail
[ "${DEBUG:-0}" = "1" ] && set -x

# Two prompts example: first uses structure_reference (base64), second is a normal prompt
# Requirements:
# - FREEPIK_API_KEY env var
# - jq, base64

API_URL="https://api.freepik.com/v1/ai/mystic"
STRUCT_URL="https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"

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

echo "Preparing structure reference (base64)..."
STRUCT_B64=$(curl -sS "$STRUCT_URL" | base64 | tr -d '\n')

submit_and_wait() {
  local payload=$1
  local out_suffix=$2

  echo "Submitting generation request..."
  local resp=$(curl -sS -X POST "$API_URL" \
    -H "x-freepik-api-key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local task_id=$(echo "$resp" | jq -r '.data.task_id')
  local status=$(echo "$resp" | jq -r '.data.status')

  if [ "$task_id" = "null" ] || [ -z "$task_id" ]; then
    echo "Request failed or invalid response:" >&2
    echo "$resp" >&2
    return 1
  fi

  local timeout=300
  local start=$(date +%s)
  local status_resp="$resp"
  while [ "$status" != "COMPLETED" ]; do
    echo "Waiting for the task to complete... (current status: $status)"
    sleep 2
    status_resp=$(curl -sS -H "x-freepik-api-key: $API_KEY" "$API_URL/$task_id")
    status=$(echo "$status_resp" | jq -r '.data.status')
    local now=$(date +%s)
    if [ $((now-start)) -gt $timeout ]; then
      echo "Timeout reached"
      return 1
    fi
  done

  echo "COMPLETED"
  local img_url=$(echo "$status_resp" | jq -r '.data.generated[0]')
  local out_dir=$(cd "$(dirname "$0")" && pwd)
  local out_file="$out_dir/generated_image_struct_${out_suffix}.jpg"
  curl -sS -L "$img_url" -o "$out_file"
  echo "Image successfully downloaded as $out_file"
}

# Prompt 1: With structure reference
read -r -d '' PAYLOAD1 <<JSON
{
  "prompt": "Close-up portrait of a smiling senior woman in a vintage blue convertible, golden hour lighting, soft bokeh",
  "structure_reference": "$STRUCT_B64",
  "structure_strength": 50,
  "resolution": "2k",
  "aspect_ratio": "square_1_1",
  "model": "realism",
  "creative_detailing": 33,
  "engine": "automatic",
  "fixed_generation": false,
  "filter_nsfw": true
}
JSON

submit_and_wait "$PAYLOAD1" "portrait_struct"

# Prompt 2: Without structure reference
read -r -d '' PAYLOAD2 <<'JSON'
{
  "prompt": "Vintage convertible driving along a coastal road at sunset, soft pastel sky, cinematic composition",
  "resolution": "2k",
  "aspect_ratio": "widescreen_16_9",
  "model": "realism",
  "creative_detailing": 33,
  "engine": "automatic",
  "fixed_generation": false,
  "filter_nsfw": true
}
JSON

submit_and_wait "$PAYLOAD2" "car_coastal"


