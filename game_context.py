import pygame
from map_manager import MapManager
from settings import *

class GameContext:
    def __init__(self, screen):
        self.screen = screen
        self.map_manager = MapManager()
        self.reset_skirmish()
        
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_big = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16)

    def reset_skirmish(self):
        self.setup_side = "NATO"
        self.setup_map = "fulda" # NOWY DEFAULT
        self.setup_limit = 600
        self.setup_points = 0
        self.player_pool = []
        self.ai_units = []
        self.selected_unit = None
        self.mission_faction = "NATO"