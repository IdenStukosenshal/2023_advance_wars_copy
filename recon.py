import pygame
from pygame.sprite import Sprite


class Recon(Sprite):
    """розвiдка"""
    def __init__(self, x, y, settings_obj, screen):
        super().__init__()
        self.settings_obj = settings_obj
        self.screen = screen
        self.spr = self.settings_obj.w_and_h_sprite_map  # Для краткости
        self.image = pygame.image.load("assets/rec2_64.png")
        self.rect = self.image.get_rect()

        self.path_list = []

        self.rect.x = x
        self.rect.y = y
        self.curr_koord = ((y // self.spr), (x // self.spr))  # текущая координата
        self.path_points = settings_obj.recon_points
        self.weights = settings_obj.weights_track

        self.link_to_graph = None
        self.link_to_path = None

    def draw_recon(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.path_list and self.get_koordinate() == self.path_list[-1]:
            self.path_list = []
            print('прибыл или остался на месте')

        elif self.path_list and self.get_koordinate() != self.path_list[-1]:
            for y, x in self.path_list:
                self.rect.x = x * self.spr
                self.rect.y = y * self.spr
                self.curr_koord = ((self.rect.y // self.spr), (self.rect.x // self.spr))

    def get_koordinate(self):
        self.curr_koord = ((self.rect.y // self.spr), (self.rect.x // self.spr))
        return self.curr_koord

    def set_unit_path(self, list_p):
        self.path_list = list_p

    def get_unit_path(self):
        return self.path_list


