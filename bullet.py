import pygame
import os

from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game, inclination):
        """Create a bullet object at the ship's current position."""

        super().__init__()      # To inherit properly from Sprite.
        self.screen = ai_game.screen    # Initialize game screen.
        self.settings = ai_game.settings    # Initialize game settings.
        self.ship = ai_game.ship    # Initialize game ship.

        # Initialize ship's bullet image.
        self.image = self.settings.heart_twemoji
        self.rect = self.image.get_rect()   # Assign a rect to it.

        # Inclination of bullet (right, left, top)
        self.inclination = inclination
        if self.inclination == None:    # If no inclination, at the top of the ship.
            self.rect.midtop = ai_game.ship.rect.midtop
            self.x = float(self.rect.x - self.settings.bullet_adjustment)
            self.y = float(self.rect.y - self.settings.bullet_adjustment)

        if self.inclination == 1:   # If 1, on the right of the ship.
            self.rect.midleft = ai_game.ship.rect.midright
            self.x = float(self.rect.x - self.settings.bullet_adjustment)
            self.y = float(self.rect.y - self.settings.bullet_adjustment)

        if self.inclination == -1:  # If -1, on the left of the ship.
            self.rect.midright = ai_game.ship.rect.midleft
            self.x = float(self.rect.x + self.settings.bullet_adjustment)
            self.y = float(self.rect.y - self.settings.bullet_adjustment)

    def update(self):
        """Manage movement of bullets."""

        if self.inclination == None:
            if self.ship.rect.bottom <= (self.ship.screen_rect.bottom) and self.ship.rect.top > ((self.settings.screen_height / 2) + self.settings.ship_adjustment):
                self.y -= self.settings.bullet_speed
                self.rect.y = self.y

            if self.ship.rect.top < (self.settings.screen_height / 2):
                self.y += self.settings.bullet_speed
                self.rect.y = self.y

        if self.inclination == 1:
            self.x += (self.settings.bullet_speed / 2.0) * self.inclination
            self.y -= self.settings.bullet_speed * self.inclination
            self.rect.x = self.x
            self.rect.y = self.y

        if self.inclination == -1:
            self.x += (self.settings.bullet_speed / 2.0) * self.inclination
            self.y -= self.settings.bullet_speed * - self.inclination
            self.rect.x = self.x
            self.rect.y = self.y

    def blitme(self):
        """Draw the bullet to the screen."""

        self.screen.blit(self.image, self.rect)     # Import image.
