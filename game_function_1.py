import pygame
import sys

from enum import Enum

from interface_objects.path_element import PathElement
from map_and_map_elements.map_element import MapElement
import map_to_graph as mp_t_g

import create_my_and_enemy_army as create_armys
import moving_processing as m_p

unit_object = None

all_units_positions = dict()
all_heli_s_positions = dict()


class ActionState(Enum):
    """Для замены всех флагов"""
    Free_move = 0  # перемещение рамки когда ничего не выбрано
    Selected = 1
    On_the_move = 2  # ограничения на действия, когда юнит в пути


flag_state = ActionState.Free_move


def check_events(screen, settings_obj, ramka_obj, path_s, map_massive):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(screen, settings_obj, event, ramka_obj, path_s,  map_massive)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ramka_obj, )


def check_key_down_events(screen, settings_obj, event, ramka_obj, path_s, map_massive):
    global unit_object, all_units_positions, all_heli_s_positions, flag_state
    # После движения старый юнит остаётся доступным по ссылке до выбора нового
    if flag_state is ActionState.On_the_move:
        if unit_object.get_u_koordinate() in all_units_positions.keys() and unit_object.type_unit != settings_obj.helicopter_type:
            flag_state = ActionState.Free_move
        elif unit_object.get_u_koordinate() in all_heli_s_positions.keys() and unit_object.type_unit == settings_obj.helicopter_type:
            flag_state = ActionState.Free_move
        else:
            pass

    if event.key == pygame.K_SPACE and flag_state is not ActionState.On_the_move:
        ramka_koord = ramka_obj.get_koordinate()

        if ramka_koord in all_units_positions.keys() and ramka_koord in all_heli_s_positions.keys()\
                and flag_state is ActionState.Free_move:
            """если выбрана точка, на которой наземный юнит и воздушный одновременно"""
            print("""По умолчанию первый - наземный""")
            unit_object = all_units_positions[ramka_obj.get_koordinate()]  # получить ссылку на объект юнита
            unit_object = create_path_for_unit(screen, settings_obj, unit_object, ramka_koord, path_s)
            flag_state = ActionState.Selected

        elif ramka_koord in all_units_positions.keys() and flag_state is ActionState.Free_move:
            print("""Выбран наземный юнит""")
            unit_object = all_units_positions[ramka_obj.get_koordinate()]  # получить ссылку на объект юнита
            flag_state = ActionState.Selected
            unit_object = create_path_for_unit(screen, settings_obj, unit_object, ramka_koord, path_s)

        elif ramka_koord in all_heli_s_positions.keys() and flag_state is ActionState.Free_move:
            print("""Выбран воздушный юнит""")
            unit_object = all_heli_s_positions[ramka_obj.get_koordinate()]  # получить ссылку на объект юнита
            flag_state = ActionState.Selected
            unit_object = create_path_for_unit(screen, settings_obj, unit_object, ramka_koord, path_s)



        if flag_state is ActionState.Selected and len(unit_object.link_to_path.get_list_path()) == 1\
               and ramka_koord in all_units_positions.keys() and ramka_koord in all_heli_s_positions.keys():
            """Ещё раз выбрана точка, занятая юнитами обоих типов"""
            if unit_object.type_unit == settings_obj.helicopter_type:
                path_s.empty()  # очищение группы, чтобы удалить с экрана старую область
                print("Переключение на наземный тип")
                unit_object = all_units_positions[ramka_obj.get_koordinate()]  # получить ссылку на объект юнита
                unit_object = create_path_for_unit(screen, settings_obj, unit_object, ramka_koord, path_s)

            elif unit_object.type_unit != settings_obj.helicopter_type:
                path_s.empty()  # очищение группы, чтобы удалить с экрана старую область
                print(" Переключение на воздушный тип")
                unit_object = all_heli_s_positions[ramka_obj.get_koordinate()]  # получить ссылку на объект юнита
                unit_object = create_path_for_unit(screen, settings_obj, unit_object, ramka_koord, path_s)
            flag_state = ActionState.Selected  # изменяем вручную, потому что могут быть многократные нажатия выбора

        elif flag_state is ActionState.Selected and len(unit_object.link_to_path.get_list_path()) == 1:
            """Если в списке только старт - ничего не делать
            Срабатывает при первом выборе юнита или если многократно нажимать кнопку на одном и том же юните"""
            pass



        if flag_state is ActionState.Selected and len(unit_object.link_to_path.get_list_path()) != 1:
            # окончательное назначение пути
            flag_state = ActionState.On_the_move
            path_u = unit_object.link_to_path.get_list_path()  # список кортежей, [(y,x), (y,x)]
            unit_object.set_unit_path(path_u)  # присваиваем юниту его путь

            if unit_object.type_unit != settings_obj.helicopter_type:
                all_units_positions[path_u[-1]] = unit_object  # сохраняем будущую позицию и юнита
                mp_t_g.graph_redacting(unit_object.get_u_koordinate(), settings_obj, map_massive, all_units_positions)
                # редактируем рёбра к стартовой и к конечной точке
            elif unit_object.type_unit == settings_obj.helicopter_type:
                all_heli_s_positions[path_u[-1]] = unit_object  # сохраняем будущую позицию и юнита
                mp_t_g.graph_redacting(unit_object.get_u_koordinate(), settings_obj, map_massive, all_heli_s_positions)
                # редактируем рёбра к стартовой и к конечной точке
            path_s.empty()   # очищение группы, чтобы удалить с экрана старую область

    if event.key == pygame.K_RIGHT:
        if flag_state is ActionState.Selected:
            m_p.moving_right_in_oblast(ramka_obj, unit_object, )
        else:
            ramka_obj.move_right = True

    if event.key == pygame.K_LEFT:
        if flag_state is ActionState.Selected:
            m_p.moving_left_in_oblast(ramka_obj, unit_object,)
        else:
            ramka_obj.move_left = True

    if event.key == pygame.K_UP:
        if flag_state is ActionState.Selected:
            m_p.moving_up_in_oblast(ramka_obj,  unit_object,)
        else:
            ramka_obj.move_up = True

    if event.key == pygame.K_DOWN:
        if flag_state is ActionState.Selected:
            m_p.moving_down_in_oblast(ramka_obj,  unit_object,)
        else:
            ramka_obj.move_down = True

    if event.key == pygame.K_BACKSPACE:
        if flag_state is ActionState.Selected:
            flag_state = ActionState.Free_move
            path_s.empty()


