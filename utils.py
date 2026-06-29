# =============================================================================
# utils.py — Funciones de utilidad reutilizables
# =============================================================================

import pygame
from settings import COLOR_TEXT


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