import pygame
from pygame.sprite import Sprite


def update(self):
    """update bullet position on screen"""
    self.y -= self.settings.bullet_speed
    self.rect.y = self.y


def draw_bullet(self):
    """draw bullet"""
    pygame.draw.rect(self.screen, self.color, self.rect)


class Bullet(Sprite):
    """class to keep track of bullet objects"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create bullet object
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # store bullet's position
        self.y = float(self.rect.y)



