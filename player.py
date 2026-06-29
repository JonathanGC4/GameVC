# =============================================================================
# player.py — Clase Player
# =============================================================================
# Responsabilidad única: estado y comportamiento del jugador.
#
# Esta clase NO conoce a los enemigos, la puntuación ni la lógica global.
# Esa separación permite:
#   - Modificar el movimiento sin tocar Game.
#   - Reemplazar el cuadrado azul por un sprite cambiando solo draw().
#   - Probar Player de forma aislada sin inicializar el juego completo.
# =============================================================================

import pygame
from settings import (
    PLAYER_SIZE, PLAYER_SPEED,
    PLAYER_START_X, PLAYER_START_Y,
    PLAYER_MAX_LIVES, INVINCIBILITY_DURATION,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_PLAYER,
)
from utils import clamp


class Player:
    """
    Jugador controlado por teclado (WASD / flechas).

    Atributos públicos relevantes
    -----------------------------
    rect        : pygame.Rect  — posición y área de colisión
    lives       : int          — vidas restantes
    invincible  : bool         — True durante el periodo de gracia
    """

    def __init__(self):
        self.rect = pygame.Rect(
            PLAYER_START_X - PLAYER_SIZE // 2,
            PLAYER_START_Y - PLAYER_SIZE // 2,
            PLAYER_SIZE,
            PLAYER_SIZE,
        )
        self.lives            = PLAYER_MAX_LIVES
        self.speed            = PLAYER_SPEED
        self.invincible       = False
        self.invincible_timer = 0.0

    # ------------------------------------------------------------------
    # CICLO PRINCIPAL
    # ------------------------------------------------------------------
    def update(self, dt):
        """Llamado una vez por frame desde Game._update()."""
        self._tick_invincibility(dt)
        direction = self._read_input()
        self._apply_movement(direction, dt)
        self._confine_to_screen()

    def draw(self, surface):
        """
        Dibuja el jugador.
        Durante la invencibilidad parpadea alternando frames visibles e invisibles.
        Para usar sprites: reemplazar pygame.draw.rect por surface.blit(sprite, self.rect).
        """
        if self.invincible and int(self.invincible_timer * 10) % 2 == 0:
            return   # Frame invisible → efecto de parpadeo

        pygame.draw.rect(surface, COLOR_PLAYER, self.rect, border_radius=6)
        inner = self.rect.inflate(-8, -8)
        pygame.draw.rect(surface, (120, 190, 255), inner, border_radius=4)

    # ------------------------------------------------------------------
    # LÓGICA DE DAÑO
    # ------------------------------------------------------------------
    def take_hit(self):
        """
        Aplica un golpe al jugador.

        Si ya está en periodo de gracia, el golpe se ignora.
        Sin esta protección el jugador perdería todas las vidas en un frame
        porque la colisión se detecta en cada tick.
        """
        if self.invincible:
            return
        self.lives            = max(0, self.lives - 1)
        self.invincible       = True
        self.invincible_timer = INVINCIBILITY_DURATION

    # ------------------------------------------------------------------
    # PROPIEDADES
    # ------------------------------------------------------------------
    @property
    def center(self):
        """Centro del jugador como (x, y). Lo usan los enemigos para perseguirle."""
        return self.rect.center

    @property
    def is_alive(self):
        return self.lives > 0

    # ------------------------------------------------------------------
    # RESET
    # ------------------------------------------------------------------
    def reset(self):
        """Restaura el jugador al estado inicial. Llamado por Game.reset()."""
        self.rect.topleft     = (
            PLAYER_START_X - PLAYER_SIZE // 2,
            PLAYER_START_Y - PLAYER_SIZE // 2,
        )
        self.lives            = PLAYER_MAX_LIVES
        self.invincible       = False
        self.invincible_timer = 0.0

    # ------------------------------------------------------------------
    # MÉTODOS PRIVADOS
    # ------------------------------------------------------------------
    def _tick_invincibility(self, dt):
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible       = False
                self.invincible_timer = 0.0

    def _read_input(self):
        """
        Lee el teclado y devuelve un vector de dirección normalizado.

        La normalización es clave para el movimiento diagonal: sin ella,
        moverse en diagonal (dx=1, dy=1) daría una velocidad un 41% mayor
        que en línea recta, porque la magnitud del vector sería √2 ≈ 1.41.
        """
        keys = pygame.key.get_pressed()
        dx   = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - \
               (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy   = (keys[pygame.K_s] or keys[pygame.K_DOWN])  - \
               (keys[pygame.K_w] or keys[pygame.K_UP])

        direction = pygame.Vector2(dx, dy)
        return direction.normalize() if direction.length() > 0 else direction

    def _apply_movement(self, direction, dt):
        """
        Desplaza el rect usando velocidad × delta_time.

        Multiplicar por dt hace el movimiento independiente del FPS:
        a 30 o 120 fotogramas/segundo el jugador recorre la misma distancia
        por segundo de tiempo real.
        """
        self.rect.x += int(direction.x * self.speed * dt)
        self.rect.y += int(direction.y * self.speed * dt)

    def _confine_to_screen(self):
        """Impide que el jugador salga de los límites de la ventana."""
        self.rect.left = clamp(self.rect.left, 0, SCREEN_WIDTH  - self.rect.width)
        self.rect.top  = clamp(self.rect.top,  0, SCREEN_HEIGHT - self.rect.height)