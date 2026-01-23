import pygame
from map_manager import MapManager
from settings import *

class GameContext:
    def __init__(self, screen):
        self.screen = screen
        self.map_manager = MapManager()
        
        # Dane potyczki
        self.setup_side = "NATO"
        self.setup_map = "default"
        self.setup_limit = 600
        self.setup_points = 0
        
        # Dane misji
        self.mission_faction = "NATO" # Wybrana frakcja w menu misji
        
        self.player_pool = []
        self.ai_units = []
        self.selected_unit = None
        
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_big = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16)