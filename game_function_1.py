import pygame
import sys

import map_to_graph
from map_element import MapElement
from path_element import PathElement
import main

from units_location_s import list_all_units

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
        processing_action_button(screen, settings_obj, ramka_obj, path_s, graph, recon_s)

    if event.key == pygame.K_RIGHT:
        if main.chang_path_global:
            vektor = 'right'
            if is_moving_alloved(vektor, ramka_obj, main.link_to_path.get_allowed_obl()):
                ramka_obj.move_right = True
                ramka_obj.update()
                peres4et_puti(settings_obj, ramka_obj, graph)
        else:
            ramka_obj.move_right = True

    if event.key == pygame.K_LEFT:
        if main.chang_path_global:
            vektor = 'left'
            if is_moving_alloved(vektor, ramka_obj, main.link_to_path.get_allowed_obl()):
                ramka_obj.move_left = True
                ramka_obj.update()
                peres4et_puti(settings_obj, ramka_obj, graph)
        else:
            ramka_obj.move_left = True

    if event.key == pygame.K_UP:
        if main.chang_path_global:
            vektor = 'up'
            if is_moving_alloved(vektor, ramka_obj, main.link_to_path.get_allowed_obl()):
                ramka_obj.move_up = True
                ramka_obj.update()
                peres4et_puti(settings_obj, ramka_obj, graph)
        else:
            ramka_obj.move_up = True

    if event.key == pygame.K_DOWN:
        if main.chang_path_global:
            vektor = 'down'
            if is_moving_alloved(vektor, ramka_obj, main.link_to_path.get_allowed_obl()):
                ramka_obj.move_down = True
                ramka_obj.update()
                peres4et_puti(settings_obj, ramka_obj, graph)
        else:
            ramka_obj.move_down = True

    #ramka_obj.update()  # дополнительное обновление позиции, чтобы путь не не отставал от рамки на 1 шаг


def processing_action_button(screen, settings_obj, ramka_obj, path_s, graph, recon_s):
    start_position = ramka_obj.get_koordinate()
    if start_position in list_all_units and main.chang_path_global is False:

        main.push_the_lever()
        path_line = PathElement(screen, settings_obj, start_position)  # Создание объекта пути
        path_s.add(path_line)  # добавить в группу путей
        main.link_to_path = path_line  # сохранить ссылку на текущий объект пути(глобально)
        main.link_to_path.set_allowed_obl(map_to_graph.get_allowed_oblast(graph, start_position, points=6))

    elif main.chang_path_global and start_position not in list_all_units:

        main.push_the_lever()
        main.link_to_path.draw_oblast_finished = True

        pa = main.link_to_path.get_node_list_path()
        for un in recon_s:
            if pa[0] == un.get_koordinate():
                un.set_list_path(pa)  # Здесь список передаётся в виде нод, переделывается в координаты в методе
        list_all_units.add(pa[-1])
        list_all_units.remove(pa[0])

def is_moving_alloved(vektor, ramka_obj, allowed_oblast):
    """Получает направление, вычисляет будущую точку
    Возвращает bool, координата вида (y, x)"""
    future_node = 0
    if vektor == 'right':
        future_node = ramka_obj.get_koordinate()[0], ramka_obj.get_koordinate()[1]+1
    elif vektor == 'left':
        future_node = ramka_obj.get_koordinate()[0], ramka_obj.get_koordinate()[1]-1
    elif vektor == 'up':
        future_node = ramka_obj.get_koordinate()[0]-1, ramka_obj.get_koordinate()[1]
    elif vektor == 'down':
        future_node = ramka_obj.get_koordinate()[0]+1, ramka_obj.get_koordinate()[1]

    if future_node in allowed_oblast:
        #print("ДВИГАТЬСЯ МОЖНО")
        pass
    else:
        print("ДВИГАТЬСЯ НЕЛЬЗЯ, очки перемещения закончились")

    return future_node in allowed_oblast


def peres4et_puti(settings_obj, ramka_obj, graph,):
    start = main.link_to_path.start_position

    if start == ramka_obj.get_koordinate():  # Путь не создаётся
        main.link_to_path.set_list_path([])
        print("НЕТ ПУТИ")
        return None

    path_list = create_path(start, ramka_obj.get_koordinate(), graph)  # расчёт пути, path_list в виде масива nodes
    rez_path_massive = []
    for y, x in path_list:
        y = y * settings_obj.w_and_h_sprite_map + settings_obj.w_and_h_sprite_map//2
        x = x * settings_obj.w_and_h_sprite_map + settings_obj.w_and_h_sprite_map//2
        rez_path_massive.append((x, y))
    #if main.chang_path_global:
    main.link_to_path.set_list_path(rez_path_massive)  # массив координат в пикселях



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

    path = map_to_graph.path_find(start, finish, graph)
    return path


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








