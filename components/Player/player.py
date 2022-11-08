class Player:
    def __init__(self):
        self.player = '█'
        self.player_x = 10
        self.player_y = 10

        self.player_x_input = 0
        self.player_y_input = 0

        self.player_attack = 0
        self.player_attack_start_position = (0,0)
        self.player_attack_step = 0
