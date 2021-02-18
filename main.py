from collections import defaultdict
import sys
from time import sleep

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


def but(array: list, element) -> list:
    """A function returns a list without a element"""
    new = array.copy()
    new.remove(element)
    return new


class Dynasty:
    """A class visualize any dynasty"""

    def __init__(self, king) -> None:
        self.king = str(king)  # A name of a king in this moment

        self.pos = dict()  # Positions of nodes
        self.pos[self.king] = (0, 0)

        self.people = []  # A list of all people even dead
        self.edges = []  # A list if all edges

        self.marriages_w = defaultdict(str)  # The value is a husband
        self.marriages_m = defaultdict(str)  # The value is a wife
        self.sons = defaultdict(list)  # The key is mother and the value is son

    def add_pearson(self, man) -> None:
        """A function adds a new pearson to the dynasty"""
        man = str(man)

        self.people.append(man)
        self.people = list(set(self.people))

    def add_marriages(self, wife, husband) -> None:
        """A function adds a new marriage to the dynasty"""
        wife = str(wife)
        husband = str(husband)

        self.add_pearson(wife)
        self.add_pearson(husband)
        self.edges.append((wife, husband))
        self.edges = list(set(self.edges))
        self.marriages_w[wife] = husband
        self.marriages_m[husband] = wife

        self.pos[wife] = (self.pos[husband][0] + 10, self.pos[husband][1])

    def add_son(self, mother, father, son) -> None:
        """A function adds a new son to the dynasty"""
        mother, father, son = str(mother), str(father), str(son)

        self.add_marriages(mother, father)
        self.add_pearson(son)
        self.edges.append((mother, son))
        self.add_pearson(son)
        self.sons[mother].append(son)

    def king_die(self) -> None:
        """A function kills a king"""
        if self.king in self.marriages_m.keys():
            wife = self.marriages_m[self.king]
            if wife in self.sons.keys():
                self.king = self.sons[wife][0]
            else:
                print("The last king has been dead")
                sys.exit()
        else:
            print("The last king has been dead. He has not been married")
            sys.exit()

    def draw(self) -> None:
        """A function draws a graph of the dynasty"""
        if len(self.edges) < 1:
            return
        graph = nx.DiGraph()

        son = []  # A list with all sons in the dynasty. Example [("mother", "son"), ("mother2", "son2")]
        for key, value in self.sons.items():
            for i in value:
                son.append((key, i))

        graph.add_nodes_from(self.people)
        graph.add_edges_from(list(self.marriages_w.items()) + son)

        pos = graphviz_layout(graph, prog="dot")

        labels = defaultdict(str)
        for node in graph.nodes():
            labels[node] = node

        color_map = {self.king: '#FF00FF'}

        colors = [color_map.get(node, '#FF0000') for node in graph.nodes()]
        nx.draw_networkx_nodes(graph, pos, self.people, 300, node_color=colors)
        nx.draw_networkx_labels(graph, pos, labels)
        nx.draw_networkx_edges(graph, pos, edgelist=list(self.marriages_w.items()), edge_color='r', arrows=False)
        nx.draw_networkx_edges(graph, pos, edgelist=son, edge_color='b', arrows=True)
        plt.show()


g = Dynasty("Frederick I of Ansbach and Bayreuth")
g.add_son("Sophia Jagiellon", "Frederick I of Ansbach and Bayreuth", "Henry VIII of England")
g.add_son("Elizabeth of York", "Henry VII of England", "Arthur, Prince of Wales")
g.add_son("Elizabeth of York", "Henry VII of England", "Margaret Tudor, Queen of Scots")
g.add_son("Elizabeth of York", "Henry VII of England", "Mary Tudor, Queen of France")
g.add_son("Anne Boleyn", "Henry VIII of England", "Mary I of England")
g.draw()
g.king_die()
g.draw()
