import pygame
from settings import *
from ui import Button

class MenuState:
    # Inicjalizacja menu głównego
    def __init__(self, ctx):
        self.ctx = ctx
        bx, bw, bh = SCREEN_WIDTH//2 - 100, 200, 45
        self.btns = {
            "misje":     Button("MISJE", bx, SCREEN_HEIGHT//2 - 130, bw, bh),
            "multi":     Button("MULTIPLAYER", bx, SCREEN_HEIGHT//2 - 70, bw, bh),
            "potyczka":  Button("POTYCZKA", bx, SCREEN_HEIGHT//2 - 10, bw, bh),
            "templates": Button("SZABLONY", bx, SCREEN_HEIGHT//2 + 50, bw, bh),
            "wyjscie":   Button("WYJŚCIE", bx, SCREEN_HEIGHT//2 + 110, bw, bh)
        }

    # Obsługa zdarzeń
    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btns["potyczka"].check(m_pos): return "SKIRMISH_SETUP"
            if self.btns["misje"].check(m_pos): return "MISSIONS"
            if self.btns["multi"].check(m_pos): return "MULTI_MSG"
            if self.btns["templates"].check(m_pos): return "TEMPLATES"
            if self.btns["wyjscie"].check(m_pos): return "EXIT_PROMPT"
        return None

    # Rysuj menu główne
    def draw(self, m_pos):
        self.ctx.screen.fill(COLOR_BG)
        title = self.ctx.font_big.render("TRYB GENERALSKI", True, COLOR_ACCENT)
        self.ctx.screen.blit(title, (SCREEN_WIDTH//2-title.get_width()//2, 150))
        for b in self.btns.values(): b.check(m_pos); b.draw(self.ctx.screen, self.ctx.font)