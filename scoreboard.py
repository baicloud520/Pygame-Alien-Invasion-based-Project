import pygame.font

# To create a froup of ships to represent available ships.
from pygame.sprite import Group
from ship import Ship   # Create an instance of Ship.


class ScoreBoard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""

        self.ai_game = ai_game      # Instance of AlienInvasion.
        self.screen = ai_game.screen    # Initialize game screen.
        self.settings = ai_game.settings    # Initialize game settings.
        self.stats = ai_game.stats      # Initialize game statistics.
        self.screen_rect = self.screen.get_rect()   # Get screen dimensions.

        self.power_status = False   # Set inactive poswer status.
        self.power_type = 0     # Reinitialize power type.

        self.prep_el_score()    # Prepare easy level initial score image.
        self.prep_nl_score()    # Prepare normal level initial score image.
        self.prep_hl_score()    # Prepare hard level initial score image.

        self.prep_el_high_score()   # Prepare initial highscore for easy level.
        # Prepare initial highscore for normal level.
        self.prep_nl_high_score()
        self.prep_hl_high_score()   # Prepare initial highscore for hard level.

        self.prep_el_level()    # Display current level for easy mode.
        self.prep_nl_level()    # Display current level for normal mode.
        self.prep_hl_level()    # Display current level for hard mode.

        self.prep_ships()   # Prepare available ships.

    def prep_el_score(self):
        """Turn the score into a rendered image."""

        # Round score to the nearest 10.
        el_rounded_score = round(self.stats.score, -1)
        # Separate rounded scores by commas.
        el_score_str = "S: {:,}".format(el_rounded_score)
        self.el_score_image = self.settings.sb_font.render(
            el_score_str, True, self.settings.sb_text_color, False)     # Prepare surface.

        # Get surface dimensions.
        self.el_score_rect = self.el_score_image.get_rect()
        self.el_score_rect.right = self.screen_rect.right - 15  # Position it.
        self.el_score_rect.top = 15

    def prep_nl_score(self):
        """Turn the score into a rendered image."""

        nl_rounded_score = round(self.stats.score, -1)
        nl_score_str = "S: {:,}".format(nl_rounded_score)
        self.nl_score_image = self.settings.sb_font.render(
            nl_score_str, True, self.settings.sb_text_color, False)

        self.nl_score_rect = self.nl_score_image.get_rect()
        self.nl_score_rect.right = self.screen_rect.right - 15
        self.nl_score_rect.top = 15

    def prep_hl_score(self):
        """Turn the score into a rendered image."""

        hl_rounded_score = round(self.stats.score, -1)
        hl_score_str = "S: {:,}".format(hl_rounded_score)
        self.hl_score_image = self.settings.sb_font.render(
            hl_score_str, True, self.settings.sb_text_color, False)

        self.hl_score_rect = self.hl_score_image.get_rect()
        self.hl_score_rect.right = self.screen_rect.right - 15
        self.hl_score_rect.top = 15

    def prep_el_high_score(self):
        """Turn the highscore into a rendered image."""

        el_high_score = round(self.stats.el_high_score, -1)
        el_high_score_str = "R: {:,}".format(el_high_score)
        self.el_high_score_image = self.settings.sb_font.render(
            el_high_score_str, True, self.settings.sb_text_color, False)

        self.el_high_score_rect = self.el_high_score_image.get_rect()
        self.el_high_score_rect.centerx = self.screen_rect.centerx
        self.el_high_score_rect.top = self.el_score_rect.top

    def prep_nl_high_score(self):
        """Turn the highscore into a rendered image."""

        nl_high_score = round(self.stats.nl_high_score, -1)
        nl_high_score_str = "R: {:,}".format(nl_high_score)
        self.nl_high_score_image = self.settings.sb_font.render(
            nl_high_score_str, True, self.settings.sb_text_color, False)

        self.nl_high_score_rect = self.nl_high_score_image.get_rect()
        self.nl_high_score_rect.centerx = self.screen_rect.centerx
        self.nl_high_score_rect.top = self.nl_score_rect.top

    def prep_hl_high_score(self):
        """Turn the highscore into a rendered image."""

        hl_high_score = round(self.stats.hl_high_score, -1)
        hl_high_score_str = "R: {:,}".format(hl_high_score)
        self.hl_high_score_image = self.settings.sb_font.render(
            hl_high_score_str, True, self.settings.sb_text_color, False)

        self.hl_high_score_rect = self.hl_high_score_image.get_rect()
        self.hl_high_score_rect.centerx = self.screen_rect.centerx
        self.hl_high_score_rect.top = self.hl_score_rect.top

    def check_el_high_score(self):
        """Check to see if there is a new high score."""

        if self.stats.score > self.stats.el_high_score:
            self.stats.el_high_score = self.stats.score
            self.prep_el_high_score()

    def check_nl_high_score(self):
        """Check to see if there is a new high score."""

        if self.stats.score > self.stats.nl_high_score:
            self.stats.nl_high_score = self.stats.score
            self.prep_nl_high_score()

    def check_hl_high_score(self):
        """Check to see if there is a new high score."""

        if self.stats.score > self.stats.hl_high_score:
            self.stats.hl_high_score = self.stats.score
            self.prep_hl_high_score()

    def prep_el_level(self):
        """Turn level into a rendered image."""

        el_level = self.stats.level
        el_level_str = f"L: {el_level}"
        self.el_level_image = self.settings.sb_font.render(
            el_level_str, True, self.settings.sb_text_color, False)

        self.el_level_rect = self.el_level_image.get_rect()
        self.el_level_rect. right = self.el_score_rect.right
        self.el_level_rect.top = self.el_score_rect.bottom + 5

    def prep_nl_level(self):
        """Turn level into a rendered image."""

        nl_level = self.stats.level
        nl_level_str = f"L: {nl_level}"
        self.nl_level_image = self.settings.sb_font.render(
            nl_level_str, True, self.settings.sb_text_color, False)

        self.nl_level_rect = self.nl_level_image.get_rect()
        self.nl_level_rect. right = self.nl_score_rect.right
        self.nl_level_rect.top = self.nl_score_rect.bottom + 5

    def prep_hl_level(self):
        """Turn level into a rendered image."""

        hl_level = self.stats.level
        hl_level_str = f"L: {hl_level}"
        self.hl_level_image = self.settings.sb_font.render(
            hl_level_str, True, self.settings.sb_text_color, False)

        self.hl_level_rect = self.hl_level_image.get_rect()
        self.hl_level_rect. right = self.hl_score_rect.right
        self.hl_level_rect.top = self.hl_score_rect.bottom + 5

    def prep_ships(self):
        """Show how many ships are left."""

        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.image = self.settings.ship_life
            ship.rect = ship.image.get_rect()
            ship.rect.x = 15 + ship_number * ship.rect.width
            ship.rect.y = 15
            self.ships.add(ship)

    def show_el_score(self):
        """Draw score to the screen."""

        self.screen.blit(self.el_score_image, self.el_score_rect)
        self.screen.blit(self.el_high_score_image, self.el_high_score_rect)
        self.screen.blit(self.el_level_image, self.el_level_rect)
        self.ships.draw(self.screen)

    def show_nl_score(self):
        """Draw score to the screen."""

        self.screen.blit(self.nl_score_image, self.nl_score_rect)
        self.screen.blit(self.nl_high_score_image, self.nl_high_score_rect)
        self.screen.blit(self.nl_level_image, self.nl_level_rect)
        self.ships.draw(self.screen)

    def show_hl_score(self):
        """Draw score to the screen."""

        self.screen.blit(self.hl_score_image, self.hl_score_rect)
        self.screen.blit(self.hl_high_score_image, self.hl_high_score_rect)
        self.screen.blit(self.hl_level_image, self.hl_level_rect)
        self.ships.draw(self.screen)
