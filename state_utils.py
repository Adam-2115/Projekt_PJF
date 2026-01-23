import pygame
import sys
from settings import *
from templates import TEMPLATES
from ui import Button

# --- STAN: PAUZA ---
class PauseState:
    def __init__(self, ctx, prev_key):
        self.ctx = ctx
        self.prev_key = prev_key
        bx, bw, bh = SCREEN_WIDTH//2 - 100, 200, 45
        self.btns = {
            "continue": Button("KONTYNUUJ", bx, SCREEN_HEIGHT//2 - 80, bw, bh),
            "to_menu":  Button("MENU GŁÓWNE", bx, SCREEN_HEIGHT//2 - 20, bw, bh),
            "quit":     Button("WYJDŹ Z GRY", bx, SCREEN_HEIGHT//2 + 40, bw, bh)
        }

    def handle_events(self, event, m_pos):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
            return self.prev_key
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btns["continue"].check(m_pos): return self.prev_key
            if self.btns["to_menu"].check(m_pos): return "MENU"
            if self.btns["quit"].check(m_pos): return "EXIT_PROMPT"
        return None

    def draw(self, m_pos):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.ctx.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self.ctx.screen, COLOR_BG, (SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2-150, 300, 350), border_radius=10)
        pygame.draw.rect(self.ctx.screen, COLOR_TEXT, (SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2-150, 300, 350), 2, border_radius=10)
        
        for b in self.btns.values():
            b.check(m_pos)
            b.draw(self.ctx.screen, self.ctx.font)

# --- STAN: KONIEC GRY ---
class GameOverState:
    def __init__(self, ctx, is_victory):
        self.ctx = ctx
        self.is_victory = is_victory
        self.btn_menu = Button("POWRÓT DO MENU", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 45)

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_menu.check(m_pos): return "MENU"
        return None

    def draw(self, m_pos):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.ctx.screen.blit(overlay, (0, 0))
        
        text = "ZWYCIĘSTWO TAKTYCZNE" if self.is_victory else "CAŁKOWITA PORAŻKA"
        color = (50, 200, 50) if self.is_victory else (200, 50, 50)
        
        title = self.ctx.font_big.render(text, True, color)
        self.ctx.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 100))
        
        self.btn_menu.check(m_pos)
        self.btn_menu.draw(self.ctx.screen, self.ctx.font)

# --- STAN: SZABLONY (Z PEŁNYMI NAZWAMI) ---
class TemplatesState:
    def __init__(self, ctx):
        self.ctx = ctx
        self.btn_back = Button("POWRÓT", 50, SCREEN_HEIGHT - 70, 120, 40)

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_back.check(m_pos): return "MENU"
        return None

    def draw(self, m_pos):
        self.ctx.screen.fill(COLOR_BG)
        y = 50
        for faction, units in TEMPLATES.items():
            color = (50, 100, 255) if faction == "NATO" else (255, 50, 50)
            header = self.ctx.font_big.render(f"--- {faction} ---", True, color)
            self.ctx.screen.blit(header, (SCREEN_WIDTH//2 - header.get_width()//2, y))
            y += 70
            
            for t in units.values():
                pygame.draw.rect(self.ctx.screen, COLOR_BTN, (SCREEN_WIDTH//2 - 400, y, 800, 45), border_radius=5)
                
                # PEŁNE NAZWY ZAMIAST SKRÓTÓW:
                txt_content = f"{t.name} | Czołgi: {int(t.tanks)} | APC: {int(t.apc)} | Ludzie: {int(t.soldiers) } | Ciężarówki: {int(t.trucks)}"
                
                txt = self.ctx.font.render(txt_content, True, COLOR_TEXT)
                self.ctx.screen.blit(txt, (SCREEN_WIDTH//2 - 380, y + 8))
                y += 55
            y += 20
            
        self.btn_back.check(m_pos)
        self.btn_back.draw(self.ctx.screen, self.ctx.font)

# --- STAN: PROSTA WIADOMOŚĆ ---
class SimpleMsgState:
    def __init__(self, ctx, msg):
        self.ctx = ctx
        self.msg = msg
        self.btn_back = Button("POWRÓT", 50, SCREEN_HEIGHT - 70, 120, 40)

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_back.check(m_pos): return "MENU"
        return None

    def draw(self, m_pos):
        self.ctx.screen.fill(COLOR_BG)
        txt = self.ctx.font_big.render(self.msg, True, (255, 200, 0))
        self.ctx.screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2))
        self.btn_back.check(m_pos)
        self.btn_back.draw(self.ctx.screen, self.ctx.font)

# --- STAN: WYJŚCIE ---
class ExitPromptState:
    def __init__(self, ctx):
        self.ctx = ctx
        self.btn_yes = Button("TAK", SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2 + 50, 100, 50)
        self.btn_no = Button("NIE", SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT//2 + 50, 100, 50)

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_yes.check(m_pos): pygame.quit(); sys.exit()
            if self.btn_no.check(m_pos): return "MENU"
        return None

    def draw(self, m_pos):
        pygame.draw.rect(self.ctx.screen, (20, 20, 20), (SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 100, 500, 250), border_radius=15)
        txt = self.ctx.font.render("CZY NA PEWNO CHCESZ WYJŚĆ?", True, COLOR_TEXT)
        self.ctx.screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2 - 40))
        self.btn_yes.check(m_pos)
        self.btn_yes.draw(self.ctx.screen, self.ctx.font)
        self.btn_no.check(m_pos)
        self.btn_no.draw(self.ctx.screen, self.ctx.font)