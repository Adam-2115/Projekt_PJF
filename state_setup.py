import pygame
import random
from settings import *
from templates import TEMPLATES
from unit import Unit
from ui import Button
from icons import draw_nato_icon

class SetupState:
    def __init__(self, ctx):
        self.ctx = ctx
        bh = 45
        # Zwiększone odstępy Y, aby przyciski nie nachodziły na napisy
        self.btns = {
            "side":  Button("ZMIEŃ STRONĘ", 100, 200, 200, bh),
            "map":   Button("ZMIEŃ MAPĘ", 100, 310, 200, bh),
            "limit": Button("ZMIEŃ LIMIT", 100, 420, 200, bh),
            "start": Button("PRZYGOTOWANIE", SCREEN_WIDTH-300, SCREEN_HEIGHT-100, 250, bh),
            "back":  Button("POWRÓT", 50, SCREEN_HEIGHT-70, 120, 40)
        }
        self.ctx.map_manager.load_map(self.ctx.setup_map)

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btns["back"].check(m_pos): return "MENU"
            
            if self.btns["side"].check(m_pos):
                self.ctx.setup_side = "PACT" if self.ctx.setup_side == "NATO" else "NATO"
                self.ctx.player_pool = []; self.ctx.setup_points = 0
                
            if self.btns["limit"].check(m_pos):
                limits = [200, 400, 600, 1000, 2000]
                curr = limits.index(self.ctx.setup_limit)
                self.ctx.setup_limit = limits[(curr + 1) % len(limits)]
                self.ctx.player_pool = []; self.ctx.setup_points = 0
                
            if self.btns["map"].check(m_pos):
                available_maps = list(self.ctx.map_manager.map_files.keys())
                curr_idx = available_maps.index(self.ctx.setup_map)
                new_idx = (curr_idx + 1) % len(available_maps)
                self.ctx.setup_map = available_maps[new_idx]
                self.ctx.map_manager.load_map(self.ctx.setup_map)

            # Usuwanie jednostek z listy (środek)
            y_list = 150
            for i, u in enumerate(self.ctx.player_pool):
                entry_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, y_list - 5, 400, 35)
                if entry_rect.collidepoint(m_pos):
                    self.ctx.setup_points -= u.template.get_firepower()
                    self.ctx.player_pool.pop(i)
                    return None
                y_list += 40

            # Kupowanie (prawo)
            p_color = COLOR_PLAYER if self.ctx.setup_side == "NATO" else COLOR_AI
            y_shop = 150
            for v in TEMPLATES[self.ctx.setup_side].values():
                if pygame.Rect(SCREEN_WIDTH-400, y_shop, 350, 35).collidepoint(m_pos):
                    cost = v.get_firepower()
                    if self.ctx.setup_points + cost <= self.ctx.setup_limit:
                        new_u = Unit(v, 0, 0, 1, p_color)
                        new_u.template = v 
                        self.ctx.player_pool.append(new_u)
                        self.ctx.setup_points += cost
                y_shop += 40

            if self.btns["start"].check(m_pos) and self.ctx.player_pool:
                self.init_ai()
                self.ctx.map_manager.load_map(self.ctx.setup_map)
                return "DEPLOYMENT"
        return None

    def init_ai(self):
        self.ctx.ai_units = []
        ai_f = "PACT" if self.ctx.setup_side == "NATO" else "NATO"
        ai_c = COLOR_AI if self.ctx.setup_side == "NATO" else COLOR_PLAYER
        pts = 0
        attempts = 0
        while pts < (self.ctx.setup_limit - 20) and attempts < 100:
            attempts += 1
            possible = [t for t in TEMPLATES[ai_f].values() if t.get_firepower() <= (self.ctx.setup_limit - pts)]
            if not possible: break
            tpl = random.choice(possible)
            u = Unit(tpl, random.randint(SCREEN_WIDTH-400, SCREEN_WIDTH-50), random.randint(100, SCREEN_HEIGHT-100), 2, ai_c)
            u.placed = True; self.ctx.ai_units.append(u); pts += tpl.get_firepower()

    def draw(self, m_pos):
        self.ctx.screen.fill(COLOR_BG)
        
        p_color = COLOR_PLAYER if self.ctx.setup_side == "NATO" else COLOR_AI
        self.ctx.screen.blit(self.ctx.font_big.render("USTAWIENIA POTYCZKI", True, COLOR_TEXT), (100, 50))
        
        # --- SEKCJA LEWA (OPCJE) ---
        # Strona
        self.ctx.screen.blit(self.ctx.font.render(f"TWOJA STRONA:", True, (200, 200, 200)), (100, 165))
        self.ctx.screen.blit(self.ctx.font.render(f"{self.ctx.setup_side}", True, p_color), (260, 165))
        
        # Mapa
        self.ctx.screen.blit(self.ctx.font.render(f"MAPA:", True, (200, 200, 200)), (100, 275))
        map_name = self.ctx.setup_map.replace('_', ' ').upper()
        self.ctx.screen.blit(self.ctx.font.render(f"{map_name}", True, COLOR_ACCENT), (170, 275))
        
        # Limit
        self.ctx.screen.blit(self.ctx.font.render(f"LIMIT PUNKTÓW:", True, (200, 200, 200)), (100, 385))
        self.ctx.screen.blit(self.ctx.font.render(f"{self.ctx.setup_limit}", True, (255, 200, 0)), (260, 385))

        for b in self.btns.values(): b.check(m_pos); b.draw(self.ctx.screen, self.ctx.font)
        
        # --- ŚRODEK (TWOJA ARMIA) ---
        self.ctx.screen.blit(self.ctx.font.render("TWOJA ARMIA:", True, COLOR_TEXT), (SCREEN_WIDTH//2 - 200, 110))
        y_list = 150
        for u in self.ctx.player_pool:
            entry_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, y_list - 5, 400, 35)
            if entry_rect.collidepoint(m_pos):
                pygame.draw.rect(self.ctx.screen, (60, 60, 70), entry_rect, border_radius=5)
                pygame.draw.rect(self.ctx.screen, (255, 50, 50), entry_rect, 1, border_radius=5)
            draw_nato_icon(self.ctx.screen, SCREEN_WIDTH//2 - 175, y_list + 12, u.color, u.u_type, False, u.rank)
            txt = self.ctx.font_small.render(u.name, True, (220, 220, 220))
            self.ctx.screen.blit(txt, (SCREEN_WIDTH//2 - 145, y_list + 3))
            y_list += 40

        # --- PRAWA (SKLEP) ---
        self.ctx.screen.blit(self.ctx.font.render("SKLEP:", True, COLOR_TEXT), (SCREEN_WIDTH-400, 110))
        y_shop = 150
        for v in TEMPLATES[self.ctx.setup_side].values():
            rect = pygame.Rect(SCREEN_WIDTH-400, y_shop, 350, 35)
            col = (60, 60, 60) if rect.collidepoint(m_pos) else (45, 45, 45)
            pygame.draw.rect(self.ctx.screen, col, rect, border_radius=5)
            self.ctx.screen.blit(self.ctx.font_small.render(f"{v.name} ({int(v.get_firepower())} pkt)", True, COLOR_TEXT), (SCREEN_WIDTH-390, y_shop+8))
            y_shop += 40
            
        # PUNKTY NA DOLE
        pts_txt = self.ctx.font_big.render(f"PUNKTY: {int(self.ctx.setup_points)} / {self.ctx.setup_limit}", True, (255, 200, 0))
        self.ctx.screen.blit(pts_txt, (SCREEN_WIDTH//2-150, SCREEN_HEIGHT-150))