import pygame
from pygame.sprite import Sprite


class MapElement(Sprite):
    """При создании объекта получает координаты и вид клетки
     '#' - поле, 'd' - дорога, 'f' - лес,
      '@' - гора, 'v' - вода, 't' - город"""
    elements = {'#': 'assets/pole_light.png',
                'd': 'assets/doroga.png',
                'f': 'assets/forest.png',
                '@': 'assets/gora.png',
                'v': 'assets/water.png',
                't': 'assets/town.png',
                }

    def __init__(self, x, y, map_massive_i_j, screen):
        super().__init__()

        self.screen = screen
        self.image = pygame.image.load(MapElement.elements[map_massive_i_j])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_map(self):
        self.screen.blit(self.image, self.rect)
