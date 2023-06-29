import heapq
import networkx as nx
import matplotlib.pyplot as plt
import algorithmx
from algorithmx.networkx import add_graph

"""
inf # 1 d 1 f 1 @ 2 v 2 t 1
"""


def map_to_massive():
    """Открывает файл
    Возвращает массив
    карта должна быть с нечётными длинами сторон
    """
    m = []
    with open("map_1.txt") as f:
        for line in f:
            x = line.rstrip('\n')
            m.append(list(x))
    return m

def massive_to_graph_inf(massive):
    """Принимает массив
    Возвращает взвешенный граф
    для infantry
     """
    g_inf = nx.Graph()
    weights = {'#': 1, 'd': 1, 'f': 1, '@': 2, 'v': 2, 't': 1}
    nodes = []
    edges = []
    len_massive = len(massive)
    len_line = len(massive[0])

    for i in range(len_massive):
        for j in range(len_line):
            nodes.append(str(i) + '.' + str(j)) # имя node состоит из её координат '0.1', '0.2'

    for i in range(0, len_massive, 2):
        for j in range(0, len_line, 2):  # формирование массива edges = [('a', 'b', weight)]
            for k_i, k_j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):

                if 0 <= i + k_i < len_massive and 0 <= j + k_j < len_line:
                    edges.append((str(i) + '.' + str(j),
                                  str(i + k_i) + '.' + str(j + k_j),
                                  max(weights[massive[i][j]], weights[massive[i + k_i][j + k_j]]))
                                 )


    """
    g_inf.add_nodes_from(nodes)
    g_inf.add_weighted_edges_from(edges)
    """

    def draw():
        g_inf.add_nodes_from(nodes)
        g_inf.add_weighted_edges_from(edges)

        plt.figure()
        pos = nx.spring_layout(g_inf)
        weight_labels = nx.get_edge_attributes(g_inf, 'weight')
        nx.draw(g_inf, pos, font_color='white', node_shape='s', with_labels=True, )
        nx.draw_networkx_edge_labels(g_inf, pos, edge_labels=weight_labels)

        plt.show()

    #draw()

    g_inf.add_nodes_from(nodes)
    g_inf.add_weighted_edges_from(edges)

    def draw_in_browser():
        server = algorithmx.http_server(port=5050)
        canvas = server.canvas()

        def start():
            add_graph(canvas, g_inf)

        canvas.onmessage('start', start)
        server.start()  # http://localhost:5050/

    draw_in_browser()


massive_to_graph_inf(map_to_massive())


def massive_to_graph_truck(massive):
    """Принимает массив
    Возвращает граф
     """
    pass


