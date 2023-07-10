import main

from map_to_graph import get_allowed_oblast
from map_to_graph import peres4et_puti
from path_element import PathElement
from units_location_s import list_all_units


def moving_right_in_oblast(ramka_obj, graph):
    """Определение следующей точки.
    Если она в списке, двигаем рамку, пересчитываем путь"""
    future_node = ramka_obj.get_koordinate()[0], ramka_obj.get_koordinate()[1] + 1  # движение вправо, x+1
    if future_node in main.link_to_path.get_allowed_obl():
        ramka_obj.move_right = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, graph)


def moving_left_in_oblast(ramka_obj, graph):
    future_node = ramka_obj.get_koordinate()[0], ramka_obj.get_koordinate()[1] - 1  # движение влево, x-1
    if future_node in main.link_to_path.get_allowed_obl():
        ramka_obj.move_left = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, graph)


def moving_up_in_oblast(ramka_obj, graph):
    future_node = ramka_obj.get_koordinate()[0] - 1, ramka_obj.get_koordinate()[1]
    if future_node in main.link_to_path.get_allowed_obl():
        ramka_obj.move_up = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, graph)


def moving_down_in_oblast(ramka_obj, graph):
    future_node = ramka_obj.get_koordinate()[0] + 1, ramka_obj.get_koordinate()[1]
    if future_node in main.link_to_path.get_allowed_obl():
        ramka_obj.move_down = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, graph)


def processing_action_button(screen, settings_obj, ramka_obj, path_s, graph, recon_s):
    start_position = ramka_obj.get_koordinate()
    if start_position in list_all_units and main.chang_path_global is False:

        main.push_the_lever()
        path_line = PathElement(screen, settings_obj, start_position)  # Создание объекта пути
        path_s.add(path_line)  # добавить в группу путей
        main.link_to_path = path_line  # сохранить ссылку на текущий объект пути(глобально)
        main.link_to_path.set_allowed_obl(get_allowed_oblast(graph, start_position, points=6))

    elif main.chang_path_global and start_position not in list_all_units:

        main.push_the_lever()
        main.link_to_path.draw_oblast_finished = True

        path_unit = main.link_to_path.get_list_path()
        for un in recon_s:
            if path_unit[0] == un.get_koordinate():
                un.set_list_path(path_unit)
        list_all_units.add(path_unit[-1])
        list_all_units.remove(path_unit[0])