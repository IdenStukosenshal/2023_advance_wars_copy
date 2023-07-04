import pygame
from pygame.sprite import Sprite


class Ramka(Sprite):
    def __init__(self, x, y, settings_obj, screen):
        super().__init__()
        self.settings_obj = settings_obj
        self.screen = screen

        self.surf = pygame.Surface((settings_obj.w_and_h_sprite_map, settings_obj.w_and_h_sprite_map))
        self.surf.set_alpha(0)

        pygame.draw.lines(self.surf, (255, 255, 255), True,
                          [(0, 0), (settings_obj.w_and_h_sprite_map, 0),
                           (settings_obj.w_and_h_sprite_map, settings_obj.w_and_h_sprite_map)],
                          3)

        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y



    def draw_ramka(self):
        self.screen.blit(self.surf, self.rect)
        print("Нарисовано")