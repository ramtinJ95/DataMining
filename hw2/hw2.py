from collections import defaultdict
import numpy as np


item_count = {}

class CandidatePair:
    def __init__(self, frequent_items):
        self.frequent_items = frequent_items
    
    def __eq__(self, candidate_pair_obj):
        is_equal = self.compare_lists(self.frequent_items, candidate_pair_obj.frequent_items)
        return is_equal

    def compare_lists(self, candidate_pair_list):
        check_len = len(self.frequent_items)
        temp_arr = self.frequent_items + candidate_pair_list
        temp_len = list(set(temp_arr))
        if check_len == temp_len:
            return True
        else:
            return False

def read_data():
    nr_transactions = 0
    with open('dataset.txt') as inputfile:
        for line in inputfile:
            nr_transactions += 1
            temp_arr = [int(x) for x in line.strip().split(' ')]  # changes from str to in to save memory
            for item in temp_arr:
                if item not in item_count.keys():
                    item_count[item] = 1
                else:
                    item_count[item] = item_count[item] + 1
    return nr_transactions


def find_singletons(support_threshold):
    singletons = {}
    for item in item_count:
        if item_count[item] > support_threshold:
            singletons[item] = True
    return singletons


def main():
    nr_transactions = read_data()
    print(len(item_count.keys()))
    s = nr_transactions / 100 # 1 % of baskets/number of transactions
    singletons = find_singletons(s)
    print(len(singletons))
    print(singletons.get(25))


main()
