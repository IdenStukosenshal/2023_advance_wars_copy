import networkx as nx
import main as m
import units_location_s

def file_map_to_massive(file_name):
    """Открывает файл.
    Возвращает массив с картой.
    """
    print("Массив карты создан")
    m = []
    with open(file_name) as f:
        for line in f:
            x = line.rstrip('\n')
            m.append(list(x))
    return m


def massive_to_graph(massive, weights):
    """Принимает массив, nodes, weights
    Возвращает взвешенный граф
    nodes типа 0.0, 0.1,
     где первое число это y(номер строки), второе х(номер столбца)

     """
    print("Граф создан")
    g_inf = nx.Graph()
    edges = []
    len_massive = len(massive)
    len_line = len(massive[0])
    for i in range(0, len_massive, 1):
        for j in range(0, len_line, 1):  # формирование массива edges = [( (y,x), (y,x), weight ), ]
            for k_i, k_j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                if 0 <= i + k_i < len_massive and 0 <= j + k_j < len_line:
                    edges.append(((i, j),
                                  (i + k_i, j + k_j),
                                  max(weights[massive[i][j]], weights[massive[i + k_i][j + k_j]]))
                                 )
    g_inf.add_weighted_edges_from(edges)
    return g_inf


def massive_to_graph_to_helicopter(massive):
    """Для helicopter все веса == 1"""
    g_heli = nx.Graph()
    edges = []
    len_massive = len(massive)
    len_line = len(massive[0])
    for i in range(0, len_massive, 1):
        for j in range(0, len_line, 1):  # формирование массива edges = [('a', 'b', weight)]
            for k_i, k_j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                if 0 <= i + k_i < len_massive and 0 <= j + k_j < len_line:
                    edges.append(((i, j),
                                  (i + k_i, j + k_j),
                                  1)
                                 )
    g_heli.add_weighted_edges_from(edges)
    return g_heli


def experimental_digraph(massive, weights):
    """Если на карте есть недостижимые точки(с максимальным весом) при пострении графа
     рёбра направленнные к ним имеют максимальный вес,
    направленные от них имеют вес соседней точки.

    На обычных участках карты рёбра симметричны(по весам), если клетка становится занятой,
     рёбра к ней будут иметь максимальный вес, а рёбра от неё обычный,
      после освобождения можно восстановить исходные веса по оставшимся рёбрам.

      Также юнит сможет передвигаться со своей занятой клетки, но не сможет занять занятую.

      Объекты одного класса будут иметь ссылку на один и тот же граф."""

    print("Экспериментальный Граф создан")
    g = nx.DiGraph()
    edges = []
    len_massive = len(massive)
    len_line = len(massive[0])
    for i in range(0, len_massive, 1):
        for j in range(0, len_line, 1):  # формирование массива edges = [( (y,x), (y,x), weight ), ]
            for k_i, k_j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                if 0 <= i + k_i < len_massive and 0 <= j + k_j < len_line:
                    max_value = max(weights.values())  #

                    if weights[massive[i][j]] == max_value:
                        edges.append(((i + k_i, j + k_j),
                                      (i, j),
                                      max(weights[massive[i][j]], weights[massive[i + k_i][j + k_j]]))
                                     )
                        edges.append(((i, j),
                                      (i + k_i, j + k_j),
                                      min(weights[massive[i][j]], weights[massive[i + k_i][j + k_j]]))
                                     )

                    elif weights[massive[i + k_i][j + k_j]] == max_value:
                        edges.append(((i + k_i, j + k_j),
                                      (i, j),
                                      min(weights[massive[i][j]], weights[massive[i + k_i][j + k_j]]))
                                     )
                        edges.append(((i, j),
                                      (i + k_i, j + k_j),
                                      max(weights[massive[i][j]], weights[massive[i + k_i][j + k_j]]))
                                     )

                    else:
                        edges.append(((i, j),
                                      (i + k_i, j + k_j),
                                      max(weights[massive[i][j]], weights[massive[i + k_i][j + k_j]]))
                                     )
                        edges.append(((i + k_i, j + k_j),
                                      (i, j),
                                      max(weights[massive[i][j]], weights[massive[i + k_i][j + k_j]]))
                                     )
    g.add_weighted_edges_from(edges)
    return g


