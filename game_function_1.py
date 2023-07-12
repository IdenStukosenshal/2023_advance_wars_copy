import pygame
import sys

from path_element import PathElement
from map_element import MapElement
from recon import Recon

from map_to_graph import experimental_digraph
from map_to_graph import graph_redacting
from map_to_graph import get_allowed_oblast

import moving_processing as m_p

from units_location_s import recon_positions

unit_object = False
chang_path_global = False

all_units_positions = dict()


def push_the_lever():
    """Эта функция вызывается при нажатии кнопки действия
    переключает флаг для управления перемещением и построением пути"""
    global chang_path_global
    if chang_path_global:
        chang_path_global = False
    else:
        chang_path_global = True


def check_events(screen, settings_obj, ramka_obj, path_s, recon_s, map_massive):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(screen, settings_obj, event, ramka_obj, path_s, recon_s, map_massive)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ramka_obj, )


def check_key_down_events(screen, settings_obj, event, ramka_obj, path_s, recon_s, map_massive):
    global unit_object, all_units_positions, chang_path_global

    if event.key == pygame.K_SPACE:
        ramka_koord = ramka_obj.get_koordinate()
        if ramka_koord in all_units_positions.keys() and chang_path_global is False:

            unit_object = all_units_positions[ramka_obj.get_koordinate()]

            push_the_lever()

            path_line = PathElement(screen, settings_obj, ramka_koord)  # создали объект пути
            path_s.add(path_line)

            allowed_obl = get_allowed_oblast(unit_object, ramka_koord)
            path_line.set_allowed_obl(allowed_obl)  # назначена разрешённая область

            unit_object.link_to_path = path_line

        elif chang_path_global:

            push_the_lever()
            unit_object.link_to_path.draw_oblast_finished = True

            unit_loc_link = None
            path_u = unit_object.link_to_path.get_list_path()
            for unit in all_units_positions.values():
                if path_u[0] == unit.get_koordinate():  # выбор перемещаемого
                    unit.set_list_path(path_u)  # присваиваем юниту его путь
                    unit_loc_link = unit
            all_units_positions[path_u[-1]] = unit_object  # сохраняем будущую позицию и юнита

            graph_redacting(unit_object.get_list_path()[0], settings_obj, map_massive, all_units_positions)

    if event.key == pygame.K_RIGHT:
        if chang_path_global:
            m_p.moving_right_in_oblast(ramka_obj, unit_object, unit_object.link_to_path)
        else:
            ramka_obj.move_right = True

    if event.key == pygame.K_LEFT:
        if chang_path_global:
            m_p.moving_left_in_oblast(ramka_obj, unit_object, unit_object.link_to_path)
        else:
            ramka_obj.move_left = True

    if event.key == pygame.K_UP:
        if chang_path_global:
            m_p.moving_up_in_oblast(ramka_obj,  unit_object, unit_object.link_to_path)
        else:
            ramka_obj.move_up = True

    if event.key == pygame.K_DOWN:
        if chang_path_global:
            m_p.moving_down_in_oblast(ramka_obj,  unit_object, unit_object.link_to_path)
        else:
            ramka_obj.move_down = True


def check_key_up_events(event, ramka_obj, ):
    if event.key == pygame.K_RIGHT:
        ramka_obj.move_right = False
    if event.key == pygame.K_LEFT:
        ramka_obj.move_left = False
    if event.key == pygame.K_UP:
        ramka_obj.move_up = False
    if event.key == pygame.K_DOWN:
        ramka_obj.move_down = False


def create_map(map_massive, settings_obj, screen, map_elements):
    """Получает имя файла с картой, объект screen
    вызывает функцию, которая создаёт массив элементов из файла.
    Для каждого элемента вычисляется его координаты(исходя из размера спрайта).
    Координаты, элемент массива, объект screen передаются в конструктор класса MapElement

    каждый элемент добавляется в группу

    """

    for i in range(len(map_massive)):
        for j in range(len(map_massive[0])):
            x = j * settings_obj.w_and_h_sprite_map
            y = i * settings_obj.w_and_h_sprite_map

            new_element = MapElement(x, y, map_massive[i][j], screen)
            map_elements.add(new_element)


def create_my_army(map_massive, screen, settings_obj, recon_s):
    global all_units_positions

    def create_recon_squad(map_massive, screen, settings_obj, recon_s):
        recon_weights = settings_obj.weights_track
        for id, yx in enumerate(recon_positions):
            y = yx[0] * settings_obj.w_and_h_sprite_map
            x = yx[1] * settings_obj.w_and_h_sprite_map
            new_rec = Recon(id, x, y, settings_obj, screen)
            all_units_positions[(yx[0], yx[1])] = new_rec  # добавление в общий словарь
            recon_s.add(new_rec)
        recon_graph = experimental_digraph(map_massive, recon_weights, all_units_positions)
        for recon in recon_s:
            recon.link_to_graph = recon_graph

    create_recon_squad(map_massive, screen, settings_obj, recon_s)




def update_screen(screen, map_elements, ramka_obj, path_s, recon_s):
    #for map_elem in map_elements.sprites():
        #map_elem.draw_map()
    # path_s.draw(screen)
    map_elements.draw(screen)
    for path in path_s.sprites():
        path.draw_path()

    for rec in recon_s.sprites():
        rec.draw_recon()

    ramka_obj.draw_ramka()

