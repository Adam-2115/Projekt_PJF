import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class MapManager:
    def __init__(self):
        self.folder = "mapy"
        self.map_files = {
            "default": "fulda.jpg",
        }
        self.current_map_img = None

    def load_map(self, map_key):
        filename = self.map_files.get(map_key, self.map_files["default"])
        full_path = os.path.join(self.folder, filename)
        
        if not os.path.exists(full_path):
            print(f"Nie znaleziono: {full_path}. Używam tła zastępczego.")
            self.current_map_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.current_map_img.fill((40, 70, 40))
            return

        full_img = pygame.image.load(full_path).convert()
        self.current_map_img = pygame.transform.scale(full_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, screen):
        if self.current_map_img:
            screen.blit(self.current_map_img, (0, 0))