import pygame
import sys
from settings import *
from templates import TEMPLATES
from unit import Unit
from ui import Button

class GeneralManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        pygame.display.set_caption("General Strategic Mode")
        
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_big = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16)
        
        self.clock = pygame.time.Clock()
        self.state = "MENU"
        
        bx, bw, bh = SCREEN_WIDTH//2 - 100, 200, 50
        self.menu_btns = {
            "misje": Button("MISJE", bx, SCREEN_HEIGHT//2 - 170, bw, bh),
            "potyczka": Button("POTYCZKA", bx, SCREEN_HEIGHT//2 - 100, bw, bh),
            "multi": Button("MULTIPLAYER", bx, SCREEN_HEIGHT//2 - 30, bw, bh),
            "templates": Button("SZABLONY", bx, SCREEN_HEIGHT//2 + 40, bw, bh),
            "wyjscie": Button("WYJŚCIE", bx, SCREEN_HEIGHT//2 + 110, bw, bh)
        }
        
        self.pause_btns = {
            "continue": Button("KONTYNUUJ", bx, SCREEN_HEIGHT//2 - 100, bw, bh),
            "to_menu": Button("MENU GŁÓWNE", bx, SCREEN_HEIGHT//2 - 30, bw, bh),
            "quit": Button("WYJDŹ Z GRY", bx, SCREEN_HEIGHT//2 + 40, bw, bh)
        }

        self.back_btn = Button("POWRÓT", 50, SCREEN_HEIGHT - 70, 120, 40)
        self.exit_yes = Button("TAK", SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2 + 50, 100, 50)
        self.exit_no = Button("NIE", SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT//2 + 50, 100, 50)

        self.units = []
        self.selected_unit = None
        self.previous_state = "BATTLE"
        
        try:
            self.map_img = pygame.image.load("mapa.png").convert()
            self.map_img = pygame.transform.scale(self.map_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.map_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.map_img.fill((40, 70, 40))

    def start_skirmish(self):
        # Inicjalizacja z nowymi kluczami NATO/PACT
        self.units = [
            Unit(TEMPLATES["NATO"]["PANCERNY"], 200, SCREEN_HEIGHT//2, 1),
            Unit(TEMPLATES["PACT"]["PANCERNY"], SCREEN_WIDTH - 200, SCREEN_HEIGHT//2, 2)
        ]
        self.state = "BATTLE"

    def handle_clicks(self, event, m_pos):
        if self.state == "MENU":
            if self.menu_btns["misje"].check(m_pos): self.state = "MISSIONS"
            if self.menu_btns["potyczka"].check(m_pos): self.start_skirmish()
            if self.menu_btns["templates"].check(m_pos): self.state = "TEMPLATES"
            if self.menu_btns["multi"].check(m_pos): self.state = "MULTI_MSG"
            if self.menu_btns["wyjscie"].check(m_pos): self.state = "EXIT_PROMPT"
        
        elif self.state in ["TEMPLATES", "MULTI_MSG", "MISSIONS"]:
            if self.back_btn.check(m_pos): self.state = "MENU"
            
        elif self.state == "PAUSE":
            if self.pause_btns["continue"].check(m_pos): self.state = self.previous_state
            if self.pause_btns["to_menu"].check(m_pos): self.state = "MENU"
            if self.pause_btns["quit"].check(m_pos): self.state = "EXIT_PROMPT"

        elif self.state == "EXIT_PROMPT":
            if self.exit_yes.check(m_pos): pygame.quit(); sys.exit()
            if self.exit_no.check(m_pos): self.state = "MENU"

        elif self.state == "BATTLE":
            if event.button == 1: # LPM - Wybór
                self.selected_unit = None
                for u in self.units:
                    u.selected = False
                    # POPRAWIONE: używamy u.w i u.h zamiast u.size
                    r = pygame.Rect(u.pos.x - u.w/2, u.pos.y - u.h/2, u.w, u.h)
                    if r.collidepoint(m_pos) and u.side == 1:
                        u.selected = True; self.selected_unit = u
            if event.button == 3 and self.selected_unit: # PPM - Ruch
                self.selected_unit.target = pygame.Vector2(m_pos)

    def run(self):
        while True:
            m_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: self.state = "EXIT_PROMPT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state in ["BATTLE", "MISSIONS"]:
                            self.previous_state = self.state
                            self.state = "PAUSE"
                        elif self.state == "PAUSE": self.state = self.previous_state
                        elif self.state == "MENU": self.state = "EXIT_PROMPT"
                        else: self.state = "MENU"
                if event.type == pygame.MOUSEBUTTONDOWN: self.handle_clicks(event, m_pos)

            if self.state == "MENU": self.draw_menu(m_pos)
            elif self.state == "TEMPLATES": self.draw_templates(m_pos)
            elif self.state == "MISSIONS": self.draw_missions(m_pos)
            elif self.state == "MULTI_MSG": self.draw_multi_msg(m_pos)
            elif self.state == "EXIT_PROMPT": self.draw_exit_prompt(m_pos)
            elif self.state == "BATTLE":
                self.update_battle()
                self.draw_battle(m_pos)
            elif self.state == "PAUSE":
                self.draw_battle(m_pos)
                self.draw_pause(m_pos)

            pygame.display.flip()
            self.clock.tick(FPS)

    def update_battle(self):
        p_units = [u for u in self.units if u.side == 1]
        a_units = [u for u in self.units if u.side == 2]
        for u in self.units:
            enemies = a_units if u.side == 1 else p_units
            u.update(enemies)
        for au in a_units:
            if not au.in_combat and p_units: au.target = p_units[0].pos
        self.units = [u for u in self.units if u.is_alive()]

    def draw_menu(self, m_pos):
        self.screen.fill(COLOR_BG)
        title = self.font_big.render("TRYB GENERALSKI", True, COLOR_ACCENT)
        self.screen.blit(title, (SCREEN_WIDTH//2-title.get_width()//2, 100))
        for b in self.menu_btns.values(): b.check(m_pos); b.draw(self.screen, self.font)

    def draw_pause(self, m_pos):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        pygame.draw.rect(self.screen, COLOR_BG, (SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2-150, 300, 350), border_radius=10)
        pygame.draw.rect(self.screen, COLOR_TEXT, (SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2-150, 300, 350), 2, border_radius=10)
        title = self.font_big.render("PAUZA", True, COLOR_TEXT)
        self.screen.blit(title, (SCREEN_WIDTH//2-title.get_width()//2, SCREEN_HEIGHT//2-220))
        for b in self.pause_btns.values(): b.check(m_pos); b.draw(self.screen, self.font)

    def draw_exit_prompt(self, m_pos):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        self.screen.blit(overlay, (0,0))
        pygame.draw.rect(self.screen, (20,20,20), (SCREEN_WIDTH//2-250, SCREEN_HEIGHT//2-100, 500, 250), border_radius=15)
        txt = self.font.render("CZY NA PEWNO CHCESZ WYJŚĆ?", True, COLOR_TEXT)
        self.screen.blit(txt, (SCREEN_WIDTH//2-txt.get_width()//2, SCREEN_HEIGHT//2-40))
        self.exit_yes.check(m_pos); self.exit_yes.draw(self.screen, self.font)
        self.exit_no.check(m_pos); self.exit_no.draw(self.screen, self.font)

    def draw_battle(self, m_pos):
        self.screen.blit(self.map_img, (0, 0))
        for u in self.units:
            u.draw(self.screen)
            # POPRAWIONE: używamy u.w i u.h zamiast u.size
            r = pygame.Rect(u.pos.x - u.w/2, u.pos.y - u.h/2, u.w, u.h)
            if r.collidepoint(m_pos) and self.state != "PAUSE":
                fire = round(u.tanks*u.tank_power + u.apc*u.apc_power + u.soldiers*u.inf_power, 1)
                txt = self.font_small.render(f"{u.name} | Czołgi: {int(u.tanks)} | APC: {int(u.apc)} | Siła: {fire}", True, (255,255,255))
                pygame.draw.rect(self.screen, (0,0,0,180), (m_pos[0]+10, m_pos[1], txt.get_width()+10, 25))
                self.screen.blit(txt, (m_pos[0]+15, m_pos[1]+5))

    def draw_templates(self, m_pos):
        self.screen.fill(COLOR_BG)
        y = 50
        for faction, units in TEMPLATES.items():
            header_color = (50, 100, 255) if faction == "NATO" else (255, 50, 50)
            txt = self.font_big.render(f"--- {faction} ---", True, header_color)
            self.screen.blit(txt, (SCREEN_WIDTH//2-txt.get_width()//2, y))
            y += 70
            for t in units.values():
                pygame.draw.rect(self.screen, COLOR_BTN, (SCREEN_WIDTH//2-400, y, 800, 60), border_radius=5)
                info = self.font.render(f"{t.name} | Czołgi: {t.tanks} | APC: {t.apc} | Ludzie: {t.soldiers}", True, COLOR_TEXT)
                self.screen.blit(info, (SCREEN_WIDTH//2-380, y+15))
                y += 70
            y += 30
        self.back_btn.check(m_pos); self.back_btn.draw(self.screen, self.font)

    def draw_missions(self, m_pos):
        self.screen.fill(COLOR_BG)
        txt = self.font_big.render("KAMPANIA", True, COLOR_ACCENT)
        self.screen.blit(txt, (SCREEN_WIDTH//2-txt.get_width()//2, 200))
        self.back_btn.check(m_pos); self.back_btn.draw(self.screen, self.font)

    def draw_multi_msg(self, m_pos):
        self.screen.fill(COLOR_BG)
        txt = self.font.render("MULTIPLAYER NIEDOSTĘPNY", True, (255, 200, 0))
        self.screen.blit(txt, (SCREEN_WIDTH//2-txt.get_width()//2, SCREEN_HEIGHT//2))
        self.back_btn.check(m_pos); self.back_btn.draw(self.screen, self.font)

if __name__ == "__main__":
    GeneralManager().run()