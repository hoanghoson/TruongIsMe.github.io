
class Settings:
    def __init__(self):
        self._static_settings()
        self._dinamic_settings()


    def _static_settings(self):
        self.screen_height, self.screen_width =800, 1400
        self.background_color = (253, 140, 255)
        # Ship
        self.ship_image = "images/ship.png"
        self.ship_limit = 2

        # Bullet
        self.bullet_width =10
        self.bullet_height = 15
        self.bullet_color = (0, 0, 0)

        # Chicken
        self.chicken_image = "images/chicken.png"
        self.fleet_drop_speed = 17
        self.speed_up_scale = 1.1

    def _dinamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed =1.0
        self.chicken_speed = 0.5
        self.chicken_score = 50
        self.score_scale =1.5

        # 1 is right -1 is left
        self.fleet_direction = 1

    def _increase_speed(self):
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.chicken_speed *= self.speed_up_scale
        self.chicken_score = int(self.chicken_score * self.speed_up_scale)
