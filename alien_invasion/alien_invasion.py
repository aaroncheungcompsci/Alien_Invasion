import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """class to manage game assets and behavior"""

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """create bullet and add to group of bullets"""
        # limits amount of bullets to show on screen
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """updates position of bullets and gets rid of old bullets"""
        self.bullets.update()

        # remove bullets that go off the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # refactored code
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()

        if not self.aliens:
            # Destroy existing bullets and creates new fleet when last alien is destroyed
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _create_alien(self, alien_number, row_number):
        # create alien and place in row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        """create fleet of aliens"""
        # create first row of aliens
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine number of rows of aliens that fit on screen
        ship_height = self.ship.rect.height

        # this is to create space above the ship
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # create the full fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """respond appropriately if aliens reach edge of window"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop entire fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # _ before name means "private" or internal use in python
    def _check_events(self):
        """Respond to keypresses"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when Play button is pressed"""
        # button click will remove play button from screen
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset game settings
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()

            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_ships()

            # get rid of remaining objects in screen
            self.aliens.empty()
            self.bullets.empty()

            # create new fleet + center ship
            self._create_fleet()
            self.ship.center_ship()


            # hiding mouse cursor (not needed but ill put it in here for reference)
            # pygame.mouse,set_visible(False)

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # draw score info
        self.sb.show_score()

        # draw play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _update_aliens(self):
        """update all positions of aliens"""
        self._check_fleet_edges()
        self.aliens.update()

        # look for collisions between the ship and alien ships
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship has been hit!")
            self._ship_hit()

        # check if any aliens hit the bottom
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # same treatment as if the ship got hit
                self._ship_hit()
                break

    def _ship_hit(self):
        """actions for ship being hit by an enemy alien ship"""
        if self.stats.ships_left > 0:
            # decrement ships
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # clear screen
            self.aliens.empty()
            self.bullets.empty()

            # new fleet and centers ship
            self._create_fleet()
            self.ship.center_ship()

            # pausing to let player see collision
            sleep(0.5)
        else:
            self.stats.game_active = False
            # sets mouse to visible (only uncomment if mouse is hidden in _check_play_button
            # pygame.mouse.set_visible(True)

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        # instance for game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        # Make the play button
        self.play_button = Button(self, "Play")
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """start main loop of game"""

        while True:
            # watch for events that happen ingame
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            # print(len(self.bullets))
            # redraw screen on each iteration of while loop
            self._update_screen()


if __name__ == '__main__':
    """main method like in java"""
    ai = AlienInvasion()
    ai.run_game()
