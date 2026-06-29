# =============================================================================
# enemy.py — Clase Enemy
# =============================================================================
# Responsabilidad única: comportamiento de un enemigo individual.
#
# La IA es deliberadamente simple (persecución directa) para que el código
# sea fácil de entender. En iteraciones futuras se puede sofisticar
# (flanqueo, formaciones, distintos tipos) sin tocar Game.
# =============================================================================

import pygame
import random
from settings import (
    ENEMY_SIZE, ENEMY_BASE_SPEED,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_ENEMY,
)


class Enemy:
    """
    Enemigo que aparece en un borde aleatorio y persigue al jugador.

    La lógica de creación está en el método estático spawn() en lugar del
    constructor para dejar claro que los enemigos no se instancian
    directamente: siempre se crean a través de spawn().
    """

    def __init__(self):
        self.rect  = pygame.Rect(0, 0, ENEMY_SIZE, ENEMY_SIZE)
        self.speed = ENEMY_BASE_SPEED

    @staticmethod
    def spawn(speed=ENEMY_BASE_SPEED):
        """
        Crea un enemigo en un borde aleatorio, justo fuera de la pantalla.

        Colocarlo fuera de la pantalla (no en el borde exacto) hace que
        entre de forma natural en lugar de aparecer de golpe.
        """
        enemy  = Enemy()
        enemy.speed = speed
        borde  = random.choice(("top", "bottom", "left", "right"))

        if borde == "top":
            enemy.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
            enemy.rect.y = -ENEMY_SIZE
        elif borde == "bottom":
            enemy.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
            enemy.rect.y = SCREEN_HEIGHT
        elif borde == "left":
            enemy.rect.x = -ENEMY_SIZE
            enemy.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        else:
            enemy.rect.x = SCREEN_WIDTH
            enemy.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)

        return enemy

    def update(self, dt, target_pos):
        """
        Mueve el enemigo hacia target_pos.

        Algoritmo: vector dirección → normalizar → escalar por speed × dt.
        Es la IA más simple posible: persecución directa sin predicción ni
        evasión de obstáculos. Suficiente para este juego y fácil de explicar.
        """
        direction = pygame.Vector2(
            target_pos[0] - self.rect.centerx,
            target_pos[1] - self.rect.centery,
        )
        if direction.length() > 0:
            direction = direction.normalize()

        self.rect.x += int(direction.x * self.speed * dt)
        self.rect.y += int(direction.y * self.speed * dt)

    def draw(self, surface):
        """
        Dibuja el enemigo.
        Para usar sprites: reemplazar pygame.draw.rect por surface.blit().
        """
        pygame.draw.rect(surface, COLOR_ENEMY, self.rect, border_radius=4)
        inner = self.rect.inflate(-6, -6)
        pygame.draw.rect(surface, (255, 100, 100), inner, border_radius=3)