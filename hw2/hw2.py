from collections import defaultdict
import numpy as np
Lk_arr = []
s_threshold = 4000
data_file_path = “./sales.dat”


def Read_Data_C0():
    C0 = defaultdict()
    data_file = open(data_file_path)
    for line in data_file:
        basket_items = set(map(int, line.split()))
        for item in basket_items:
            if item in C0.keys():
                C0[item] = C0[item] + 1
            else:
                C0[item] = 1
    data_file.close()
    return C0


def Count_Occurences_Of_Itemsets(Ck):
    data_file = open(data_file_path)
    for line in data_file:
        basket_items = set(map(int, line.split()))
        for itemset in Ck.keys():
            itemset_in_basket = True
            for item in itemset:
                if item not in basket_items:
                    itemset_in_basket = False
                    break
            if itemset_in_basket == True:
                Ck[itemset] = Ck[itemset] + 1
    data_file.close()
    return Ck


def Filter_By_S_Threshold(Ck):
    Lk = defaultdict()
    for itemset in Ck.keys():
        if Ck[itemset] >= s_threshold:
            Lk[itemset] = Ck[itemset]
    return Lk


def Generate_CkPlus1(L0, Lk):
    return 0


def Create_Frequent_Itemsets(C0):
    return 0


def Print_Empty_Lines(n_lines):
    for a in range(n_lines):
        print(“”)


def Main():
    C0 = Read_Data_C0()
    L0 = Filter_By_S_Threshold(C0)
    print(L0)
    Print_Empty_Lines(3)
    print(len(L0))
    print(len(C0.keys()))


Main()
