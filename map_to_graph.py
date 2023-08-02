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


def massive_to_graph_to_helicopter(map_massive, max_weight, all_helicopters_positions):
    """
    Создание графа для конкретного класса, веса карты не влияют, поэтому
    для helicopter все веса == 1 кроме занятых точек
    """
    print("Граф для air_forces создан")
    g = nx.DiGraph()
    edges = []
    len_massive = len(map_massive)
    len_line = len(map_massive[0])

    for i in range(0, len_massive, 1):
        for j in range(0, len_line, 1):  # формирование массива edges = [( (y,x), (y,x), weight ), ]
            for k_i, k_j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                if 0 <= i + k_i < len_massive and 0 <= j + k_j < len_line:
                    edges.append(((i, j),
                                  (i + k_i, j + k_j),
                                  1)
                                 )
                    edges.append(((i + k_i, j + k_j),
                                  (i, j),
                                  1)
                                 )
    g.add_weighted_edges_from(edges)

    edges2 = []
    for unit_point in all_helicopters_positions:
        for neigh_y, neigh_x in g.adj[unit_point]:
            edges2.append(((neigh_y, neigh_x), unit_point, max_weight))
    g.add_weighted_edges_from(edges2)

    """Это можно переделать, добавлять рёбра в самом процессе, а не после"""
    return g


def experimental_digraph(massive, weights, all_units_positions):
    """Если на карте есть недостижимые точки(с максимальным весом) при пострении графа
     рёбра направленнные к ним и от них имеют максимальный вес.
    На обычных участках карты рёбра симметричны(max, по весу), если клетка становится занятой,
     рёбра к ней будут иметь максимальный вес, а рёбра от неё не изменятся,
      чтобы юнит смог покинуть занятую клетку, но не смог занять занятую.

      Объекты одного класса будут иметь ссылку на один и тот же граф."""

    print("Граф для ground_forces создан")
    g = nx.DiGraph()
    edges = []
    len_massive = len(massive)
    len_line = len(massive[0])
    max_value = weights['inaccessible']
    for i in range(0, len_massive, 1):
        for j in range(0, len_line, 1):  # формирование массива edges = [( (y,x), (y,x), weight ), ]
            for k_i, k_j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                if 0 <= i + k_i < len_massive and 0 <= j + k_j < len_line:
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
            edges2.append(((neigh_y, neigh_x), unit_point, max_value))
    g.add_weighted_edges_from(edges2)

    """Это можно переделать, добавлять рёбра в самом процессе, а не после"""
    return g


def calculate_allowed_oblast(unit_object, start):
    """Формируем словарь разрешённых для посещения точек с помощью алгоритма Дейкстры
    Добавляем только те, до которых хватит очков перемещения
    возвращает словарь вида {(6, 6): 6.0, (6, 7): 7.5, ...}
    Вызывается 1 раз при выборе юнита"""
    graph = unit_object.link_to_graph

    oblast_rez = dict()

    oblast_dict = nx.single_source_dijkstra_path_length(graph, start,)  # алгоритм Дейкстры от точки старта

    for node, sum_weight in oblast_dict.items():
        if sum_weight <= unit_object.path_points:
            oblast_rez[node] = sum_weight
    return oblast_rez


def peres4et_puti(ramka_obj, unit_object,):
    """Вызывается при каждом перемещении рамки после выбора юнита, присваивает объекту пути
    список пути вида [(0, 1), (1, 2), (1, 3), ...]"""

    start = unit_object.link_to_path.start_position

    if start == ramka_obj.get_koordinate():
        unit_object.link_to_path.set_list_path([start])
        # это для того, чтобы обнулить путь при возвращении рамки на юнита, иначе остаться на месте не получится

    else:
        path_list = nx.astar_path(unit_object.link_to_graph, start, ramka_obj.get_koordinate())  # алгоритм A*
        # A* может принимать эвристическую функцию для ускорения поиска пути или хотя бы для того, чтобы сделать путь более естественным(более прямым)
        # Похоже сейчас это равносильно алгоритму Дейкстры

        unit_object.link_to_path.set_list_path(path_list)
        # получаем по ссылке объект пути и изменяем его

    def len_path(link_t_pat, ):
        a_dict = link_t_pat.get_allowed_obl()
        p_list = link_t_pat.get_list_path()
        end = p_list[-1]
        return a_dict[end]
    count_points = len_path(unit_object.link_to_path)
    #print(f"будет израсходованно {count_points} очков из {unit_object.path_points} на пути: {unit_object.link_to_path.get_list_path()}, тип юнита:{unit_object.type_unit}")


