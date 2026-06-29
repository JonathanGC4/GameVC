# =============================================================================
# utils.py — Iteración 4: se añade draw_hearts()
# =============================================================================

import pygame
from settings import COLOR_TEXT, COLOR_HEART_FULL, COLOR_HEART_EMPTY


def draw_text(surface, text, size, x, y, color=COLOR_TEXT, anchor="topleft"):
    """Dibuja texto en una superficie. anchor puede ser 'topleft', 'center', etc."""
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    setattr(text_rect, anchor, (x, y))
    surface.blit(text_surface, text_rect)
    return text_rect


def clamp(value, minimum, maximum):
    """Restringe value al intervalo [minimum, maximum]."""
    return max(minimum, min(value, maximum))


def draw_hearts(surface, current_lives, max_lives, x, y, size=18, gap=6):
    """
    Dibuja una fila de corazones que representan las vidas del jugador.

    Los corazones llenos muestran las vidas restantes; los vacíos, las perdidas.
    Cada corazón es un rombo (rotación de un cuadrado 45°) para distinguirlo
    visualmente del cuadrado del jugador y los enemigos.

    Parámetros
    ----------
    surface      : pygame.Surface — donde se dibuja
    current_lives: int  — vidas actuales
    max_lives    : int  — vidas máximas (total de corazones a dibujar)
    x, y         : int  — esquina superior izquierda del primer corazón
    size         : int  — mitad del lado del rombo en píxeles
    gap          : int  — separación entre corazones
    """
    for i in range(max_lives):
        cx = x + i * (size * 2 + gap) + size   # Centro X del corazón i
        cy = y + size                            # Centro Y

        # Un rombo son 4 puntos: arriba, derecha, abajo, izquierda
        points = [
            (cx,        cy - size),   # Arriba
            (cx + size, cy),          # Derecha
            (cx,        cy + size),   # Abajo
            (cx - size, cy),          # Izquierda
        ]

        color = COLOR_HEART_FULL if i < current_lives else COLOR_HEART_EMPTY
        pygame.draw.polygon(surface, color, points)

        # Borde más oscuro para darle profundidad
        border_color = (255, 100, 130) if i < current_lives else (60, 20, 30)
        pygame.draw.polygon(surface, border_color, points, width=2)