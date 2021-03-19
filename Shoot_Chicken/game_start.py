
class GameStart:
    def __init__(self,cs_game):
        self.settings = cs_game.settings
        self.reset_starts()
        self.game_active = False
        self.score = 0
        self.high_score = 0
        self.level_start =0
    def reset_starts(self):
        self.ships_left = self.settings.ship_limit
