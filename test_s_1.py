"""Прверил добавление названия node как (y, x)"""

import networkx as nx
import algorithmx
from algorithmx.networkx import add_graph


g = nx.Graph()
edges = [ ((1, 2), (1, 3), 3), ((1, 3), (1, 4), 4), ((1, 4), (1, 2), 5) ]
edges.append( ((1, 4), (1, 10), 10)  )
g.add_weighted_edges_from(edges)



def draw_in_browser(graph):
    """Рисование графа в браузере
    http://localhost:5050/"""
    server = algorithmx.http_server(port=5050)
    canvas = server.canvas()

    def start():
        add_graph(canvas, graph)

    canvas.onmessage('start', start)
    server.start()


draw_in_browser(g)

