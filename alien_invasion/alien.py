import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent an alien."""

    def __init__(self, ai_game):
        """Initialize alien"""
        super().__init__()
        self.screen = ai_game.screen

        # load alien image and set the rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # start each new alien near the top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact horizontal position
        self.x = float(self.rect.x)

