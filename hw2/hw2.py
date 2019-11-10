from collections import defaultdict
import numpy as np


item_count = {}


class CandidatePair:
    def __init__(self, frequent_items):
        self.frequent_items = frequent_items
        self.nr_occurrences = 0
        self.nr_items_matched_in_basket = 0

    def __eq__(self, candidate_pair_obj):
        is_equal = self.compare_lists(
            self.frequent_items, candidate_pair_obj.frequent_items)
        return is_equal

    def __str__(self):
        return self.frequent_items
    '''
    this is just for testing now have to write a proper method for this soon
    '''

    def __repr__(self):
        return "<Test a:%s b:%s>" % (self.frequent_items[0], self.frequent_items[1])

    def compare_lists(self, candidate_pair_list):
        check_len = len(self.frequent_items)
        temp_arr = self.frequent_items + candidate_pair_list
        temp_len = list(set(temp_arr))
        if check_len == temp_len:
            return True
        else:
            return False

    def one_match_found(self):
        self.nr_items_matched_in_basket += 1

    def is_full_match(self):
        if self.nr_items_matched_in_basket == len(self.frequent_items):
            self.nr

def read_data():
    nr_transactions = 0
    with open('dataset.txt') as inputfile:
        for line in inputfile:
            nr_transactions += 1
            # changes from str to in to save memory
            temp_arr = [int(x) for x in line.strip().split(' ')]
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


def generate_candidate_pairs(singletons, k_itemset_list=None):
    singletons = list(singletons)
    if k_itemset_list == None:
        dubbeltons = []
        for i in range(len(singletons)):
            for j in range(i+1, len(singletons)):
                candidate_pair = CandidatePair([singletons[i], singletons[j]])
                dubbeltons.append(candidate_pair)
        return dubbeltons
    else:
        return 0


def ith_filter(candidate_pair_list, singletons, support_threshold):
    k_itemset_count = []
    k_pair = len(candidate_pair_list[0].frequent_items)
    with open('dataset.txt') as inputfile:
        for line in inputfile:
            basket = [int(x) for x in line.strip().split(' ')]
            matched_items_candidate_pair = defaultdict(list)
            for item in basket:
                if item in singletons:
                    for candidate_pair in candidate_pair_list:
                        if item in candidate_pair.frequent_items:
                            matched_items_candidate_pair[item].append(candidate_pair)


def main():
    nr_transactions = read_data()
    print(len(item_count.keys()))
    s = nr_transactions / 100  # 1 % of baskets/number of transactions
    singletons = find_singletons(s)
    print(len(singletons))
    print(singletons.get(25))
    dubletons = generate_candidate_pairs(singletons)
    print(dubletons)


main()
