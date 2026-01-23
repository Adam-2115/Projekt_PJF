import pygame
from settings import FPS, COMBAT_RANGE, AUTO_ENGAGE_RANGE
from icons import draw_nato_icon

class Unit:
    def __init__(self, template, x, y, side, color, is_stationary=False):
        self.template = template
        self.name = template.name
        self.side = side 
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
        
        if "Pancerny" in self.name or "Pancerna" in self.name:
            self.u_type = "PANCERNY"
        elif "Zmechanizowany" in self.name or "Zmechanizowana" in self.name:
            self.u_type = "ZMECHANIZOWANY"
        else:
            self.u_type = "PIECHOTA"

        self.max_hp = self.soldiers + (self.apc * 5) + (self.tanks * 10) + 1
        self.is_stationary = is_stationary
        self.selected = False
        self.in_combat = False
        self.placed = True 
        self.w, self.h = 36, 28
        # Lista wrogów, z którymi walczę w tej klatce
        self.current_targets = []

    def is_alive(self):
        return self.soldiers > 0 or self.tanks > 0 or self.apc > 0

    def update(self, enemies, allies):
        self.in_combat = False
        self.current_targets = []
        
        # Walka
        for e in enemies:
            if self.pos.distance_to(e.pos) < COMBAT_RANGE:
                self.in_combat = True
                self.current_targets.append(e)
                # Przekazujemy listę sojuszników, aby obliczyć bonus za przewagę
                self.fight(e, allies)
        
        # Ruch
        if not self.in_combat and not self.is_stationary:
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

    def fight(self, enemy, allies):
        # Obliczamy ilu sojuszników też atakuje TEGO SAMEGO wroga
        # Zaczynamy od 1 (my sami)
        attackers_count = 1
        for ally in allies:
            if ally != self and ally.is_alive():
                # Jeśli sojusznik jest blisko wroga, uznajemy że pomaga
                if ally.pos.distance_to(enemy.pos) < COMBAT_RANGE:
                    attackers_count += 1
        
        # Bonus za przewagę liczebną, mnożnik od 1.0 do maksymalnie 2.0, 0.1 za każdego dodatkowego sojusznika
        multiplier = 1.0 + (0.1 * (attackers_count - 1))
        if multiplier > 2.0: multiplier = 2.0

        # Obrażenia bazowe
        base_dmg = (self.tanks * self.tank_power + self.apc * self.apc_power + self.soldiers * self.inf_power) / FPS
        
        # Finalne obrażenia
        final_dmg = base_dmg * multiplier
        
        # Aplikacja obrażeń
        if enemy.tanks > 0:
            enemy.tanks = max(0, enemy.tanks - (final_dmg * 0.05))
            enemy.soldiers = max(0, enemy.soldiers - (final_dmg * 0.2))
        elif enemy.apc > 0:
            enemy.apc = max(0, enemy.apc - (final_dmg * 0.15))
            enemy.soldiers = max(0, enemy.soldiers - (final_dmg * 0.4))
        else:
            enemy.soldiers = max(0, enemy.soldiers - final_dmg)

    def draw(self, screen):
        if self.side == 1 and self.pos.distance_to(self.target) > 15:
            l_color = (255, 255, 255) if self.selected else (150, 150, 150)
            pygame.draw.line(screen, l_color, self.pos, self.target, 2)
            pygame.draw.circle(screen, l_color, (int(self.target.x), int(self.target.y)), 4)

        draw_nato_icon(screen, self.pos.x, self.pos.y, self.color, self.u_type, self.selected, self.rank)
        
        hp_pct = (self.soldiers + self.apc*5 + self.tanks*10) / self.max_hp
        bar_y = self.pos.y + self.h//2 + 4
        pygame.draw.rect(screen, (0,0,0), (self.pos.x - self.w//2, bar_y, self.w, 4))
        pygame.draw.rect(screen, (0,255,0), (self.pos.x - self.w//2, bar_y, self.w * max(0, hp_pct), 4))