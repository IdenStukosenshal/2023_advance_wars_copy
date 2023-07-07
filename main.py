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

    weights_track = {'#': 1.25, 'd': 1, 'f': 1.75, '@': 900, 'v': 900, 't': 1.25}
    graph = map_to_graph.massive_to_graph(map_massive, weights_track)

    """Веса и граф должны быть получены в зависимости от выбранного юнита
    Связать с функцией check_events в будущем"""

    ramka_obj = Ramka(64, 64, settings_obj, screen)

    path_s = Group()

    link_to_path = None

    while True:

        clock.tick(settings_obj.fps)
        ramka_obj.update()
        game_function_1.check_events(screen, settings_obj, ramka_obj, path_s, graph)
        game_function_1.update_screen(screen, map_elements, ramka_obj, path_s)

        pygame.display.flip()


vidiya_game()

"""Управление:
Перемещение рамки на стрелочки, поставить стартовую точку - SPACE, поставить конечную точку - тоже SPACE .
После установки стартовой точки можно наблюдать построение путей в зависимости от положения рамки"""
