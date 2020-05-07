import pygame
import os

from pygame.sprite import Sprite


class EnemyBullet(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""

        super().__init__()  # To inherit properly from Sprite.
        self.screen = ai_game.screen    # Initialize game screen.
        self.settings = ai_game.settings    # Initialize game settings.

        self.image = self.settings.happy_twemoji    # Initialize 2nd line alien image.
        self.rect = self.image.get_rect()   # Assign it to a rect.
        self.rect.x = self.rect.width   # Start each new alien at the
        self.rect.y = self.rect.height  # top left of the screen.
        self.x = float(self.rect.x)     # Store alien's exact horizontal position.

        self.bonus = False      # Initialize power-up creating flag to False.

    def check_edges(self):
        """Return True if alien hits the screen edge."""

        screen_rect = self.screen.get_rect()    # Get screen dimensions.
        if self.rect.right >= screen_rect.right or self.rect.left <= 0: # Return True if alien hits rigth or left edgee.
            return True

    def update(self):
        """Move the alien right or left."""

        self.x += (self.settings.alien_speed *
                   self.settings.enemy_bullet_direction)    # Update alien's horizontal posititon.
        self.rect.x = self.x    # Store position.
