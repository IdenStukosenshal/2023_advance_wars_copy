import pygame
import sys

import map_to_graph
from map_element import MapElement
from path_element import PathElement
from ramka import Ramka


def check_events(ramka_obj, start_experim):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, ramka_obj, start_experim)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ramka_obj, )


def check_key_down_events(event, ramka_obj, start_experim):
    if event.key == pygame.K_RIGHT:
        ramka_obj.move_right = True
    if event.key == pygame.K_LEFT:
        ramka_obj.move_left = True
    if event.key == pygame.K_UP:
        ramka_obj.move_up = True
    if event.key == pygame.K_DOWN:
        ramka_obj.move_down = True

    if event.key == pygame.K_SPACE:
        start_experim.append(ramka_obj.y_x_to_graph)
        ramka_obj.path_drawing_allowed = True

    if event.key == pygame.K_BACKSPACE:
        ramka_obj.path_drawing_allowed = False


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


def create_path(start, finish, map_massive, screen, settings_obj):
    """Получает словарь весов, graph, start, finish, points

    Передаёт фукции path_find аргументы, получает от неё путь в str формате, преобразовывает в int,
    И создаёт объект линии на основе пути

    По идее, граф должен строиться где-то вне, при выборе юнита"""

    weights_track = {'#': 1.5, 'd': 1, 'f': 1.75, '@': 9000, 'v': 9000, 't': 1.25} # тестовые данные

    points = 1000000
    graph = map_to_graph.massive_to_graph(map_massive, weights_track)

    path = map_to_graph.path_find(start, finish, graph, points)
    rez_path_massive = []
    for yx in path:
        yx = yx.split('.')
        y = int(yx[0]) * settings_obj.w_and_h_sprite_map + settings_obj.w_and_h_sprite_map//2
        x = int(yx[1]) * settings_obj.w_and_h_sprite_map + settings_obj.w_and_h_sprite_map//2
        rez_path_massive.append((x, y))
    path_line = PathElement(rez_path_massive, screen)

    path_line.draw_path()


def update_screen(map_elements, ramka_obj):
    for map_elem in map_elements.sprites():
        map_elem.draw_map()
    ramka_obj.draw_ramka()








