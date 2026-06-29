# =============================================================================
# game.py — Iteraciones 6 y 7: Game Over animado + reinicio pulido
# =============================================================================

import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS,
    COLOR_BACKGROUND, COLOR_ACCENT, COLOR_TEXT,
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


HIT_FLASH_DURATION   = 0.2
GAMEOVER_FADE_SPEED  = 180   # Unidades de opacidad por segundo (0-255)


class Game:
    def __init__(self, screen):
        self.screen  = screen
        self.clock   = pygame.time.Clock()
        self.running = True

        self.player  = Player()
        self.enemies = []

        self.elapsed_time = 0.0
        self.score        = 0
        self.state        = "playing"   # "playing" | "game_over" | "restarting"

        self.spawn_timer  = 0.0
        self.spawn_rate   = ENEMY_SPAWN_RATE
        self.enemy_speed  = ENEMY_BASE_SPEED

        self.hit_flash_timer  = 0.0
        self.difficulty_timer = 0.0
        self.difficulty_level = 0

        # --- Nuevo en Iteración 6: animación de Game Over ---
        self.gameover_alpha   = 0.0    # Opacidad actual del overlay (0–255)
        self.gameover_overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )

        # --- Nuevo en Iteración 7: animación de reinicio ---
        self.restart_alpha    = 255.0  # Opacidad del fade-out negro al reiniciar
        self.restarting       = False  # True mientras dura la animación de entrada

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
                    self._begin_restart()   # ← ya no llama a reset() directamente

    # ------------------------------------------------------------------
    def _update(self, dt):
        # Animación de entrada tras reinicio (fade-in desde negro)
        if self.restarting:
            self.restart_alpha -= GAMEOVER_FADE_SPEED * dt
            if self.restart_alpha <= 0:
                self.restart_alpha = 0
                self.restarting    = False
            return   # Durante el fade-in no se actualiza la lógica

        if self.state == "game_over":
            # En game_over solo animamos el overlay; el juego está congelado
            self._update_gameover_fade(dt)
            return

        # Estado "playing" — lógica normal
        self.player.update(dt)
        self._update_enemies(dt)
        self._check_collisions()
        self._update_difficulty(dt)
        self._check_game_over()

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= dt

        self.elapsed_time += dt
        self.score = int(self.elapsed_time)

    def _update_gameover_fade(self, dt):
        """Incrementa la opacidad del overlay hasta llegar a su máximo."""
        if self.gameover_alpha < 200:
            self.gameover_alpha = min(200, self.gameover_alpha + GAMEOVER_FADE_SPEED * dt)

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
        self.difficulty_timer += dt
        if self.difficulty_timer >= DIFFICULTY_INTERVAL:
            self.difficulty_timer -= DIFFICULTY_INTERVAL
            self.difficulty_level += 1
            self.enemy_speed = min(
                self.enemy_speed + DIFFICULTY_SPEED_INCREMENT,
                DIFFICULTY_MAX_ENEMY_SPEED,
            )
            self.spawn_rate = max(
                self.spawn_rate - DIFFICULTY_SPAWN_DECREMENT,
                DIFFICULTY_MIN_SPAWN_RATE,
            )

    def _check_game_over(self):
        if not self.player.is_alive:
            self.state          = "game_over"
            self.gameover_alpha = 0.0   # Empezar el fade desde transparente

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

        # Fade-in negro al entrar/reiniciar (siempre encima de todo)
        if self.restarting and self.restart_alpha > 0:
            fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade.set_alpha(int(self.restart_alpha))
            fade.fill((0, 0, 0))
            self.screen.blit(fade, (0, 0))

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
        # Izquierda
        draw_text(self.screen, f"Puntos: {self.score}", 28,
                  x=16, y=12, anchor="topleft")
        mins = int(self.elapsed_time) // 60
        secs = int(self.elapsed_time) % 60
        draw_text(self.screen, f"Tiempo: {mins:02d}:{secs:02d}", 28,
                  x=16, y=42, anchor="topleft")
        draw_text(self.screen, f"Nivel: {self.difficulty_level}", 22,
                  x=16, y=72, anchor="topleft", color=(160, 160, 200))

        # Centro: corazones
        heart_size  = 16
        heart_gap   = 8
        total_width = PLAYER_MAX_LIVES * (heart_size * 2 + heart_gap) - heart_gap
        hearts_x    = (SCREEN_WIDTH - total_width) // 2
        draw_hearts(self.screen,
                    current_lives=self.player.lives,
                    max_lives=PLAYER_MAX_LIVES,
                    x=hearts_x, y=10, size=heart_size, gap=heart_gap)

        # Derecha
        draw_text(self.screen, f"Enemigos: {len(self.enemies)}", 24,
                  x=SCREEN_WIDTH - 16, y=12, anchor="topright",
                  color=(180, 100, 100))
        draw_text(self.screen, f"Vel. enemigo: {int(self.enemy_speed)} px/s", 20,
                  x=SCREEN_WIDTH - 16, y=44, anchor="topright",
                  color=(140, 100, 100))

        # Inferior
        draw_text(self.screen,
                  "WASD / Flechas: mover  |  R: reiniciar  |  ESC: salir",
                  20, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 22,
                  anchor="center", color=(120, 120, 140))

    def _draw_game_over(self):
        """
        Pantalla de Game Over con tres capas:
          1. Overlay oscuro con fade-in animado.
          2. Textos con la puntuación final y nivel alcanzado.
          3. Instrucción de reinicio parpadeante.
        """
        # 1. Overlay con fade-in
        self.gameover_overlay.fill((0, 0, 0, 0))
        self.gameover_overlay.fill(
            (10, 5, 20, int(self.gameover_alpha))
        )
        self.screen.blit(self.gameover_overlay, (0, 0))

        # Solo mostrar textos cuando el overlay está suficientemente opaco
        if self.gameover_alpha < 80:
            return

        # Calcular opacidad relativa del texto (aparece después del overlay)
        text_alpha = min(255, int((self.gameover_alpha - 80) * 3.5))

        # 2. Superficie temporal para aplicar alpha al texto
        text_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Título
        _draw_text_alpha(text_surf, "GAME OVER", 80,
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 110,
                         (*COLOR_ACCENT, text_alpha), anchor="center")

        # Línea separadora
        sep_alpha = min(255, text_alpha)
        pygame.draw.line(
            text_surf,
            (255, 200, 50, sep_alpha),
            (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 60),
            (SCREEN_WIDTH // 2 + 180, SCREEN_HEIGHT // 2 - 60),
            2,
        )

        # Estadísticas
        mins = int(self.elapsed_time) // 60
        secs = int(self.elapsed_time) % 60
        stats = [
            (f"Tiempo sobrevivido:  {mins:02d}:{secs:02d}", 30, (220, 220, 220, text_alpha)),
            (f"Puntuación final:      {self.score}",         30, (220, 220, 220, text_alpha)),
            (f"Nivel alcanzado:       {self.difficulty_level}", 30, (160, 160, 220, text_alpha)),
        ]
        for i, (text, size, color) in enumerate(stats):
            _draw_text_alpha(text_surf, text, size,
                             SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT // 2 - 20 + i * 38,
                             color, anchor="center")

        self.screen.blit(text_surf, (0, 0))

        # 3. Instrucción de reinicio parpadeante (una vez el overlay es completo)
        if self.gameover_alpha >= 190:
            # Parpadeo: visible durante 0.7 s, invisible 0.3 s (usando tiempo real)
            ticks = pygame.time.get_ticks()
            if (ticks // 700) % 2 == 0:
                draw_text(self.screen, "Pulsa  R  para reiniciar", 30,
                          x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 120,
                          anchor="center", color=(200, 200, 255))

    # ------------------------------------------------------------------
    def _begin_restart(self):
        """
        Inicia la secuencia de reinicio con fade-out a negro.
        El reset real ocurre aquí; el fade-in oculta el 'salto' visual.
        """
        self.reset()
        self.restarting    = True
        self.restart_alpha = 255.0   # Empieza en negro total y se disuelve

    def reset(self):
        self.player.reset()
        self.enemies.clear()
        self.elapsed_time     = 0.0
        self.score            = 0
        self.state            = "playing"
        self.spawn_timer      = 0.0
        self.spawn_rate       = ENEMY_SPAWN_RATE
        self.enemy_speed      = ENEMY_BASE_SPEED
        self.hit_flash_timer  = 0.0
        self.difficulty_timer = 0.0
        self.difficulty_level = 0
        self.gameover_alpha   = 0.0


# ------------------------------------------------------------------------------
# Función auxiliar — fuera de la clase porque es un detalle de rendering puro
# ------------------------------------------------------------------------------
def _draw_text_alpha(surface, text, size, x, y, color_with_alpha, anchor="topleft"):
    """
    Como draw_text() pero acepta un color RGBA para controlar la opacidad
    del texto individualmente. Necesario para el fade-in escalonado del
    Game Over sin depender de Surface.set_alpha() global.
    """
    font       = pygame.font.SysFont(None, size)
    text_surf  = font.render(text, True, color_with_alpha[:3])
    text_surf.set_alpha(color_with_alpha[3])
    text_rect  = text_surf.get_rect()
    setattr(text_rect, anchor, (x, y))
    surface.blit(text_surf, text_rect)