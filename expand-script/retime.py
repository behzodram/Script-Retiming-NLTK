import re
from nltk import pos_tag
import argparse
import os


TARGET_INTERVAL = 3.0   # soft maqsad: har ~3 sekundda bo'lak
SEARCH_WINDOW = 1.5     # 3s nuqtasi atrofida qancha izlash (sekund)
COPULA = {"is", "are", "was", "were", "be", "been", "being", "am"}

PAUSE_BONUS = {
    ",": 0.5, "-": 0.7, "—": 0.7, "...": 0.7, "…": 0.7,
    ".": 1.0, ";": 1.0, "!": 1.0, "?": 1.0,
}


def parse_timed_script(text):
    """'(M:SS) matn...' bloklarini (start_sekund, matn) ro'yxatiga aylantiradi."""
    pattern = re.compile(r"\((\d+):(\d{2})\)\s*")
    matches = list(pattern.finditer(text))
    blocks = []
    for i, m in enumerate(matches):
        start = int(m.group(1)) * 60 + int(m.group(2))
        text_start = m.end()
        text_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block_text = re.sub(r"\s+", " ", text[text_start:text_end].strip())
        blocks.append((start, block_text))
    return blocks


def word_weight(word):
    """Tinish belgisiga qarab og'irlik (pauza qancha uzun bo'lsa)."""
    for punct, bonus in PAUSE_BONUS.items():
        if word.endswith(punct):
            return 1.0 + bonus
    return 1.0


def tag_words(raw_words):
    clean = [re.sub(r"[^\w']", "", w) for w in raw_words]
    return pos_tag(clean, tagset="universal")  # [(so'z, TAG), ...]


def candidate_score(word, tag, time_diff):
    """Ot/sifat/fe'l bo'lsa va 3s nuqtasiga yaqin bo'lsa — yuqori ball."""
    if tag == "VERB" and word.lower() not in COPULA:
        priority = 1.2
    elif tag == "NOUN":
        priority = 1.0
    elif tag == "ADJ":
        priority = 0.8
    elif tag == "VERB":  # copula (is/are/was...)
        priority = 0.3
    else:
        return None
    return priority - abs(time_diff) * 0.5


def expand_block(start, end, raw_words):
    n = len(raw_words)
    if n == 0:
        return []

    weights = [word_weight(w) for w in raw_words]
    total_weight = sum(weights)
    duration = end - start
    unit = duration / total_weight if total_weight else 0

    word_times, cum = [], 0.0
    for w in weights:
        word_times.append(start + unit * cum)
        cum += w

    tagged = tag_words(raw_words)

    breakpoints = [0]
    next_target = start + TARGET_INTERVAL
    i = 1
    while next_target < end - 0.5:
        best_idx, best_score = None, float("-inf")
        for j in range(i, n):
            wt = word_times[j]
            if wt > next_target + SEARCH_WINDOW:
                break
            if wt < next_target - SEARCH_WINDOW:
                continue
            word, tag = tagged[j]
            score = candidate_score(word, tag, wt - next_target)
            if score is not None and score > best_score:
                best_score, best_idx = score, j
        if best_idx is not None and best_idx > breakpoints[-1]:
            breakpoints.append(best_idx)
            i = best_idx + 1
        next_target += TARGET_INTERVAL

    breakpoints = sorted(set(breakpoints))
    segments = []
    for idx, bp in enumerate(breakpoints):
        seg_end = breakpoints[idx + 1] if idx + 1 < len(breakpoints) else n
        chunk = " ".join(raw_words[bp:seg_end])
        segments.append((round(word_times[bp], 1), chunk))
    return segments


def format_timestamp(seconds):
    m = int(seconds // 60)
    s = seconds - m * 60
    return f"({m}:{s:04.1f})"


def retime_script(input_text):
    blocks = parse_timed_script(input_text)
    output_lines = []
    for idx, (start, block_text) in enumerate(blocks):
        end = blocks[idx + 1][0] if idx + 1 < len(blocks) else start + 5
        raw_words = block_text.split(" ")
        for ts, chunk in expand_block(start, end, raw_words):
            output_lines.append(f"{format_timestamp(ts)} {chunk}")
    return "\n".join(output_lines)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Timing qilingan scriptni qayta timing qilish.")
    parser.add_argument(
        "--input", default="input_script.txt",
        help="Kirish script fayli (default: input_script.txt)"
    )
    parser.add_argument(
        "--output", default="../out-test/data/expanded_script.txt",
        help="Chiqish fayli (default: ../out-test/data/expanded_script.txt)"
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        raw_text = f.read()

    new_script = retime_script(raw_text)

    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(new_script)

    print(f"Tayyor: {args.output} yaratildi.")
