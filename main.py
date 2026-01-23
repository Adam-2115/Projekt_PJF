import pygame
import sys
from settings import *
from game_context import GameContext
from state_menu import MenuState
from state_setup import SetupState
from state_deployment import DeploymentState
from state_battle import BattleState
from state_utils import TemplatesState, SimpleMsgState, ExitPromptState, PauseState, GameOverState
from state_missions import MissionsState, MissionSelectionState, MissionBriefingState, MissionDeploymentState

class GeneralEngine:
    # Inicjalizacja gry
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        self.ctx = GameContext(self.screen)
        
        self.states = {
            "MENU": MenuState(self.ctx),
            "SKIRMISH_SETUP": SetupState(self.ctx),
            "DEPLOYMENT": DeploymentState(self.ctx),
            "BATTLE": BattleState(self.ctx),
            "TEMPLATES": TemplatesState(self.ctx),
            "MISSIONS": MissionsState(self.ctx),
            "MISSION_SELECT": MissionSelectionState(self.ctx),
            "MISSION_BRIEFING": MissionBriefingState(self.ctx),
            "MISSION_DEPLOYMENT": MissionDeploymentState(self.ctx),
            "MULTI_MSG": SimpleMsgState(self.ctx, "MULTIPLAYER OBECNIE NIEDOSTĘPNY"),
            "EXIT_PROMPT": ExitPromptState(self.ctx)
        }
        self.current_state = self.states["MENU"]
        self.prev_state_key = "MENU"

    # Główna pętla gry
    def run(self):
        while True:
            m_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                
                res = self.current_state.handle_events(event, m_pos)
                if res:
                    if res == "MENU": 
                        self.ctx.reset_skirmish()
                    
                    if res == "PAUSE":
                        self.prev_state_key = "BATTLE" if self.current_state == self.states["BATTLE"] else "DEPLOYMENT"
                        self.states["PAUSE"] = PauseState(self.ctx, self.prev_state_key)
                        self.current_state = self.states["PAUSE"]
                    elif res == "EXIT_FROM_MENU":
                        self.states["EXIT_PROMPT"] = ExitPromptState(self.ctx, "MENU")
                        self.current_state = self.states["EXIT_PROMPT"]
                    elif res == "EXIT_PROMPT":
                        prev = self.prev_state_key if isinstance(self.current_state, PauseState) else "MENU"
                        self.states["EXIT_PROMPT"] = ExitPromptState(self.ctx, prev)
                        self.current_state = self.states["EXIT_PROMPT"]
                    elif res in self.states:
                        self.current_state = self.states[res]

            if self.current_state == self.states["BATTLE"]:
                outcome = self.current_state.update()
                if outcome:
                    self.states["GAMEOVER"] = GameOverState(self.ctx, outcome == "VICTORY")
                    self.current_state = self.states["GAMEOVER"]

            self.screen.fill((0, 0, 0))
            
            # Pobieranie stanów specjalnych
            p_s = self.states.get("PAUSE")
            g_s = self.states.get("GAMEOVER")
            e_s = self.states.get("EXIT_PROMPT")
            
            if self.current_state in [p_s, g_s]:
                # Rysuj tło zależnie od tego gdzie byliśmy
                if self.prev_state_key == "BATTLE" or self.current_state == g_s:
                    self.states["BATTLE"].draw(m_pos)
                else:
                    self.states.get("DEPLOYMENT", self.states["MENU"]).draw(m_pos)
                self.current_state.draw(m_pos)
            
            elif self.current_state == e_s:
                # Jeśli wychodzimy z MENU, rysuj MENU pod spodem
                if e_s.prev_state == "MENU":
                    self.states["MENU"].draw(m_pos)
                self.current_state.draw(m_pos)
            
            else:
                self.current_state.draw(m_pos)
            
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    GeneralEngine().run()