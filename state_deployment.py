import pygame
from settings import *
from ui import Button
from icons import draw_nato_icon

class DeploymentState:
    def __init__(self, ctx):
        self.ctx = ctx
        self.btn_start = Button("ROZPOCZNIJ BITWĘ", SCREEN_WIDTH//2-100, 50, 200, 45)
        self.dragged_unit = None

    def handle_events(self, event, m_pos):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return "PAUSE"
        
        # --- LPM: PRZESUWANIE / STAWIANIE (TYLKO W STREFIE) ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_start.check(m_pos) and all(u.placed for u in self.ctx.player_pool):
                return "BATTLE"
            
            # Próba podniesienia jednostki
            for u in self.ctx.player_pool:
                r = pygame.Rect(u.pos.x-u.w/2, u.pos.y-u.h/2, u.w, u.h)
                if r.collidepoint(m_pos) and u.placed:
                    self.dragged_unit = u
                    u.placed = False
                    return None

            # Próba postawienia nowej jednostki
            if m_pos[0] <= DEPLOY_ZONE_WIDTH:
                for u in self.ctx.player_pool:
                    if not u.placed and u != self.dragged_unit:
                        u.pos = pygame.Vector2(m_pos)
                        u.target = pygame.Vector2(m_pos)
                        u.placed = True
                        break

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragged_unit:
                if m_pos[0] <= DEPLOY_ZONE_WIDTH:
                    self.dragged_unit.pos = pygame.Vector2(m_pos)
                    self.dragged_unit.placed = True
                self.dragged_unit = None

        # --- PPM: ZAZNACZANIE I ROZKAZY RUCHU (DOWOLNE MIEJSCE) ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            unit_under_mouse = None
            for u in self.ctx.player_pool:
                r = pygame.Rect(u.pos.x-u.w/2, u.pos.y-u.h/2, u.w, u.h)
                if r.collidepoint(m_pos) and u.placed:
                    unit_under_mouse = u
                    break
            
            if unit_under_mouse:
                # Zaznaczamy jednostkę do wydania rozkazu
                for other in self.ctx.player_pool: other.selected = False
                unit_under_mouse.selected = True
                self.ctx.selected_unit = unit_under_mouse
            elif self.ctx.selected_unit:
                # Jeśli jakaś jest wybrana, PPM ustawia jej cel (cel może być wszędzie)
                self.ctx.selected_unit.target = pygame.Vector2(m_pos)

        return None

    def draw(self, m_pos):
        self.ctx.map_manager.draw(self.ctx.screen)
        
        # Rysowanie strefy rozstawienia
        is_pact = self.ctx.setup_side == "PACT"
        z_c = (255, 50, 50, 40) if is_pact else (50, 100, 255, 40)
        l_c = (255, 50, 50) if is_pact else (100, 150, 255)
        zone = pygame.Surface((DEPLOY_ZONE_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        zone.fill(z_c); self.ctx.screen.blit(zone, (0, 0))
        pygame.draw.line(self.ctx.screen, l_c, (DEPLOY_ZONE_WIDTH, 0), (DEPLOY_ZONE_WIDTH, SCREEN_HEIGHT), 2)
        
        # Rysowanie jednostek i ich linii
        for u in self.ctx.player_pool: 
            if u.placed: u.draw(self.ctx.screen)
            
        # Duch jednostki pod myszką
        p_color = COLOR_PLAYER if not is_pact else COLOR_AI
        ghost = self.dragged_unit
        if not ghost:
            for u in self.ctx.player_pool:
                if not u.placed: ghost = u; break
        if ghost:
            draw_nato_icon(self.ctx.screen, m_pos[0], m_pos[1], p_color, ghost.u_type, False, ghost.rank)
            if m_pos[0] > DEPLOY_ZONE_WIDTH:
                self.ctx.screen.blit(self.ctx.font_small.render("TYLKO W STREFIE!", True, (255, 50, 50)), (m_pos[0]-40, m_pos[1]-35))
            
        self.btn_start.check(m_pos); self.btn_start.draw(self.ctx.screen, self.ctx.font)