# =============================================================================
# player.py — Iteración 3: invencibilidad temporal tras recibir daño
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


# Segundos de invencibilidad tras recibir un golpe
INVINCIBILITY_DURATION = 1.5


class Player:
    def __init__(self):
        self.rect  = pygame.Rect(
            PLAYER_START_X - PLAYER_SIZE // 2,
            PLAYER_START_Y - PLAYER_SIZE // 2,
            PLAYER_SIZE, PLAYER_SIZE,
        )
        self.lives = PLAYER_MAX_LIVES
        self.speed = PLAYER_SPEED

        # --- Nuevo en Iteración 3 ---
        self.invincible      = False   # True mientras dure el periodo de gracia
        self.invincible_timer = 0.0   # Tiempo restante de invencibilidad

    # ------------------------------------------------------------------
    def update(self, dt):
        self._update_invincibility(dt)
        direction = self._get_movement_direction()
        self._move(direction, dt)
        self._clamp_to_screen()

    def _update_invincibility(self, dt):
        """Descuenta el timer de invencibilidad y la desactiva al llegar a 0."""
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible       = False
                self.invincible_timer = 0.0

    # ------------------------------------------------------------------
    def draw(self, surface):
        """
        Parpadeo visual durante la invencibilidad: el jugador se dibuja
        sólo en los frames 'pares' del timer (cada ~0.1 s), creando el
        efecto de parpadeo clásico de los juegos de arcade.
        """
        if self.invincible:
            # Parpadear: visible sólo cuando la parte entera de timer*10 es par
            if int(self.invincible_timer * 10) % 2 == 0:
                return   # Frame invisible → efecto de parpadeo

        pygame.draw.rect(surface, COLOR_PLAYER, self.rect, border_radius=6)
        inner = self.rect.inflate(-8, -8)
        pygame.draw.rect(surface, (120, 190, 255), inner, border_radius=4)

    # ------------------------------------------------------------------
    def take_hit(self):
        """
        Llamado por Game al detectar colisión.
        Reduce una vida y activa el periodo de invencibilidad.
        Sin invencibilidad el jugador perdería todas las vidas en un frame.
        """
        if self.invincible:
            return   # Ya está en periodo de gracia, ignorar el golpe

        self.lives = max(0, self.lives - 1)
        self.invincible       = True
        self.invincible_timer = INVINCIBILITY_DURATION

    # ------------------------------------------------------------------
    def _get_movement_direction(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += 1

        direction = pygame.Vector2(dx, dy)
        if direction.length() > 0:
            direction = direction.normalize()
        return direction

    def _move(self, direction, dt):
        self.rect.x += int(direction.x * self.speed * dt)
        self.rect.y += int(direction.y * self.speed * dt)

    def _clamp_to_screen(self):
        self.rect.left = clamp(self.rect.left, 0, SCREEN_WIDTH  - self.rect.width)
        self.rect.top  = clamp(self.rect.top,  0, SCREEN_HEIGHT - self.rect.height)

    @property
    def center(self):
        return self.rect.center

    @property
    def is_alive(self):
        return self.lives > 0

    def reset(self):
        self.rect.topleft = (
            PLAYER_START_X - PLAYER_SIZE // 2,
            PLAYER_START_Y - PLAYER_SIZE // 2,
        )
        self.lives            = PLAYER_MAX_LIVES
        self.invincible       = False
        self.invincible_timer = 0.0