import pygame
from pygame.sprite import Sprite


class GroundForces(Sprite):
    """Базовый класс для наземных юнитов"""
    def __init__(self, x, y, settings_obj, screen):
        super().__init__()
        self.settings_obj = settings_obj
        self.screen = screen
        self.spr = self.settings_obj.w_and_h_sprite_map  # Для краткости
        self.image = pygame.Surface((self.spr, self.spr))
        self.image.fill((255, 255, 255))  # белый квадрат по умолчанию
        self.rect = self.image.get_rect()

        self.path_list = []

        self.rect.x = x
        self.rect.y = y
        self.curr_koord = ((y // self.spr), (x // self.spr))  # текущая координата, работает только если обновлять в нужное время
        self.path_points = 20  # тестовое значение
        self.weights = settings_obj.weights_track  #  веса по умолчанию для техники

        self.link_to_graph = None
        self.link_to_path = None

        self.speed = settings_obj.speed
        self.pixel_path = []
        self.l = 0
        self.r = 1
        self.flag = 0
        self.type_unit = None

    def draw_gr_forc(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.pixel_path and self.get_u_pixel_coordinate() != self.pixel_path[-1]:
            self.dvij()

    def get_u_koordinate(self):
        return self.curr_koord

    def get_u_pixel_coordinate(self):
        return self.rect.x, self.rect.y

    def set_unit_path(self, list_p):
        self.path_list = list_p

        self.pixel_path = []
        for y, x in self.path_list:
            y *= self.spr
            x *= self.spr
            self.pixel_path.append((x, y))

        self.flag = 1

    def get_unit_path(self):
        return self.path_list

    def dvij(self):
        """
        delta высчитывается так: из координат второй точки пути вычитаются координаты первой точки пути,
         разница всегда равна размеру спрайта. Разделив на него получаем -1, 0 или 1.
         При достижении второй точки пути переключаемся на 2 и 3, далее 3 и 4 и тд
        """
        if self.flag and self.pixel_path:
            delta_x = (self.pixel_path[self.r][0] - self.pixel_path[self.l][0])//self.spr * self.speed
            delta_y = (self.pixel_path[self.r][1] - self.pixel_path[self.l][1])//self.spr * self.speed
            self.rect.x += delta_x
            self.rect.y += delta_y
            if (self.rect.x, self.rect.y) == self.pixel_path[self.r]:  # обновлять координаты только в этот момент
                self.curr_koord = ((self.rect.y // self.spr), (self.rect.x // self.spr))
                self.l += 1
                self.r += 1
            if (self.rect.x, self.rect.y) == self.pixel_path[-1]:  # обновлять координаты только в этот момент
                self.curr_koord = ((self.rect.y // self.spr), (self.rect.x // self.spr))
                self.flag = 0
                self.l = 0
                self.r = 1
                self.pixel_path = []
