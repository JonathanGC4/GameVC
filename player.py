# =============================================================================
# player.py — Clase Player
# =============================================================================

import pygame
from settings import (
    PLAYER_SIZE, PLAYER_SPEED,
    PLAYER_START_X, PLAYER_START_Y,
    PLAYER_MAX_LIVES,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_PLAYER,
)
from utils import clamp


class Player:
    def __init__(self):
        self.rect = pygame.Rect(
            PLAYER_START_X - PLAYER_SIZE // 2,
            PLAYER_START_Y - PLAYER_SIZE // 2,
            PLAYER_SIZE,
            PLAYER_SIZE,
        )
        self.lives = PLAYER_MAX_LIVES
        self.speed = PLAYER_SPEED

    def update(self, dt):
        direction = self._get_movement_direction()
        self._move(direction, dt)
        self._clamp_to_screen()

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_PLAYER, self.rect, border_radius=6)
        inner = self.rect.inflate(-8, -8)
        pygame.draw.rect(surface, (120, 190, 255), inner, border_radius=4)

    def _get_movement_direction(self):
        """Lee el teclado y devuelve un vector de dirección normalizado."""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= 1  # Y crece hacia abajo
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += 1

        direction = pygame.Vector2(dx, dy)
        if direction.length() > 0:
            direction = direction.normalize()  # Diagonal a la misma velocidad
        return direction

    def _move(self, direction, dt):
        """Mueve el jugador usando delta time para independencia de FPS."""
        self.rect.x += int(direction.x * self.speed * dt)
        self.rect.y += int(direction.y * self.speed * dt)

    def _clamp_to_screen(self):
        """Impide que el jugador salga de los límites de la ventana."""
        self.rect.left = clamp(self.rect.left, 0, SCREEN_WIDTH  - self.rect.width)
        self.rect.top  = clamp(self.rect.top,  0, SCREEN_HEIGHT - self.rect.height)

    @property
    def center(self):
        return self.rect.center

    @property
    def is_alive(self):
        return self.lives > 0

    def lose_life(self):
        self.lives = max(0, self.lives - 1)

    def reset(self):
        self.rect.topleft = (
            PLAYER_START_X - PLAYER_SIZE // 2,
            PLAYER_START_Y - PLAYER_SIZE // 2,
        )
        self.lives = PLAYER_MAX_LIVES