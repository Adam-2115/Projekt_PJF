import pygame

pygame.init()
info = pygame.display.Info()

# Ekran
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
FPS = 60
COMBAT_RANGE = 35

# Kolory
COLOR_BG = (30, 35, 40)
COLOR_BTN = (50, 60, 70)
COLOR_BTN_HOVER = (80, 90, 100)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (200, 50, 50)
COLOR_PLAYER = (50, 150, 255)
COLOR_AI = (255, 50, 50)