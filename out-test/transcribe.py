import whisper


def transcribe_audio(audio_path, model_size="small", language="en"):
    """
    Audio faylni Whisper orqali so'z darajasida timestamp bilan transkripsiya qiladi.
    Natija: [(start_sekund, so'z), ...]
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language=language, word_timestamps=True)

    word_times = []
    for segment in result["segments"]:
        for w in segment.get("words", []):
            word_times.append((w["start"], w["word"].strip()))
    return word_times


def save_as_timed_script(word_times, output_path, group_seconds=3.0):
    """
    So'z darajasidagi timestamplarni ~group_seconds oralig'ida
    (M:SS) matn... formatiga guruhlab, faylga yozadi.
    """
    if not word_times:
        return

    lines = []
    current_start = word_times[0][0]
    current_words = []

    for start, word in word_times:
        if start - current_start >= group_seconds and current_words:
            lines.append(_format_line(current_start, current_words))
            current_start = start
            current_words = []
        current_words.append(word)

    if current_words:
        lines.append(_format_line(current_start, current_words))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _format_line(start_sec, words):
    m = int(start_sec // 60)
    s = start_sec - m * 60
    return f"({m}:{s:04.1f}) {' '.join(words)}"