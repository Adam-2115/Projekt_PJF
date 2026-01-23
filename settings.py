import pygame

pygame.init()
info = pygame.display.Info()

SCREEN_WIDTH = info.current_w # Szerokość ekranu
SCREEN_HEIGHT = info.current_h # Wysokość ekranu
FPS = 60 # Klatki na sekundę
COMBAT_RANGE = 35 # Zasięg walki jednostek
AUTO_ENGAGE_RANGE = 100 # Promień automatycznego wykrywania wroga
DEPLOY_ZONE_WIDTH = int(SCREEN_WIDTH * 0.3) # Szerokość strefy rozstawiania jednostek
COLOR_BG = (30, 35, 40) # Kolor tła
COLOR_BTN = (50, 60, 70) # Kolor przycisków
COLOR_BTN_HOVER = (80, 90, 100) # Kolor przycisków po najechaniu
COLOR_TEXT = (255, 255, 255) # Kolor tekstu
COLOR_ACCENT = (200, 50, 50) # Kolor akcentu
COLOR_NATO = (50, 100, 255) # Kolor jednostek NATO
COLOR_PACT = (255, 50, 50) # Kolor jednostek PACT
COLOR_ZONE_NATO = (50, 100, 255, 40) # Kolor strefy NATO
COLOR_ZONE_PACT = (255, 50, 50, 40) # Kolor strefy PACT