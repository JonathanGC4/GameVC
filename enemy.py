# =============================================================================
# enemy.py — Clase Enemy (Iteración 2: spawn y persecución)
# =============================================================================

import pygame
import random
from settings import (
    ENEMY_SIZE, ENEMY_BASE_SPEED,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_ENEMY,
)


class Enemy:
    def __init__(self):
        self.rect   = pygame.Rect(0, 0, ENEMY_SIZE, ENEMY_SIZE)
        self.speed  = ENEMY_BASE_SPEED
        self.active = True

    @staticmethod
    def spawn(speed=ENEMY_BASE_SPEED):
        """
        Crea un enemigo en un borde aleatorio de la pantalla.
        El borde se elige al azar entre los cuatro lados; dentro de ese
        borde la posición es también aleatoria para que no aparezcan
        siempre en el mismo punto.
        """
        enemy = Enemy()
        enemy.speed = speed

        borde = random.choice(["top", "bottom", "left", "right"])

        if borde == "top":
            enemy.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
            enemy.rect.y = -ENEMY_SIZE          # Justo fuera del borde superior
        elif borde == "bottom":
            enemy.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
            enemy.rect.y = SCREEN_HEIGHT        # Justo fuera del borde inferior
        elif borde == "left":
            enemy.rect.x = -ENEMY_SIZE
            enemy.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        else:  # right
            enemy.rect.x = SCREEN_WIDTH
            enemy.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)

        return enemy

    def update(self, dt, target_pos):
        """
        Mueve el enemigo hacia target_pos (el centro del jugador).

        Se calcula un vector desde el enemigo hasta el jugador, se normaliza
        (para que la velocidad sea constante sin importar la distancia) y se
        multiplica por speed y dt.
        """
        # Vector desde el enemigo hasta el jugador
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        direction = pygame.Vector2(dx, dy)

        # Normalizar sólo si hay distancia real (evita dividir entre 0)
        if direction.length() > 0:
            direction = direction.normalize()

        self.rect.x += int(direction.x * self.speed * dt)
        self.rect.y += int(direction.y * self.speed * dt)

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_ENEMY, self.rect, border_radius=4)
        # Resalte interior para consistencia visual con el jugador
        inner = self.rect.inflate(-6, -6)
        pygame.draw.rect(surface, (255, 100, 100), inner, border_radius=3)

    def is_off_screen(self):
        """
        Devuelve True si el enemigo está muy lejos de la pantalla.
        Útil en iteraciones futuras si los enemigos pueden salir por el borde
        opuesto (p.ej. tras un knockback).
        """
        margin = 200
        return (self.rect.right  < -margin or
                self.rect.left   > SCREEN_WIDTH  + margin or
                self.rect.bottom < -margin or
                self.rect.top    > SCREEN_HEIGHT + margin)