# =============================================================================
# settings.py — Configuración centralizada del juego
# =============================================================================
# REGLA: ningún otro archivo debe contener "números mágicos".
# Cualquier valor ajustable vive aquí con su unidad y justificación.
# =============================================================================

# -----------------------------------------------------------------------------
# VENTANA
# -----------------------------------------------------------------------------
SCREEN_WIDTH  = 800   # px
SCREEN_HEIGHT = 600   # px
WINDOW_TITLE  = "Survival Game"
TARGET_FPS    = 60    # Fotogramas por segundo objetivo

# -----------------------------------------------------------------------------
# COLORES (R, G, B)
# -----------------------------------------------------------------------------
COLOR_BACKGROUND  = (15,  15,  25)    # Fondo oscuro azulado
COLOR_PLAYER      = (60,  140, 255)   # Azul para el jugador
COLOR_ENEMY       = (220, 50,  50)    # Rojo para los enemigos
COLOR_TEXT        = (240, 240, 240)   # Blanco suave para HUD
COLOR_ACCENT      = (255, 200, 50)    # Amarillo dorado para resaltes
COLOR_HEART_FULL  = (220, 50,  80)    # Corazón lleno
COLOR_HEART_EMPTY = (80,  30,  40)    # Corazón vacío

# -----------------------------------------------------------------------------
# JUGADOR
# -----------------------------------------------------------------------------
PLAYER_SIZE    = 36    # Lado del cuadrado en px
PLAYER_SPEED   = 280   # px/s (usa delta time)
PLAYER_START_X = SCREEN_WIDTH  // 2
PLAYER_START_Y = SCREEN_HEIGHT // 2
PLAYER_MAX_LIVES       = 3
INVINCIBILITY_DURATION = 1.5   # Segundos de gracia tras recibir daño

# -----------------------------------------------------------------------------
# ENEMIGOS
# -----------------------------------------------------------------------------
ENEMY_SIZE       = 30     # Lado del cuadrado en px
ENEMY_BASE_SPEED = 120    # px/s velocidad inicial
ENEMY_SPAWN_RATE = 2.0    # Segundos entre apariciones al inicio

# -----------------------------------------------------------------------------
# DIFICULTAD PROGRESIVA
# -----------------------------------------------------------------------------
DIFFICULTY_INTERVAL        = 10    # Segundos entre escalones de dificultad
DIFFICULTY_SPEED_INCREMENT = 15    # px/s que se suman a enemy_speed cada escalón
DIFFICULTY_SPAWN_DECREMENT = 0.15  # Segundos que se restan a spawn_rate cada escalón
DIFFICULTY_MAX_ENEMY_SPEED = 400   # Tope de velocidad de enemigos (px/s)
DIFFICULTY_MIN_SPAWN_RATE  = 0.4   # Tope mínimo de tiempo entre spawns (s)

# -----------------------------------------------------------------------------
# EFECTOS VISUALES
# -----------------------------------------------------------------------------
HIT_FLASH_DURATION  = 0.2    # Segundos que dura el viñeteado rojo al recibir daño
GAMEOVER_FADE_SPEED = 180    # Opacidad por segundo del fade del Game Over (0-255)