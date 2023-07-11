import pygame
from pygame.sprite import Group

from settings import Settings
import game_function_1
import map_to_graph
from ramka import Ramka
from units_location_s import set_all_units

link_to_path = None

chang_path_global = False

ramka_position = None

set_all_units_copy = set_all_units.copy()
# копия предыдущих занятых позиций для быстрого их получения и возвращения их состояния

koord_and_units_dict = dict()
# словарь юнитов(value) и их координат(key) для доступа при выборе рамкой

changed_graph_for_tracks = None  # общий граф для техники с подкорректированными весами занятых клеток
changed_graph_for_infantry = None

unit_object = False
def push_the_lever():
    """Эта функция вызывается при нажатии кнопки действия
    переключает флаг для управления перемещением и построением пути"""
    global chang_path_global
    if chang_path_global:
        chang_path_global = False
    else:
        chang_path_global = True


def vidiya_game():
    global changed_graph_for_tracks, ramka_position
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
    ramka_position = ramka_obj.get_koordinate()
    path_s = Group()



    #graph_track = map_to_graph.experimental_digraph(map_massive, settings_obj.weights_track)
    #changed_graph_for_tracks = game_function_1.graph_redacting(graph_track, settings_obj,)
    recon_s = Group()

    game_function_1.create_my_army(map_massive, screen, settings_obj, recon_s)



    while True:

        clock.tick(settings_obj.fps)
        ramka_obj.update()

        recon_s.update()

        game_function_1.check_events(screen, settings_obj, ramka_obj, path_s, recon_s)
        game_function_1.update_screen(screen, map_elements, ramka_obj, path_s, recon_s)

        pygame.display.flip()


if __name__ == '__main__': # для предотвращения зацикливания импортов
    vidiya_game()

"""Управление:
Перемещение рамки на стрелочки, поставить стартовую точку - SPACE, поставить конечную точку - тоже SPACE .
После установки стартовой точки можно наблюдать построение путей в зависимости от положения рамки"""
