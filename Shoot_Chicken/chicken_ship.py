
import pygame
from setting_game import Settings
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,cs_game):
        """Initialize the Ship"""
        super().__init__()
        self.screen = cs_game.screen
        self.screen_rect = cs_game.screen.get_rect()

        self.settings = cs_game.settings
        # Load the ship and get it rect
        self.image = pygame.image.load(self.settings.ship_image)
        self.rect = self.image.get_rect()


        self.moving_right= False
        self.moving_left = False
        # Start the ship in the bottom
        self.center_ship()
    def update(self):
        """Update move ship"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # Update moving speed
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
    def blitme(self):
        """Draw the ship at it current location"""
        self.screen.blit(self.image,self.rect)

