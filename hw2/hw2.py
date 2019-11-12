from collections import defaultdict
import numpy as np
import time
Lk_arr = []
s_threshold = 1000
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
        basket_items = dict.fromkeys(basket_itemsets.intersection(Lk_arr[0]), 0)
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
    start_time = 0
    print(L0)
    Print_Empty_Lines(3)
    while True:
        star_time = time.time()
        Ckp1 = Generate_CkPlus1(Lk_arr[0], Lk_arr[k - 1])
        print("Generate_CkPlus1", time.time() - start_time)
        start_time = time.time()
        Ckp1 = Count_Occurences_Of_Itemsets(Ckp1, k)
        print("Count_Occurences_Of_Itemsets", time.time() - start_time)
        start_time = time.time()
        Lkp1 = Filter_By_S_Threshold(Ckp1)
        print("Filter_By_S_Threshold", time.time() - start_time)
        if len(Lkp1) <= 0:
            break
        Lk_arr.append(Lkp1)
        print(Lkp1)
        Print_Empty_Lines(3)
        k = k + 1
    return 0

def Support_Of_Iemset():
    return 0

def Confidence_Of_Itemset():
    return 0
    
def Interest_Of_Itemset():
    return 0

def Print_Empty_Lines(n_lines):
    for a in range(n_lines):
        print("")


def Main():
    C0 = Read_Data_C0()
    Create_Frequent_Itemsets(C0)


Main()
"""


def Count_Occurences_Of_Itemsets(Ck):
    data_file = open(data_file_path)
    basket_nr = 1
    for line in data_file:
        start_time = time.time()
        basket_nr = basket_nr + 1
        basket_items = list(map(int, line.split()))
        basket_items.sort()
        for itemset in Ck.keys():
            itemset_in_basket = True
            for item in itemset:
                if item not in basket_items:
                    itemset_in_basket = False
                    break
            if itemset_in_basket == True:
                Ck[itemset] = Ck[itemset] + 1
        print(“Basket_nr”, basket_nr)
    data_file.close()
    return Ck
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
    """
