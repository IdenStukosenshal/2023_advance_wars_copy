import pygame
from pygame.sprite import Group

from settings import Settings
import game_function_1
import map_to_graph
from ramka import Ramka
from recon import Recon

link_to_path = None

chang_path_global = False


def push_the_lever():
    """Эта функция вызывается при нажатии кнопки действия
    переключает флаг для управления перемещением и построением пути"""
    global chang_path_global
    if chang_path_global:
        chang_path_global = False
    else:
        chang_path_global = True


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

    weights_track = {'#': 1.5, 'd': 1, 'f': 2, '@': 90, 'v': 90, 't': 1}
    graph = map_to_graph.massive_to_graph(map_massive, weights_track)

    """Веса и граф должны быть получены в зависимости от выбранного юнита
    Связать с функцией check_events в будущем"""

    ramka_obj = Ramka(64, 64, settings_obj, screen)

    path_s = Group()

    recon_s = Group()
    from units_location_s import recon_positions
    for id, yx in enumerate(recon_positions):
        y = yx[0] * settings_obj.w_and_h_sprite_map
        x = yx[1] * settings_obj.w_and_h_sprite_map
        new_rec = Recon(id, x, y, settings_obj, screen)
        recon_s.add(new_rec)



    while True:

        clock.tick(settings_obj.fps)
        ramka_obj.update()

        recon_s.update()

        game_function_1.check_events(screen, settings_obj, ramka_obj, path_s, graph, recon_s)
        game_function_1.update_screen(screen, map_elements, ramka_obj, path_s, recon_s)

        pygame.display.flip()


if __name__ == '__main__': # для предотвращения зацикливания импортов
    vidiya_game()

"""Управление:
Перемещение рамки на стрелочки, поставить стартовую точку - SPACE, поставить конечную точку - тоже SPACE .
После установки стартовой точки можно наблюдать построение путей в зависимости от положения рамки"""
