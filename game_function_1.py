import pygame
import sys

from path_element import PathElement
from map_element import MapElement
from recon_new import Recon
from infantry import Inf
from helicopter import Helicopter

from map_to_graph import experimental_digraph, massive_to_graph_to_helicopter
from map_to_graph import graph_redacting, get_allowed_oblast

import moving_processing as m_p

from units_location_s import recon_positions, infantry_positions, helicopters_position

unit_object = False
chang_path_global = False

all_units_positions = dict()
all_heli_s_positions = dict()

flag = True


def push_the_lever():
    """Эта функция вызывается при нажатии кнопки действия
    переключает флаг для управления перемещением и построением пути"""
    global chang_path_global
    if chang_path_global:
        chang_path_global = False
    else:
        chang_path_global = True


def check_events(screen, settings_obj, ramka_obj, path_s, map_massive):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(screen, settings_obj, event, ramka_obj, path_s,  map_massive)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ramka_obj, )


def check_key_down_events(screen, settings_obj, event, ramka_obj, path_s, map_massive):
    global unit_object, all_units_positions, chang_path_global, flag
    if event.key == pygame.K_SPACE:
        ramka_koord = ramka_obj.get_koordinate()

        """Костыль(flag) убирает вылет когда юнит находится в пути,
         но выбирается его пункт назначения."""
        flag = True
        for unit in all_units_positions.values():
            if unit.get_u_koordinate() not in all_units_positions.keys():  #
                flag = False

        if ramka_koord in all_units_positions.keys() and chang_path_global is False and flag:
            unit_object = all_units_positions[ramka_obj.get_koordinate()]  # получить ссылку на объект юнита
            push_the_lever()
            path_line = PathElement(screen, settings_obj, ramka_koord)  # создали объект пути
            path_s.add(path_line)  # добавили в группу
            allowed_obl = get_allowed_oblast(unit_object, ramka_koord)  # получаем разрешённую область
            path_line.set_allowed_obl(allowed_obl)  # назначена разрешённая область
            unit_object.link_to_path = path_line  # сохраняем объект пути в экземпляре передвигаемого юнита

        elif chang_path_global:
            # окончательное назначение пути
            push_the_lever()
            path_u = unit_object.link_to_path.get_list_path()  # список кортежей, [(y,x), (y,x)]
            unit_object.set_unit_path(path_u)  # присваиваем юниту его путь
            all_units_positions[path_u[-1]] = unit_object  # сохраняем будущую позицию и юнита
            graph_redacting(unit_object.get_u_koordinate(), settings_obj, map_massive, all_units_positions)
            # редактируем рёбра к стартовой и к конечной точке

            del unit_object.link_to_path
            for path in path_s.copy():
                path_s.remove(path)

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

    if event.key ==pygame.K_BACKSPACE:
        if chang_path_global:  # вроде работает, пока багов не замечено
            push_the_lever()
            del unit_object.link_to_path
            for path in path_s.copy():
                path_s.remove(path)


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
    """Получает массив карты
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


def create_my_army(map_massive, screen, settings_obj, gr_force_s, heli_s):
    global all_units_positions, all_heli_s_positions

    create_recon_squad(map_massive, screen, settings_obj, gr_force_s, all_units_positions)
    create_infantry_squad(map_massive, screen, settings_obj, gr_force_s, all_units_positions)
    create_helicopter_squad(map_massive, screen, settings_obj, heli_s, all_heli_s_positions)


def create_recon_squad(map_massive, screen, settings_obj, gr_force_s, all_units_positions):
    recon_weights = settings_obj.weights_track
    print(recon_weights)
    for yx in recon_positions:
        y = yx[0] * settings_obj.w_and_h_sprite_map
        x = yx[1] * settings_obj.w_and_h_sprite_map
        new_rec = Recon(x, y, settings_obj, screen)
        all_units_positions[(yx[0], yx[1])] = new_rec  # добавление в общий словарь
        gr_force_s.add(new_rec)
    recon_graph = experimental_digraph(map_massive, recon_weights, all_units_positions)
    for unit in gr_force_s:
        if unit.type_unit == 'recon':
            unit.link_to_graph = recon_graph


def create_infantry_squad(map_massive, screen, settings_obj, gr_force_s, all_units_positions):
    inf_weights = settings_obj.weights_inf
    for yx in infantry_positions:
        y = yx[0] * settings_obj.w_and_h_sprite_map
        x = yx[1] * settings_obj.w_and_h_sprite_map
        new_inf = Inf(x, y, settings_obj, screen)
        all_units_positions[(yx[0], yx[1])] = new_inf  # добавление в общий словарь
        gr_force_s.add(new_inf)
    inf_graph = experimental_digraph(map_massive, inf_weights, all_units_positions)
    for unit in gr_force_s:
        if unit.type_unit == 'infantry':
            unit.link_to_graph = inf_graph


def create_helicopter_squad(map_massive, screen, settings_obj, heli_s, all_heli_s_positions):
    max_weight = settings_obj.max_value
    for yx in helicopters_position:
        y = yx[0] * settings_obj.w_and_h_sprite_map
        x = yx[1] * settings_obj.w_and_h_sprite_map
        new_heli = Helicopter(x, y, settings_obj, screen)
        all_heli_s_positions[(yx[0], yx[1])] = new_heli
        heli_s.add(new_heli)
    heli_graph = massive_to_graph_to_helicopter(map_massive, max_weight, all_heli_s_positions)
    for heli in heli_s:
        heli.link_to_graph = heli_graph


def update_screen(screen, map_elements, ramka_obj, path_s, recon_s, heli_s):
    #for map_elem in map_elements.sprites():
        #map_elem.draw_map()
    # path_s.draw(screen)
    map_elements.draw(screen)

    for path in path_s.sprites():
        path.draw_path()
    for unit in recon_s.sprites():
        unit.draw_gr_forc()
    for unit in heli_s.sprites():
        unit.draw_gr_forc()

    ramka_obj.draw_ramka()

