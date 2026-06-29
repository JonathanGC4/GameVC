# =============================================================================
# main.py — Punto de entrada
# =============================================================================

import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE
from game    import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()