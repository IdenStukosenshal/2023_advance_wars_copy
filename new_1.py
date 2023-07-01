
import networkx as nx
import matplotlib.pyplot as plt
import algorithmx
from algorithmx.networkx import add_graph

from path_finding import path_find


weights_inf = {'#': 1, 'd': 1, 'f': 1, '@': 2, 'v': 2, 't': 1}
weights_track = {'#': 1.5, 'd': 1, 'f': 1.75, '@': 9000, 'v': 9000, 't': 1}


def map_to_massive(file_name):
    """Открывает файл
    Возвращает массив с картой.
    карта должна быть с нечётными длинами сторон
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
     """
    g_inf = nx.Graph()
    edges = []
    len_massive = len(massive)
    len_line = len(massive[0])
    for i in range(0, len_massive, 1):
        for j in range(0, len_line, 1):  # формирование массива edges = [('a', 'b', weight)]
            for k_i, k_j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                if 0 <= i + k_i < len_massive and 0 <= j + k_j < len_line:
                    edges.append((str(i) + '.' + str(j),
                                  str(i + k_i) + '.' + str(j + k_j),
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
                    edges.append((str(i) + '.' + str(j),
                                  str(i + k_i) + '.' + str(j + k_j),
                                  1)
                                 )
    g_heli.add_weighted_edges_from(edges)
    return g_heli


file_name1 = "map_1.txt"

map_massive = map_to_massive(file_name1)
graph = massive_to_graph(map_massive, weights_track)

start = '0.1'
finish = '0.16'

path = path_find(start, finish, graph, points=22)
print(path)


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
