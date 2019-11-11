from collections import defaultdict
import numpy as np


item_count = {}


class CandidatePair:
    id = 0

    def __init__(self, frequent_items):
        self.frequent_items = frequent_items
        self.nr_occurrences = 0
        self.id = CandidatePair.id
        CandidatePair.id += 1


    def __eq__(self, candidate_pair_obj):
        is_equal = self.compare_lists(
            self.frequent_items, candidate_pair_obj.frequent_items)
        return is_equal
    
    def __hash__(self):
        return self.id

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
    
    def is_match(self, frequent_basket_items):

        item_set_length = len(self.frequent_items)
        nr_matching_items = 0
        is_match = False
        for item in frequent_basket_items:
            if nr_matching_items == item_set_length:
                return True
            if item in self.frequent_items:
                nr_matching_items += 1
        return False 

    def set_new_occurrence(self):
        self.nr_occurrences += 1
    
    def get_nr_occurrence(self):
        return self.nr_occurrences

def read_data():
    nr_transactions = 0
    with open('dataset.txt') as inputfile:
        for line in inputfile:
            nr_transactions += 1
            # changes from str to int to save memory
            basket = [int(x) for x in line.strip().split(' ')]
            for item in basket:
                if item not in item_count.keys():
                    item_count[item] = 1
                else:
                    item_count[item] = item_count[item] + 1
    return nr_transactions


def find_singletons(support_threshold,k_itemset_count = item_count):
    singletons = {}
    for item in k_itemset_count:
        if k_itemset_count[item] > support_threshold:
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


def ith_filter(candidate_pair_list, singletons):
    found_candidate_pairs = {}
    k_pair = len(candidate_pair_list[0].frequent_items)
    dataset = []
    nr_matches = 0
    with open('dataset.txt') as inputfile:
        line_nr = 0
        for line in inputfile:
            basket = [int(x) for x in line.strip().split(' ')]
            dataset.append(basket)
        for basket in dataset:
            frequent_basket_items = []
            for item in basket:
                if item in singletons:
                    frequent_basket_items.append(item)
            i = 0
            for candidate_pair in candidate_pair_list:
                print(i)
                i += 1
                if candidate_pair.is_match(frequent_basket_items):
                    if candidate_pair not in found_candidate_pairs.keys():
                        print("here")
                        found_candidate_pairs[candidate_pair] = 1
                    else:
                        print("not here")
                        found_candidate_pairs[candidate_pair] += 1
            
    return found_candidate_pairs


            
def main():
    nr_transactions = read_data()
    print(len(item_count.keys()))
    s = nr_transactions / 100  # 1 % of baskets/number of transactions
    singletons = find_singletons(s)
    print(len(singletons))
    print(singletons.get(25))
    dubletons = generate_candidate_pairs(singletons)
    print(len(dubletons))
    #v = ith_filter(dubletons, singletons)
    #print(len(v))

main()
