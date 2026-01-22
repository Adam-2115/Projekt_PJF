import pygame

def draw_nato_icon(screen, x, y, side, unit_type, selected):
    """
    Rysuje profesjonalną ikonę NATO APP-6.
    side: 1 (NATO/Niebieski), 2 (PACT/Czerwony)
    unit_type: 'PANCERNY', 'PIECHOTA', 'ZMECHANIZOWANY'
    """
    # Kolory
    color = (50, 100, 255) if side == 1 else (255, 50, 50)
    bg_color = (240, 240, 240) # Jasne wypełnienie środka
    
    # Wymiary ikony
    w, h = 36, 28
    rect = pygame.Rect(x - w//2, y - h//2, w, h)
    
    # 1. Tło ikony
    pygame.draw.rect(screen, bg_color, rect)
    
    # 2. Ramka zewnętrzna
    border_thickness = 3 if selected else 2
    pygame.draw.rect(screen, color, rect, border_thickness)
    
    # 3. Szczebel jednostki: || (Batalion)
    # Rysujemy dwie pionowe kreski nad ramką
    pygame.draw.rect(screen, color, (x - 3, rect.y - 8, 2, 6))
    pygame.draw.rect(screen, color, (x + 2, rect.y - 8, 2, 6))
    
    # 4. Symbol wewnątrz (Zależnie od typu)
    # Piechota (X)
    if unit_type in ["PIECHOTA", "ZMECHANIZOWANY"]:
        pygame.draw.line(screen, color, rect.topleft, rect.bottomright, 2)
        pygame.draw.line(screen, color, rect.topright, rect.bottomleft, 2)
    
    # Pancerny (Elipsa)
    if unit_type in ["PANCERNY", "ZMECHANIZOWANY"]:
        # Elipsa symbolizująca gąsienicę czołgu
        inner_rect = rect.inflate(-10, -12)
        # Jeśli to zmechanizowana, wypełniamy elipsę tłem, żeby nie zlewała się z X
        if unit_type == "ZMECHANIZOWANY":
             pygame.draw.ellipse(screen, bg_color, inner_rect)
        pygame.draw.ellipse(screen, color, inner_rect, 2)