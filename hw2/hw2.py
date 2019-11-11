from collections import defaultdict
import numpy as np

Lk_arr = []
s_threshold = 2000
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
    print(L0)
    Print_Empty_Lines(3)
    while True:
        Ckp1 = Generate_CkPlus1(Lk_arr[0], Lk_arr[k - 1])
        Ckp1 = Count_Occurences_Of_Itemsets(Ckp1)
        Lkp1 = Filter_By_S_Threshold(Ckp1)
        if len(Lkp1) <= 0:
            break
        Lk_arr.append(Lkp1)
        print(Lkp1)
        Print_Empty_Lines(3)
        k = k + 1
    return 0


def Print_Empty_Lines(n_lines):
    for a in range(n_lines):
        print("")


def Main():
    C0 = Read_Data_C0()
    Create_Frequent_Itemsets(C0)


Main()
