import pygame
import time


class AudioPlayer:
    """Audio faylni pygame.mixer orqali ijro etadi va joriy pozitsiyani beradi."""

    def __init__(self, audio_path):
        pygame.mixer.init()
        self.audio_path = audio_path
        self.start_time = None
        self._loaded = False

    def load(self):
        pygame.mixer.music.load(self.audio_path)
        self._loaded = True

    def play(self):
        if not self._loaded:
            self.load()
        pygame.mixer.music.play()
        self.start_time = time.time()

    def get_position(self):
        """Joriy audio pozitsiyasini sekundlarda qaytaradi."""
        if self.start_time is None:
            return 0.0
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms == -1:
            return 0.0
        return pos_ms / 1000.0

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def stop(self):
        pygame.mixer.music.stop()