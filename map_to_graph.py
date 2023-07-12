import networkx as nx


def file_map_to_massive(file_name):
    """Открывает файл.
    Возвращает массив с картой.
    """
    m = []
    with open(file_name) as f:
        for line in f:
            x = line.rstrip('\n')
            m.append(list(x))
    return m


def massive_to_graph(massive, weights):
    """Принимает массив, nodes, weights
    Возвращает взвешенный граф
    nodes типа (0,0), (0,1),
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


def experimental_digraph(massive, weights, all_units_positions):
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

    edges2 = []
    for unit_point in all_units_positions:
        for neigh_y, neigh_x in g.adj[unit_point]:
            edges2.append(((neigh_y, neigh_x), unit_point, 90))
    g.add_weighted_edges_from(edges2)
    return g


def get_allowed_oblast(unit_object, start):
    """Формируем словарь разрешённых для посещения точек с помощью алгоритма Дейкстры
    Добавляем только те, до которых хватит очков перемещения"""
    graph = unit_object.link_to_graph

    oblast_rez = dict()

    oblast_dict = nx.single_source_dijkstra_path_length(graph, start,)

    for node, sum_weight in oblast_dict.items():
        if sum_weight <= unit_object.path_points:
            oblast_rez[node] = sum_weight
    return oblast_rez


def peres4et_puti(ramka_obj, unit_object, link_to_path):

    start = link_to_path.start_position

    if start == ramka_obj.get_koordinate():  # Путь из двух одинаковых точек
        link_to_path.set_list_path([start, start])
        print("ПУТЬ из начала в начало", link_to_path.list_path)
        #return link_to_path
    else:
        path_list = nx.astar_path(unit_object.link_to_graph, start, ramka_obj.get_koordinate())  # алгоритм A*  результат вида [(0, 1), (1, 2), (1, 3), ]
        link_to_path.set_list_path(path_list)
        print("идёт пересчёт пути", path_list)
        #return link_to_path


def graph_redacting(start_point, settings_obj, massive, all_units_positions):
    """изменяет граф в соответствии с изменяемыми координатами юнитов,
    Нужно вызывать эту функцию при каждом перемещении юнита"""
    unit = all_units_positions.pop(start_point)  # удаляем из общего словаря стартовую точку,
    graph = unit.link_to_graph
    start_point = unit.get_unit_path()[0]
    end_point = unit.get_unit_path()[-1]
    weights = unit.weights

    # увеличение весов к последней точке пути
    edges = []
    for neigh_y, neigh_x in graph.adj[end_point]:
        edges.append(((neigh_y, neigh_x), end_point, settings_obj.max_value))
    graph.add_weighted_edges_from(edges)  # изменение весов рёбер к занятым точкам

    # восстановление весов освобождённой точки(первой точки пути)
    edges_orig = restore_weights(graph, massive, weights, start_point)
    graph.add_weighted_edges_from(edges_orig)  # изменение весов освобождённых точек

    """ПРОБЛЕМА: ВОЗНИКАЕТ РЕБРО В ВИДЕ ПЕТЛИ, КОТОРОЕ ПОКА НЕ ВЛИЯЕТ НИ НА ЧТО"""

    for unit in all_units_positions.values():
        unit.link_to_graph = graph



def restore_weights(graph, massive, weights, start_point):
    """Восстановление рёбер по куску оригинальной карты(3, 5 или 8 соседей)"""

    edges = []
    p_y, p_x = start_point
    for n_y, n_x in graph.adj[start_point]:
        max_value = max(weights.values())
        if weights[massive[p_y][p_x]] == max_value:  # если стартовая была непроходимой (на всякий случай)
            edges.append(((n_y, n_x),
                          start_point,
                          max(weights[massive[p_y][p_x]], weights[massive[n_y][n_x]]))
                         )
            edges.append((start_point,
                          (n_y, n_x),  # если соседняя со стартовой была непроходимой
                          min(weights[massive[p_y][p_x]], weights[massive[n_y][n_x]]))
                         )

        elif weights[massive[n_y][n_x]] == max_value:
            edges.append(((n_y, n_x),
                          start_point,
                          min(weights[massive[p_y][p_x]], weights[massive[n_y][n_x]]))
                         )
            edges.append(((p_y, p_x),
                          start_point,
                          max(weights[massive[p_y][p_x]], weights[massive[n_y][n_x]]))
                         )

        else:
            edges.append(((p_y, p_x),  # то же правило, что и при создании карты
                          (n_y, n_x),
                          max(weights[massive[p_y][p_x]], weights[massive[n_y][n_x]]))
                         )
            edges.append(((n_y, n_x),
                          (p_y, p_x),
                          max(weights[massive[p_y][p_x]], weights[massive[n_y][n_x]]))
                         )

    return edges


# shortest_path = nx.dijkstra_path(graph, start, finish)
# s = g_inf.adj['0.0']
# вес ребра = G[node1][node2]['weight']

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