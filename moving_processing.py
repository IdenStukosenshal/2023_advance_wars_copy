import main

from map_to_graph import get_allowed_oblast
from map_to_graph import peres4et_puti
from map_to_graph import graph_redacting
from path_element import PathElement
from units_location_s import set_all_units


def moving_right_in_oblast(ramka_obj, unit_obj):
    """Определение следующей точки.
    Если она в списке, двигаем рамку, пересчитываем путь"""
    future_node = ramka_obj.get_koordinate()[0], ramka_obj.get_koordinate()[1] + 1  # движение вправо, x+1
    if future_node in main.link_to_path.get_allowed_obl():
        ramka_obj.move_right = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, unit_obj)


def moving_left_in_oblast(ramka_obj, unit_obj):
    future_node = ramka_obj.get_koordinate()[0], ramka_obj.get_koordinate()[1] - 1  # движение влево, x-1
    if future_node in main.link_to_path.get_allowed_obl():
        ramka_obj.move_left = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, unit_obj)


def moving_up_in_oblast(ramka_obj, unit_obj):
    future_node = ramka_obj.get_koordinate()[0] - 1, ramka_obj.get_koordinate()[1]
    if future_node in main.link_to_path.get_allowed_obl():
        ramka_obj.move_up = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, unit_obj)


def moving_down_in_oblast(ramka_obj, unit_obj):
    future_node = ramka_obj.get_koordinate()[0] + 1, ramka_obj.get_koordinate()[1]
    if future_node in main.link_to_path.get_allowed_obl():
        ramka_obj.move_down = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, unit_obj)


def processing_action_button(screen, settings_obj, path_s, recon_s, unit_obj, ramka_obj):
    ramka_koord = ramka_obj.get_koordinate()

    if ramka_koord in set_all_units and main.chang_path_global is False and unit_obj is not None:

        set_all_units.remove(ramka_koord)  # чтобы была возможность переместиться на свою же позицию(остаться)
        main.koord_and_units_dict.pop(ramka_koord)

        main.push_the_lever()
        print(set_all_units, "удалено", ramka_koord)
        path_line = PathElement(screen, settings_obj, ramka_koord)  # Создание объекта пути
        path_s.add(path_line)  # добавить в группу путей
        main.link_to_path = path_line  # сохранить ссылку на текущий объект пути(глобально)

        allowed_obl = get_allowed_oblast(unit_obj, ramka_koord)
        main.link_to_path.set_allowed_obl(allowed_obl)

    elif main.chang_path_global: # and ramka_obj.get_koordinate() not in set_all_units:

        main.push_the_lever()
        main.link_to_path.draw_oblast_finished = True

        path_u = main.link_to_path.get_list_path()
        for unit_rec in recon_s:
            if path_u[0] == unit_rec.get_koordinate(): # выбор перемещаемого
                unit_rec.set_list_path(path_u)  # присваиваем юниту его путь
                set_all_units.add(path_u[-1])
                unit_rec.link_to_graph = graph_redacting(unit_rec.link_to_graph, settings_obj)

                main.koord_and_units_dict[path_u[-1]] = unit_rec
