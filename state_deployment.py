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
        
        # Stawianie jednostek i ich przesuwanie
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_start.check(m_pos):
                # Pozwól zacząć tylko jeśli wszystko rozstawione
                if all(u.placed for u in self.ctx.player_pool):
                    return "BATTLE"
            
            # Sprawdź czy klikam w już postawioną jednostkę
            for u in self.ctx.player_pool:
                if u.placed:
                    r = pygame.Rect(u.pos.x-u.w/2, u.pos.y-u.h/2, u.w, u.h)
                    if r.collidepoint(m_pos):
                        self.dragged_unit = u
                        u.placed = False # Zdejmij z mapy
                        return None

            # Jeśli nie podnosimy, to stawiamy nową jednostkę
            if m_pos[0] <= DEPLOY_ZONE_WIDTH:
                # Znajdź pierwszą wolną jednostkę
                unit_to_place = self.dragged_unit
                if not unit_to_place:
                    for u in self.ctx.player_pool:
                        if not u.placed:
                            unit_to_place = u
                            break
                
                if unit_to_place:
                    unit_to_place.pos = pygame.Vector2(m_pos)
                    unit_to_place.target = pygame.Vector2(m_pos)
                    unit_to_place.placed = True
                    self.dragged_unit = None # Puść jeśli coś trzymaliśmy

        # Upuszczenie jednostki
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragged_unit:
                if m_pos[0] <= DEPLOY_ZONE_WIDTH:
                    self.dragged_unit.pos = pygame.Vector2(m_pos)
                    self.dragged_unit.placed = True
                self.dragged_unit = None

        # Wydanwanie rozkazów 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            unit_under_mouse = None
            for u in self.ctx.player_pool:
                if u.placed:
                    r = pygame.Rect(u.pos.x-u.w/2, u.pos.y-u.h/2, u.w, u.h)
                    if r.collidepoint(m_pos):
                        unit_under_mouse = u; break
            
            if unit_under_mouse:
                for other in self.ctx.player_pool: other.selected = False
                unit_under_mouse.selected = True
                self.ctx.selected_unit = unit_under_mouse
            elif self.ctx.selected_unit:
                self.ctx.selected_unit.target = pygame.Vector2(m_pos)

        return None

    def draw(self, m_pos):
        self.ctx.map_manager.draw(self.ctx.screen)
        
        # Strefa
        is_pact = self.ctx.setup_side == "PACT"
        z_c = COLOR_ZONE_PACT if is_pact else COLOR_ZONE_NATO
        l_c = (255, 50, 50) if is_pact else (100, 150, 255)
        
        zone = pygame.Surface((DEPLOY_ZONE_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        zone.fill(z_c)
        self.ctx.screen.blit(zone, (0, 0))
        pygame.draw.line(self.ctx.screen, l_c, (DEPLOY_ZONE_WIDTH, 0), (DEPLOY_ZONE_WIDTH, SCREEN_HEIGHT), 2)
        
        # Rysuj postawione jednostki
        for u in self.ctx.player_pool: 
            if u.placed: u.draw(self.ctx.screen)
            
        # Rysuj ducha (jednostkę na kursorze)
        ghost = self.dragged_unit
        if not ghost:
            # Jeśli nic nie trzymamy, pokaż następną w kolejce
            for u in self.ctx.player_pool:
                if not u.placed:
                    ghost = u
                    break
        
        if ghost:
            p_color = COLOR_NATO if not is_pact else COLOR_PACT
            draw_nato_icon(self.ctx.screen, m_pos[0], m_pos[1], p_color, ghost.u_type, False, ghost.rank)
            
            # Podpowiedź, że nie można stawiać poza strefą
            if m_pos[0] > DEPLOY_ZONE_WIDTH:
                txt = self.ctx.font_small.render("STREFA!", True, (255, 50, 50))
                self.ctx.screen.blit(txt, (m_pos[0]-20, m_pos[1]-40))
            else:
                txt = self.ctx.font_small.render(ghost.name, True, (255, 255, 255))
                self.ctx.screen.blit(txt, (m_pos[0]+20, m_pos[1]))

        self.btn_start.check(m_pos)
        self.btn_start.draw(self.ctx.screen, self.ctx.font)