def path_find(start, finish, graph):
    """
    :param points: кол-во очков пути юнита
    :param start: стартовая node
    :param finish: конечная node
    :param graph: граф юнита
    :return: восстановленный путь start->end
    """
    # shortest_path = nx.dijkstra_path(graph, start, finish)
    # соседи 0.0  ->   {'0.1': {'weight': 9000}, '1.0': {'weight': 9000}, '1.1': {'weight': 9000}}
    # s = g_inf.adj['0.0']
    # вес ребра = G[node1][node2]['weight']

    shortest_path = nx.astar_path(graph, start, finish)  # алгоритм A*  результат вида [(0, 1), (1, 2), (1, 3), ]

    def len_path(path_list):
        """
        проходим по списку nodes и суммируем вес рёбер
        Это лучше, чем ещё раз считать функцией
        nx.dijkstra_path_length(graph, start, finish)"""
        len_p = 0
        l, r = 0, 1
        while r != len(path_list):
            len_p += graph[path_list[l]][path_list[r]]['weight']
            l += 1
            r += 1
        return len_p

    print("путь пересчитан: ", shortest_path, "Длина пути=: ", len_path(shortest_path))
    return shortest_path


def get_allowed_oblast(unit_obj, start):
    """Формируем словарь разрешённых для посещения точек с помощью алгоритма Дейкстры
    Добавляем только те, до которых хватит очков перемещения"""
    graph = unit_obj.link_to_graph

    oblast_rez = dict()

    oblast_dict = nx.single_source_dijkstra_path_length(graph, start,)
    print(" В ОБЩЕЙ ОБЛАСТИ (4, 5)", oblast_dict[(4, 5)])
    print(" В ОБЩЕЙ ОБЛАСТИ (2, 3)", oblast_dict[(2, 3)])
    for node, sum_weight in oblast_dict.items():
        if sum_weight <= unit_obj.path_points:
            oblast_rez[node] = sum_weight
    return oblast_rez


def peres4et_puti(ramka_obj, unit_obj):
    start = m.link_to_path.start_position

    if start == ramka_obj.get_koordinate():  # Путь из двух одинаковых точек
        m.link_to_path.set_list_path([start, start])
        print("ПУТЬ из начала в начало", m.link_to_path.list_path)

    else:
        path_list = path_find(start, ramka_obj.get_koordinate(), unit_obj.link_to_graph)  # ф-ция расчёта пути
        m.link_to_path.set_list_path(path_list)


def graph_redacting(graph, settings_obj, ):
    """изменяет граф в соответствии с изменяемыми координатами юнитов,
    сейчас они хранятся в общем множестве set_all_units

    Нужно вызывать эту функцию при каждом перемещении юнита"""
    edges = []
    for y, x in units_location_s.set_all_units:  # увеличение весов
        for neigh_y, neigh_x in graph.adj[(y, x)]:
            edges.append(((neigh_y, neigh_x), (y, x), settings_obj.max_value))
    graph.add_weighted_edges_from(edges)  # изменение весов рёбер к занятым точкам

    # возвращение предыдущего состояния
    edges_orig = []
    # вес ребра = G[node1][node2]['weight']
    diff_set = m.set_all_units_copy - units_location_s.set_all_units # вычесть те позиции, которые остались занятыми
    print(diff_set, "DIFF SET")
    if diff_set:
        for y, x in diff_set:
            for neigh_y, neigh_x in graph.adj[(y, x)]:  # получаем оригинальный вес ребра, от освобождённой точки к соседям
                orig_weight = graph[(y, x)][neigh_y, neigh_x]['weight']
                edges_orig.append(((neigh_y, neigh_x), (y, x), orig_weight))
        graph.add_weighted_edges_from(edges_orig)  # изменение весов освобождённых точек

    m.set_all_units_copy = units_location_s.set_all_units.copy()    # теперь сохраняются текущие координаты

    return graph




'''
# Визуализация графа в браузере, чтобы использовать нужно установить algorithmx
import algorithmx
from algorithmx.networkx import add_graph

file_name1 = "map_tests.txt"
map_massive = file_map_to_massive(file_name1)
weights_track_tests = {'#': 1.5, 'd': 1, 'f': 1.75, '@': 9000, 'v': 9000, 't': 1}
graph = experimental_digraph(map_massive, weights_track_tests)


def draw_in_browser(graph):
    """Рисование графа в браузере
    http://localhost:5050/"""
    server = algorithmx.http_server(port=5050)
    canvas = server.canvas()

    def start():
        add_graph(canvas, graph)

    canvas.onmessage('start', start)
    server.start()


def test_path_finding():
    start = (0, 1)
    finish = (1, 15)
    path = path_find(start, finish, graph,)
    print(path)


#test_path_finding()
#draw_in_browser(graph)
'''