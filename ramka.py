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
        self.y_x_to_graph = ((y // self.spr_razm), (x // self.spr_razm))  # текущая координата

    def draw_ramka(self):
        self.screen.blit(self.ramka, self.rect)

    def update(self):

        if self.move_left and self.rect.left > 0:
            self.rect.centerx -= self.spr_razm
            self.move_left = False
            self.__update_coordinate()

        if self.move_right and self.rect.right < self.settings_obj.screen_w:
            self.rect.centerx += self.spr_razm
            self.move_right = False
            self.__update_coordinate()

        if self.move_up and self.rect.top > 0:
            self.rect.centery -= self.spr_razm
            self.move_up = False
            self.__update_coordinate()

        if self.move_down and self.rect.bottom < self.settings_obj.screen_h:
            self.rect.centery += self.spr_razm
            self.move_down = False
            self.__update_coordinate()

    def __update_coordinate(self):
        """Изменение текущих координат рамки.
        Преобразование координат к виду (y, x) Для работы с графом.
        Вызывается только в момент изменения координат"""
        self.y_x_to_graph = ( (self.rect.y // self.spr_razm), (self.rect.x // self.spr_razm) )

    def get_koordinate(self):
        return self.y_x_to_graph



