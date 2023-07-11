import pygame
from pygame.sprite import Sprite


class Recon(Sprite):
    """розвiдка"""
    def __init__(self, id, x, y, settings_obj, screen, changed_graph):
        super().__init__()
        self.settings_obj = settings_obj
        self.screen = screen
        self.spr = self.settings_obj.w_and_h_sprite_map  # Для краткости

        #self.image = pygame.image.load("")

        self.image = pygame.Surface((self.spr, self.spr))
        self.image.fill((0, 150, 100))
        self.rect = self.image.get_rect()

        self.id = id
        self.path_list = []

        self.rect.x = x
        self.rect.y = y

        self.curr_koord = ((y // self.spr), (x // self.spr))  # текущая координата
        self.path_points = settings_obj.recon_points
        self.weights = settings_obj.weights_track

        #self.type_un = "recon"

        self.link_to_graph = changed_graph

    def draw_recon(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.path_list and (self.rect.x, self.rect.y) == self.path_list[-1]:
            self.path_list = []

        elif self.path_list and (self.rect.x, self.rect.y) != self.path_list[-1]:
            print("БЫЛ ПЕРЕМЕЩЁН")
            for x, y in self.path_list:
                self.rect.x = x
                self.rect.y = y
                self.__update_coordinate()

    def __update_coordinate(self):
        self.curr_koord = ( (self.rect.y // self.spr), (self.rect.x // self.spr) )

    def get_koordinate(self):
        return self.curr_koord

    def set_list_path(self, list_p):
        for y, x in list_p:
            x = x * self.spr
            y = y * self.spr
            self.path_list.append((x, y))
