
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,cs_game):
        super().__init__()
        self.screen = cs_game.screen
        self.settings = cs_game.settings
        self.color = self.settings.bullet_color

        # Create a rect for bullet
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        # pUt bullet mid top the ship
        self.rect.midtop = cs_game.ship.rect.midtop

        self.y = float(self.rect.y)
    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)