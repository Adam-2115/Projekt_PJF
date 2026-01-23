import pygame
import random
from settings import *
from templates import TEMPLATES
from unit import Unit
from ui import Button

class SetupState:
    def __init__(self, ctx):
        self.ctx = ctx
        bh = 45
        self.btns = {
            "side":  Button("ZMIEŃ STRONĘ", 100, 250, 200, bh),
            "map":   Button("ZMIEŃ MAPĘ", 100, 310, 200, bh),
            "limit": Button("ZMIEŃ LIMIT", 100, 370, 200, bh),
            "start": Button("PRZYGOTOWANIE", SCREEN_WIDTH-300, SCREEN_HEIGHT-100, 250, bh),
            "back":  Button("POWRÓT", 50, SCREEN_HEIGHT-70, 120, 40)
        }

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btns["back"].check(m_pos): return "MENU"
            if self.btns["side"].check(m_pos):
                self.ctx.setup_side = "PACT" if self.ctx.setup_side == "NATO" else "NATO"
                self.ctx.player_pool = []; self.ctx.setup_points = 0
            if self.btns["limit"].check(m_pos):
                limits = [200, 400, 600, 1000, 1500]; curr = limits.index(self.ctx.setup_limit)
                self.ctx.setup_limit = limits[(curr + 1) % len(limits)]
                self.ctx.player_pool = []; self.ctx.setup_points = 0
            if self.btns["map"].check(m_pos):
                maps = ["default", "mission_1"]; curr = maps.index(self.ctx.setup_map)
                self.ctx.setup_map = maps[(curr+1)%len(maps)]
            
            player_color = COLOR_PLAYER if self.ctx.setup_side == "NATO" else COLOR_AI
            y = 150
            for v in TEMPLATES[self.ctx.setup_side].values():
                if pygame.Rect(SCREEN_WIDTH-400, y, 350, 35).collidepoint(m_pos):
                    cost = v.get_firepower()
                    if self.ctx.setup_points + cost <= self.ctx.setup_limit:
                        self.ctx.player_pool.append(Unit(v, 0, 0, 1, player_color))
                        self.ctx.setup_points += cost
                y += 40
            
            if self.btns["start"].check(m_pos) and self.ctx.player_pool:
                self.init_ai(); self.ctx.map_manager.load_map(self.ctx.setup_map)
                return "DEPLOYMENT"
        return None

    def init_ai(self):
        self.ctx.ai_units = []
        ai_faction = "PACT" if self.ctx.setup_side == "NATO" else "NATO"
        ai_color = COLOR_AI if self.ctx.setup_side == "NATO" else COLOR_PLAYER
        pts = 0
        while pts < (self.ctx.setup_limit - 20):
            possible = [t for t in TEMPLATES[ai_faction].values() if t.get_firepower() <= (self.ctx.setup_limit - pts)]
            if not possible: break
            tpl = random.choice(possible)
            u = Unit(tpl, random.randint(SCREEN_WIDTH-400, SCREEN_WIDTH-50), random.randint(100, SCREEN_HEIGHT-100), 2, ai_color)
            u.placed = True; self.ctx.ai_units.append(u); pts += tpl.get_firepower()

    def draw(self, m_pos):
        self.ctx.screen.fill(COLOR_BG)
        p_color = COLOR_PLAYER if self.ctx.setup_side == "NATO" else COLOR_AI
        self.ctx.screen.blit(self.ctx.font_big.render("USTAWIENIA POTYCZKI", True, COLOR_TEXT), (100, 50))
        self.ctx.screen.blit(self.ctx.font.render(f"STRONA: {self.ctx.setup_side}", True, p_color), (100, 220))
        for b in self.btns.values(): b.check(m_pos); b.draw(self.ctx.screen, self.ctx.font)
        y = 150
        for v in TEMPLATES[self.ctx.setup_side].values():
            rect = pygame.Rect(SCREEN_WIDTH-400, y, 350, 35)
            pygame.draw.rect(self.ctx.screen, (50,50,50), rect, border_radius=5)
            self.ctx.screen.blit(self.ctx.font_small.render(f"{v.name} ({int(v.get_firepower())} pkt)", True, COLOR_TEXT), (SCREEN_WIDTH-390, y+8))
            y += 40
        self.ctx.screen.blit(self.ctx.font_big.render(f"PUNKTY: {int(self.ctx.setup_points)} / {self.ctx.setup_limit}", True, (255, 200, 0)), (SCREEN_WIDTH//2-150, SCREEN_HEIGHT-150))