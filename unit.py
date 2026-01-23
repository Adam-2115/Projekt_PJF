import pygame
from settings import FPS, COMBAT_RANGE, AUTO_ENGAGE_RANGE
from icons import draw_nato_icon

class Unit:
    def __init__(self, template, x, y, side, color):
        self.name = template.name
        self.side = side # 1-Gracz, 2-AI
        self.color = color
        self.rank = template.rank
        self.pos = pygame.Vector2(x, y)
        self.target = pygame.Vector2(x, y)
        
        self.tanks = float(template.tanks)
        self.apc = float(template.apc)
        self.soldiers = float(template.soldiers)
        self.tank_power = template.tank_power
        self.apc_power = template.apc_power
        self.inf_power = template.inf_power
        self.speed = template.speed
        
        if self.tanks > 0 and self.apc > 0: self.u_type = "ZMECHANIZOWANY"
        elif self.tanks > 0: self.u_type = "PANCERNY"
        else: self.u_type = "PIECHOTA"

        self.max_hp = self.soldiers + (self.apc * 5) + (self.tanks * 10) + 1
        self.selected = False
        self.in_combat = False
        self.placed = False 
        self.w, self.h = 36, 28

    def is_alive(self):
        return self.soldiers > 0 or self.tanks > 0 or self.apc > 0

    def update(self, enemies):
        self.in_combat = False
        # 1. Walka
        for e in enemies:
            if self.pos.distance_to(e.pos) < COMBAT_RANGE:
                self.in_combat = True
                self.fight(e)
                break
        
        # 2. Ruch i Auto-Engage
        if not self.in_combat:
            if self.side == 1 and self.pos.distance_to(self.target) < 15:
                nearest = None
                min_d = AUTO_ENGAGE_RANGE
                for e in enemies:
                    d = self.pos.distance_to(e.pos)
                    if d < min_d: min_d = d; nearest = e
                if nearest: self.target = pygame.Vector2(nearest.pos)

            if self.pos.distance_to(self.target) > 5:
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
        # Rysuj linię rozkazu TYLKO dla gracza (może wychodzić poza strefę)
        if self.side == 1 and self.pos.distance_to(self.target) > 15:
            l_color = (255, 255, 255) if self.selected else (150, 150, 150)
            pygame.draw.line(screen, l_color, self.pos, self.target, 2)
            pygame.draw.circle(screen, l_color, (int(self.target.x), int(self.target.y)), 4)

        draw_nato_icon(screen, self.pos.x, self.pos.y, self.color, self.u_type, self.selected, self.rank)
        
        hp_pct = (self.soldiers + self.apc*5 + self.tanks*10) / self.max_hp
        bar_y = self.pos.y + self.h//2 + 4
        pygame.draw.rect(screen, (0,0,0), (self.pos.x - self.w//2, bar_y, self.w, 4))
        pygame.draw.rect(screen, (0,255,0), (self.pos.x - self.w//2, bar_y, self.w * max(0, hp_pct), 4))