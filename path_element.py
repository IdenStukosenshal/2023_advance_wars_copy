import pygame
from pygame.sprite import Sprite


class PathElement(Sprite):
    """Когда объект создаётся, он не рисуется сразу.
    Получает готовый массив координат для построения линии,
    Каждая координата в центре спрайта"""
    def __init__(self, screen, settings_obj, start_position):
        super().__init__()
        self.screen = screen
        self.settings_obj = settings_obj

        self.list_path = []
        self.start_position = start_position
        self.allowed_oblast_list = None

        self.draw_oblast_finished = False

    def draw_path(self,):
        if self.allowed_oblast_list and not self.draw_oblast_finished:
            koord_list = self.__allowed_oblast_to_koordinate(self.allowed_oblast_list)
            self.__drawing_oblast(koord_list)

        if len(self.list_path) > 1 and self.list_path[0] != self.list_path[1]:
            pygame.draw.lines(self.screen, (0, 200, 200), False, self.list_path, 2)

    def __allowed_oblast_to_koordinate(self, nodes_list):
        """Возвращает координаты доступной области в пикселях"""
        rez_list = []
        for y, x in nodes_list:
            y = y * self.settings_obj.w_and_h_sprite_map
            x = x * self.settings_obj.w_and_h_sprite_map
            rez_list.append((y, x))
        return rez_list

    def __drawing_oblast(self, koord_list):
        for y, x in koord_list:
            pygame.draw.rect(self.screen, (255, 255, 255), (x+3, y+3, self.settings_obj.w_and_h_sprite_map-6, self.settings_obj.w_and_h_sprite_map-6), 1)

    def __drawing_arrow(self, list_path):
        """Рисует одну из 8 стрелочек в зависимости от направления пути(последние 2 точки)"""
        pass

    def set_list_path(self, list_path):
        self.list_path = list_path

    def get_list_path(self):
        return self.list_path

    def get_node_list_path(self):
        rez = []
        for x, y in self.list_path:
            y = y // self.settings_obj.w_and_h_sprite_map
            x = x // self.settings_obj.w_and_h_sprite_map
            rez.append((y, x))

        return rez

    def set_allowed_obl(self, nodes_list):
        self.allowed_oblast_list = nodes_list

    def get_allowed_obl(self):
        return self.allowed_oblast_list



