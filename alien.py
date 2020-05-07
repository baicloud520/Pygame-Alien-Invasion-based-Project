import pygame
import os

from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""

        super().__init__()      # To inherit properly from Sprite.
        self.screen = ai_game.screen    # Initialize game screen.
        self.settings = ai_game.settings    # Initialize game settings.

        # Initialize 1st line alien image.
        self.image = self.settings.angry_twemoji    # Initialize 1st line alien image.
        self.rect = self.image.get_rect()   # Assign it to a rect.
        self.rect.x = self.rect.width   # Start each new alien at the
        self.rect.y = self.rect.height  # top left of the screen.
        # Store alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien hits edge of screen."""

        screen_rect = self.screen.get_rect()    # Get screen dimensions.
        # Return True if alien hits rigth or left edgee. Else False.
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""

        # Update alien's horizontal posititon.
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x    # Store position.
