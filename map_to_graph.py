import networkx as nx

weights_inf = {'#': 1, 'd': 1, 'f': 1, '@': 2, 'v': 2, 't': 1}
weights_track = {'#': 1.5, 'd': 1, 'f': 1.75, '@': 9000, 'v': 9000, 't': 1}


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
    nodes типа 0.0, 0.1,
     где первое число это y(номер строки), второе х(номер столбца)

     """
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


def path_find(start, finish, graph, points=10):
    """
    :param points: кол-во очков пути юнита
    :param start: стартовая node
    :param finish: конечная node
    :param graph: граф юнита
    :return: восстановленный путь start->end или None, если пути нет
    """
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

    if len_path(shortest_path) > points:
        return None
    return shortest_path

'''
# Визуализация графа в браузере, чтобы использовать нужно установить algorithmx
import algorithmx
from algorithmx.networkx import add_graph

file_name1 = "map_1.txt"
map_massive = file_map_to_massive(file_name1)
graph = massive_to_graph(map_massive, weights_track)


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
    path = path_find(start, finish, graph, points=22)
    print(path)


test_path_finding()
draw_in_browser(graph)
'''