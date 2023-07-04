import pygame
from pygame.sprite import Sprite


class PathElement(Sprite):
    """Получает готовый массив координат для построения линии"""
    def __init__(self, path_massive, screen):
        super().__init__()
        self.path_massive = path_massive
        self.screen = screen

    def draw_path(self):
        #self.screen.blit( )
        pygame.draw.lines(self.screen, (255, 255, 255), False, self.path_massive, 3)