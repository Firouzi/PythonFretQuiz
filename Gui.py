import pygame

class GuiButton:
    def __init__(self,
                 name,
                 text_surface,
                 position,
                 mode = "ANY",  # "ANY", "SETUP", "NOTE_QUIZ"...
                 button_color = (200, 200, 0),
                 button_thickness = 10):
        self.name = name
        self.text_surface = text_surface
        self.position = position
        self.mode = mode
        self.button_color = button_color
        self.button_thickness = button_thickness

        self.is_active = True
        bounding_rect = text_surface.get_bounding_rect()
        self.width = bounding_rect[2]
        self.height = bounding_rect[3]
        self.button_rect = pygame.Rect(position[0] - 15,
                                       position[1] + 10,
                                       self.width + 30,
                                       self.height + 15)

    def checkClick(self, pos):
        if self.is_active:
            if self.button_rect[0] < pos[0] < self.button_rect[0] + self.button_rect[2]:
                if self.button_rect[1] < pos[1] < self.button_rect[1]+ self.button_rect[3]:
                    return True
        return False

    def render(self, screen):
        if self.is_active:
            screen.blit(self.text_surface, self.position)
            pygame.draw.rect(screen,
                             self.button_color,
                             self.button_rect,
                             self.button_thickness)


#non interactive text
class GuiText:
    def __init__(self,
                 name,
                 text_surface,
                 position,
                 mode = "ANY"):
        self.name = name
        self.text_surface = text_surface
        self.position = position
        self.mode = mode

        self.is_active = True

    def render(self, screen):
        if self.is_active:
            screen.blit(self.text_surface, self.position)

class GuiContainer:
    def __init__(self,
                 gui_widgets,
                 screen):
        self.gui_widgets = gui_widgets
        self.screen = screen
        self.mode = "SETUP"

    def setMode(self, mode):
        self.mode=mode

    def checkClick(self, pos):
        for widget in self.gui_widgets:
            if widget.mode == "ANY" or widget.mode == self.mode:
                if widget.checkClick(pos):
                    return widget
        return None

    def render(self):
        for widget in self.gui_widgets:
            if widget.mode =="ANY" or widget.mode == self.mode:
                widget.render(self.screen)
