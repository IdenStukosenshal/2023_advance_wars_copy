import pygame
from pygame.sprite import Sprite
from ground_forces import GroundForces


class Recon(GroundForces, Sprite):
    def __init__(self, x, y, settings_obj, screen):
        super().__init__(x, y, settings_obj, screen)  # передача аргументов в конструктор надкласса = GroundForces.__init__(self, ...)
        self.image = pygame.image.load("assets/rec2_64.png")
        self.path_points = settings_obj.recon_points