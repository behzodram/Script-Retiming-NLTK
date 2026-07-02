#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR="./pulled-png"

# ---- OUTPUT_DIR mavjudligini va ichida fayl bor-yo'qligini tekshirish ----
if [[ -d "$OUTPUT_DIR" ]]; then
    existing_count=$(find "$OUTPUT_DIR" -type f | wc -l)
    if (( existing_count > 0 )); then
        read -rp "\"$OUTPUT_DIR\" papkasida $existing_count ta fayl bor. Uni tozalab, qaytadan yuklashni xohlaysizmi? (ha/yo'q): " answer
        case "$answer" in
            ha|Ha|HA|y|Y|yes|Yes)
                echo "🧹 Papka tozalanmoqda..."
                rm -f "$OUTPUT_DIR"/*
                ;;
            *)
                echo "❌ Bekor qilindi. Jarayon to'xtatildi."
                exit 0
                ;;
        esac
    fi
fi

mkdir -p "$OUTPUT_DIR"

# ---- Oxirgi nechta jobni olish kerakligini so'raymiz ----
read -rp "Nechta oxirgi jobni tekshirish kerak? " N

if ! [[ "$N" =~ ^[0-9]+$ ]]; then
    echo "❌ Xato: butun son kiriting (masalan: 40)"
    exit 1
fi

# higgsfield generate list --json | jq -c \
higgsfield generate list --size "$N" --json | jq -c \
  --argjson n "$N" \
  '.[0:$n] | .[] | select(.status == "completed" and .result_url != null)' \
  > /tmp/filtered_jobs.jsonl

count=$(wc -l < /tmp/filtered_jobs.jsonl)
echo "Topilgan tugallangan joblar: $count / $N"

while IFS= read -r job; do
    job_id=$(jq -r '.id' <<< "$job")
    url=$(jq -r '.result_url' <<< "$job")
    prompt=$(jq -r '.params.prompt' <<< "$job")

    if [[ "$prompt" =~ ^S([0-9]+):([0-9]+)T ]]; then
        minutes="${BASH_REMATCH[1]}"
        seconds="${BASH_REMATCH[2]}"
        rand_suffix=$(tr -dc 'a-z0-9' </dev/urandom | head -c4) || true
        # filename=$(printf "S%02d-%02d_%s.png" "$minutes" "$seconds" "$rand_suffix")
        filename=$(printf "S%02d-%02d_%s.png" "$((10#$minutes))" "$((10#$seconds))" "$rand_suffix")
    else
        echo "⚠️  Timestamp topilmadi ($job_id): ${prompt:0:40}..."
        rand_suffix=$(tr -dc 'a-z0-9' </dev/urandom | head -c4) || true
        filename="unknown_${rand_suffix}.png"
    fi

    dest="$OUTPUT_DIR/$filename"

    echo "⬇️  $filename  <-  $job_id"
    curl -sL "$url" -o "$dest"

done < /tmp/filtered_jobs.jsonl

echo "✅ Tayyor. Fayllar: $OUTPUT_DIR (jami: $(ls "$OUTPUT_DIR" | wc -l))"
