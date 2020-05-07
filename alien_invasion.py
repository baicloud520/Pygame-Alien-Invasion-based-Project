
import sys  # To exit game.
import pygame   # Functionalities needed to make a game.
import random   # Random generation of numbers, objects, etc.
import os

from time import sleep  # To pause game when needed.
from datetime import date   # Time acquisition.

from settings import Settings   # Import functionalities defined in Settings class.
from cloud import Cloud     # Import functionalities defined in Cloud class.
from ship import Ship   # Import functionalities defined in Ship class.
from bullet import Bullet   # Import functionalities defined in Bullet class.
from enemy_bullet import EnemyBullet    # Import functionalities defined in EnemyBullet class.
from alien import Alien     # Import functionalities defined in Alien class.
from game_stats import GameStats    # Import functionalities defined in GameStats class.
from scoreboard import ScoreBoard   # Import functionalities defined in ScoreBoard class.
from button import Button   # Import functionalities defined in Button class.
from powers import Powers   # Import functionalities defined in Powers class.
from pygame_functions import *  # Import functionalities defined in pygame_functions.py


class AlienInvasion:
    """Main class controlling game assets"""

    def __init__(self):
        """Initialization of game, and game resources."""

        pygame.init()   # Background settings needed for Pygame to work properly.
        self.settings = Settings()  # Settings instance. Initialization of Settings' arguments in AlienInvasion class.

        # self.song_file = "YOUR_CHOICE.wav"    # Addition of background music.
        # pygame.mixer.music.load(self.song_file)
        # pygame.mixer.music.play(-1)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  # Create display window (surface), to display game elements.
        pygame.display.set_caption("Emoji Invasion")    # Surface is updated after each loop.

        self.stats = GameStats(self)    # GameStats instance.
        self.sb = ScoreBoard(self)  # ScoreBoard instance.

        # Prepare welcoming page with user input. ---> pygame_functions.py
        screenSize(self.settings.screen_width, self.settings.screen_height)     # Create welcoming page.
        newcloud = make_cloud(self.settings.cloud, self.settings.screen_width, self.settings.screen_height, self.settings.clouds_total)     # Create clouds on welcoming page.

        today = date.today()    # Prepate current date for welcoming page.
        year = today.year
        month = today.month
        day = today.day
        self.full_date = f"{day}/{month}/{year}"
        local_time = makeLabel(self.full_date, 30, 50, 20, "black", "comicsans")
        showLabel(local_time)

        welcome_label = makeLabel("Welcome to Emoji Invasion!", 70, (self.settings.screen_width/2), (self.settings.screen_height/4), "black", "comicsans")
        showLabel(welcome_label)    # Show welcoming message.

        instruction_label = makeLabel("Please, enter your name:", 40, (self.settings.screen_width/2), (self.settings.screen_height/2) - 20, "black", "comicsans")
        showLabel(instruction_label)   # Show instructions.

        word_box = makeTextBox(self.settings.screen_width/2, self.settings.screen_height/2 + 20, 200, 0, "...", 0, 30)
        showTextBox(word_box)   # Ask user for username.
        self.entry = textBoxInput(word_box)     # Save user input.

        self.buttons = Button(self)     # Button instance.
        self.buttons.prep_menu_msgs("Select game difficulty:", f"Good luck, {self.entry}! :)")
        self.buttons.prep_difficulty_level_msgs("Easy", "Normal", "Hard")
        # self.buttons.prep_ib_msg("Info")

        self.ship = Ship(self)  # Ship instance. Self gives access Ship to AlienInvasion's resources.
        self.po = Powers(self)  # Power instance.
        self.clouds = pygame.sprite.Group()     # Sprite for clouds. Draws clouds on screen.
        self.bullets = pygame.sprite.Group()    # Sprite for bullets. Draws and uupdates at each pass through of main loop.
        self.enemy_bullets = pygame.sprite.Group()  # Sprite for 2nd line of aliens.
        self.aliens = pygame.sprite.Group()     # Spire for 1st line of aliens.

        self._create_fleet_of_enemy_bullet()    # Helper method to create a fleet of 2nd line aliens.
        self._create_fleet()    # Helper method to create a fleet of 1st line aliens.
        self._create_cloud()    # Helper method to create a group of clouds.

    def run_game(self):
        """Game's main loop. It controls the game."""

        FPS = 60    # Frame Per Second (FPS).
        clock = pygame.time.Clock()     # Check events, then update main loop FPS times per second.

        while True:     # Main loop. Screen, event management and update.

            clock.tick(FPS)     # Consistancy of main loop.

            self._check_events()    # Check events. Always, even if game is inactive.

            if self.stats.game_active:  # Flag controlling game activity (on/off).

                self.ship.update()  # Update ship.
                self._update_bullets()  # Update bullets.
                self._update_aliens()   # Update aliens (1st and 2nd line).

                if self.po.status:  # If power-up status is active, update power-ups.
                    self._update_po()

            self._update_screens()  # Whether game is active or not, update screen.
            self._save_high_score() # Save to external file current highscore values.

    def _check_events(self):
        """Method responding to keypresses and mouse events."""

        for event in pygame.event.get():    # Check keyboard and mouse events to detect movements (list).

            if event.type == pygame.QUIT:   # End game by clicking game window's
                sys.exit()  # close button.

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # Return cursor's x-, y-coordinates when mouse clicked.
                self._check_buttons(mouse_pos)  # Send mouse position to _check_buttons helper method.
                if self.sb.power_type == 4:     # If powe type is 4, check what power type user selected.
                    self._check_power_up_buttons(mouse_pos)

            elif event.type == pygame.KEYDOWN:  # Keys are down.
                self._check_keydown_events(event)   # Check executed movement.

            elif event.type == pygame.KEYUP:    # Keys are up.
                self._check_keyup_events(event) # Check released key.

    def _check_buttons(self, mouse_pos):
        """Start new game when player selects one of the difficulty levels."""

        elpb_button_clicked = self.buttons.elpb_rect.collidepoint(mouse_pos)
        if elpb_button_clicked and not self.stats.game_active:  # If easy level and game inactive.
            self.settings.initialize_easy_level_settings()  # Initialize starting parameters.
            self._start_game()  # Start game.

        nlpb_button_clicked = self.buttons.nlpb_rect.collidepoint(mouse_pos)
        if nlpb_button_clicked and not self.stats.game_active:
            self.settings.initialize_normal_level_settings()
            self._start_game()

        hlpb_button_clicked = self.buttons.hlpb_rect.collidepoint(mouse_pos)
        if hlpb_button_clicked and not self.stats.game_active:
            self.settings.initialize_hard_level_settings()
            self._start_game()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""

        if event.key == pygame.K_RIGHT:     # Right arrow.
            self.ship.moving_right = True   # Flag activating movmebet to the rigth.

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True

        elif event.key == pygame.K_UP:
            self.ship.moving_up = True

        elif event.key == pygame.K_q:   # Key Q.
            sys.exit()  # Exit game.

        elif event.key == pygame.K_SPACE:   # Key space.
            self.ship.firing = True     # Fire bullet.

        elif event.key == pygame.K_p:   # Key P.
            self.pause = True   # Pause flag acitvated.
            pygame.mouse.set_visible(True)
            if self.stats.game_active:      # Only if game is active.
                self._paused()  # Execute helper method, that pauses game.

        elif event.key == pygame.K_c:   # Key C.
            if self.stats.game_active:
                self.pause = False  # Pause flag inactive. Game continues.
                pygame.mouse.set_visible(False)     # Set mouse cursor invisible.

        elif event.key == pygame.K_m:   # Key M.
            if self.stats.game_active:
                self.pause = False  # Pause flag inactive. Game continues.
                self._return_menu() # Return to game menu.

    def _paused(self):
        """A simple way to pause the game."""

        while self.pause:   # While paused, check events (Continue/return Menu/Quit).
            self._check_events()    # Check events. Especially kepress events (C/M/Q).

            self.screen.fill(self.settings.bg_color)    # Fill screen with default background.
            self.clouds.draw(self.screen)   # Fill screen with clouds.

            self.buttons.prep_pause_menu_msgs("Pause", "Press C to continue.", "Press M to menu.", "Press Q to quit.")     # Prepare pause menu messages.
            self.buttons.draw_pause_msgs()  # Draw pause messages.

            pygame.display.flip()   # Display latest screen settings.

    def _check_keyup_events(self, event):
        """Respond to kreypresses."""

        if event.key == pygame.K_RIGHT:     # If right key released.
            self.ship.moving_right = False  # Set it to False.

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

        elif event.key == pygame.K_UP:
            self.ship.moving_up = False

        elif event.key == pygame.K_SPACE:   # If space key released.
            self.ship.firing = False    # Stop firing.

    def _start_game(self):
        """A simple method to start/restart a game."""

        if not self.stats.game_active:  # If game is incative.

            if self.settings.dif_level == "Easy":   # Reset game statiistics, scores, and level.
                self.stats.reset_el_stats()
                self.stats.game_active = True   # Activate game (main while loop).
                self.sb.prep_el_score()
                self.sb.prep_el_level()

            if self.settings.dif_level == "Normal":
                self.stats.reset_nl_stats()
                self.stats.game_active = True
                self.sb.prep_nl_score()
                self.sb.prep_nl_level()

            if self.settings.dif_level == "Hard":
                self.stats.reset_hl_stats()
                self.stats.game_active = True
                self.sb.prep_hl_score()
                self.sb.prep_hl_level()

            self.sb.prep_ships()    # After selecting level prepare life.
            self._reset_screen()    # Reset screen settings (aliens, player, clouds, etc.).

            pygame.mouse.set_visible(False)     # Hide mouse cursor.

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""

        self._cooldown_ship()    # Method controlling frequency of bullets.

        if len(self.bullets) < self.settings.bullets_allowed and self.ship.firing:  # If limitation is respected and space key is hit.

            if self.ship.cooldown_counter == 0:     # If cooldown is 0.
                new_bullet = Bullet(self, None)     # Create Bullet instance.
                self.bullets.add(new_bullet)    # Add new bullet to the sprite group.

                if self.sb.power_type == 1:     # If collision with power up is 1, then:
                    new_bullet_r = Bullet(self, 1)  # Create new bullet on the rigth side of player.
                    self.bullets.add(new_bullet_r)
                    new_bullet_l = Bullet(self, -1)     # Create new bullet on the left side of player.
                    self.bullets.add(new_bullet_l)

            self.ship.cooldown_counter += 1     # Increment cooldown counter.
            # print(self.ship.cooldown_counter) # To check if ouur trick works.

    def _cooldown_ship(self):
        """A simple method to regulate shooting frequency."""
        if self.ship.cooldown_counter >= self.settings.COOLDOWN_SHIP:   # If couunter is bigger than contstant.
            self.ship.cooldown_counter = 0      # Reset counter to be 0 and start creating new bullets.

    def _cooldown_power(self):
        """A simple method to regulate power-up frequency."""
        if self.po.cooldown_counter >= self.settings.COOLDOWN_POWER:    # Same as for _cooldown_ship().
            self.po.cooldown_counter = 0

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""

        self._fire_bullet()     # Check if bullets were fired.
        self.bullets.update()   # Update bullet sprite.

        for bullet in self.bullets.copy():  # Get rid of bullets when they hit screen edges.
            if bullet.rect.top <= 0:        # We can't remove items from a list or group within
                self.bullets.remove(bullet)     # a for loop ---> must make a copy.
            elif bullet.rect.bottom >= self.settings.screen_height:
                self.bullets.remove(bullet)
            elif bullet.rect.left <= 0:
                self.bullets.remove(bullet)
            elif bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)
        # print(len(self.bullets))      # To check if bullets were removed.

        self._check_bullet_alien_collisions()   # Check bullet-alien (1st and 2nd line) collisions.

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""

        if self.settings.dif_level == "Easy":       # Easy level.
            self._check_bullet_alien_collisions_easy_level()

        if self.settings.dif_level == "Normal":     # Normal level.
            self._check_bullet_alien_collisions_normal_level()

        if self.settings.dif_level == "Hard":       # Hard level.
            self._check_bullet_alien_collisions_hard_level()

        if not self.aliens and not self.enemy_bullets:  # If no more enemies left,
            self._start_new_level()                     # start new level.

    def _check_bullet_alien_collisions_easy_level(self):
        """If easy level selected, check collisions between bullets and aliens."""

        collision_b_a = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)      # Pygame returns a collision dictionary.
        collision_b_eb = pygame.sprite.groupcollide(
            self.bullets, self.enemy_bullets, True, True)

        if collision_b_a:   # Check if collision dictionary exists.
            for aliens in collision_b_a.values():   # Add scoring point for each collided alien.
                self.stats.score += self.settings.a_point * \
                    len(aliens)
            self.sb.prep_el_score()     # Create new image with updated score value.
            self.sb.check_el_high_score()   # Comprare current score with registered highscore.

        if collision_b_eb:
            for enemy_bullets in collision_b_eb.values():
                self.stats.score += self.settings.eb_point * \
                    len(enemy_bullets)
                for enemy_bullet in self.enemy_bullets.sprites():   # For aliens in 2nd line, create a power-
                    if enemy_bullet.bonus and self.po.cooldown_counter == 0:    # up if conditions are met.
                        pos = enemy_bullet.rect     # Assign position of power-up to random alien (sprites are not in order).
                        self.po.status = True   # Activate power-up status.
                        self.po.generate_rand_pow(pos)  # Generate power-up.
            self.po.cooldown_counter += 1   # Increment cooldown-counter.
            self._cooldown_power()  # Check cooldown counter.
            self.sb.prep_el_score()
            self.sb.check_el_high_score()

    def _check_bullet_alien_collisions_normal_level(self):
        """If normal level selected, check collisions between bullets and aliens."""

        collision_b_a = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        collision_b_eb = pygame.sprite.groupcollide(
            self.bullets, self.enemy_bullets, True, True)

        if collision_b_a:
            for aliens in collision_b_a.values():
                self.stats.score += self.settings.a_point * \
                    len(aliens)
            self.sb.prep_nl_score()
            self.sb.check_nl_high_score()

        if collision_b_eb:
            for enemy_bullets in collision_b_eb.values():
                self.stats.score += self.settings.eb_point * \
                    len(enemy_bullets)
                for enemy_bullet in self.enemy_bullets.sprites():
                    if enemy_bullet.bonus and self.po.cooldown_counter == 0:
                        pos = enemy_bullet.rect
                        self.po.status = True
                        self.po.generate_rand_pow(pos)
            self.po.cooldown_counter += 1
            self._cooldown_power()
            self.sb.prep_nl_score()
            self.sb.check_nl_high_score()

    def _check_bullet_alien_collisions_hard_level(self):
        """If hard level selected, check collisions between bullets and aliens."""

        collision_b_a = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        collision_b_eb = pygame.sprite.groupcollide(
            self.bullets, self.enemy_bullets, True, True)

        if collision_b_a:
            for aliens in collision_b_a.values():
                self.stats.score += self.settings.a_point * \
                    len(aliens)
            self.sb.prep_hl_score()
            self.sb.check_hl_high_score()

        if collision_b_eb:
            for enemy_bullets in collision_b_eb.values():
                self.stats.score += self.settings.eb_point * \
                    len(enemy_bullets)
                for enemy_bullet in self.enemy_bullets.sprites():
                    if enemy_bullet.bonus and self.po.cooldown_counter == 0:
                        pos = enemy_bullet.rect
                        self.po.status = True
                        self.po.generate_rand_pow(pos)
            self.po.cooldown_counter += 1
            # print(self.po.cooldown_counter)   # To check power-up generation cooldown counter.
            self._cooldown_power()
            self.sb.prep_hl_score()
            self.sb.check_hl_high_score()

    def _update_po(self):
        """A simple method to uupdate power-ups."""

        self._check_po_ship_collision()     # Check poper-up - ship collision.
        self.po.update()    # Update vertical position of falling power-up.

    def _check_po_ship_collision(self):
        """A simple method to check collision between power-ups adn ship."""

        if pygame.Rect.colliderect(self.po.rect, self.ship.rect):   # Chcek collission.
            self.sb.power_type = self.po.pow    # Recognize power-up type.

            if self.sb.power_type == 1:     # If 1, fire triple bullets.
                self._fire_bullet()

            if self.sb.power_type == 2:
                self.settings.count_pause = 0   # Reset to zero if 2 consecutive freeze.
                self._update_aliens()

            if self.sb.power_type == 3:     # If 3, increase ship's life.
                self.stats.ships_left += 1
                self.sb.prep_ships()

            if self.sb.power_type == 4:     # If 4, get lucky box.
                self.lucky_box = True
                self._lucky_box()

            self.po.status = False  # Stop creation of powerups.

    def _lucky_box(self):
        """A simple method for choosing a power-up."""

        while self.lucky_box:
            self._check_events()
            self.screen.fill(self.settings.bg_color)
            self.clouds.draw(self.screen)

            self.buttons.prep_lucky_box("Select a power-up:")   # Prepare contents of lucky box.
            self.buttons.draw_lucky_box()   # Draw power-ups.

            pygame.display.flip()
            pygame.mouse.set_visible(True)
        pygame.mouse.set_visible(False)

    def _check_power_up_buttons(self, mouse_pos):
        """A simple method to select power-ups in lucky box."""

        ac_button_clicked = self.buttons.acpb_rect.collidepoint(mouse_pos)  # Select alarm clock.
        if ac_button_clicked:   # If clicked on alarm clock.
            self.sb.power_type = 1  # Power type is 1.
            self.lucky_box = False  # Exit lucky box.

        hv_button_clicked = self.buttons.hvpb_rect.collidepoint(mouse_pos)
        if hv_button_clicked:
            self.sb.power_type = 2
            self.settings.count_pause = 0
            self.lucky_box = False

        exl_button_clicked = self.buttons.exlpb_rect.collidepoint(mouse_pos)
        if exl_button_clicked:
            self.sb.power_type = 3
            self.stats.ships_left += 1
            self.sb.prep_ships()
            self.lucky_box = False

    def _start_new_level(self):
        """Start new level alien fleets are destroyed."""

        self._reset_screen()    # Reset screen settings.
        self.settings.increase_speed()  # Increase game speed.

        if self.settings.dif_level == "Easy":   # Initialize easy level.
            self.stats.level += 1   # Increase level statistics.
            self.sb.prep_el_level() # Draw new level statisctics.

        if self.settings.dif_level == "Normal":
            self.stats.level += 1
            self.sb.prep_nl_level()

        if self.settings.dif_level == "Hard":
            self.stats.level += 1
            self.sb.prep_hl_level()

        sleep(1.0)  # Pause game for a second.

    def _create_fleet(self):
        """Create alien fleet (1st row)."""

        alien = Alien(self)     # Alien instamce.
        alien_width, alien_height = alien.rect.size     # Get rect size.

        space_x = alien.rect.x / self.settings.alien_adjustment     # Indent of 1st alien.
        available_space_x = self.settings.screen_width - \
            (2 * space_x + alien_width)     # Available space in x-direction.
        number_aliens_x = int(available_space_x // (2 * space_x + alien_width))     # Number of aliens that fits along x-direction.

        ship_height = self.ship.rect.height     # Get ship's image height.
        space_y = alien.rect.y / self.settings.alien_adjustment     # Indent from y-direction.
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)  # Available space along y-direction.
        number_rows = int(available_space_y // (space_y + alien_height))    # Number of aliens tthat fits along y-direction.

        for row_number in range(number_rows):   # Create alien fleet (1st line).
            for alien_number in range(number_aliens_x):     # Loop through x-direction.
                self._create_alien(alien_number, row_number)    # Loop through along y-direction.
        # print(f"How many aliens? {len(self.aliens)}")     # Check how many aliens been created.

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        space_x = alien.rect.x / self.settings.alien_adjustment
        alien.x = (space_x + (1.5 * space_x + alien_width) * alien_number)
        alien.rect.x = alien.x

        space_y = alien.rect.y / self.settings.alien_adjustment
        alien.y = 4 * space_y + (space_y + alien_height) * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)      # Add created alien to aliens sprite.

    def _create_fleet_of_enemy_bullet(self):
        """Create alien fleet (2nd line). Same method as befor"""

        enemy_bullet = EnemyBullet(self)
        enemy_bullet_width, enemy_bullet_height = enemy_bullet.rect.size

        space_x = enemy_bullet.rect.x / self.settings.alien_adjustment
        available_space_x = self.settings.screen_width - \
            (2 * space_x + enemy_bullet_width)
        number_enemy_bullet_x = int(
            available_space_x // (2 * space_x + enemy_bullet_width))

        ship_height = self.ship.rect.height
        space_y = enemy_bullet.rect.y / self.settings.alien_adjustment
        available_space_y = (self.settings.screen_height -
                             (3 * enemy_bullet_height) - ship_height)
        number_rows = int(available_space_y // (space_y + enemy_bullet_height))

        num1 = random.randint(0, number_rows - 1)   # Generate random number for power up.
        num2 = random.randint(0, number_enemy_bullet_x - 1)     # Generate random number for power up.

        for row_number in range(number_rows):
            for number_enemy_bullet in range(number_enemy_bullet_x):
                self._create_enemy_bullet(
                    number_enemy_bullet, row_number, num1, num2)

    def _create_enemy_bullet(self, number_enemy_bullet, row_number, num1, num2):
        """Create an enemy bullet and place it in the row."""

        enemy_bullet = EnemyBullet(self)
        enemy_bullet_width, enemy_bullet_height = enemy_bullet.rect.size
        if row_number == num1 and number_enemy_bullet == num2: # If randomly generated numbers match, create power-up.
            enemy_bullet.bonus = True
            # print(f"Selected power up position (row:column): {num1}:{num2}")  # Check position of power-up.

        space_x = enemy_bullet.rect.x / self.settings.alien_adjustment
        enemy_bullet.x = (
            space_x + (1.5 * space_x + enemy_bullet_width) * number_enemy_bullet)
        enemy_bullet.rect.x = enemy_bullet.x

        space_y = enemy_bullet.rect.y / self.settings.alien_adjustment
        enemy_bullet.y = 4 * space_y + \
            (space_y + enemy_bullet_height) * row_number
        enemy_bullet.rect.y = enemy_bullet.y
        self.enemy_bullets.add(enemy_bullet)

    def _check_fleet_edges(self):
        """Respond appropriately if 1st line alien hits an edge."""

        for alien in self.aliens.sprites(): # Check all alien in the aliens sprite.
            if alien.check_edges():     # If hits edge change direction (1st and 2nd line).
                self._change_fleet_direction()
                self._change_enemy_bullets_fleet_direction()
                break   # Break out from loop.
            elif not alien.check_edges():   # If 1st line does not hit edge, but not empty, check 2nd line.
                self._check_enemy_bullets_edges()
                break

        if not self.aliens:     # If 1st line aliens empty, check only 2nd line.
            self._check_enemy_bullets_edges()

    def _check_enemy_bullets_edges(self):
        """Respond appropriately 2nd line alien hits an edge."""

        for enemy_bullet in self.enemy_bullets.sprites():
            if enemy_bullet.check_edges():
                self._change_enemy_bullets_fleet_direction()
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _change_enemy_bullets_fleet_direction(self):

        for enemy_bullet in self.enemy_bullets.sprites():
            enemy_bullet.rect.y += self.settings.fleet_drop_speed
        self.settings.enemy_bullet_direction *= -1

    def _update_aliens(self):
        """A simple method containing all movement for aliens."""

        if self.sb.power_type == 2 and self.settings.count_pause <= 160:    # Freeze aliens.
            self.settings.count_pause += 1
            # print(f"Time until freeze stops: {self.settings.count_pause}")    # For verification.

        else:
            self._check_fleet_edges()   # Chech collision between aliens and edges.
            self.aliens.update()    # Update each alien in aliens sprite.
            self.enemy_bullets.update()   # Update each alien in enemy_bullets sprite.
            self._check_aliens_bottom()     # Collision 1st line aliens - bottom.
            self._check_enemy_bullets_bottom()  # Collision 2nd line aliens - bottom.

            if pygame.sprite.spritecollideany(self.ship, self.aliens):  # Check alien-ship collision. Returns None, if no collision
                self._ship_hit()    # Arguments: sprite & group (all members).
            if pygame.sprite.spritecollideany(self.ship, self.enemy_bullets):
                self._ship_hit()

    def _check_enemy_bullets_bottom(self):
        screen_rect = self.screen.get_rect()
        for enemy_bullet in self.enemy_bullets.sprites():
            if enemy_bullet.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_aliens_bottom(self):
        """Check if an alien have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 1:   # If life not empty.
            self.stats.ships_left -= 1  # Decrement ships left.
            self.sb.prep_ships()    # Update scoreboard.
            self._reset_screen()    # Reset screen contents.
            sleep(1.0)
        else:
            self._return_menu()     # If no more ship left, open menu.

    def _return_menu(self):
        """If more life left, reinitialize the screen."""

        self.stats.game_active = False  # Set game incactive.
        self.sb.ships.empty()   # Get rid of ships.
        self._reset_screen()
        pygame.mouse.set_visible(True)

    def _reset_screen(self):
        """When game ends, reset screen."""

        self.clouds.empty()     # Get rid of clouds.
        self.aliens.empty()     # Get rid of 1st line aliens
        self.enemy_bullets.empty()  # Get rid of 2nd line aliens
        self.bullets.empty()    # Get rid of bullets.

        self.po.status = False      # Reset power-up status (off).
        self.sb.power_type = 0      # Reset power type (off).
        self.settings.count_pause = 0   # Reset count_pause.

        self._create_cloud()    # Generate new sprite group of clouds.
        self._create_fleet_of_enemy_bullet()    # Generate new 2nd line aliens.
        self._create_fleet()    # Generate new 1st line aliens
        self.settings.enemy_bullet_direction = abs(
            self.settings.enemy_bullet_direction)   # Make sure  2nd line aliens go to the rigth.
        self.settings.fleet_direction = abs(self.settings.fleet_direction)  # Make sure  1st line aliens go to the rigth.
        self.ship.center_ship()     # Re-center ship's position.

    def _create_cloud(self):
        """Create clouds in random position (x, y)."""

        number_clouds = int(self.settings.clouds_total)     # Make sure it's an integer.
        for number in range(number_clouds):     # Generate clouds.
            cloud = Cloud(self)     # Create Cloud instance
            self.clouds.add(cloud)  # Add cloud to clouds sprote.

    def _update_screens(self):
        """Update images on the screen, and flip to the new screen."""

        self.screen.fill(self.settings.bg_color)    # Fill screen with background color.
        self.clouds.draw(self.screen)       # Draw clouds.

        if self.stats.game_active:      # If game mode is active, draw ship.
            self.ship.blitme()

        if self.stats.game_active:      # If game is active, draw bullets.
            for bullet in self.bullets.sprites():
                bullet.blitme()

        if self.stats.game_active:      # If game is active draw 2nd line aliens.
            self.enemy_bullets.draw(self.screen)

        if self.stats.game_active:
            self.aliens.draw(self.screen)   # If game is active draw 1st line aliens.

        if self.settings.dif_level == "Easy" and self.stats.game_active:    # If easy level and active game:
            self.sb.show_el_score()     # draw the score information.

        if self.settings.dif_level == "Normal" and self.stats.game_active:
            self.sb.show_nl_score()

        if self.settings.dif_level == "Hard" and self.stats.game_active:
            self.sb.show_hl_score()

        if not self.stats.game_active:  # Draw menu buttons if game is inactive.
            self.buttons.draw_button()

        if self.po.status:      # Drae power-ups.
            self.po.blitme()

        pygame.display.flip()   # COntinuous update of recent screen settings.

    def _save_high_score(self):
        """Save highscore data, when quitting game."""

        date = self.full_date   # Get date (dd/mm/yy).
        player_name = self.entry    # Get player's name.

        highscores = [self.stats.el_high_score, self.stats.nl_high_score, self.stats.hl_high_score]     # Get high scores.
        myFiles = ['el_high_scores.txt', 'nl_high_scores.txt', 'hl_high_scores.txt']     # Read old high scores from files.
        cwd = os.getcwd()   # Get current working directory (cwd).

        for file_name, highscore in zip(myFiles, highscores):   # Read old highscores.
            with open(os.path.join(cwd, file_name), encoding='utf-8') as f:
                contents = f.read()     # Read file contents.
            words = contents.split()    # Split content to list of entries.
            old_high_score = words[-1]  # Get last entry.

            if int(highscore) > int(old_high_score):    # If new hiighscore, save it.
                with open(os.path.join(os.getcwd(), file_name), 'w') as f:
                    f.write(f"{date} {player_name} {highscore}")    # Save info to file.

if __name__ == '__main__':
    ai = AlienInvasion()    # Game instance.
    ai.run_game()       # Run the game.
