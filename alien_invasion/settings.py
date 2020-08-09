class Settings:
    """settings for Alien Invasion"""
    def __init__(self):
        """settings vary depending on machine, change accordingly"""
        # screen settings
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_speed = .25
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # alien settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        # positive fleet direction = right, negative fleet direction = left
        self.fleet_direction = 1
