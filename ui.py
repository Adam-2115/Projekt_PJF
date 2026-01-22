import pygame
from settings import COLOR_BTN, COLOR_BTN_HOVER, COLOR_TEXT

class Button:
    def __init__(self, text, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.is_hovered = False

    def draw(self, screen, font):
        color = COLOR_BTN_HOVER if self.is_hovered else COLOR_BTN
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 2, border_radius=5)
        t_surf = font.render(self.text, True, COLOR_TEXT)
        screen.blit(t_surf, t_surf.get_rect(center=self.rect.center))

    def check(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered