
import pygame
from pygame.sprite import Sprite

class Chicken(Sprite):
    def __init__(self,cs_game):
        super().__init__()
        self.screen = cs_game.screen
        self.settings = cs_game.settings

        # Load  image and get_rect
        self.image = pygame.image.load(self.settings.chicken_image)
        self.rect = self.image.get_rect()

        # Store each new chicken new the top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right > screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # Move chicken
        self.x += self.settings.chicken_speed * self.settings.fleet_direction
        # update again
        self.rect.x = self.x




