import pygame
from settings import *
from ui import Button

# --- KLASA 1: WYBÓR FRAKCJI (KAFELKI) ---
class MissionsState:
    def __init__(self, ctx):
        self.ctx = ctx
        # Definiujemy duże kafelki (przyciski) bez tekstu (tekst narysujemy sami kolorowy)
        self.btns = {
            "NATO": Button("", SCREEN_WIDTH//2 - 350, SCREEN_HEIGHT//2 - 150, 300, 300),
            "PACT": Button("", SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//2 - 150, 300, 300),
            "back": Button("POWRÓT", 50, SCREEN_HEIGHT - 70, 120, 40)
        }

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btns["back"].check(m_pos): return "MENU"
            
            if self.btns["NATO"].check(m_pos):
                self.ctx.mission_faction = "NATO"
                return "MISSION_SELECT"
                
            if self.btns["PACT"].check(m_pos):
                self.ctx.mission_faction = "PACT"
                return "MISSION_SELECT"
        return None

    def draw(self, m_pos):
        self.ctx.screen.fill(COLOR_BG)
        title = self.ctx.font_big.render("WYBIERZ FRAKCJĘ KAMPANII", True, COLOR_TEXT)
        self.ctx.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

        # --- KAFELEK NATO ---
        is_nato_hover = self.btns["NATO"].check(m_pos)
        # Tło kafelka (ciemny granat)
        pygame.draw.rect(self.ctx.screen, (20, 30, 50), self.btns["NATO"].rect, border_radius=15)
        # Obramowanie (niebieskie)
        pygame.draw.rect(self.ctx.screen, COLOR_PLAYER, self.btns["NATO"].rect, 4 if is_nato_hover else 2, border_radius=15)
        
        # KOLOROWY NAPIS NATO
        txt_nato = self.ctx.font_big.render("NATO", True, COLOR_PLAYER)
        txt_nato_rect = txt_nato.get_rect(center=self.btns["NATO"].rect.center)
        self.ctx.screen.blit(txt_nato, txt_nato_rect)
        
        # --- KAFELEK PACT ---
        is_pact_hover = self.btns["PACT"].check(m_pos)
        # Tło kafelka (ciemna czerwień)
        pygame.draw.rect(self.ctx.screen, (50, 20, 20), self.btns["PACT"].rect, border_radius=15)
        # Obramowanie (czerwone)
        pygame.draw.rect(self.ctx.screen, COLOR_AI, self.btns["PACT"].rect, 4 if is_pact_hover else 2, border_radius=15)
        
        # KOLOROWY NAPIS PACT
        txt_pact = self.ctx.font_big.render("PACT", True, COLOR_AI)
        txt_pact_rect = txt_pact.get_rect(center=self.btns["PACT"].rect.center)
        self.ctx.screen.blit(txt_pact, txt_pact_rect)

        # Przycisk powrotu (standardowy)
        self.btns["back"].check(m_pos)
        self.btns["back"].draw(self.ctx.screen, self.ctx.font)

# --- KLASA 2: LISTA MISJI ---
class MissionSelectionState:
    def __init__(self, ctx):
        self.ctx = ctx
        self.btn_back = Button("POWRÓT", 50, SCREEN_HEIGHT - 70, 120, 40)
        
        self.mission_btns = []
        for i in range(5):
            self.mission_btns.append(Button(f"OPERACJA {i+1}", SCREEN_WIDTH//2 - 200, 200 + i*70, 400, 50))

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_back.check(m_pos): return "MISSIONS"
            
            for i, btn in enumerate(self.mission_btns):
                if btn.check(m_pos):
                    print(f"Start misji {i+1} dla {self.ctx.mission_faction}")
        return None

    def draw(self, m_pos):
        self.ctx.screen.fill(COLOR_BG)
        
        # Dynamiczny kolor nagłówka
        faction_color = COLOR_PLAYER if self.ctx.mission_faction == "NATO" else COLOR_AI
        title = self.ctx.font_big.render(f"OPERACJE: {self.ctx.mission_faction}", True, faction_color)
        self.ctx.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))

        for btn in self.mission_btns:
            btn.check(m_pos)
            btn.draw(self.ctx.screen, self.ctx.font)

        self.btn_back.check(m_pos)
        self.btn_back.draw(self.ctx.screen, self.ctx.font)