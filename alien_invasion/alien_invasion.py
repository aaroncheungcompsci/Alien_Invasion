import sys
import pygame
from settings import Settings
from ship import Ship


def _check_keydown_events(self, event):
    if event.key == pygame.K_RIGHT:
        self.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        self.ship.moving_left = True
    elif event.key == pygame.K_q:
        sys.exit()


def _check_keyup_events(self, event):
    if event.key == pygame.K_RIGHT:
        self.ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        self.ship.moving_left = False


# _ before name means "private" or internal use in python
def _check_events(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            _check_keydown_events(self, event)
        elif event.type == pygame.KEYUP:
            _check_keyup_events(self, event)


def _update_screen(self):
    self.screen.fill(self.bg_color)
    self.ship.blitme()
    pygame.display.flip()


class AlienInvasion:
    """class to manage game assets and behavior"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """start main loop of game"""

        while True:
            # watch for events
            _check_events(self)
            self.ship.update()
            # redraw screen on each iteration of while loop
            _update_screen(self)


if __name__ == '__main__':
    """main method like in java"""
    ai = AlienInvasion()
    ai.run_game()
