import pygame
from pygame.sprite import Group

from settings import Settings
import game_function_1
import map_to_graph
from ramka import Ramka
settings_obj = Settings()


def vidiya_game():
    pygame.init()
    screen = pygame.display.set_mode((settings_obj.screen_w, settings_obj.screen_h))
    pygame.display.set_caption('CooL_ViDiYa_GaMe')
    clock = pygame.time.Clock()

    map_elements = Group()
    file_name = "map_1.txt"
    map_massive = map_to_graph.file_map_to_massive(file_name)
    game_function_1.create_map(map_massive, settings_obj, screen, map_elements)

    ramka_obj = Ramka(0, 0, settings_obj, screen)

    #start = '0.1'

    start_experim = []

    while True:

        clock.tick(settings_obj.fps)
        game_function_1.check_events(ramka_obj, start_experim)
        ramka_obj.update()
        game_function_1.update_screen(map_elements, ramka_obj)

        finish = ramka_obj.y_x_to_graph
        if start_experim and ramka_obj.path_drawing_allowed:
            game_function_1.create_path(start_experim[-1], finish, map_massive, screen, settings_obj)

        pygame.display.flip()


vidiya_game()

"""Управление:
Перемещение рамки на стрелочки, поставить стартовую точку - SPACE, отменить - Backspace.
После установки стартовой точки можно наблюдать построение путей в зависимости от положения рамки"""
