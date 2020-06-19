class GameStats:
    """Tracks some stats for the game"""

    def __init__(self, ai_game):
        """initialize stats"""

        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """initialize stats that change during the game"""
        self.ships_left = self.settings.ship_limit