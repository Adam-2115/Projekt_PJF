import pygame

pygame.init()
info = pygame.display.Info()

SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
FPS = 60
COMBAT_RANGE = 35
AUTO_ENGAGE_RANGE = 100 # Promień automatycznego wykrywania wroga

DEPLOY_ZONE_WIDTH = int(SCREEN_WIDTH * 0.3)

COLOR_BG = (30, 35, 40)
COLOR_BTN = (50, 60, 70)
COLOR_BTN_HOVER = (80, 90, 100)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (200, 50, 50)
COLOR_PLAYER = (50, 100, 255)
COLOR_AI = (255, 50, 50)
COLOR_ZONE = (50, 100, 255, 40)