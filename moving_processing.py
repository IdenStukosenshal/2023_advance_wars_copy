
from map_to_graph import peres4et_puti


def moving_right_in_oblast(ramka_obj, unit_object, link_to_path):
    """Определение следующей точки.
    Если она в списке, двигаем рамку, пересчитываем путь"""
    future_node = ramka_obj.get_koordinate()[0], ramka_obj.get_koordinate()[1] + 1  # движение вправо, x+1

    if future_node in link_to_path.get_allowed_obl():
        ramka_obj.move_right = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, unit_object, link_to_path)


def moving_left_in_oblast(ramka_obj, unit_object, link_to_path):
    future_node = ramka_obj.get_koordinate()[0], ramka_obj.get_koordinate()[1] - 1  # движение влево, x-1

    if future_node in link_to_path.get_allowed_obl():
        ramka_obj.move_left = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, unit_object, link_to_path)


def moving_up_in_oblast(ramka_obj, unit_object, link_to_path):
    future_node = ramka_obj.get_koordinate()[0] - 1, ramka_obj.get_koordinate()[1]

    if future_node in link_to_path.get_allowed_obl():
        ramka_obj.move_up = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, unit_object, link_to_path)


def moving_down_in_oblast(ramka_obj, unit_object, link_to_path):
    future_node = ramka_obj.get_koordinate()[0] + 1, ramka_obj.get_koordinate()[1]

    if future_node in link_to_path.get_allowed_obl():
        ramka_obj.move_down = True
        ramka_obj.update()
        peres4et_puti(ramka_obj, unit_object, link_to_path)






