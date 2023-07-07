import pygame
from pygame.sprite import Sprite

import main


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
        self.allowed_oblast_experim = None

        self.draw_oblast_finished = None

    def draw_path(self,):
        if self.allowed_oblast_experim and main.chang_path_global and not self.draw_oblast_finished:
            koord_list = self._nodes_to_koordinate(self.allowed_oblast_experim)
            self._drawing_oblast(koord_list)
        if len(self.list_path) > 1 and self.list_path[0] != self.list_path[1]:
            pygame.draw.lines(self.screen, (0, 200, 200), False, self.list_path, 2)

    def _nodes_to_koordinate(self, nodes_list):
        rez_list = []
        for y, x in nodes_list:
            y = y * self.settings_obj.w_and_h_sprite_map
            x = x * self.settings_obj.w_and_h_sprite_map
            rez_list.append((y, x))
        return rez_list

    def _drawing_oblast(self, koord_list):
        for y, x in koord_list:
            pygame.draw.rect(self.screen, (255, 255, 255), (x+3, y+3, self.settings_obj.w_and_h_sprite_map-6, self.settings_obj.w_and_h_sprite_map-6), 1)

    def _drawing_arrow(self, list_path):
        """Рисует одну из 8 стрелочек в зависимости от направления пути(последние 2 точки)"""
        pass



