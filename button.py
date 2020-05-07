import pygame.font  # Render text to the screen.


class Button:
    """Creation of simple buttons for a game."""

    def __init__(self, ai_game):
        """Initialize button attributes."""

        self.screen = ai_game.screen    # Initialize game screen.
        self.settings = ai_game.settings    # Initialize game settings.
        self.screen_rect = self.screen.get_rect()   # Get screen dimension.

        # Build the info button's rect object and center it.
        # self.ib_rect = pygame.Rect(
        #     0, 0, self.settings.dlpb_width, self.settings.dlpb_height)
        # self.ib_rect.center = (self.settings.screen_width - 105,
        #                        self.settings.screen_height - 40)

        self.elpb_rect = pygame.Rect(
            0, 0, self.settings.dlpb_width, self.settings.dlpb_height)  # Easy level play button rect object.
        self.elpb_rect.center = ((self.settings.screen_width / 2),
                                 (self.settings.screen_height / 2) - (self.settings.screen_height / 8))  # Easy level play button position.

        self.nlpb_rect = pygame.Rect(
            0, 0, self.settings.dlpb_width, self.settings.dlpb_height)  # Normal level play button rect object.
        self.nlpb_rect.center = (
            (self.settings.screen_width / 2), (self.settings.screen_height / 2))    # Normal level play button position.

        self.hlpb_rect = pygame.Rect(
            0, 0, self.settings.dlpb_width, self.settings.dlpb_height)  # Hard level play button rect object.
        self.hlpb_rect.center = ((self.settings.screen_width / 2),
                                 (self.settings.screen_height / 2) + (self.settings.screen_height / 8))  # Hard level play button position.

        self.acpb_rect = pygame.Rect(
            0, 0, self.settings.dlpb_width, self.settings.dlpb_width)   # Alarm clock power-up play button rect object.
        self.acpb_rect.center = ((1 * self.settings.screen_width / 6) + (self.settings.dlpb_width / 2.0),
                                 (self.settings.screen_height / 2) + self.settings.dlpb_height)     # Alarm clock power-up play button position.

        self.hvpb_rect = pygame.Rect(
            0, 0, self.settings.dlpb_width, self.settings.dlpb_width)   # High voltage power-up play button rect object.
        self.hvpb_rect.center = ((3 * self.settings.screen_width / 6),
                                 (self.settings.screen_height / 2) + self.settings.dlpb_height)     # High voltage power-up play button position.

        self.exlpb_rect = pygame.Rect(
            0, 0, self.settings.dlpb_width, self.settings.dlpb_width)   # Extra life power-up play button rect object.
        self.exlpb_rect.center = ((5 * self.settings.screen_width / 6) - (self.settings.dlpb_width / 2.0),
                                  (self.settings.screen_height / 2) + self.settings.dlpb_height)    # Extra life power-up play button position.

    def prep_menu_msgs(self, msg1, msg2):
        """Turn msg into a rendered image and center text on the button."""

        self.gdb_msg_image = self.settings.pb_font.render(
            msg1, True, self.settings.pb_text_color, False)
        self.gdb_msg_image_rect = self.gdb_msg_image.get_rect()
        self.gdb_msg_image_rect.center = (
            (self.settings.screen_width / 2), (self.settings.screen_height / 2) - (self.settings.screen_height / 4))

        self.glb_msg_image = self.settings.pb_font.render(
            msg2, True, self.settings.pb_text_color, False)
        self.glb_msg_image_rect = self.glb_msg_image.get_rect()
        self.glb_msg_image_rect.center = (
            (self.settings.screen_width / 2), self.settings.screen_height - (self.settings.screen_height / 6))

    def prep_difficulty_level_msgs(self, easy, normal, hard):
        """Turn msg into a rendered image and center text on the button."""

        self.elpb_msg_image = self.settings.dlpb_font.render(
            easy, True, self.settings.dlpb_text_color, self.settings.elpb_button_color)
        self.elpb_msg_image_rect = self.elpb_msg_image.get_rect()
        self.elpb_msg_image_rect.center = (
            (self.settings.screen_width / 2), (self.settings.screen_height / 2) - (self.settings.screen_height / 8))

        self.nlpb_msg_image = self.settings.dlpb_font.render(
            normal, True, self.settings.dlpb_text_color, self.settings.nlpb_button_color)
        self.nlpb_msg_image_rect = self.nlpb_msg_image.get_rect()
        self.nlpb_msg_image_rect.center = (
            (self.settings.screen_width / 2), (self.settings.screen_height / 2))

        self.hlpb_msg_image = self.settings.dlpb_font.render(
            hard, True, self.settings.dlpb_text_color, self.settings.hlpb_button_color)
        self.hlpb_msg_image_rect = self.hlpb_msg_image.get_rect()
        self.hlpb_msg_image_rect.center = (
            (self.settings.screen_width / 2), (self.settings.screen_height / 2) + (self.settings.screen_height / 8))

    def prep_lucky_box(self, msg):
        """Center power-up images on corresponding buttons."""

        self.lb_msg = self.settings.pb_font.render(
            msg, True, self.settings.pb_text_color, False)
        self.lb_msg_rect = self.lb_msg.get_rect()
        self.lb_msg_rect.center = (
            (self.settings.screen_width / 2), (self.settings.screen_height / 2) - (2 * self.settings.pb_height))

        self.ac_image = self.settings.lucky_box_1   # Assign alarm clock image.
        self.ac_image_rect = self.ac_image.get_rect()
        self.ac_image_rect.center = ((1 * self.settings.screen_width / 6) + (self.settings.dlpb_width / 2.0),
                                     (self.settings.screen_height / 2) + self.settings.dlpb_height)

        # Assign high voltage image.
        self.hv_image = self.settings.lucky_box_2
        self.hv_image_rect = self.hv_image.get_rect()
        self.hv_image_rect.center = ((3 * self.settings.screen_width / 6),
                                     (self.settings.screen_height / 2) + self.settings.dlpb_height)

        self.exl_image = self.settings.lucky_box_3  # Assign freeze image.
        self.exl_image_rect = self.hv_image.get_rect()
        self.exl_image_rect.center = ((5 * self.settings.screen_width / 6) - (self.settings.dlpb_width / 2.0),
                                      (self.settings.screen_height / 2) + self.settings.dlpb_height)

    # def prep_ib_msg(self, msg):
    #     """Turn msg into a rendered image and center text on the button."""

    #     self.ib_msg_image = self.settings.dlpb_font.render(
    #         msg, True, self.settings.pb_text_color, self.settings.ib_button_color)
    #     self.ib_msg_image_rect = self.ib_msg_image.get_rect()
    #     self.ib_msg_image_rect.center = (self.settings.screen_width - 105,
    #                                      self.settings.screen_height - 40)

    def prep_pause_menu_msgs(self, msg1, msg2, msg3, msg4):
        """A simple method to prepare pause menu messages."""

        self.pmsg = self.settings.pb_font.render(
            msg1, True, self.settings.pb_text_color, False)
        self.pmsg_rect = self.pmsg.get_rect()
        self.pmsg_rect.center = (
            (self.settings.screen_width / 2), (self.settings.screen_height / 2) - self.settings.pb_height)

        self.pmsg_ic = self.settings.dlpb_font.render(
            msg2, True, self.settings.pb_text_color, False)
        self.pmsg_rect_ic = self.pmsg_ic.get_rect()
        self.pmsg_rect_ic.center = (
            (self.settings.screen_width / 2), (self.settings.screen_height / 2) + self.settings.dlpb_height)

        self.pmsg_im = self.settings.dlpb_font.render(
            msg3, True, self.settings.pb_text_color, False)
        self.pmsg_rect_im = self.pmsg_im.get_rect()
        self.pmsg_rect_im.center = (
            (self.settings.screen_width / 2), (self.settings.screen_height / 2) + (2 * self.settings.dlpb_height))

        self.pmsg_iq = self.settings.dlpb_font.render(
            msg4, True, self.settings.pb_text_color, False)
        self.pmsg_rect_iq = self.pmsg_iq.get_rect()
        self.pmsg_rect_iq.center = (
            (self.settings.screen_width / 2), (self.settings.screen_height / 2) + (3 * self.settings.dlpb_height))

    def draw_pause_msgs(self):
        """Draw pause menu messages."""

        self.screen.blit(self.pmsg, self.pmsg_rect)
        self.screen.blit(self.pmsg_ic, self.pmsg_rect_ic)
        self.screen.blit(self.pmsg_im, self.pmsg_rect_im)
        self.screen.blit(self.pmsg_iq, self.pmsg_rect_iq)

    def draw_button(self):
        """Draw blank button and then draw message."""

        # self.screen.fill(self.settings.pb_button_color, self.pb_rect) # To check rect and image position overlap.
        self.screen.blit(self.gdb_msg_image, self.gdb_msg_image_rect)
        self.screen.blit(self.glb_msg_image, self.glb_msg_image_rect)
        # self.screen.blit(self.ib_msg_image, self.ib_msg_image_rect)
        self.screen.fill(self.settings.elpb_button_color,
                         self.elpb_rect)
        self.screen.blit(self.elpb_msg_image, self.elpb_msg_image_rect)
        self.screen.fill(self.settings.nlpb_button_color,
                         self.nlpb_rect)
        self.screen.blit(self.nlpb_msg_image, self.nlpb_msg_image_rect)
        self.screen.fill(self.settings.hlpb_button_color,
                         self.hlpb_rect)
        self.screen.blit(self.hlpb_msg_image, self.hlpb_msg_image_rect)

    def draw_lucky_box(self):
        """Draw contents of lucky box."""

        self.screen.blit(self.lb_msg, self.lb_msg_rect)
        # self.screen.fill(self.settings.pb_button_color, self.acpb_rect) # To check rect and image position overlap.
        self.screen.blit(self.ac_image, self.ac_image_rect)
        self.screen.blit(self.hv_image, self.hv_image_rect)
        self.screen.blit(self.exl_image, self.exl_image_rect)
