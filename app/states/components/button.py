import pygame
from pygame.locals import *
from app.constants import *

class Button:
    def __init__(self, text, x, y, callback, width=200, height=50, font_size=24):
        self.text = text
        self.x = x
        self.y = y
        self.callback = callback
        self.width = width
        self.height = height
        self.font_size = font_size
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

    def set_text(self, text):
        self.text = text

    def draw(self, canvas):
        # Draw the button with a shadow bottom and right
        pygame.draw.rect(canvas, BUTTON_BACKGROUND, self.rect)
        pygame.draw.line(canvas, BUTTON_SHADOW, (self.x - self.width // 2, self.y + self.height // 2), (self.x + self.width // 2, self.y + self.height // 2), 2)
        pygame.draw.line(canvas, BUTTON_SHADOW, (self.x + self.width // 2, self.y - self.height // 2), (self.x + self.width // 2, self.y + self.height // 2), 2)

        # Draw the text
        font = pygame.font.Font(relative_resource_path("app/assets/fonts/pixel_font.ttf"), self.font_size)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x, self.y)

        # get text width. if over the button, scale it down
        text_width = text_rect.width
        text_height = text_rect.height
        if text_width > self.width:
            text_surface = pygame.transform.scale(text_surface, (self.width - 10, text_height))
            text_rect = text_surface.get_rect()
            text_rect.center = (self.x, self.y)
        
        # Blit the text
        canvas.blit(text_surface, text_rect)

    def update_size_and_position(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

    def handle_click(self, event):
        if event.type == MOUSEBUTTONUP:
            # Get the mouse position in screen coordinates
            screen_mouse_pos = pygame.mouse.get_pos()

            # Convert the mouse position to canvas coordinates
            screen_width, screen_height = pygame.display.get_surface().get_size()
            canvas_width, canvas_height = SCREEN_WIDTH, SCREEN_HEIGHT  # Use your base resolution here
            canvas_mouse_pos = (
                screen_mouse_pos[0] * (canvas_width / screen_width),
                screen_mouse_pos[1] * (canvas_height / screen_height),
            )

            # Check if the button was clicked
            if self.rect.collidepoint(canvas_mouse_pos):
                self.callback()