def check_key_up_events(event, ramka_obj, ):
    """Обработка поднимания клавиши, пока не используется"""
    if event.key == pygame.K_RIGHT:
        ramka_obj.move_right = False
    if event.key == pygame.K_LEFT:
        ramka_obj.move_left = False
    if event.key == pygame.K_UP:
        ramka_obj.move_up = False
    if event.key == pygame.K_DOWN:
        ramka_obj.move_down = False


def create_path_for_unit(screen, settings_obj, unit_object, ramka_koord, path_s):
    """Получает объект юнита, создаёт путь, сохраняет его в объекте юнита
     и возвращает юнит"""
    path_line = PathElement(screen, settings_obj, ramka_koord)  # создали объект пути
    path_s.add(path_line)  # добавили в группу
    allowed_obl = mp_t_g.calculate_allowed_oblast(unit_object, ramka_koord)  # получаем разрешённую область
    path_line.set_allowed_obl(allowed_obl)  # назначена разрешённая область
    unit_object.link_to_path = path_line  # сохраняем объект пути в экземпляре передвигаемого юнита
    return unit_object


def create_map(map_massive, settings_obj, screen, map_elements):
    """Получает массив карты
    Для каждого элемента вычисляется его координаты(исходя из размера спрайта).
    Координаты, элемент массива(символ), объект screen передаются в конструктор класса MapElement.
    каждый элемент добавляется в группу
    """
    for i in range(len(map_massive)):
        for j in range(len(map_massive[0])):
            x = j * settings_obj.w_and_h_sprite_map
            y = i * settings_obj.w_and_h_sprite_map

            new_element = MapElement(x, y, map_massive[i][j], screen)
            map_elements.add(new_element)


def create_my_army(map_massive, screen, settings_obj, gr_force_s, heli_s):
    """Создаёт юниты по классам, ссылки на объекты сохраняются в группах и в словарях вместе с координатами.
    После добавления позиций вызов функции создающей графы

    Функции меняют изменяемые переменные, поэтому возвращение не требуется"""
    global all_units_positions, all_heli_s_positions

    create_armys.create_recon_squad( screen, settings_obj, gr_force_s, all_units_positions)
    create_armys.create_infantry_squad( screen, settings_obj, gr_force_s, all_units_positions)
    create_armys.create_helicopter_squad(screen, settings_obj, heli_s, all_heli_s_positions)

    create_armys.preparing_graph(map_massive, settings_obj, all_units_positions, all_heli_s_positions, gr_force_s, heli_s)


def update_screen(screen, map_elements, ramka_obj, path_s, recon_s, heli_s):
    #for map_elem in map_elements.sprites():
        #map_elem.draw_map()
    # path_s.draw(screen)
    map_elements.draw(screen)

    for path in path_s.sprites():
        path.draw_path()
    #for unit in recon_s.sprites():
        #unit.draw_gr_forc()
    recon_s.draw(screen)
    #for unit in heli_s.sprites():
        #unit.draw_gr_forc()
    heli_s.draw(screen)

    ramka_obj.draw_ramka()

