import pygame

import sys

import map_to_graph
from map_element import MapElement


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def create_map(file_name, settings_obj, screen, map_elements):
    """получает имя файла с картой, объект screen
    вызывает функцию, которая создаёт массив элементов из файла.
    Для каждого элемента вычисляется его координаты(исходя из размера спрайта).
    Координаты, элемент массива, объект screen передаются в конструктор класса MapElement

    каждый элемент добавляется в группу

    """
    map_massive = map_to_graph.file_map_to_massive(file_name)

    for i in range(len(map_massive)):
        for j in range(len(map_massive[0])):
            x = j * settings_obj.w_and_h_sprite_map
            y = i * settings_obj.w_and_h_sprite_map

            new_element = MapElement(x, y, map_massive[i][j], screen)

            map_elements.add(new_element)


def update_screen(map_elements):
    for map_elem in map_elements.sprites():
        map_elem.draw_map()





