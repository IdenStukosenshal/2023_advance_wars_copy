import networkx as nx


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
    # вес ребра = G[1][2]['weight']

    shortest_path = nx.astar_path(graph, start, finish)  # алгоритм A*  результат вида ['0.1', '1.2', '1.3']

    def len_path(path_list):
        """проходим по списку nodes и суммируем вес рёбер
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
