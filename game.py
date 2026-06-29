# =============================================================================
# game.py — Clase Game (Iteración 2: enemigos, spawn y colisiones básicas)
# =============================================================================

import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS,
    COLOR_BACKGROUND, COLOR_ACCENT,
    ENEMY_BASE_SPEED, ENEMY_SPAWN_RATE, ENEMY_SPEED_SCALE,
)
from player import Player
from enemy  import Enemy
from utils  import draw_text


class Game:
    def __init__(self, screen):
        self.screen  = screen
        self.clock   = pygame.time.Clock()
        self.running = True

        self.player  = Player()
        self.enemies = []

        self.elapsed_time  = 0.0
        self.score         = 0
        self.state         = "playing"

        # --- Nuevo en Iteración 2 ---
        self.spawn_timer   = 0.0   # Acumula tiempo desde el último spawn
        self.spawn_rate    = ENEMY_SPAWN_RATE  # Segundos entre spawns
        self.enemy_speed   = ENEMY_BASE_SPEED  # Aumenta con el tiempo

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

        self.elapsed_time += dt
        self.score = int(self.elapsed_time)

        # self._update_difficulty()  # Iteración 5
        # self._check_game_over()    # Iteración 6

    def _update_enemies(self, dt):
        """
        Hace dos cosas:
        1. Mueve todos los enemigos activos hacia el jugador.
        2. Genera un nuevo enemigo cada vez que el spawn_timer supera spawn_rate.
        """
        # Mover enemigos existentes
        for enemy in self.enemies:
            enemy.update(dt, self.player.center)

        # Temporizador de spawn
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0.0
            self.enemies.append(Enemy.spawn(speed=self.enemy_speed))

    def _check_collisions(self):
        """
        Detecta si algún enemigo toca al jugador.
        Por ahora sólo imprime en consola; las vidas y el game over
        se implementarán en las Iteraciones 3 y 6.
        """
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                # TODO (Iteración 3): self.player.lose_life() + feedback visual
                print("¡Colisión detectada!")  # Placeholder visible en consola

    # ------------------------------------------------------------------
    def _draw(self):
        self.screen.fill(COLOR_BACKGROUND)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)
        self._draw_hud()

        if self.state == "game_over":
            self._draw_game_over()

        pygame.display.flip()

    def _draw_hud(self):
        draw_text(self.screen, f"Puntos: {self.score}", 28,
                  x=16, y=12, anchor="topleft")

        mins = int(self.elapsed_time) // 60
        secs = int(self.elapsed_time) % 60
        draw_text(self.screen, f"Tiempo: {mins:02d}:{secs:02d}", 28,
                  x=16, y=42, anchor="topleft")

        draw_text(self.screen, f"Vidas: {self.player.lives}", 28,
                  x=SCREEN_WIDTH - 16, y=12, anchor="topright")

        # Contador de enemigos en pantalla (útil para debug)
        draw_text(self.screen, f"Enemigos: {len(self.enemies)}", 22,
                  x=SCREEN_WIDTH - 16, y=44, anchor="topright",
                  color=(180, 100, 100))

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
        self.elapsed_time = 0.0
        self.score        = 0
        self.state        = "playing"
        self.spawn_timer  = 0.0
        self.enemy_speed  = ENEMY_BASE_SPEED