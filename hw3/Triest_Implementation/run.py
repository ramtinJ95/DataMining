from triest_base import TriestBase
from triest_impr import TriestImpr

mode = 2
file_path = "./data/facebookDataset.txt"
M_vals= [817000]

for M in M_vals:
    if mode == 1:
        model = TriestBase(M)
    else:
        model = TriestImpr(M)

    with open(file_path) as f:
        for line in f:
            if line.startswith('%'):
                continue
            my_list = list(map(int, line.strip().split()))
            u = my_list[0]
            v = my_list[1]
            if u != v:
                if (u,v) not in model.sample.S.keys() and (v,u) not in model.sample.S.keys():
                    model.run(u,v)

        print("============ FINAL OUTPUT IS ====================")
        print(model.return_counters()) 