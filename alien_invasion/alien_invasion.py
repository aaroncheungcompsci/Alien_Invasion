import sys
import pygame
from settings import Settings


class AlienInvasion:
    """class to manage game assets and behavior"""

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))

        pygame.display.set_caption("Alien Invasion")

        self.bg_color = (230, 230, 230)

    def run_game(self):
        """start main loop of game"""

        while True:
            # watch for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
