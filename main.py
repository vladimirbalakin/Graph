from collections import defaultdict
import sys
from time import sleep

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


def but(array, value):
    new = array.copy()
    new.remove(value)
    return new


class Dynasty:

    def __init__(self, king):
        self.king = str(king)
        self.people = []
        self.edges = []
        self.marriages_w = defaultdict(str)  # The value is a husband
        self.marriages_m = defaultdict(str)  # The value is a wife
        self.sons = defaultdict(str)

    def add_pearson(self, man):
        man = str(man)
        self.people.append(man)
        self.people = list(set(self.people))

    def add_marriages(self, wife, husband):
        wife = str(wife)
        husband = str(husband)
        self.add_pearson(wife)
        self.add_pearson(husband)
        self.edges.append((wife, husband))
        self.edges = list(set(self.edges))
        self.marriages_w[wife] = husband
        self.marriages_m[husband] = wife

    def add_son(self, mother, father, son):
        mother, father, son = str(mother), str(father), str(son)
        self.add_marriages(mother, father)
        self.add_pearson(son)
        self.edges.append((mother, son))
        self.add_pearson(son)
        self.sons[mother] = son

    def king_die(self):
        if self.king in self.marriages_m.keys():
            wife = self.marriages_m[self.king]
            if wife in self.sons.keys():
                self.king = self.sons[wife]
            else:
                sys.exit()
        else:
            sys.exit()

    def draw(self):
        if len(self.edges) < 1:
            return
        # print(self.edges, type(self.edges))
        # g = igraph.Graph(list(self.edges))
        # layout = g.layout("kk")
        # igraph.plot(g, layout=layout)
        graph = nx.DiGraph()
        graph.add_nodes_from(self.people)
        graph.add_edges_from(list(self.marriages_w.items()) + list(self.sons.items()))
        pos = graphviz_layout(graph, prog="dot")
        labels = defaultdict(str)
        for node in graph.nodes():
            labels[node] = node
        nx.draw_networkx_nodes(graph, pos, but(self.people, self.king), 300, "#FF0000")
        # nx.draw_networkx_nodes(graph, pos, self.people, 300, "#FF0000")
        nx.draw_networkx_nodes(graph, pos, self.king, 300, "#FF00FF")
        nx.draw_networkx_labels(graph, pos, labels)
        nx.draw_networkx_edges(graph, pos, edgelist=list(self.marriages_w.items()), edge_color='r', arrows=False)
        nx.draw_networkx_edges(graph, pos, edgelist=list(self.sons.items()), edge_color='b', arrows=True)
        plt.show()


g = Dynasty(0)
g.add_son(1, 0, 9)
g.draw()
g.king_die()
sleep(3)
g.add_son(4, 9, 6)
g.draw()
