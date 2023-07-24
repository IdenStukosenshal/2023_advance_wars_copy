from my_army.recon_new import Recon
from my_army.infantry import Inf
from my_army.helicopter import Helicopter
from map_to_graph import experimental_digraph, massive_to_graph_to_helicopter
from units_location_s import recon_positions, infantry_positions, helicopters_position


def create_recon_squad(screen, settings_obj, gr_force_s, all_units_positions):
    """Создаёт объект, добавляет ссылку в словарь и в группу"""
    for yx in recon_positions:
        y = yx[0] * settings_obj.w_and_h_sprite_map
        x = yx[1] * settings_obj.w_and_h_sprite_map
        new_rec = Recon(x, y, settings_obj, screen)
        all_units_positions[(yx[0], yx[1])] = new_rec  # добавление в общий словарь
        gr_force_s.add(new_rec)


def create_infantry_squad(screen, settings_obj, gr_force_s, all_units_positions):
    """Создаёт объект, добавляет ссылку в словарь и в группу"""
    for yx in infantry_positions:
        y = yx[0] * settings_obj.w_and_h_sprite_map
        x = yx[1] * settings_obj.w_and_h_sprite_map
        new_inf = Inf(x, y, settings_obj, screen)
        all_units_positions[(yx[0], yx[1])] = new_inf  # добавление в общий словарь
        gr_force_s.add(new_inf)


def create_helicopter_squad(screen, settings_obj, heli_s, all_heli_s_positions):
    """Создаёт объект, добавляет ссылку в словарь и в группу"""
    for yx in helicopters_position:
        y = yx[0] * settings_obj.w_and_h_sprite_map
        x = yx[1] * settings_obj.w_and_h_sprite_map
        new_heli = Helicopter(x, y, settings_obj, screen)
        all_heli_s_positions[(yx[0], yx[1])] = new_heli
        heli_s.add(new_heli)


def preparing_graph(map_massive, settings_obj, all_units_positions, all_heli_s_positions, gr_force_s, heli_s):
    """
     создаёт графы для каждого типа юнитов на основе карты и их позиций, присваивает юнитам графы в группах
    """
    inf_weights = settings_obj.weights_inf
    recon_weights = settings_obj.weights_track
    max_weight = settings_obj.max_value

    inf_graph = experimental_digraph(map_massive, inf_weights, all_units_positions)
    for unit in gr_force_s:
        if unit.type_unit == settings_obj.infantry_type:
            unit.link_to_graph = inf_graph

    recon_graph = experimental_digraph(map_massive, recon_weights, all_units_positions)
    for unit in gr_force_s:
        if unit.type_unit == settings_obj.recon_type:
            unit.link_to_graph = recon_graph

    heli_graph = massive_to_graph_to_helicopter(map_massive, max_weight, all_heli_s_positions)
    for heli in heli_s:
        heli.link_to_graph = heli_graph
