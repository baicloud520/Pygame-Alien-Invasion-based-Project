import os


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""

        self.settings = ai_game.settings    # Initialize game settings.

        self.reset_el_stats()   # Initialize easy level statistics.
        self.reset_nl_stats()   # Initialize normal level statistics.
        self.reset_hl_stats()   # Initialize hard level statistics.

        self.game_active = False    # Start game in an inactive state.

        myFiles = ['el_high_scores.txt',
                   'nl_high_scores.txt', 'hl_high_scores.txt']  # Initialize highscores from earlier games.
        cwd = os.getcwd()

        # Empty list to store highscores from earlier games.
        initialize_highscore = []
        for file_name in myFiles:
            with open(os.path.join(cwd, file_name), encoding='utf-8') as f:
                contents = f.read()     # Read file contents.
            words = contents.split()    # Split items of each file.
            old_highscore = words[-1]   # Get last item (highscore).
            # Add it to list initialize_highscore.
            initialize_highscore.append(old_highscore)

        # Initialize easy level highscore.
        self.el_high_score = int(initialize_highscore[0])
        # Initialize normal level highscore.
        self.nl_high_score = int(initialize_highscore[1])
        # Initialize hard level highscore.
        self.hl_high_score = int(initialize_highscore[2])

    def reset_el_stats(self):
        """Initialize statistics, for easy level, that can be change during the game."""

        # Number of available ships.
        self.ships_left = self.settings.ship_limit
        self.score = 0      # Score.
        self.level = 1      # Level.

    def reset_nl_stats(self):
        """Initialize statistics, for normal level, that can be change during the game."""

        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def reset_hl_stats(self):
        """Initialize statistics, for hard level, that can be change during the game."""

        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
