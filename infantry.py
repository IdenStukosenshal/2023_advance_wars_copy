import pygame
from pygame.sprite import Sprite
from ground_forces import GroundForces


class Inf(GroundForces, Sprite):
    def __init__(self, x, y, settings_obj, screen):
        super().__init__( x, y, settings_obj, screen)  # передача аргументов в конструктор надкласса = GroundForces.__init__(self, ...)
        self.path_points = settings_obj.infantry_points
        self.weights = settings_obj.weights_inf

        self.image = pygame.image.load("assets/soldier_snk.png")  # размер оригинального спрайта 48X54
        surf = pygame.Surface((settings_obj.w_and_h_sprite_map, settings_obj.w_and_h_sprite_map))
        surf.fill((0, 255, 0))  # создаётся поверхность с любым цветом, размером 64x64
        surf.blit(self.image, (8, 5))  # на неё выводится image,
        surf.set_colorkey((0, 255, 0))  # убирается цвет поверхности
        self.image = surf

        self.type_unit = 'infantry'




