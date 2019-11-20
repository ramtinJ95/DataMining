import random
from collections import defaultdict


class EdgeSample:
    def __init__(self):
        self.S = {}
        self.neighborhood = defaultdict(set)

    def add_edge(self, u, v):
        self.S[(u, v)] = 1
        self.edit_neighborhood('+', u, v)

    def remove_random_edge(self):
        rand_choice = random.randint(0, len(self.S)-1)
        tempKeys = list(self.S.keys())
        key = tempKeys[rand_choice]
        self.S.pop(key)
        self.edit_neighborhood('-', key[0], key[1])
        return key[0], key[1]

    def get_intersection_neighborhood(self, u, v):
        if u in self.neighborhood and v in self.neighborhood:
            return self.neighborhood[u].intersection(self.neighborhood[v])
        else:
            return None

    def edit_neighborhood(self, op, u, v):
        if op == '+':
            self.neighborhood[u].add(v)
            self.neighborhood[v].add(u)
        elif op == '-':
            try:
                self.neighborhood[u].remove(v)
                self.neighborhood[v].remove(u)
            except:
                pass
        if not self.neighborhood[u]:
            self.neighborhood.pop(u)

        if not self.neighborhood[v]:
            self.neighborhood.pop(v)
