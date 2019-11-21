import random
from edge_sample import EdgeSample
from collections import defaultdict


class TriestBase:
    def __init__(self, M):
        self.M = M
        self.sample = EdgeSample()
        self.globalTau = 0
        self.localTau = {}
        self.time = 0

    def sample_edge(self, u, v):
        if self.time <= self.M:
            return True
        elif random.random() <= (self.M / self.time):
            u_dash, v_dash = self.sample.remove_random_edge()
            self.update_counters(u_dash, v_dash, '-')
            return True
        return False

    def update_counters(self, u, v, op):
        common_neighborhood = self.sample.get_intersection_neighborhood(u, v)

        if not common_neighborhood:
            return

        for c in common_neighborhood:
            if op == '+':
                self.globalTau += 1

                if c in self.localTau:
                    self.localTau[c] += 1
                else:
                    self.localTau[c] = 1

                if u in self.localTau:
                    self.localTau[u] += 1
                else:
                    self.localTau[u] = 1

                if v in self.localTau:
                    self.localTau[v] += 1
                else:
                    self.localTau[v] = 1
            elif op == '-':
                self.globalTau -= 1

                self.localTau[c] -= 1
                if self.localTau[c] == 0:
                    self.localTau.pop(c)

                self.localTau[u] -= 1
                if self.localTau[u] == 0:
                    self.localTau.pop(u)

                self.localTau[v] -= 1
                if self.localTau[v] == 0:
                    self.localTau.pop(v)

    def flip_coin(self):
        head = random.random()
        if head <= self.M/self.time:
            return True
        else:
            return False

    def return_counters(self):
        eps = max(1, ((self.time) * (self.time - 1) * (self.time - 2)
                      ) / (self.M * (self.M - 1) * (self.M - 2)))

        global_estimate = int(eps * self.globalTau)

        for key in self.localTau:
            self.localTau[key] = int(self.localTau[key] * eps)

        return {'global': global_estimate}

    def run(self, u, v):
        self.time += 1
        if self.sample_edge(u, v):
            self.sample.add_edge(u, v)
            self.update_counters(u, v, '+')
