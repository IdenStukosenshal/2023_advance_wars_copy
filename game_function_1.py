import pygame
import sys


from map_element import MapElement
from recon import Recon

import main
import moving_processing as m_p

import units_location_s


def check_events(screen, settings_obj, ramka_obj, path_s, graph, recon_s):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(screen, settings_obj, event, ramka_obj, path_s, graph, recon_s)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ramka_obj, )


def check_key_down_events(screen, settings_obj, event, ramka_obj, path_s, graph, recon_s):
    if event.key == pygame.K_SPACE:
        m_p.processing_action_button(screen, settings_obj, ramka_obj, path_s, graph, recon_s)

    if event.key == pygame.K_RIGHT:
        if main.chang_path_global:
            m_p.moving_right_in_oblast(ramka_obj, graph)
        else:
            ramka_obj.move_right = True

    if event.key == pygame.K_LEFT:
        if main.chang_path_global:
            m_p.moving_left_in_oblast(ramka_obj, graph)
        else:
            ramka_obj.move_left = True

    if event.key == pygame.K_UP:
        if main.chang_path_global:
            m_p.moving_up_in_oblast(ramka_obj, graph)
        else:
            ramka_obj.move_up = True

    if event.key == pygame.K_DOWN:
        if main.chang_path_global:
            m_p.moving_down_in_oblast(ramka_obj, graph)
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



def create_my_army(screen, settings_obj, recon_s):

    for id, yx in enumerate(units_location_s.recon_positions):
        y = yx[0] * settings_obj.w_and_h_sprite_map
        x = yx[1] * settings_obj.w_and_h_sprite_map
        new_rec = Recon(id, x, y, settings_obj, screen)
        recon_s.add(new_rec)



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

