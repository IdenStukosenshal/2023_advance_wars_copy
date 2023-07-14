
class Settings:
    def __init__(self):
        self.screen_w = 1216
        self.screen_h = 896
        self.fps = 30
        self.w_and_h_sprite_map = 64  # 64 пикселя
        self.max_value = 90
        self.weights_track = {'#': 1.5, 'd': 1, 'f': 2, '@': self.max_value, 'v': self.max_value, 't': 1.125, 'inaccessible': self.max_value}
        self.weights_inf = {'#': 1, 'd': 1, 'f': 1.3, '@': 2, 'v': 2, 't': 1, 'inaccessible': self.max_value}

        self.recon_points = 6
        self.speed = 16 # пикселя за кадр




