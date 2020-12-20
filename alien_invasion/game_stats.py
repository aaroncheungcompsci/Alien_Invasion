class GameStats:
    """Tracks some stats for the game"""

    def __init__(self, ai_game):
        """initialize stats"""

        self.settings = ai_game.settings
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

        self.reset_stats()
        # Start game in an inactive state
        self.game_active = False

    def reset_stats(self):
        """initialize stats that change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
