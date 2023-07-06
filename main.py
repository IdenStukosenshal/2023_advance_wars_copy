import pygame
from pygame.sprite import Group

from settings import Settings
import game_function_1
import map_to_graph
from ramka import Ramka



def vidiya_game():
    settings_obj = Settings()

    pygame.init()
    screen = pygame.display.set_mode((settings_obj.screen_w, settings_obj.screen_h))
    pygame.display.set_caption('CooL_ViDiYa_GaMe')
    clock = pygame.time.Clock()

    map_elements = Group()
    file_name = "map_1.txt"
    map_massive = map_to_graph.file_map_to_massive(file_name)
    game_function_1.create_map(map_massive, settings_obj, screen, map_elements)  # добавляет элементы карты в группу

    ramka_obj = Ramka(64, 64, settings_obj, screen)

    while True:

        clock.tick(settings_obj.fps)
        game_function_1.check_events(ramka_obj)
        ramka_obj.update()
        game_function_1.update_screen(screen, map_elements, ramka_obj)

        finish = ramka_obj.y_x_to_graph
        start = ramka_obj.start_experim
        if ramka_obj.path_drawing_allowed:
            game_function_1.create_path(start, finish, map_massive, screen, settings_obj)

        pygame.display.flip()


vidiya_game()

"""Управление:
Перемещение рамки на стрелочки, поставить стартовую точку - SPACE, отменить - Backspace.
После установки стартовой точки можно наблюдать построение путей в зависимости от положения рамки"""
