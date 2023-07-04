"""В этом файле X и Y координаты поменяны местами"""


import networkx as nx

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
    nodes типа 0.0, 0.1,
     где первое число это x(номер столбца), второе y(номер строки)
     """
    g_inf = nx.Graph()
    edges = []
    len_massive = len(massive)
    len_line = len(massive[0])
    for y in range(0, len_massive, 1):
        for x in range(0, len_line, 1):  # формирование массива edges = [('a', 'b', weight)]
            for k_i, k_j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                if 0 <= y + k_i < len_massive and 0 <= x + k_j < len_line:

                    edges.append((str(x) + '.' + str(y),
                                  str(x + k_j) + '.' + str(y + k_i),
                                  max(weights[massive[y][x]], weights[massive[y + k_i][x + k_j]]))
                                 )
    g_inf.add_weighted_edges_from(edges)
    return g_inf


file_name1 = "map_1.txt"

map_massive = map_to_massive(file_name1)
graph = massive_to_graph(map_massive, weights_track)
