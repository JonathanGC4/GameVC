# =============================================================================
# game.py — Iteración 3: colisiones completas con feedback visual
# =============================================================================


import pygame
from utils import draw_text, draw_hearts
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS,
    COLOR_BACKGROUND, COLOR_ACCENT,
    ENEMY_BASE_SPEED, ENEMY_SPAWN_RATE,
    PLAYER_MAX_LIVES, 
)
from player import Player
from enemy  import Enemy
from utils  import draw_text


# Duración del flash rojo en pantalla al recibir daño (segundos)
HIT_FLASH_DURATION = 0.2


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

        # --- Nuevo en Iteración 3 ---
        self.hit_flash_timer = 0.0   # Tiempo restante del flash rojo

    # ------------------------------------------------------------------
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

        # Descontar el flash de daño
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= dt

        self.elapsed_time += dt
        self.score = int(self.elapsed_time)

        # self._update_difficulty()  # Iteración 5
        self._check_game_over()       # Ya podemos activarlo en Iteración 3

    def _update_enemies(self, dt):
        for enemy in self.enemies:
            enemy.update(dt, self.player.center)

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0.0
            self.enemies.append(Enemy.spawn(speed=self.enemy_speed))

    def _check_collisions(self):
        """
        Recorre los enemigos y aplica daño si tocan al jugador.
        El jugador tiene invencibilidad temporal (gestionada en Player),
        así que take_hit() internamente ignora golpes repetidos.
        """
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_hit()
                self.hit_flash_timer = HIT_FLASH_DURATION
                break   # Un solo golpe por frame es suficiente

    def _check_game_over(self):
        """Cambia el estado a game_over cuando el jugador se queda sin vidas."""
        if not self.player.is_alive:
            self.state = "game_over"

    # ------------------------------------------------------------------
    def _draw(self):
        self.screen.fill(COLOR_BACKGROUND)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

        # Flash rojo en los bordes al recibir daño
        if self.hit_flash_timer > 0:
            self._draw_hit_flash()

        self._draw_hud()

        if self.state == "game_over":
            self._draw_game_over()

        pygame.display.flip()

    def _draw_hit_flash(self):
        """
        Dibuja un viñeteado rojo semitransparente en los bordes de la pantalla.
        La opacidad es proporcional al tiempo restante del flash para que
        desaparezca suavemente en lugar de cortarse de golpe.
        """
        # Opacidad entre 0 y 160 según el tiempo restante
        alpha = int((self.hit_flash_timer / HIT_FLASH_DURATION) * 160)

        flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Dibujar sólo los bordes (cuatro rectángulos finos), no toda la pantalla
        border = 40
        rects = [
            pygame.Rect(0, 0, SCREEN_WIDTH, border),               # Arriba
            pygame.Rect(0, SCREEN_HEIGHT - border, SCREEN_WIDTH, border),  # Abajo
            pygame.Rect(0, 0, border, SCREEN_HEIGHT),              # Izquierda
            pygame.Rect(SCREEN_WIDTH - border, 0, border, SCREEN_HEIGHT),  # Derecha
        ]
        for rect in rects:
            pygame.draw.rect(flash, (220, 30, 30, alpha), rect)

        self.screen.blit(flash, (0, 0))

    def _draw_hud(self):
        """
        HUD completo — Iteración 4:
          - Puntuación y tiempo (izquierda)
          - Corazones de vida (centro superior)
          - Contador de enemigos (derecha)
          - Barra de ayuda (parte inferior)
        """
        # --- Columna izquierda ---
        draw_text(self.screen, f"Puntos: {self.score}", 28,
                  x=16, y=12, anchor="topleft")

        mins = int(self.elapsed_time) // 60
        secs = int(self.elapsed_time) % 60
        draw_text(self.screen, f"Tiempo: {mins:02d}:{secs:02d}", 28,
                  x=16, y=42, anchor="topleft")

        # --- Centro superior: corazones ---
        # Calculamos el ancho total para centrarlos en la pantalla
        heart_size = 16
        heart_gap  = 8
        total_width = PLAYER_MAX_LIVES * (heart_size * 2 + heart_gap) - heart_gap
        hearts_x = (SCREEN_WIDTH - total_width) // 2

        draw_hearts(
            self.screen,
            current_lives=self.player.lives,
            max_lives=PLAYER_MAX_LIVES,
            x=hearts_x,
            y=10,
            size=heart_size,
            gap=heart_gap,
        )

        # --- Columna derecha ---
        draw_text(self.screen, f"Enemigos: {len(self.enemies)}", 24,
                  x=SCREEN_WIDTH - 16, y=12, anchor="topright",
                  color=(180, 100, 100))

        # --- Barra inferior de ayuda ---
        draw_text(self.screen,
                  "WASD / Flechas: mover  |  R: reiniciar  |  ESC: salir",
                  20, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 22,
                  anchor="center", color=(120, 120, 140))

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        draw_text(self.screen, "GAME OVER", 72,
                  x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 - 40,
                  anchor="center", color=COLOR_ACCENT)
        draw_text(self.screen, f"Puntuación final: {self.score}", 36,
                  x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 30,
                  anchor="center")
        draw_text(self.screen, "Pulsa R para reiniciar", 28,
                  x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 80,
                  anchor="center", color=(180, 180, 200))

    # ------------------------------------------------------------------
    def reset(self):
        self.player.reset()
        self.enemies.clear()
        self.elapsed_time    = 0.0
        self.score           = 0
        self.state           = "playing"
        self.spawn_timer     = 0.0
        self.enemy_speed     = ENEMY_BASE_SPEED
        self.hit_flash_timer = 0.0