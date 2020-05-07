import pygame
import os


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""

        # Screen settings (dimensions in pixels, colors in pixels - RGB):
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (135, 206, 235)

        # Play button settings:
        self.pb_width, self.pb_height = 600, 50
        self.pb_button_color = (130, 179, 0)
        self.pb_text_color = (0, 0, 0)
        self.pb_font = pygame.font.SysFont("comicsans", 60)

        # Difficulty levels pb settings:
        self.dlpb_width, self.dlpb_height = 130, 40
        self.dlpb_text_color = (255, 255, 255)
        self.elpb_button_color = (255, 206, 3)
        self.nlpb_button_color = (253, 97, 4)
        self.hlpb_button_color = (240, 5, 5)
        self.dlpb_font = pygame.font.SysFont("comicsans", 50)

        # Ship settings:
        self.ship_adjustment = 5
        self.ship_limit = 3

        self.player_ship = pygame.image.load(
            os.path.join("twemojis", "kiss_twemoji.png"))
        self.ship_life = pygame.image.load(
            os.path.join("twemojis", "sunglass_twemoji.png"))

        # Bullet settings:
        self.heart_twemoji = pygame.image.load(
            os.path.join("twemojis", "heart_twemoji.png"))
        self.bullet_adjustment = 10.0
        self.bullets_allowed = 30
        self.COOLDOWN_SHIP = 3

        # Scoreboard settings:
        self.sb_text_color = (0, 0, 0)
        self.sb_font = pygame.font.SysFont("comicsans", 40)

        # Power-up settings:
        self.count_pause = 0    # Counter for alarm clock freeze duration.
        self.power_up_speed = 5.0
        self.COOLDOWN_POWER = 18    # Set frequency for powr-up appearences.

        self.power_up_1 = pygame.image.load(
            os.path.join("twemojis", "high_voltage_twemoji.png"))
        self.power_up_2 = pygame.image.load(
            os.path.join("twemojis", "alarm_clock_twemoji.png"))
        self.power_up_3 = pygame.image.load(
            os.path.join("twemojis", "pill_twemoji.png"))
        self.power_up_4 = pygame.image.load(
            os.path.join("twemojis", "wrapped_gift_twemoji.png"))

        self.lucky_box_1 = pygame.image.load(
            os.path.join("twemojis", "super_high_voltage_twemoji.png"))
        self.lucky_box_2 = pygame.image.load(
            os.path.join("twemojis", "super_alarm_clock_twemoji.png"))
        self.lucky_box_3 = pygame.image.load(
            os.path.join("twemojis", "super_pill_twemoji.png"))

        # Alien settings:
        self.alien_adjustment = 3.0
        self.fleet_drop_speed = 20

        self.angry_twemoji = pygame.image.load(
            os.path.join("twemojis", "angry_twemoji.png"))
        self.happy_twemoji = pygame.image.load(
            os.path.join("twemojis", "happy_twemoji.png"))

        # Cloud settings:
        self.clouds_total = 15

        self.cloud = pygame.image.load(
            os.path.join("twemojis", "cloud_twemoji.png"))

        # Game speed settings:
        self.speedup_scale = 1.1  # Evolution of game difficulty by level.
        self.score_scale = 1.5      # Evolution of alien point scores.

        self.initialize_easy_level_settings()
        self.initialize_normal_level_settings()
        self.initialize_hard_level_settings()

    def initialize_easy_level_settings(self):
        """Method that initiates easy level game settings."""

        self.dif_level = "Easy"

        self.ship_speed = 6.0
        self.bullet_speed = 8.0
        self.alien_speed = 4.0

        self.a_point = 10
        self.eb_point = 20

        self.fleet_direction = 1
        self.enemy_bullet_direction = 1

    def initialize_normal_level_settings(self):
        """Method that initiates normal level game settings."""

        self.dif_level = "Normal"

        self.ship_speed = 8.0
        self.bullet_speed = 10.0
        self.alien_speed = 5.0

        self.a_point = 20
        self.eb_point = 30

        self.fleet_direction = 1
        self.enemy_bullet_direction = 1

    def initialize_hard_level_settings(self):
        """Method that initiates hard level game settings."""

        self.dif_level = "Hard"

        self.ship_speed = 11.0
        self.bullet_speed = 12.0
        self.alien_speed = 6.0

        self.a_point = 30
        self.eb_point = 40

        self.fleet_direction = 1
        self.enemy_bullet_direction = 1

    def increase_speed(self):
        """Increase speed and alien point settings."""

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.a_point = int(self.a_point * self.score_scale)
        self.eb_point = int(self.eb_point * self.score_scale)
