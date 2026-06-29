# =============================================================================
# utils.py — Funciones auxiliares reutilizables
# =============================================================================
# Aquí viven funciones que no pertenecen a ninguna clase pero que varios
# módulos comparten.  Mantenerlas aquí evita duplicación y facilita tests.
# =============================================================================

import pygame
from settings import COLOR_TEXT, COLOR_HEART_FULL, COLOR_HEART_EMPTY


def draw_text(surface, text, size, x, y, color=COLOR_TEXT, anchor="topleft"):
    """
    Renderiza texto en una superficie de Pygame.

    Parámetros
    ----------
    surface : pygame.Surface
    text    : str   — cadena a mostrar
    size    : int   — tamaño de fuente en puntos
    x, y    : int   — coordenadas según `anchor`
    color   : tuple — RGB
    anchor  : str   — atributo de Rect: "topleft", "center", "topright"…

    Retorna el Rect ocupado por el texto (útil para calcular espaciado).
    """
    font         = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect    = text_surface.get_rect()
    setattr(text_rect, anchor, (x, y))
    surface.blit(text_surface, text_rect)
    return text_rect


def clamp(value, minimum, maximum):
    """
    Restringe `value` al intervalo [minimum, maximum].

    Ejemplos
    --------
    clamp(820, 0, 800) → 800   # fuera del borde derecho
    clamp(-5,  0, 800) → 0     # fuera del borde izquierdo
    clamp(400, 0, 800) → 400   # dentro del rango
    """
    return max(minimum, min(value, maximum))


def draw_hearts(surface, current_lives, max_lives, x, y, size=18, gap=6):
    """
    Dibuja una fila de rombos que representan las vidas del jugador.

    Los rombos llenos muestran vidas restantes; los vacíos, las perdidas.
    Usar rombos en lugar de cuadrados los distingue visualmente del jugador
    y los enemigos, que también son cuadrados.

    Parámetros
    ----------
    surface       : pygame.Surface
    current_lives : int — vidas actuales
    max_lives     : int — total de rombos a dibujar
    x, y          : int — esquina superior izquierda del primer rombo
    size          : int — radio del rombo en px (distancia centro→punta)
    gap           : int — separación horizontal entre rombos en px
    """
    for i in range(max_lives):
        cx = x + i * (size * 2 + gap) + size
        cy = y + size

        points = [
            (cx,        cy - size),   # Arriba
            (cx + size, cy),          # Derecha
            (cx,        cy + size),   # Abajo
            (cx - size, cy),          # Izquierda
        ]

        color        = COLOR_HEART_FULL  if i < current_lives else COLOR_HEART_EMPTY
        border_color = (255, 100, 130)   if i < current_lives else (60, 20, 30)

        pygame.draw.polygon(surface, color,        points)
        pygame.draw.polygon(surface, border_color, points, width=2)