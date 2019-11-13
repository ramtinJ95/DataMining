from collections import defaultdict
from itertools import combinations
import numpy as np
import time
Lk_arr = []
s_threshold = 1000
c_threshold = 0.5
data_file_path = "./dataset.txt"


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


def Count_Occurences_Of_Itemsets(Ck, k):
    data_file = open(data_file_path)
    for line in data_file:
        basket_itemsets = set(map(int, line.split()))
        basket_items = dict.fromkeys(
            basket_itemsets.intersection(Lk_arr[0]), 0)
        for a in range(k):
            basket_itemsets = basket_itemsets.intersection(Lk_arr[a])
            basket_itemsets = dict.fromkeys(basket_itemsets, 0)
            basket_itemsets = Generate_CkPlus1(basket_items, basket_itemsets)
            basket_itemsets = set(basket_itemsets.keys())
        for itemset in basket_itemsets:
            if itemset in Ck.keys():
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
    Ckp1 = defaultdict()
    Ckp1Temp = defaultdict()
    for itemset in Lk.keys():
        for item in L0.keys():
            if type(itemset) is int:
                Ckp1Temp[itemset, item] = 0
            else:
                Ckp1Temp[itemset + (item, )] = 0
    for itemset in Ckp1Temp.keys():
        items_in_order = True
        for item_index in range(len(itemset) - 1):
            if itemset[item_index] >= itemset[item_index + 1]:
                items_in_order = False
                break
        if items_in_order == True:
            Ckp1[itemset] = Ckp1Temp[itemset]
    return Ckp1


def Create_Frequent_Itemsets(C0):
    k = 1
    L0 = Filter_By_S_Threshold(C0)
    Lk_arr.append(L0)
    Print_Empty_Lines(3)
    while True:
        Ckp1 = Generate_CkPlus1(Lk_arr[0], Lk_arr[k - 1])
        Ckp1 = Count_Occurences_Of_Itemsets(Ckp1, k)
        Lkp1 = Filter_By_S_Threshold(Ckp1)
        if len(Lkp1) <= 0:
            break
        Lk_arr.append(Lkp1)
        Print_Keys_And_Counts(Lkp1)
        Print_Empty_Lines(3)
        k = k + 1
    return 0


def Generate_Rules():
    rules = []
    for k in range(1, len(Lk_arr)):
        for itemset in Lk_arr[k]:
            all_subsets = Get_All_Subsets_Of_Itemset(itemset)
            for subset in all_subsets:
                if Get_Confidence(subset, itemset) >= c_threshold:
                    if type(subset) == int:
                        set1 = [subset]
                        set2 = []
                        for x in list(itemset):
                            if x != subset:
                                set2.append(x)
                        rule = [set1, set2]
                        rules.append(rule)
                    else:
                        temp1 = list(subset)
                        temp2 = list(itemset)
                        set1 = list(subset)
                        set2 = []
                        for x in temp2:
                            if x not in temp1:
                                set2.append(x)
                        rule = [set1, set2]
                        rules.append(rule)
    return rules


def Get_All_Subsets_Of_Itemset(itemset):
    k_max = len(itemset)
    all_subsets = []
    for k in range(1, k_max):
        k_subset = list((combinations(itemset, k)))
        all_subsets.append(k_subset)
    all_subsets = list(np.array(all_subsets).flatten())
    all_subsets_final = []
    for subset in all_subsets:
        if type(subset) != tuple:
            all_subsets_final.append(int(subset))
        elif type(subset) == tuple and len(subset) == 1:
            all_subsets_final.append(int(subset[0]))
        else:
            all_subsets_final.append(subset)
    return all_subsets_final


def Get_Confidence(fromA, fromA_U_toB):
    if type(fromA) is int and type(fromA_U_toB) is int:
        sup_fromA_U_toB = Lk_arr[0][fromA_U_toB]
        sup_fromA = Lk_arr[0][fromA]
        return float(sup_fromA_U_toB) / float(sup_fromA)
    elif type(fromA) is int:
        k = len(fromA_U_toB)
        sup_fromA_U_toB = Lk_arr[k - 1][fromA_U_toB]
        sup_fromA = Lk_arr[0][fromA]
        return float(sup_fromA_U_toB) / float(sup_fromA)
    elif type(fromA_U_toB) is int:
        k = len(fromA)
        sup_fromA_U_toB = Lk_arr[0][fromA_U_toB]
        sup_fromA = Lk_arr[k - 1][fromA]
        return float(sup_fromA_U_toB) / float(sup_fromA)
    else:
        k1 = len(fromA_U_toB)
        k2 = len(fromA)
        sup_fromA_U_toB = Lk_arr[k1 - 1][fromA_U_toB]
        sup_fromA = Lk_arr[k2 - 1][fromA]
        return float(sup_fromA_U_toB) / float(sup_fromA)


def Print_Empty_Lines(n_lines):
    for a in range(n_lines):
        print("")


def Print_Rules(rules):
    for rule in rules:
        print(rule[0], end= " ")
        print("- ->", end= " ")
        print(rule[1])


def Print_Keys_And_Counts(Lk):
    for itemset in Lk.keys():
        print("Itemset: ", itemset, end= "\t")
        print("Occurences in Baskets: ", Lk[itemset])


def Main():
    print("s_threshold", s_threshold)
    print("c_threshold", c_threshold)
    C0 = Read_Data_C0()
    Create_Frequent_Itemsets(C0)
    Print_Empty_Lines(3)
    rules = Generate_Rules()
    Print_Rules(rules)


Main()
