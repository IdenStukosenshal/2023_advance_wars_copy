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
        self.allowed_oblast_experim = None

    def draw_path(self,):
        if len(self.list_path) > 1 and self.list_path[0] != self.list_path[1]:
            pygame.draw.lines(self.screen, (255, 255, 255), False, self.list_path, 3)




