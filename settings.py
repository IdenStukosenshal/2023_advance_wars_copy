
class Settings:
    def __init__(self):
        self.screen_w = 1216
        self.screen_h = 896
        self.fps = 30
        self.w_and_h_sprite_map = 64  # 64 пикселя
        self.max_value = 90
        self.weights_track = {'#': 1.5, 'd': 1, 'f': 2, '@': self.max_value, 'v': self.max_value, 't': 1.25, 'inaccessible': self.max_value}
        self.weights_inf = {'#': 1, 'd': 1, 'f': 1.3, '@': 2, 'v': 2, 't': 1, 'inaccessible': self.max_value}
        self.weights_heli = {'#': 1, 'd': 1, 'f': 1, '@': 1, 'v': 1, 't': 1, 'inaccessible': self.max_value}

        self.recon_points = 6
        self.infantry_points = 3
        self.tank_points = 5
        self.helicopter_points = 6

        self.speed = 32  # пикселей за кадр, должно быть кратно размеру спрайта, иначе не будет точного попадания в координаты

        self.infantry_type = 'infantry'
        self.recon_type = 'recon'
        self.helicopter_type = 'helicopter'

        self.list_all_types = [self.infantry_type, self.recon_type, self.helicopter_type]
        self.all_weights = {self.recon_type: self.weights_track, self.infantry_type: self.weights_inf, self.helicopter_type: self.weights_heli}




