# =============================================================================
# enemy.py — Clase Enemy (esqueleto listo para Iteración 2)
# =============================================================================

import pygame
from settings import ENEMY_SIZE, ENEMY_BASE_SPEED


class Enemy:
    def __init__(self):
        self.rect   = pygame.Rect(0, 0, ENEMY_SIZE, ENEMY_SIZE)
        self.speed  = ENEMY_BASE_SPEED
        self.active = False

    @staticmethod
    def spawn(speed=ENEMY_BASE_SPEED):
        """Crea un enemigo en un borde aleatorio. Lógica completa en Iteración 2."""
        enemy = Enemy()
        enemy.speed  = speed
        enemy.active = True
        return enemy

    def update(self, dt, target_pos):
        """Persigue a target_pos. Se implementa en Iteración 2."""
        pass  # TODO (Iteración 2)

    def draw(self, surface):
        """Dibuja el enemigo. Se implementa en Iteración 2."""
        pass  # TODO (Iteración 2)