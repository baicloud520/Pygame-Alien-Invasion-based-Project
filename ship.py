import pygame
import os

from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()      # To properly inherite from Sptire.

        self.screen = ai_game.screen    # Initialize game screen.
        self.settings = ai_game.settings    # Initialize game settings.

        self.screen_rect = ai_game.screen.get_rect()    # Get screen's rect.
        # Load ship image. Same directiry as .py files!
        self.image = self.settings.player_ship
        self.rect = self.image.get_rect()       # Assign to it a rect.
        # Position each ship at screen's midbottom.
        self.rect.midbottom = self.screen_rect.midbottom
        # Store decimal value for ship's x-coordinate
        self.x = float(self.rect.x)
        # Store decimal value for ship's y-coordinate
        self.y = float(self.rect.y)

        self.moving_right = False   # Movement flag to implement
        self.moving_left = False    # continuous motion.
        self.moving_down = False
        self.moving_up = False

        self.firing = False     # Inactive fire.
        self.cooldown_counter = 0   # Reset cooldown for firing bullets.

    def update(self):
        """Update ship's position based on movement flags."""

        if self.moving_right and self.rect.right < self.screen_rect.right - self.settings.ship_adjustment:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > self.settings.ship_adjustment:
            self.x -= self.settings.ship_speed

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom - self.settings.ship_adjustment:
            self.y += self.settings.ship_speed

        if self.moving_up and self.rect.top > ((2 * self.settings.screen_height / 4) - self.settings.ship_adjustment):
            self.y -= self.settings.ship_speed

        self.rect.x = self.x    # Update rect's x-coordinate.
        self.rect.y = self.y    # Update rect's y-coordinate.

    def blitme(self):
        """Draw the ship to the screen at the position specified by 'self.rect'."""

        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
