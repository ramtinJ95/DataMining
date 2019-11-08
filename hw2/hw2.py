import numpy as np

def import_dataset():
    dataset = []
    with open('dataset.txt') as inputfile:
        for line in inputfile:
            dataset.append(line.strip().split(' '))
        return dataset

def get_unique_items(dataset):
    dataset = np.hstack(np.array(dataset))
    only_unique_items = np.unique(dataset)
    return only_unique_items

def build_occurrence_dict(uniqe_items, dataset):
    item_nr_occurrences = {}
    for item in uniqe_items:
        nr_occurrences = 0
        for basket in dataset:
            if item in basket:
                nr_occurrences += 1 
        item_nr_occurrences[item] = nr_occurrences
    return item_nr_occurrences

def main():
    dataset = import_dataset()
    unique_items = get_unique_items(dataset)
    print()
    print("number of baskets", len(dataset))
    print()
    print(unique_items)
    print("number of unique items", len(unique_items))
    item_nr_occurrences = build_occurrence_dict(unique_items,dataset)
    print("dict length", len(item_nr_occurrences))


main()