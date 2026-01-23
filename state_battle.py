import pygame
from settings import *

class BattleState:
    def __init__(self, ctx):
        self.ctx = ctx

    def handle_events(self, event, m_pos):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "PAUSE"
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.ctx.selected_unit = None
                for u in self.ctx.player_pool:
                    u.selected = False
                    r = pygame.Rect(u.pos.x - u.w/2, u.pos.y - u.h/2, u.w, u.h)
                    if r.collidepoint(m_pos):
                        u.selected = True
                        self.ctx.selected_unit = u
            
            if event.button == 3 and self.ctx.selected_unit:
                self.ctx.selected_unit.target = pygame.Vector2(m_pos)
        return None

    def update(self):
        for au in self.ctx.ai_units:
            if not au.is_stationary and not au.in_combat and self.ctx.player_pool:
                nearest = min(self.ctx.player_pool, key=lambda p: au.pos.distance_to(p.pos))
                au.target = pygame.Vector2(nearest.pos)
        
        for u in self.ctx.player_pool:
            u.update(self.ctx.ai_units, self.ctx.player_pool)
        for u in self.ctx.ai_units:
            u.update(self.ctx.player_pool, self.ctx.ai_units)

        # Usuwanie zniszczonych
        self.ctx.player_pool = [u for u in self.ctx.player_pool if u.is_alive()]
        self.ctx.ai_units = [u for u in self.ctx.ai_units if u.is_alive()]
        
        if not self.ctx.ai_units: return "VICTORY"
        if not self.ctx.player_pool: return "DEFEAT"
        return None

    def draw(self, m_pos):
        self.ctx.map_manager.draw(self.ctx.screen)
        all_units = self.ctx.player_pool + self.ctx.ai_units
        for u in all_units:
            u.draw(self.ctx.screen)
        for u in all_units:
            r = pygame.Rect(u.pos.x - u.w/2, u.pos.y - u.h/2, u.w, u.h)
            if r.collidepoint(m_pos):
                fire = round(u.tanks*u.tank_power + u.apc*u.apc_power + u.soldiers*u.inf_power, 1)
                txts = [
                    self.ctx.font_small.render(f"{u.name}", True, (255, 255, 255)),
                    self.ctx.font_small.render(f"Siła ognia: {fire}", True, (255, 200, 50)),
                    self.ctx.font_small.render(f"Czołgi: {int(u.tanks)} | APC: {int(u.apc)} | Ludzie: {int(u.soldiers)}", True, (200, 255, 200))
                ]
                max_w = max(t.get_width() for t in txts) + 20
                tooltip_rect = pygame.Rect(m_pos[0] + 15, m_pos[1] + 15, max_w, 65)
                
                bg = pygame.Surface((tooltip_rect.w, tooltip_rect.h))
                bg.set_alpha(200)
                bg.fill((10, 10, 10))
                self.ctx.screen.blit(bg, (tooltip_rect.x, tooltip_rect.y))
                pygame.draw.rect(self.ctx.screen, (200, 200, 200), tooltip_rect, 1)
                
                for i, t in enumerate(txts):
                    self.ctx.screen.blit(t, (tooltip_rect.x + 10, tooltip_rect.y + 5 + i*18))