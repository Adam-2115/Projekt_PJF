import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class MapManager:
    def __init__(self):
        self.folder = "mapy"
        # Mapy z folderu 'mapy'
        self.map_files = {
            "fulda": "fulda.jpg",
            "debe_wielkie": "debe_wielkie.jpg",
            "gdansk": "gdansk.jpg",
            "siennica": "siennica.jpg",
            "warszawa_zoliborz": "warszawa_zoliborz.jpg"
        }
        self.current_map_img = None

    def load_map(self, map_key):
        """Ładuje wybraną mapę z folderu."""
        filename = self.map_files.get(map_key, "fulda.jpg")
        full_path = os.path.join(self.folder, filename)
        
        if not os.path.exists(full_path):
            print(f"Ostrzeżenie: Nie znaleziono {full_path}. Tworzę tło zastępcze.")
            self.current_map_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.current_map_img.fill((40, 70, 40))
            return

        try:
            full_img = pygame.image.load(full_path).convert()
            self.current_map_img = pygame.transform.scale(full_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            print(f"Mapa załadowana: {filename}")
        except pygame.error as e:
            print(f"Błąd ładowania obrazu: {e}")
            self.current_map_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.current_map_img.fill((100, 20, 20))

    def draw(self, screen):
        if self.current_map_img:
            screen.blit(self.current_map_img, (0, 0))