import random

class Edge:
    def __init__(self, frm, to):
        if frm < to:
            self.frm = frm
            self.to = to
        else:
            self.to = frm
            self.frm = to

    def __hash__(self):
        return hash((self.frm, self.to))

    def __eq__(self, other):
        return isinstance(self, type(other)) and other.frm == self.frm and self.to == other.to

class Triest_basic:
    def __init__(self, S_size): # S_size is M in the paper
        self.time = 0 # t in the paper
        self.tau = 0
        self.edge_sampled = set()
        self.S_size = S_size
        self.counters = {}
    
    def sample_edge(self, edge):
        if self.time <= self.S_size:
            return True
        if random.random() <= (self.S_size / self.time):
            edge_to_remove = random.sample(self.edge_sampled,1)[0]
            self.edge_sampled.remove(edge_to_remove)
            self.update_counters('-', edge)
            return True
        return False
    
    def update_counters(self, op, edge):
        s1 = set()
        s2 = set()
        for sample_edge in self.edge_sampled:
            if sample_edge.frm == edge.frm:
                s1.add(sample_edge.to)
            if sample_edge.to == edge.frm:
                s1.add(sample_edge.frm)
            if sample_edge.frm == edge.to:
                s2.add(sample_edge.to)
            if sample_edge.to == edge.to:
                s2.add(sample_edge.frm)
        for c in (s1 & s2):
            if op == '+':
                self.tau += 1
                self.counters[c] = self.counters.get(c, 0) + 1
                self.counters[edge.frm] = self.counters.get(edge.frm, 0) + 1
                self.counters[edge.to] = self.counters.get(edge.to, 0) + 1
            elif op == '-':
                self.tau -= 1
                self.counters[c] = self.counters.get(c, 0) - 1
                if self.counters[c] <= 0:
                    del self.counters[c]
                self.counters[edge.frm] = self.counters.get(edge.frm, 0) - 1
                if self.counters[edge.frm] <= 0:
                    del self.counters[edge.frm]
                self.counters[edge.to] = self.counters.get(edge.to, 0) - 1
                if self.counters[edge.to] <= 0:
                    del self.counters[edge.to]
    
    def run(self, stream_edges):
        for edge in stream_edges:
            if self.time % 1000 == 0:
                print ("element: ", self.time, "value: ", self.tau)
            self.time += 1
            if self.sample_edge(edge):
                self.edge_sampled.add(edge)
                self.update_counters('+', edge)
        eps = (self.time *(self.time - 1)* (self.time - 2)) / (self.S_size * (self.S_size - 1) * (self.S_size - 2))
        if eps < 1:
            eps = 1
        return self.tau * eps

class Triest_impr:
    def __init__(self, S_size):
        self.time = 0 # t in the paper
        self.tau = 0
        self.edge_sampled = set()
        self.S_size = S_size
        self.counters = {}

    def sample_edge(self, edge):
        if self.time <= self.S_size:
            return True
        if random.random() <= (self.S_size / self.time):
            edge_to_remove = random.sample(self.edge_sampled,1)[0]
            self.edge_sampled.remove(edge_to_remove)
            return True
        return False
    
    def update_counters(self, edge):
        s1 = set()
        s2 = set()
        for sample_edge in self.edge_sampled:
            if sample_edge.frm == edge.frm:
                s1.add(sample_edge.to)
            if sample_edge.to == edge.frm:
                s1.add(sample_edge.frm)
            if sample_edge.frm == edge.to:
                s2.add(sample_edge.to)
            if sample_edge.to == edge.to:
                s2.add(sample_edge.frm)
        eta = ((self.time - 1) * (self.time - 2)) / (self.S_size * (self.S_size - 1))
        if eta < 1:
            eta = 1
        for c in (s1 & s2):
            self.tau += eta
            self.counters[c] = self.counters.get(c, 0) + eta
            self.counters[edge.frm] = self.counters.get(edge.frm, 0) + eta
            self.counters[edge.to] = self.counters.get(edge.to, 0) + eta
    
    def run(self, stream_edges):
        for edge in stream_edges:
            if self.time % 1000 == 0:
                print ("element: ", self.time, "value: ", self.tau)
            self.time += 1
            self.update_counters(edge)
            if self.sample_edge(edge):
                self.edge_sampled.add(edge)
        return self.tau



edges = set()
test_set = set()

def read_data():
    with open('facebookDataset.txt') as f:
        for line in f:
            if line[0] == "%":
                continue
            data = line.split()
            if data[0] != data[1]:
                test_set.add(Edge(data[0], data[1]))

def main():
    run_base_triest = False
    if run_base_triest:
        S_size = 1000
        read_data()
        t = Triest_basic(S_size)
        expected = t.run(test_set)
        true_value = Triest_basic(len(test_set)).run(test_set)
        print("With ", S_size, "samples the expected value is ", expected," . The true value is ", true_value," . Error: ", abs(true_value - expected)," triangles")
    else:
        S_size = 1000
        read_data()
        t = Triest_impr(S_size)
        expected = t.run(test_set)
        true_value = Triest_impr(len(test_set)).run(test_set)
        print("With ", S_size, "samples the expected value is ", expected," . The true value is ", true_value," . Error: ", abs(true_value - expected)," triangles")

main()