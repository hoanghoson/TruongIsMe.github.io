import pygame.font
from pygame.sprite import Group
from chicken_ship import Ship

class ScoreBoard():
    def __init__(self,cs_game):
        """Initialize the ScoreBoard"""
        self.cs_game = cs_game
        self.screen = cs_game.screen
        self.settings = cs_game.settings
        self.screen_rect = cs_game.screen.get_rect()
        self.starts = cs_game.starts

        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

    def prep_score(self):
        roud_score = round(self.starts.score,-1)
        score_str = "{:,}".format(roud_score)
        self.score_image = self.font.render("Score "+score_str,True,self.text_color,self.settings.background_color)

        #Display the score
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right =self.screen_rect.right-20
        self.score_rect.top = 20


    def prep_high_score(self):
        high_score = round(self.starts.high_score,-1)
        high_score_str ="{:,}".format(high_score)
        high_score_txt="High Score"
        self.hs_image = self.font.render(high_score_str,True,self.text_color,self.settings.background_color)
        self.hs_image_text = self.font.render(high_score_txt,True,self.text_color,self.settings.background_color)
        # Display the hight score
        self.high_score_rect = self.hs_image.get_rect()
        self.high_score_rect_1 = self.hs_image.get_rect()

        self.high_score_rect.center= self.screen_rect.center
        self.high_score_rect_1.center= self.screen_rect.center

        self.high_score_rect.top = 60
        self.high_score_rect_1.top= 10

    def prep_level(self):
        level_str = str(f"Level {self.starts.level_start}")

        self.lv_image = self.font.render(level_str, True, self.text_color, self.settings.background_color)

        # Display the level
        self.level_rect = self.lv_image.get_rect()
        self.level_rect.right = self.screen_rect.right-20
        self.level_rect.top = 60

    def prep_ship(self):
        self.ships = Group()
        for ship_number in range(self.starts.ships_left):
            ship = Ship(self.cs_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hs_image, self.high_score_rect)
        self.screen.blit(self.lv_image,self.level_rect)
        self.screen.blit(self.hs_image_text,self.high_score_rect_1)
        self.ships.draw(self.screen)

    def _check_high_score(self):
        if self.starts.score > self.starts.high_score:
            self.starts.high_score = self.starts.score
            self.prep_high_score()



