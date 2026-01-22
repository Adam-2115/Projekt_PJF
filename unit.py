import pygame
from settings import FPS, COMBAT_RANGE
from icons import draw_nato_icon # Importujemy nasz nowy plik

class Unit:
    def __init__(self, template, x, y, side):
        self.name = template.name
        self.side = side # 1-NATO, 2-PACT
        self.pos = pygame.Vector2(x, y)
        self.target = pygame.Vector2(x, y)
        
        # Statystyki z szablonu
        self.tanks = float(template.tanks)
        self.apc = float(template.apc)
        self.soldiers = float(template.soldiers)
        self.tank_power = template.tank_power
        self.apc_power = template.apc_power
        self.inf_power = template.inf_power
        self.speed = template.speed
        
        # Typ jednostki do ikony (wyciągamy z nazwy lub statystyk)
        if self.tanks > 0 and self.apc > 0: self.u_type = "ZMECHANIZOWANY"
        elif self.tanks > 0: self.u_type = "PANCERNY"
        else: self.u_type = "PIECHOTA"

        self.max_hp = self.soldiers + (self.apc * 5) + (self.tanks * 10) + 1
        self.selected = False
        self.in_combat = False
        self.w, self.h = 36, 28 # Wymiary ikony

    def is_alive(self):
        return self.soldiers > 0 or self.tanks > 0 or self.apc > 0

    def update(self, enemies):
        self.in_combat = False
        for e in enemies:
            if self.pos.distance_to(e.pos) < COMBAT_RANGE:
                self.in_combat = True
                self.fight(e)
                break
        if not self.in_combat and self.pos.distance_to(self.target) > 5:
            dir_vec = (self.target - self.pos).normalize()
            self.pos += dir_vec * self.speed

    def fight(self, enemy):
        dmg = (self.tanks * self.tank_power + self.apc * self.apc_power + self.soldiers * self.inf_power) / FPS
        if enemy.tanks > 0:
            enemy.tanks = max(0, enemy.tanks - (dmg * 0.05))
            enemy.soldiers = max(0, enemy.soldiers - (dmg * 0.2))
        elif enemy.apc > 0:
            enemy.apc = max(0, enemy.apc - (dmg * 0.15))
            enemy.soldiers = max(0, enemy.soldiers - (dmg * 0.4))
        else:
            enemy.soldiers = max(0, enemy.soldiers - dmg)

    def draw(self, screen):
        # 1. Rysujemy ikonę NATO z zewnętrznego pliku
        draw_nato_icon(screen, self.pos.x, self.pos.y, self.side, self.u_type, self.selected)
        
        # 2. Pasek życia (pod ikoną)
        current_hp = self.soldiers + (self.apc * 5) + (self.tanks * 10)
        hp_pct = current_hp / self.max_hp
        bar_y = self.pos.y + self.h//2 + 4
        pygame.draw.rect(screen, (0,0,0), (self.pos.x - self.w//2, bar_y, self.w, 4))
        pygame.draw.rect(screen, (0,255,0), (self.pos.x - self.w//2, bar_y, self.w * max(0, hp_pct), 4))
        
        # 3. Linia do celu
        if self.selected and self.pos.distance_to(self.target) > 10:
            pygame.draw.line(screen, (255, 255, 255), self.pos, self.target, 1)