def graph_redacting(start_point, settings_obj, massive, unit_positions,):
    """изменяет граф в соответствии с изменяемыми координатами юнитов,
    Нужно вызывать эту функцию при каждом перемещении юнита,
    все рёбра, связанные со стартовой и конечной точкой

    + Возможно каким-то непонятным способом образуется 9-ое ребро из задействованной точки,
    проверить
    """
    unit = unit_positions[start_point]
    start_point = unit.get_unit_path()[0]
    end_point = unit.get_unit_path()[-1]

    if start_point != end_point:  # только в этом случае удаляем старт, поскольку сохранение произошло до этого
        unit_positions.pop(start_point)  # УСТАРЕЛО, теперь выбор той же точки не доступен
    # изменяем графы для всех типов юнитов в соответствии с их весами

    for current_type in settings_obj.list_all_types:  # итераций по числу типов, пока всего 3
        for unit in unit_positions.values():  # изменение графа у всех юнитов чтобы не осталось персональной копии
            if unit.type_unit == current_type:  # только для соответствующего типа
                current_graph = unit.link_to_graph

                weight = settings_obj.all_weights[current_type]  # словарь self.all_weights = {'infantry': self.weights_inf ...}
                max_value = weight['inaccessible']

                edges = restore_weights(current_graph, massive, weight, start_point)
                current_graph.add_weighted_edges_from(edges)

                edges = end_point_weighting(current_graph, max_value, end_point)
                current_graph.add_weighted_edges_from(edges)

                unit.link_to_graph = current_graph  # присвоение изменённого графа

        """Изменяем граф только у юнитов одного словаря, в котором текущий юнит,
         поскольку юниты из разных словарей могут находиться на одной точке и не влияют друг на друга"""

        """Сейчас происходит лишнее изменение графов, поскольку самих юнитов больше, чем их типов
        Можно составлять словарь из типа и изменённого графа и проверять вхождение"""



def restore_weights(graph, massive, weights, start_point):
    """Восстановление только входящих рёбер к стартовой точке по куску оригинальной карты(3, 5 или 8 соседей)
    Исходящие не были затронуты"""
    edges = []
    p_y, p_x = start_point
    for n_y, n_x in graph.adj[start_point]:
        edges.append(((n_y, n_x),
                      start_point,
                      max(weights[massive[p_y][p_x]], weights[massive[n_y][n_x]]))
                     )
    return edges


def end_point_weighting(graph, max_value, end_point):
    """утяжеление весов рёбер к занятой точке"""
    edges = []
    for neigh_y, neigh_x in graph.adj[end_point]:
        edges.append(((neigh_y, neigh_x), end_point, max_value))
    return edges


# shortest_path = nx.dijkstra_path(graph, start, finish)
# s = g_inf.adj['0.0']
# вес ребра = G[node1][node2]['weight']


'''
# Визуализация графа в браузере, чтобы использовать нужно установить algorithmx
import algorithmx
from algorithmx.networkx import add_graph

units_positions = [(2, 3), (4, 5)]
file_name1 = "map_tests.txt"
file_name2 = "map_1.txt"
map_massive = file_map_to_massive(file_name2)
weights_track_tests = {'#': 1.5, 'd': 1, 'f': 2, '@': 90, 'v': 90, 't': 1.125, 'inaccessible': 90}
graph = experimental_digraph(map_massive, weights_track_tests, units_positions)


def draw_in_browser(graph):
    """Рисование графа в браузере
    http://localhost:5050/"""
    server = algorithmx.http_server(port=5050)
    canvas = server.canvas()

    def start():
        add_graph(canvas, graph)

    canvas.onmessage('start', start)
    server.start()

#draw_in_browser(graph)
'''
