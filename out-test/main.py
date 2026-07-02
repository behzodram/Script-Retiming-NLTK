import argparse
import re
import time
import textwrap

import pygame

from audio import AudioPlayer
from transcribe import transcribe_audio, save_as_timed_script
from video import load_images, get_current_image, ImageCache

WINDOW_W, WINDOW_H = 1280, 720
IMAGE_AREA_H = 560          # rasm uchun ajratilgan balandlik
SUBTITLE_AREA_H = WINDOW_H - IMAGE_AREA_H
BG_COLOR = (18, 18, 18)
SUBTITLE_BG = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
TIMESTAMP_COLOR = (150, 150, 150)


def parse_timed_script(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    pattern = re.compile(r"\((\d+):(\d+(?:\.\d+)?)\)\s*")
    matches = list(pattern.finditer(text))
    blocks = []
    for i, m in enumerate(matches):
        start = int(m.group(1)) * 60 + float(m.group(2))
        text_start = m.end()
        text_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block_text = re.sub(r"\s+", " ", text[text_start:text_end].strip())
        blocks.append((start, block_text))
    return blocks


def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines, current = [], ""
    for w in words:
        trial = f"{current} {w}".strip()
        if font.size(trial)[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def run_video(audio_path, script_path, images_dir):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Script Preview — audio + rasm + transkript")
    clock = pygame.time.Clock()

    text_font = pygame.font.SysFont("segoeui", 28)
    ts_font = pygame.font.SysFont("consolas", 18)

    images = load_images(images_dir)
    blocks = parse_timed_script(script_path)
    cache = ImageCache()

    player = AudioPlayer(audio_path)
    player.play()

    idx = 0
    n = len(blocks)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pos = player.get_position()

        while idx + 1 < n and blocks[idx + 1][0] <= pos:
            idx += 1

        current_start, current_text = blocks[idx] if idx < n else (0, "")
        img_path = get_current_image(images, pos)

        screen.fill(BG_COLOR)

        # --- rasm ---
        target_w = WINDOW_W
        target_h = IMAGE_AREA_H
        surf = cache.get(img_path, (target_w, target_h))
        screen.blit(surf, (0, 0))

        # --- subtitle fon ---
        pygame.draw.rect(screen, SUBTITLE_BG, (0, IMAGE_AREA_H, WINDOW_W, SUBTITLE_AREA_H))

        # --- timestamp ---
        m, s = int(current_start // 60), current_start % 60
        ts_surf = ts_font.render(f"[{m}:{s:04.1f}]", True, TIMESTAMP_COLOR)
        screen.blit(ts_surf, (20, IMAGE_AREA_H + 10))

        # --- matn (wrap qilingan) ---
        lines = wrap_text(current_text, text_font, WINDOW_W - 40)
        y = IMAGE_AREA_H + 40
        for line in lines:
            line_surf = text_font.render(line, True, TEXT_COLOR)
            screen.blit(line_surf, (20, y))
            y += text_font.get_linesize()

        pygame.display.flip()
        clock.tick(30)

        if not player.is_playing() and idx >= n - 1:
            time.sleep(1.0)
            running = False

    pygame.quit()


def main():
    parser = argparse.ArgumentParser(
        description="Audio + rasm + transkript scriptni bitta oynada sinxron ko'rsatish."
    )
    parser.add_argument("--audio", required=True, help="Audio fayl yo'li (mp3/wav)")
    parser.add_argument(
        "--script",
        help="Timing qilingan .txt script (bo'lmasa, --transcribe bilan avtomatik yaratiladi)",
    )
    parser.add_argument(
        "--images", default="data/pulled-png",
        help="S{MM}-{SS}_xxxx.png rasmlar papkasi (default: data/pulled-png)",
    )
    parser.add_argument(
        "--transcribe",
        action="store_true",
        help="Scriptni berilmasa, Whisper orqali audio'dan avtomatik yaratadi",
    )
    parser.add_argument("--group-seconds", type=float, default=3.0)
    args = parser.parse_args()

    script_path = args.script

    if args.transcribe or not script_path:
        print("Audio transkripsiya qilinmoqda (Whisper)...")
        word_times = transcribe_audio(args.audio)
        script_path = "transcribed_script.txt"
        save_as_timed_script(word_times, script_path, group_seconds=args.group_seconds)
        print(f"Transkripsiya tayyor: {script_path}")

    run_video(args.audio, script_path, args.images)


if __name__ == "__main__":
    main()