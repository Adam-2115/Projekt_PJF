import pygame
from settings import *
from ui import Button
from mission_data import MISSIONS_DB
from unit import Unit
from templates import TEMPLATES
from icons import draw_nato_icon

class MissionsState:
    def __init__(self, ctx):
        self.ctx = ctx
        self.btns = {
            "NATO": Button("", SCREEN_WIDTH//2 - 350, SCREEN_HEIGHT//2 - 150, 300, 300),
            "PACT": Button("", SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//2 - 150, 300, 300),
            "back": Button("POWRÓT", 50, SCREEN_HEIGHT - 70, 120, 40)
        }

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btns["back"].check(m_pos): return "MENU"
            if self.btns["NATO"].check(m_pos): self.ctx.mission_faction = "NATO"; return "MISSION_SELECT"
            if self.btns["PACT"].check(m_pos): self.ctx.mission_faction = "PACT"; return "MISSION_SELECT"
        return None

    def draw(self, m_pos):
        self.ctx.screen.fill(COLOR_BG)
        title = self.ctx.font_big.render("WYBIERZ FRAKCJĘ KAMPANII", True, COLOR_TEXT)
        self.ctx.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        for key, color, txt in [("NATO", COLOR_NATO, "NATO"), ("PACT", COLOR_PACT, "PACT")]:
            is_h = self.btns[key].check(m_pos)
            pygame.draw.rect(self.ctx.screen, (20,20,20), self.btns[key].rect, border_radius=15)
            pygame.draw.rect(self.ctx.screen, color, self.btns[key].rect, 4 if is_h else 2, border_radius=15)
            t = self.ctx.font_big.render(txt, True, color)
            self.ctx.screen.blit(t, t.get_rect(center=self.btns[key].rect.center))
        self.btns["back"].check(m_pos); self.btns["back"].draw(self.ctx.screen, self.ctx.font)

class MissionSelectionState:
    def __init__(self, ctx):
        self.ctx = ctx
        self.btn_back = Button("POWRÓT", 50, SCREEN_HEIGHT - 70, 120, 40)
        self.mission_btns = [Button("", SCREEN_WIDTH//2 - 200, 200 + i*70, 400, 55) for i in range(5)]

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_back.check(m_pos): return "MISSIONS"
            for i, btn in enumerate(self.mission_btns):
                if btn.check(m_pos):
                    self.ctx.current_mission = MISSIONS_DB[self.ctx.mission_faction][i]
                    return "MISSION_BRIEFING"
        return None

    def draw(self, m_pos):
        self.ctx.screen.fill(COLOR_BG)
        f_c = COLOR_NATO if self.ctx.mission_faction == "NATO" else COLOR_PACT
        title = self.ctx.font_big.render(f"OPERACJE: {self.ctx.mission_faction}", True, f_c)
        self.ctx.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        for i, btn in enumerate(self.mission_btns):
            btn.check(m_pos); btn.text = f"{i+1}. {MISSIONS_DB[self.ctx.mission_faction][i]['title']}"
            btn.draw(self.ctx.screen, self.ctx.font)
        self.btn_back.check(m_pos); self.btn_back.draw(self.ctx.screen, self.ctx.font)

class MissionBriefingState:
    def __init__(self, ctx):
        self.ctx = ctx
        self.btn_next = Button("DO PLANOWANIA", SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 130, 300, 50)
        self.btn_cancel = Button("ANULUJ", SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 70, 300, 40)

    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_cancel.check(m_pos): return "MISSION_SELECT"
            if self.btn_next.check(m_pos):
                self.setup_mission_data()
                return "MISSION_DEPLOYMENT"
        return None

    def setup_mission_data(self):
        m = self.ctx.current_mission
        self.ctx.is_mission_mode = True
        self.ctx.map_manager.load_map(m["map"])
        p_c = COLOR_NATO if self.ctx.mission_faction == "NATO" else COLOR_PACT
        ai_c = COLOR_PACT if self.ctx.mission_faction == "NATO" else COLOR_NATO
        
        self.ctx.player_pool = [Unit(TEMPLATES[self.ctx.mission_faction][u[0]], u[1], u[2], 1, p_c) for u in m["player_units"]]
        ai_f = "PACT" if self.ctx.mission_faction == "NATO" else "NATO"
        self.ctx.ai_units = [Unit(TEMPLATES[ai_f][u[0]], u[1], u[2], 2, ai_c, is_stationary=u[3]) for u in m["ai_units"]]

    def draw(self, m_pos):
        self.ctx.screen.fill((20, 25, 30))
        m = self.ctx.current_mission
        f_c = COLOR_NATO if self.ctx.mission_faction == "NATO" else COLOR_PACT
        pygame.draw.rect(self.ctx.screen, f_c, (SCREEN_WIDTH//2-400, 100, 800, 450), 2, border_radius=10)
        t = self.ctx.font_big.render(m["title"], True, f_c)
        self.ctx.screen.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, 130))
        y = 220
        for line in [f"MAPA: {m['map'].upper()}", "", m["desc"], "", f"CEL: {m['goal']}"]:
            self.ctx.screen.blit(self.ctx.font.render(line, True, COLOR_TEXT), (SCREEN_WIDTH//2-350, y)); y += 35
        self.btn_next.check(m_pos); self.btn_next.draw(self.ctx.screen, self.ctx.font)
        self.btn_cancel.check(m_pos); self.btn_cancel.draw(self.ctx.screen, self.ctx.font)

# Zwiad przed misją plus przygotowanie do bitwy
class MissionDeploymentState:
    # Przycisk rozpoczęcia bitwy
    def __init__(self, ctx):
        self.ctx = ctx
        self.btn_battle = Button("ROZPOCZNIJ BITWĘ", SCREEN_WIDTH//2 - 150, 50, 300, 50)

    # Obsługa zdarzeń
    def handle_events(self, event, m_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.btn_battle.check(m_pos): return "BATTLE"
            if event.button == 3:
                unit_hit = None
                for u in self.ctx.player_pool:
                    r = pygame.Rect(u.pos.x-u.w/2, u.pos.y-u.h/2, u.w, u.h)
                    if r.collidepoint(m_pos): unit_hit = u; break
                if unit_hit:
                    for u in self.ctx.player_pool: u.selected = False
                    unit_hit.selected = True; self.ctx.selected_unit = unit_hit
                elif self.ctx.selected_unit:
                    self.ctx.selected_unit.target = pygame.Vector2(m_pos)
        return None

    # Rysuj ekran rozstawienia i zwiadu
    def draw(self, m_pos):
        self.ctx.map_manager.draw(self.ctx.screen)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA); overlay.fill((0,0,0,100)); self.ctx.screen.blit(overlay, (0,0))
        for au in self.ctx.ai_units: au.draw(self.ctx.screen)
        for u in self.ctx.player_pool: u.draw(self.ctx.screen)
        self.btn_battle.check(m_pos); self.btn_battle.draw(self.ctx.screen, self.ctx.font)
        instr = self.ctx.font_small.render("Wykryto pozycje wroga. Wyznacz kierunki natarcia.", True, (255, 255, 255))
        self.ctx.screen.blit(instr, (SCREEN_WIDTH//2 - instr.get_width()//2, 110))