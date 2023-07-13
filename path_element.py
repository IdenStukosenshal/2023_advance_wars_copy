import pygame
from pygame.sprite import Sprite


class PathElement(Sprite):
    """Когда объект создаётся, он не рисуется сразу.
    Получает список точек для построения пути"""
    def __init__(self, screen, settings_obj, start_position):
        super().__init__()
        self.screen = screen
        self.settings_obj = settings_obj
        self.start_position = start_position
        self.list_path = [start_position, start_position]  # для возможности остаться на своей позиции без перемещения
        self.allowed_oblast_list = None
        self.spr_rzm = self.settings_obj.w_and_h_sprite_map

    def draw_path(self,):
        if self.allowed_oblast_list:
            koord_list = self.__allowed_oblast_to_koordinate(self.allowed_oblast_list)
            self.__drawing_oblast(koord_list)

        if len(self.list_path) > 1 and self.list_path[0] != self.list_path[1]: # временное решение, путь отображается только вместе с областью
            path_koord_list = self.__list_path_to_koordinate(self.list_path)
            pygame.draw.lines(self.screen, (0, 200, 200), False, path_koord_list, 3)

    def __allowed_oblast_to_koordinate(self, nodes_list):
        """Получает разрешённую область в виде списка нод.
        Возвращает координаты доступной области в пикселях"""
        rez_list = []
        for y, x in nodes_list:
            y = y * self.spr_rzm
            x = x * self.spr_rzm
            rez_list.append((x, y))
        return rez_list

    def __list_path_to_koordinate(self, list_path):
        """Получает список нод и возвращает список координат для построения пути"""
        rez_path_massive = []
        for y, x in list_path:
            y = y * self.spr_rzm + self.spr_rzm // 2
            x = x * self.spr_rzm + self.spr_rzm // 2
            rez_path_massive.append((x, y))
        return rez_path_massive

    def __drawing_oblast(self, koord_list):
        for x, y in koord_list:
            pygame.draw.rect(self.screen, (255, 255, 255), (x+3, y+3, self.spr_rzm-6, self.spr_rzm-6), 1)

    def set_list_path(self, list_path):
        self.list_path = list_path

    def get_list_path(self):
        return self.list_path

    def set_allowed_obl(self, nodes_list):
        self.allowed_oblast_list = nodes_list

    def get_allowed_obl(self):
        return self.allowed_oblast_list



