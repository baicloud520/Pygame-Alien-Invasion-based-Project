import pygame
import random


class Powers():

    def __init__(self, ai_game):
        """Initialize power-ups."""

        self.screen = ai_game.screen    # Initialize game screen.
        self.settings = ai_game.settings    # Initialize game settings.
        # Initialize screen dimensions.
        self.screen_rect = ai_game.screen.get_rect()

        self.status = False     # Start with inactive power-up status.
        self.cooldown_counter = 0   # Initialize cooldown counter.

    def generate_rand_pow(self, pos):
        """Randomly generate a power-up."""

        self.pow = random.randint(1, 4)   # In range of power-up types.
        if self.pow == 1:       # If 1, assign corresponding power-up image.
            self.pow_image = self.settings.power_up_1
        if self.pow == 2:
            self.pow_image = self.settings.power_up_2
        if self.pow == 3:
            self.pow_image = self.settings.power_up_3
        if self.pow == 4:
            self.pow_image = self.settings.power_up_4

        self.rect = self.pow_image.get_rect()   # Get rect for image.
        self.rect.center = pos.center       # Center coordinates.
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the ship to the screen at the position specified by 'self.rect'."""

        self.screen.blit(self.pow_image, self.rect)

    def update(self):
        """ Move the power-up downward, until it hits bottom."""

        self.y += self.settings.power_up_speed
        self.rect.y = self.y
        # If image hits bottom, inactivate power-up.
        if self.rect.bottom >= self.screen_rect.bottom:
            self.status = False
