class Button:
    def __init__(self, pygame, window, background_color, position, size=None, border_radius=3, font=None, text=None,
                 text_color=None, hover_color_degree=15):
        self.window = window
        self.pygame = pygame
        self.font = font
        self.border_radius = border_radius
        self.background_color = background_color
        self.text_color = text_color
        self.hover_color_degree = hover_color_degree
        self.text = text
        self.button_pos_x = position[0]
        self.button_pos_y = position[1]
        if self.font is not None:
            self.bFont = self.font.render(self.text, True, self.text_color)
        else:
            self.bFont = None
        if size is None:
            self.button_size_x = None
            self.button_size_y = None
            if self.bFont is not None:
                self.button_size_x = self.bFont.get_width() + 10
                self.button_size_y = self.bFont.get_height() + 10
                self.button_pos_x -= self.button_size_x / 2
                self.button_pos_y -= self.button_size_y / 2
        else:
            self.button_size_x = size[0]
            self.button_size_y = size[1]
        self.state_hover = True
        self.draw_button()
        self.draw_text()

    def update(self):
        if self.is_mouse_in():
            self.hover()
        else:
            self.draw_button()

    def is_mouse_in(self):
        mouse_pos = self.pygame.mouse.get_pos()
        max_x = self.button_size_x + self.button_pos_x
        min_x = self.button_pos_x
        max_y = self.button_size_y + self.button_pos_y
        min_y = self.button_pos_y
        return max_x >= mouse_pos[0] >= min_x and max_y >= mouse_pos[1] >= min_y

    def draw_button(self, force=False):
        if self.state_hover or force:
            self.state_hover = False
            self.pygame.draw.rect(self.window, self.background_color,
                                  (self.button_pos_x, self.button_pos_y, self.button_size_x, self.button_size_y),
                                  border_radius=self.border_radius)
            self.pygame.display.update()
            self.draw_text()

    def hover(self):
        if not self.state_hover:
            self.state_hover = True
            hover_color = [max(0, x - self.hover_color_degree) for x in self.background_color]
            self.pygame.draw.rect(self.window, hover_color,
                                  (self.button_pos_x, self.button_pos_y, self.button_size_x, self.button_size_y),
                                  border_radius=self.border_radius)
            self.pygame.display.update()
            self.draw_text()

    def draw_text(self):
        if self.font is not None:
            font_pos_x = self.button_pos_x + (self.button_size_x / 2) - (self.bFont.get_width() / 2)
            self.window.blit(self.bFont, (font_pos_x, self.button_pos_y))
        self.pygame.display.update()
