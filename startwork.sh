#!/usr/bin/env bash

set -e

LINK_FILE="ClaudeChatLink.txt"
WORK_DIR="out-test"

echo "========================================"
echo "        🚀 WORK SESSION STARTED"
echo "========================================"
echo

if [ ! -f "$LINK_FILE" ]; then
    echo "❌ $LINK_FILE topilmadi!"
    exit 1
fi

echo "📌 Claude chat linklari:"
echo

count=1
grep -Eo 'https://[^[:space:]]+' "$LINK_FILE" | while read -r url
do
    echo "[$count] $url"
    count=$((count+1))
done
