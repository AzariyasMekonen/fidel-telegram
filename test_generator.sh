#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

IMAGE_NAME="adwactf/fidel-telegram-generator:latest"
TEST_FLAG="AdwaCTF{DYNAMIC_GENERATOR_TEST_PASSED_1896}"
OUT_DIR="$(pwd)/test_output"

echo "[1/4] Building generator image..."
if command -v podman >/dev/null 2>&1; then
    CONTAINER_CLI="podman"
elif command -v docker >/dev/null 2>&1; then
    CONTAINER_CLI="docker"
else
    echo "Error: neither podman nor docker found." >&2
    exit 1
fi

$CONTAINER_CLI build -t "$IMAGE_NAME" .

echo "[2/4] Preparing output directory..."
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

echo "[3/4] Spawning container with dynamic flag..."
$CONTAINER_CLI run --rm \
  -e FLAG="$TEST_FLAG" \
  -e USER_ID="participant_test_101" \
  -v "$OUT_DIR:/output:Z" \
  "$IMAGE_NAME"

echo "[4/4] Verifying generated message and solving..."
if [ ! -f "$OUT_DIR/message.txt" ]; then
    echo "Error: /output/message.txt was not generated!" >&2
    exit 1
fi

echo "Generated ciphertext:"
cat "$OUT_DIR/message.txt"
echo

echo "Solving generated ciphertext with solve.py:"
RECOVERED=$(python3 solve/solve.py "$OUT_DIR/message.txt" | tail -n 1)

if [ "$RECOVERED" = "$TEST_FLAG" ]; then
    echo "SUCCESS: Flag verified: $RECOVERED"
    rm -rf "$OUT_DIR"
    exit 0
else
    echo "FAIL: Expected $TEST_FLAG but got $RECOVERED" >&2
    exit 1
fi
