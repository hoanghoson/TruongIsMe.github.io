import sys
import pygame
from time import sleep
from setting_game import Settings
from chicken_ship import Ship
from bullet import Bullet
from chicken import Chicken
from game_start import GameStart
from score_board import ScoreBoard
from button import Button


class ChickenManage:
    def __init__(self):
        """Initialize the manage game"""
        pygame.init()
        # instance of settings
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.bg_color = self.settings.background_color
        pygame.display.set_caption("Shooting Chicken")
        self.starts = GameStart(self)
        self.score_board = ScoreBoard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.chickens = pygame.sprite.Group()
        self.file_save = 'score.txt'
        self._create_fleet()
        self.HIGH_SCORE = []
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the game"""
        while True:
            self._check_events()
            if self.starts.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_chicken()
            # else:
            # self.file_handler_write(self.HIGH_SCORE)
            self._update_screen()

    def _check_events(self):
        # Watch keyboard the mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_events_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_events_keyup(event)

    def _check_events_keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE or event.key == pygame.K_t:
            self._fire_bullet()

    def _check_events_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_play_button(self, mouse_pos):
        """Colllist mouse button"""
        buton_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if buton_clicked and not self.starts.game_active:
            # reset dinamic speed
            self.settings._dinamic_settings()
            # reset the game
            self.starts.reset_starts()
            self.starts.game_active = True

            # restore score and level
            self.starts.score = 0
            self.score_board.prep_score()

            self.starts.level_start = 0
            self.score_board.prep_level()

            self.score_board.prep_ship()
            # get rid of any remaining chickens and buulet
            self.chickens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(True)

    def _fire_bullet(self):
        """Create a new bullet and add it the group"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        # Get grid of bullet
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_chicken_collisions()

    def _check_bullet_chicken_collisions(self):
        # check for any bullet that have hitss chicken
        collisions = pygame.sprite.groupcollide(self.bullets, self.chickens, True, True)
        if collisions:
            for chicken in collisions.values():
                self.starts.score += self.settings.chicken_score * len(chicken)
            self.score_board.prep_score()
            self.score_board._check_high_score()
        if not self.chickens:
            # Desttroy bullet and crete new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings._increase_speed()
            # _increase_levels
            self.starts.level_start += 1
            self.score_board.prep_level()

    def _create_fleet(self):
        new_chicken = Chicken(self)
        chicken_width, chicken_height = new_chicken.rect.size
        # get x
        available_space_x = self.settings.screen_width - (2 * chicken_width)
        number_of_chicken_x = available_space_x // (2 * chicken_width)

        # get hight ship and get y
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - 5 * chicken_height - ship_height
        number_of_rows = available_space_y // (2 * chicken_height)

        # Create full chicken
        for row in range(number_of_rows):
            for column in range(number_of_chicken_x):
                self._create_chicken(column, row)

    def _create_chicken(self, number_of_chicken_x, row_number):
        new_chicken = Chicken(self)
        chicken_width, chicken_height = new_chicken.rect.size
        new_chicken.x = chicken_width + 2 * chicken_width * number_of_chicken_x + 20
        new_chicken.rect.x = new_chicken.x
        new_chicken.rect.y = new_chicken.rect.height * 2 + 2 * new_chicken.rect.height * row_number
        self.chickens.add(new_chicken)

    def _update_chicken(self):
        self._check_fleet_edges()
        self.chickens.update()
        # chicken collisions with ship
        if pygame.sprite.spritecollideany(self.ship, self.chickens):
            self._ship_hit()
        self._check_chiken_edges_bottom()

    def _check_chiken_edges_bottom(self):
        screen_rect = self.screen.get_rect()
        for chicken in self.chickens.sprites():
            if chicken.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        # decrease ships left
        if self.starts.ships_left > 0:
            self.starts.ships_left -= 1
            self.score_board.prep_ship()

            self.chickens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.starts.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        for chicken in self.chickens.sprites():
            if chicken.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # fleet drop
        for chicken in self.chickens.sprites():
            chicken.rect.y += self.settings.fleet_drop_speed
        # chang direction fleet to left and right
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # Redraw screen during game begin
        self.screen.fill(self.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.chickens.draw(self.screen)
        self.score_board.show_score()
        if not self.starts.game_active:
            self.play_button.draw_button()
        # Make the most recenttly draw screen
        pygame.display.flip()

    # def file_handler_read(self):
    # with open(self.file_save, mode='r', encoding='utf-8') as file_opject:

    # def file_handler_write(self , HIGH_SCORE):
    #     with open(self.file_save, "a+", encoding='utf-8') as file_opject:
    #         HIGH_SCORE.append(self.starts.high_score)
    #         file_opject.write(f"{self.starts.high_score}")


if __name__ == "__main__":
    cs = ChickenManage()
    cs.run_game()
