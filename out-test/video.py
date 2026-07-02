import os
import re
import pygame

# S00-23_cc3q.png -> daqiqa=00, sekund=23
IMAGE_PATTERN = re.compile(r"^S(\d{2})-(\d{2})_.*\.(png|jpg|jpeg)$", re.IGNORECASE)


def load_images(images_dir):
    """
    'data/pulled-png/' papkasidagi S{MM}-{SS}_xxxx.png fayllarini
    (start_sekund, fayl_yoli) ro'yxatiga aylantiradi, vaqt bo'yicha saralangan.
    """
    images = []
    for fname in os.listdir(images_dir):
        m = IMAGE_PATTERN.match(fname)
        if not m:
            continue
        minute, second = int(m.group(1)), int(m.group(2))
        start = minute * 60 + second
        images.append((start, os.path.join(images_dir, fname)))
    images.sort(key=lambda x: x[0])
    if not images:
        raise FileNotFoundError(f"'{images_dir}' ichida S{{MM}}-{{SS}}_xxxx.png formatidagi rasm topilmadi.")
    return images


def get_current_image(images, pos_sec):
    """Berilgan audio pozitsiyasiga mos keluvchi eng so'nggi rasmni qaytaradi."""
    current = images[0][1]
    for start, path in images:
        if start <= pos_sec:
            current = path
        else:
            break
    return current


class ImageCache:
    """Rasmlarni har safar diskdan qayta o'qimaslik uchun keshlaydi (scale bilan)."""

    def __init__(self):
        self._cache = {}

    def get(self, path, target_size):
        key = (path, target_size)
        if key not in self._cache:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, target_size)
            self._cache[key] = img
        return self._cache[key]