# =============================================================================
# main.py — Punto de entrada
# =============================================================================
# Responsabilidad única: inicializar Pygame y lanzar el juego.
#
# No contiene lógica de juego.  Esta separación permite importar Game en
# tests sin abrir una ventana real, y agregar argumentos de línea de
# comandos (--fullscreen, --debug) sin tocar la lógica del juego.
# =============================================================================

import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE
from game    import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    Game(screen).run()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()