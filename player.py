# =============================================================================
# player.py — Iteración 3: invencibilidad temporal tras recibir daño
# =============================================================================

import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS,
    COLOR_BACKGROUND, COLOR_ACCENT,
    ENEMY_BASE_SPEED, ENEMY_SPAWN_RATE,
    PLAYER_MAX_LIVES,
    DIFFICULTY_SPEED_INCREMENT,
    DIFFICULTY_SPAWN_DECREMENT,
    DIFFICULTY_INTERVAL,
    DIFFICULTY_MIN_SPAWN_RATE,
    DIFFICULTY_MAX_ENEMY_SPEED,
)
from player import Player
from enemy  import Enemy
from utils  import draw_text, draw_hearts


HIT_FLASH_DURATION = 0.2
from utils import clamp


# Segundos de invencibilidad tras recibir un golpe
INVINCIBILITY_DURATION = 1.5
class Game:
    def __init__(self, screen):
        self.screen  = screen
        self.clock   = pygame.time.Clock()
        self.running = True

        self.player  = Player()
        self.enemies = []

        self.elapsed_time = 0.0
        self.score        = 0
        self.state        = "playing"

        self.spawn_timer  = 0.0
        self.spawn_rate   = ENEMY_SPAWN_RATE
        self.enemy_speed  = ENEMY_BASE_SPEED

        self.hit_flash_timer = 0.0

        # --- Nuevo en Iteración 5 ---
        self.difficulty_timer = 0.0   # Acumula tiempo hacia el próximo escalón
        self.difficulty_level = 0     # Nivel actual (sólo informativo para el HUD)

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

    def run(self):
        while self.running:
            dt = self.clock.tick(TARGET_FPS) / 1000.0
            dt = min(dt, 0.2)
            self._handle_events()
            self._update(dt)
            self._draw()
      # ------------------------------------------------------------------
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r:
                    self.reset()

    # ------------------------------------------------------------------
    def _update(self, dt):
        if self.state != "playing":
            return

        self.player.update(dt)
        self._update_enemies(dt)
        self._check_collisions()
        self._update_difficulty(dt)    # ← activo desde Iteración 5
        self._check_game_over()

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= dt

        self.elapsed_time += dt
        self.score = int(self.elapsed_time)

    def _update_enemies(self, dt):
        for enemy in self.enemies:
            enemy.update(dt, self.player.center)

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0.0
            self.enemies.append(Enemy.spawn(speed=self.enemy_speed))

    def _check_collisions(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_hit()
                self.hit_flash_timer = HIT_FLASH_DURATION
                break

    def _update_difficulty(self, dt):
        """
        Cada DIFFICULTY_INTERVAL segundos sube un escalón de dificultad:
          - Los enemigos nuevos son más rápidos.
          - El tiempo entre spawns se reduce.

        Se usan topes máximo y mínimo para que el juego sea difícil pero
        no imposible: los enemigos no superarán DIFFICULTY_MAX_ENEMY_SPEED
        y el spawn_rate no bajará de DIFFICULTY_MIN_SPAWN_RATE.
        """
        self.difficulty_timer += dt

        if self.difficulty_timer >= DIFFICULTY_INTERVAL:
            self.difficulty_timer -= DIFFICULTY_INTERVAL   # Resetear sin perder el sobrante
            self.difficulty_level += 1

            # Aumentar velocidad de enemigos (con tope)
            self.enemy_speed = min(
                self.enemy_speed + DIFFICULTY_SPEED_INCREMENT,
                DIFFICULTY_MAX_ENEMY_SPEED,
            )

            # Reducir tiempo entre spawns (con suelo mínimo)
            self.spawn_rate = max(
                self.spawn_rate - DIFFICULTY_SPAWN_DECREMENT,
                DIFFICULTY_MIN_SPAWN_RATE,
            )

    def _check_game_over(self):
        if not self.player.is_alive:
            self.state = "game_over"

    # ------------------------------------------------------------------
    def _draw(self):
        self.screen.fill(COLOR_BACKGROUND)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

        if self.hit_flash_timer > 0:
            self._draw_hit_flash()

        self._draw_hud()

        if self.state == "game_over":
            self._draw_game_over()

        pygame.display.flip()

    def _draw_hit_flash(self):
        alpha = int((self.hit_flash_timer / HIT_FLASH_DURATION) * 160)
        flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        border = 40
        rects = [
            pygame.Rect(0, 0, SCREEN_WIDTH, border),
            pygame.Rect(0, SCREEN_HEIGHT - border, SCREEN_WIDTH, border),
            pygame.Rect(0, 0, border, SCREEN_HEIGHT),
            pygame.Rect(SCREEN_WIDTH - border, 0, border, SCREEN_HEIGHT),
        ]
        for rect in rects:
            pygame.draw.rect(flash, (220, 30, 30, alpha), rect)
        self.screen.blit(flash, (0, 0))

    def _draw_hud(self):
        # --- Izquierda ---
        draw_text(self.screen, f"Puntos: {self.score}", 28,
                  x=16, y=12, anchor="topleft")

        mins = int(self.elapsed_time) // 60
        secs = int(self.elapsed_time) % 60
        draw_text(self.screen, f"Tiempo: {mins:02d}:{secs:02d}", 28,
                  x=16, y=42, anchor="topleft")

        # Nivel de dificultad actual (nuevo en Iteración 5)
        draw_text(self.screen, f"Nivel: {self.difficulty_level}", 22,
                  x=16, y=72, anchor="topleft", color=(160, 160, 200))

        # --- Centro: corazones ---
        heart_size  = 16
        heart_gap   = 8
        total_width = PLAYER_MAX_LIVES * (heart_size * 2 + heart_gap) - heart_gap
        hearts_x    = (SCREEN_WIDTH - total_width) // 2

        draw_hearts(self.screen,
                    current_lives=self.player.lives,
                    max_lives=PLAYER_MAX_LIVES,
                    x=hearts_x, y=10,
                    size=heart_size, gap=heart_gap)

        # --- Derecha ---
        draw_text(self.screen, f"Enemigos: {len(self.enemies)}", 24,
                  x=SCREEN_WIDTH - 16, y=12, anchor="topright",
                  color=(180, 100, 100))

        # Velocidad actual de los enemigos (útil para la presentación académica)
        draw_text(self.screen, f"Vel. enemigo: {int(self.enemy_speed)} px/s", 20,
                  x=SCREEN_WIDTH - 16, y=44, anchor="topright",
                  color=(140, 100, 100))

        # --- Inferior ---
        draw_text(self.screen,
                  "WASD / Flechas: mover  |  R: reiniciar  |  ESC: salir",
                  20, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 22,
                  anchor="center", color=(120, 120, 140))

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        draw_text(self.screen, "GAME OVER", 72,
                  x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 - 50,
                  anchor="center", color=COLOR_ACCENT)
        draw_text(self.screen, f"Puntuación final: {self.score}", 36,
                  x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 20,
                  anchor="center")
        draw_text(self.screen, f"Nivel alcanzado: {self.difficulty_level}", 28,
                  x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 60,
                  anchor="center", color=(160, 160, 200))
        draw_text(self.screen, "Pulsa R para reiniciar", 28,
                  x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 100,
                  anchor="center", color=(180, 180, 200))

    # ------------------------------------------------------------------
    def reset(self):
        self.player.reset()
        self.enemies.clear()
        self.elapsed_time    = 0.0
        self.score           = 0
        self.state           = "playing"
        self.spawn_timer     = 0.0
        self.spawn_rate      = ENEMY_SPAWN_RATE
        self.enemy_speed     = ENEMY_BASE_SPEED
        self.hit_flash_timer = 0.0
        self.difficulty_timer = 0.0    # ← nuevo en Iteración 5
        self.difficulty_level = 0      # ← nuevo en Iteración 5