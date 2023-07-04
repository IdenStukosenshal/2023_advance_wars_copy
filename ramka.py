import pygame
from pygame.sprite import Sprite


class Ramka(Sprite):
    def __init__(self, x, y, settings_obj, screen):
        super().__init__()
        self.settings_obj = settings_obj
        self.screen = screen

        self.ramka = pygame.image.load("assets/ramka.png")
        self.ramka.set_colorkey((0, 128, 0))  # делаем фон прозрачным

        self.rect = self.ramka.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

        self.spr_razm = self.settings_obj.w_and_h_sprite_map  # Для краткости

        self.y_x_to_graph = str(y // self.spr_razm) + '.' + str(x // self.spr_razm)
        # Преобразование координат к виду 'y.x' Для работы с графом, начальные координаты


    def draw_ramka(self):
        self.screen.blit(self.ramka, self.rect)

    def update(self):

        if self.move_left and self.rect.left > 0:
            self.rect.centerx -= self.spr_razm
            self.move_left = False
        if self.move_right and self.rect.right < self.settings_obj.screen_w:
            self.rect.centerx += self.spr_razm
            self.move_right = False

        if self.move_up and self.rect.top > 0:
            self.rect.centery -= self.spr_razm
            self.move_up = False
        if self.move_down and self.rect.bottom < self.settings_obj.screen_h:
            self.rect.centery += self.spr_razm
            self.move_down = False

        self.y_x_to_graph = str((self.rect.centery-self.spr_razm//2) // self.spr_razm) + '.' + str(
            (self.rect.centerx-self.spr_razm//2) // self.spr_razm)  # Это вычисляется каждый раз, нужно перенести

        # Преобразование координат к виду 'y.x' Для работы с графом

