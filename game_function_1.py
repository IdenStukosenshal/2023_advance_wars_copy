import pygame
import sys


from map_element import MapElement
from recon import Recon
from map_to_graph import experimental_digraph
from map_to_graph import graph_redacting
import main
import moving_processing as m_p

import units_location_s


def check_events(screen, settings_obj, ramka_obj, path_s, recon_s):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(screen, settings_obj, event, ramka_obj, path_s, recon_s)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ramka_obj, )


def check_key_down_events(screen, settings_obj, event, ramka_obj, path_s, recon_s):

    if main.chang_path_global:
        unit_obj = main.unit_object
        print(unit_obj, "ВЫБРАН")
    else:
        unit_obj = False

    if event.key == pygame.K_SPACE:
        if ramka_obj.get_koordinate() in main.koord_and_units_dict.keys() and main.chang_path_global is False:
            unit_obj = main.koord_and_units_dict[ramka_obj.get_koordinate()]
            main.unit_object = unit_obj
            print(unit_obj, "ВЫБРАН")
        m_p.processing_action_button(screen, settings_obj, path_s, recon_s, unit_obj, ramka_obj)

    if event.key == pygame.K_RIGHT:
        if main.chang_path_global and unit_obj:
            m_p.moving_right_in_oblast(ramka_obj, unit_obj)
        elif not unit_obj:
            ramka_obj.move_right = True

    if event.key == pygame.K_LEFT:
        if main.chang_path_global and unit_obj:
            m_p.moving_left_in_oblast(ramka_obj, unit_obj)
        elif not unit_obj:
            ramka_obj.move_left = True

    if event.key == pygame.K_UP:
        if main.chang_path_global and unit_obj:
            m_p.moving_up_in_oblast(ramka_obj,  unit_obj)
        elif not unit_obj:
            ramka_obj.move_up = True

    if event.key == pygame.K_DOWN:
        if main.chang_path_global and unit_obj:
            m_p.moving_down_in_oblast(ramka_obj,  unit_obj)
        elif not unit_obj:
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

    graph_track = experimental_digraph(map_massive, settings_obj.weights_track)
    changed_graph_for_tracks = graph_redacting(graph_track, settings_obj, )

    for id, yx in enumerate(units_location_s.recon_positions):
        y = yx[0] * settings_obj.w_and_h_sprite_map
        x = yx[1] * settings_obj.w_and_h_sprite_map
        new_rec = Recon(id, x, y, settings_obj, screen, changed_graph_for_tracks)
        recon_s.add(new_rec)

        main.koord_and_units_dict[(yx[0], yx[1])] = new_rec  # добавление  в общий словарь


'''
def graph_redacting(graph, settings_obj, ):
    """изменяет граф в соответствии с изменяемыми координатами юнитов,
    сейчас они хранятся в общем множестве set_all_units

    Нужно вызывать эту функцию при каждом перемещении юнита"""
    edges = []
    for y, x in units_location_s.set_all_units:  # увеличение весов
        for neigh_y, neigh_x in graph.adj[(y, x)]:
            edges.append(((neigh_y, neigh_x), (y, x), settings_obj.max_value))
    graph.add_weighted_edges_from(edges)  # изменение весов рёбер к занятым точкам

    # возвращение предыдущего состояния
    edges_orig = []
    # вес ребра = G[node1][node2]['weight']
    diff_set = main.set_all_units_copy - units_location_s.set_all_units  # вычесть те позиции, которые остались занятыми
    if diff_set:
        for y, x in diff_set:
            for neigh_y, neigh_x in graph.adj[(y, x)]:  # получаем оригинальный вес ребра, от освобождённой точки к соседям
                orig_weight = graph[(y, x)][neigh_y, neigh_x]['weight']
                edges_orig.append(((neigh_y, neigh_x), (y, x), orig_weight))
        graph.add_weighted_edges_from(edges)  # изменение весов освобождённых точек

    main.set_all_units_copy = units_location_s.set_all_units.copy()    # теперь сохраняются текущие координаты

    return graph

'''


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

