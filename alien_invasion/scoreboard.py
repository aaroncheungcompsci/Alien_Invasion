import pygame.font


class Scoreboard:
    """keeps track of scoring information"""

    def __init__(self, ai_game):
        """initialize scorekeeping attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare initial score image
        self.prep_score()

    def prep_score(self):
        """Turn score into rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)

        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # display score at top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw score on screen"""
        self.screen.blit(self.score_image, self.score_rect)