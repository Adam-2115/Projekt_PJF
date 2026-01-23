import pygame

def draw_nato_icon(screen, x, y, color, unit_type, selected, rank):
    # Piechota: tylko X
    # Pancerny: tylko elipsa
    # Zmechanizowany: X + elipsa
    bg_color = (240, 240, 240)
    w, h = 36, 28
    rect = pygame.Rect(x - w//2, y - h//2, w, h)
    
    # Tło ikony
    pygame.draw.rect(screen, bg_color, rect)
    
    # Ramka zewnętrzna
    thickness = 3 if selected else 2
    pygame.draw.rect(screen, color, rect, thickness)
    
    # Szczebel batalionu/kompanii
    if rank == 1: # Kompania (|)
        pygame.draw.rect(screen, color, (x - 1, rect.y - 8, 2, 6))
    elif rank == 2: # Batalion (||)
        pygame.draw.rect(screen, color, (x - 4, rect.y - 8, 2, 6))
        pygame.draw.rect(screen, color, (x + 2, rect.y - 8, 2, 6))
    
    # Rysuj X 
    if unit_type in ["PIECHOTA", "ZMECHANIZOWANY"]:
        pygame.draw.line(screen, color, rect.topleft, rect.bottomright, 2)
        pygame.draw.line(screen, color, rect.topright, rect.bottomleft, 2)
    
    # Rysuj Elipsę 
    if unit_type in ["PANCERNY", "ZMECHANIZOWANY"]:
        inner_rect = rect.inflate(-10, -12)
        # Jeśli to zmech, czyścimy tło pod elipsą, żeby X nie przechodził przez środek
        if unit_type == "ZMECHANIZOWANY":
             pygame.draw.ellipse(screen, bg_color, inner_rect)
        pygame.draw.ellipse(screen, color, inner_rect, 2)