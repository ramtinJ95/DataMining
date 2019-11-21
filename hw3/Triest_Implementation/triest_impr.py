import random
from edge_sample import EdgeSample
from collections import defaultdict


class TriestImpr:
    def __init__(self, M):
        self.M = M
        self.sample = EdgeSample()
        self.globalTau = 0
        self.localTau = {}
        self.time = 0

    def sample_edge(self, u, v):
        if self.time <= self.M:
            return True
        elif self.flip_biased_coin():
            u_dash, v_dash = self.sample.remove_random_edge()
            return True
        return False

    def update_counters(self, u, v, op):
        common_neighborhood = self.sample.get_intersection_neighborhood(u, v)
        
        if not common_neighborhood:
            return

        eta = max(1, int(((self.time-1)*(self.time-2))/(self.M * (self.M - 1)))) 

        for c in common_neighborhood:

            if op == '+':
                self.globalTau += eta

                if c in self.localTau:
                    self.localTau[c] += eta
                else:
                    self.localTau[c]=eta

                if u in self.localTau:
                    self.localTau[u] += eta
                else:
                    self.localTau[u]=eta

                if v in self.localTau:
                    self.localTau[v] += eta
                else:
                    self.localTau[v]=eta

    def flip_biased_coin(self):
        head_prob=random.random()

        if head_prob <= self.M/self.time:
            return True
        else:
            return False

    def return_counters(self):
        return {'global': self.globalTau}

    def run(self, u, v):
        self.time += 1
        self.update_counters(u, v, '+')
        if self.sample_edge(u, v):
            self.sample.add_edge(u, v)
