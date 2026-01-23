import pygame
import random
from settings import *
from templates import TEMPLATES
from unit import Unit
from ui import Button
from icons import draw_nato_icon

class SetupState:
    # Inicjalizacja ekranu ustawień potyczki
    def __init__(self, ctx):
        self.ctx = ctx
        bh = 45
        self.btns = {
            "side":  Button("ZMIEŃ STRONĘ", 100, 200, 200, bh),
            "map":   Button("ZMIEŃ MAPĘ", 100, 310, 200, bh),
            "limit": Button("ZMIEŃ LIMIT", 100, 420, 200, bh),
            "start": Button("PRZYGOTOWANIE", SCREEN_WIDTH-300, SCREEN_HEIGHT-100, 250, bh),
            "back":  Button("POWRÓT", 50, SCREEN_HEIGHT-70, 120, 40)
        }
        self.ctx.map_manager.load_map(self.ctx.setup_map)

    # Obsługa zdarzeń
    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btns["back"].check(m_pos): return "MENU"
            if self.btns["side"].check(m_pos):
                self.ctx.setup_side = "PACT" if self.ctx.setup_side == "NATO" else "NATO"
                self.ctx.player_pool = []; self.ctx.setup_points = 0
            if self.btns["limit"].check(m_pos):
                limits = [100, 200, 400, 600, 1000]
                self.ctx.setup_limit = limits[(limits.index(self.ctx.setup_limit) + 1) % len(limits)]
                self.ctx.player_pool = []; self.ctx.setup_points = 0
            if self.btns["map"].check(m_pos):
                maps = list(self.ctx.map_manager.map_files.keys())
                self.ctx.setup_map = maps[(maps.index(self.ctx.setup_map) + 1) % len(maps)]
                self.ctx.map_manager.load_map(self.ctx.setup_map)

            # Usuwanie jednostek
            y_list = 150
            for i, u in enumerate(self.ctx.player_pool):
                if pygame.Rect(SCREEN_WIDTH//2-200, y_list-5, 400, 35).collidepoint(m_pos):
                    self.ctx.setup_points -= u.template.get_firepower()
                    self.ctx.player_pool.pop(i); return None
                y_list += 40

            # Wybór jednostek z dostępnych
            p_color = COLOR_NATO if self.ctx.setup_side == "NATO" else COLOR_PACT
            y_shop = 150
            for v in TEMPLATES[self.ctx.setup_side].values():
                if pygame.Rect(SCREEN_WIDTH-400, y_shop, 350, 35).collidepoint(m_pos):
                    cost = v.get_firepower()
                    if self.ctx.setup_points + cost <= self.ctx.setup_limit:
                        unit = Unit(v, 0, 0, 1, p_color)
                        unit.template = v # Do pobrania ceny przy usuwaniu
                        unit.placed = False 
                        self.ctx.player_pool.append(unit)
                        self.ctx.setup_points += cost
                y_shop += 40

            if self.btns["start"].check(m_pos) and self.ctx.player_pool:
                self.init_ai()
                # Wczytujemy mapę ponownie, by zresetować ewentualne zmiany
                self.ctx.map_manager.load_map(self.ctx.setup_map)
                return "DEPLOYMENT"
        return None

    def init_ai(self):
        self.ctx.ai_units = []
        ai_f = "PACT" if self.ctx.setup_side == "NATO" else "NATO"
        ai_c = COLOR_PACT if self.ctx.setup_side == "NATO" else COLOR_NATO
        pts = 0
        attempts = 0
        while pts < (self.ctx.setup_limit - 20) and attempts < 100:
            attempts += 1
            possible = [t for t in TEMPLATES[ai_f].values() if t.get_firepower() <= (self.ctx.setup_limit - pts)]
            if not possible: break
            tpl = random.choice(possible)
            # AI od razu ma placed=True
            u = Unit(tpl, random.randint(SCREEN_WIDTH-400, SCREEN_WIDTH-50), random.randint(100, SCREEN_HEIGHT-100), 2, ai_c)
            u.placed = True; self.ctx.ai_units.append(u); pts += tpl.get_firepower()

    def draw(self, m_pos):
        self.ctx.screen.fill(COLOR_BG)
        p_c = COLOR_NATO if self.ctx.setup_side == "NATO" else COLOR_PACT
        
        self.ctx.screen.blit(self.ctx.font_big.render("USTAWIENIA POTYCZKI", True, COLOR_TEXT), (100, 50))
        self.ctx.screen.blit(self.ctx.font.render(f"STRONA:", True, (200,200,200)), (100, 165))
        self.ctx.screen.blit(self.ctx.font.render(f"{self.ctx.setup_side}", True, p_c), (200, 165))
        
        map_name = self.ctx.setup_map.replace('_', ' ').upper()
        self.ctx.screen.blit(self.ctx.font.render(f"MAPA:", True, (200,200,200)), (100, 275))
        self.ctx.screen.blit(self.ctx.font.render(f"{map_name}", True, COLOR_ACCENT), (170, 275))
        
        self.ctx.screen.blit(self.ctx.font.render(f"LIMIT:", True, (200,200,200)), (100, 385))
        self.ctx.screen.blit(self.ctx.font.render(f"{self.ctx.setup_limit} PKT", True, (255, 200, 0)), (170, 385))

        for b in self.btns.values(): b.check(m_pos); b.draw(self.ctx.screen, self.ctx.font)
        
        # Lista jednostek gracza
        self.ctx.screen.blit(self.ctx.font.render("TWOJA ARMIA:", True, COLOR_TEXT), (SCREEN_WIDTH//2 - 200, 110))
        y_list = 150
        for u in self.ctx.player_pool:
            entry_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, y_list - 5, 400, 35)
            if entry_rect.collidepoint(m_pos):
                pygame.draw.rect(self.ctx.screen, (60, 60, 70), entry_rect, border_radius=5)
                pygame.draw.rect(self.ctx.screen, (255, 50, 50), entry_rect, 1, border_radius=5)
            draw_nato_icon(self.ctx.screen, SCREEN_WIDTH//2 - 180, y_list + 12, u.color, u.u_type, False, u.rank)
            self.ctx.screen.blit(self.ctx.font_small.render(u.name, True, (220,220,220)), (SCREEN_WIDTH//2 - 150, y_list + 3))
            y_list += 40

        # SKLEP
        self.ctx.screen.blit(self.ctx.font.render("JEDNOSTKI:", True, COLOR_TEXT), (SCREEN_WIDTH-400, 110))
        y_shop = 150
        for v in TEMPLATES[self.ctx.setup_side].values():
            rect = pygame.Rect(SCREEN_WIDTH-400, y_shop, 350, 35)
            col = (60,60,60) if rect.collidepoint(m_pos) else (45,45,45)
            pygame.draw.rect(self.ctx.screen, col, rect, border_radius=5)
            self.ctx.screen.blit(self.ctx.font_small.render(f"{v.name} ({int(v.get_firepower())} pkt)", True, COLOR_TEXT), (SCREEN_WIDTH-390, y_shop+8))
            y_shop += 40
            
        self.ctx.screen.blit(self.ctx.font_big.render(f"PUNKTY: {int(self.ctx.setup_points)} / {self.ctx.setup_limit}", True, (255, 200, 0)), (SCREEN_WIDTH//2-150, SCREEN_HEIGHT-150))