import pygame
import os
import random

from pygame.sprite import Sprite


class Cloud(Sprite):
    """A class to manage clouds."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""

        super().__init__()  # To inherit properly from Sprite.
        self.screen = ai_game.screen    # Initialize game screen.
        self.settings = ai_game.settings    # Initialize game settings.

        self.image = self.settings.cloud    # Initialize cloud's image.
        self.rect = self.image.get_rect()   # Assign a rect to it.
        self.x = float(self.rect.x)     # Revert x-coordinate to a float.
        self.y = float(self.rect.y)     # Revert y-coordinate to a float.

        self._make_clouds()     # Helper method to create a cloud.

    def _make_clouds(self):
        """Make clouds."""

        # Generate random x-coordinate.
        self.x = random.randint(0, self.settings.screen_width)
        # Generate random y-coordinate.
        self.y = random.randint(0, self.settings.screen_height)
        self.rect.x = self.x
        self.rect.y = self.y
