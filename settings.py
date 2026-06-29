# =============================================================================
# settings.py — Configuración centralizada del juego
# =============================================================================

# VENTANA
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
WINDOW_TITLE  = "Survival Game — Iteración 1"
TARGET_FPS    = 60

# COLORES (R, G, B)
COLOR_BACKGROUND = (15, 15, 25)
COLOR_PLAYER     = (60, 140, 255)
COLOR_ENEMY      = (220, 50, 50)
COLOR_TEXT       = (240, 240, 240)
COLOR_ACCENT     = (255, 200, 50)

# JUGADOR
PLAYER_SIZE    = 36
PLAYER_SPEED   = 280
PLAYER_START_X = SCREEN_WIDTH  // 2
PLAYER_START_Y = SCREEN_HEIGHT // 2

# ENEMIGOS (Iteración 2)
ENEMY_SIZE       = 30
ENEMY_BASE_SPEED = 120
ENEMY_SPAWN_RATE = 2.0
ENEMY_SPEED_SCALE = 0.05

# SISTEMA DE JUEGO
PLAYER_MAX_LIVES = 3
COLOR_HEART_FULL  = (220, 50,  80)   # Rojo para corazón lleno
COLOR_HEART_EMPTY = (80,  30,  40)   # Rojo oscuro para corazón vacío
# DIFICULTAD PROGRESIVA
DIFFICULTY_SPEED_INCREMENT  = 15    # px/s que se suman cada 10 segundos
DIFFICULTY_SPAWN_DECREMENT  = 0.15  # segundos que se restan al spawn_rate cada 10 s
DIFFICULTY_INTERVAL         = 10    # cada cuántos segundos sube la dificultad
DIFFICULTY_MIN_SPAWN_RATE   = 0.4   # spawn_rate mínimo (no puede bajar de esto)
DIFFICULTY_MAX_ENEMY_SPEED  = 400   # velocidad máxima de los enemigos