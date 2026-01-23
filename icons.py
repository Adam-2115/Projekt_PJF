import pygame

def draw_nato_icon(screen, x, y, color, unit_type, selected, rank):
    bg_color = (240, 240, 240)
    w, h = 36, 28
    rect = pygame.Rect(x - w//2, y - h//2, w, h)
    
    pygame.draw.rect(screen, bg_color, rect)
    thickness = 3 if selected else 2
    pygame.draw.rect(screen, color, rect, thickness)
    
    # RYSOWANIE RANGI (Kreski na górze)
    if rank == 1: # Kompania (|)
        pygame.draw.rect(screen, color, (x - 1, rect.y - 8, 2, 6))
    elif rank == 2: # Batalion (||)
        pygame.draw.rect(screen, color, (x - 4, rect.y - 8, 2, 6))
        pygame.draw.rect(screen, color, (x + 2, rect.y - 8, 2, 6))
    
    # Symbole wewnątrz
    if unit_type in ["PIECHOTA", "ZMECHANIZOWANY"]:
        pygame.draw.line(screen, color, rect.topleft, rect.bottomright, 2)
        pygame.draw.line(screen, color, rect.topright, rect.bottomleft, 2)
    
    if unit_type in ["PANCERNY", "ZMECHANIZOWANY"]:
        inner_rect = rect.inflate(-10, -12)
        if unit_type == "ZMECHANIZOWANY":
             pygame.draw.ellipse(screen, bg_color, inner_rect)
        pygame.draw.ellipse(screen, color, inner_rect, 2)