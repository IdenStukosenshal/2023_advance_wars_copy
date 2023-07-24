import pygame
from pygame.sprite import Sprite
from my_army.ground_forces import GroundForces


class Helicopter(GroundForces, Sprite):
    def __init__(self, x, y, settings_obj, screen):
        super().__init__( x, y, settings_obj, screen)  # передача аргументов в конструктор надкласса = GroundForces.__init__(self, ...)
        self.path_points = settings_obj.helicopter_points
        self.image = pygame.image.load("assets/helicopter.png")  # размер оригинального спрайта 64X46

        self.type_unit = settings_obj.helicopter_type