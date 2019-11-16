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
    def __init__(self, S_size): # S_size = M
        self.t = 0 # time
        self.tau = 0
        self.edge_sampled = set()
        self.S_size = S_size
        self.counters = {}

edges = set()
test_set = set()

def read_data():
    with open('dataset.txt') as f:
        for line in f:
            if line[0] == "%":
                continue
            data = line.split()
            if data[0] != data[1]:
                test_set.add(Edge(data[0], data[1]))