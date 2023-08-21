import pygame
from pyvidplayer2 import Video
from app.constants import *
from app.states.state import State

class Tutorial(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        # Create a Video instance
        self.vid = Video(relative_resource_path("app/assets/videos/tutorial.mp4"))

        # pause music from pygame
        pygame.mixer.music.pause()  

        # Set up Pygame display
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(self.vid.name)

    def draw(self, surface):
        # Update the video frame
        if self.vid.draw(self.win, (0, 0), force_draw=False):
            pygame.display.update()

        # Update the screen
        pygame.display.flip()

    def handle_event(self, event):
        # if spacebar is pressed, toggle play/pause
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.vid.toggle_pause()
        # if escape is pressed, stop the video and return to main menu
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.vid.stop()
            self.game.show_main_menu()
        # if video is finished, return to main menu
        elif event.type == pygame.USEREVENT and event.code == "finished":
            self.game.show_main_menu()
        # if video is paused, seek forward/backward
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if key == "r":
                self.vid.restart()
            elif key == "right":
                self.vid.seek(15)
            elif key == "left":
                self.vid.seek(-15)
            elif key == "up":
                self.vid.set_volume(1.0)
            elif key == "down":
                self.vid.set_volume(0.0)
