import pygame
from pygame.sprite import Group

from settings import Settings
import game_function_1
import map_to_graph
from interface_objects.ramka import Ramka


def vidiya_game():
    unit_object = None

    settings_obj = Settings()

    pygame.init()
    screen = pygame.display.set_mode((settings_obj.screen_w, settings_obj.screen_h))
    pygame.display.set_caption('CooL_ViDiYa_GaMe')
    clock = pygame.time.Clock()

    map_elements = Group()
    file_name = "map_and_map_elements/map_1.txt"
    map_massive = map_to_graph.file_map_to_massive(file_name)
    game_function_1.create_map(map_massive, settings_obj, screen, map_elements)  # добавляет элементы карты в группу
    ramka_obj = Ramka(64, 64, settings_obj, screen)

    path_s = Group()
    gr_force_s = Group()
    heli_s = Group()

    game_function_1.create_my_army(map_massive, screen, settings_obj, gr_force_s, heli_s)

    while True:

        clock.tick(settings_obj.fps)
        ramka_obj.update()

        unit_object = game_function_1.check_events(screen, settings_obj, ramka_obj, path_s, map_massive, unit_object)
        gr_force_s.update()
        heli_s.update()
        game_function_1.update_screen(screen, map_elements, ramka_obj, path_s, gr_force_s, heli_s)

        pygame.display.flip()


if __name__ == '__main__': # для предотвращения зацикливания импортов
    vidiya_game()
