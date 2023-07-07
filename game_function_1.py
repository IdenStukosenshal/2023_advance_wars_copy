import pygame
import sys

import map_to_graph
from map_element import MapElement
from path_element import PathElement


def check_events(screen, settings_obj, ramka_obj, path_s, graph):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(screen, settings_obj, event, ramka_obj, path_s, graph)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ramka_obj, )


def check_key_down_events(screen, settings_obj, event, ramka_obj, path_s, graph):

    if event.key == pygame.K_RIGHT:
        ramka_obj.move_right = True
    if event.key == pygame.K_LEFT:
        ramka_obj.move_left = True
    if event.key == pygame.K_UP:
        ramka_obj.move_up = True
    if event.key == pygame.K_DOWN:
        ramka_obj.move_down = True

    if event.key == pygame.K_SPACE:
        if ramka_obj.path_changing_allowed is False:
            ramka_obj.path_changing_allowed = True
            start_position = ramka_obj.y_x_to_graph
            path_line = PathElement(screen, settings_obj, start_position)  # Создание объекта пути
            path_s.add(path_line)
            ramka_obj.link_to_current_path = path_line  # сохранить ссылку на текущий объект в объекте рамки, костыль?
        else:
            ramka_obj.path_changing_allowed = False

    ramka_obj.update()  # дополнительное обновление позиции, чтобы она не отставала

    if ramka_obj.path_changing_allowed is True:
        peres4et_puti(settings_obj, ramka_obj, graph)


def peres4et_puti(settings_obj, ramka_obj, graph,):
    start = ramka_obj.link_to_current_path.start_position

    if start == ramka_obj.y_x_to_graph:  # Путь не создаётся
        ramka_obj.link_to_current_path.list_path = []
        print("НЕТ ПУТИ")
        return None

    path_list = create_path(start, ramka_obj.y_x_to_graph, graph)  # расчёт пути, path_list в виде масива nodes
    rez_path_massive = []
    for y, x in path_list:
        y = y * settings_obj.w_and_h_sprite_map + settings_obj.w_and_h_sprite_map//2
        x = x * settings_obj.w_and_h_sprite_map + settings_obj.w_and_h_sprite_map//2
        rez_path_massive.append((x, y))
    if ramka_obj.path_changing_allowed:
        ramka_obj.link_to_current_path.list_path = rez_path_massive


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


def create_path(start, finish, graph):
    """Получает start, finish, graph.

    Передаёт фукции path_find аргументы, получает от неё путь в формате [(y, x), (y, x)],
     где (y, x) - это название node и её координаты.
     Возвращает путь

    """

    points = 10000

    path = map_to_graph.path_find(start, finish, graph, points)
    return path


def update_screen(screen, map_elements, ramka_obj, path_s):
    #for map_elem in map_elements.sprites():
        #map_elem.draw_map()
    # path_s.draw(screen)
    map_elements.draw(screen)
    for path in path_s.sprites():
        path.draw_path()
    ramka_obj.draw_ramka()








