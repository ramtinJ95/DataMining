from collections import defaultdict
import numpy as np
import random

#########PARAMETERS#########
k = 10
n_docs = 10
nr_hashes = 100
nr_bands = 20
nr_rows = 5
threshold = 0.01
############################

file_paths = []
doc_shingle_ids = defaultdict(set)
shingle_id_docs = defaultdict(set)
shingle_id = {}
random.seed(200)
np.random.seed(200)

list_a = np.random.randint(low=1, high=10000, size=nr_hashes)
list_b = np.random.randint(low=1, high=10000, size=nr_hashes)


def Store_File_Paths():
    for a in range(5):
        file_paths.append("./20_newsgroups/sci.med/" + str(a))
    for a in range(5):
        file_paths.append("./20_newsgroups/sci.space/" + str(a + 5))


def Create_Shingles():
    next_shingle_id = 0
    for doc_nr in range(n_docs):
        doc = open(file_paths[doc_nr])
        for line in doc:
            for doc_ind in range(len(line) - k + 1):
                shingle = line[doc_ind:doc_ind + k]
                if shingle in shingle_id.keys():
                    shingle_id_docs[shingle_id[shingle]].add(doc_nr)
                    doc_shingle_ids[doc_nr].add(shingle_id.get(shingle))
                else:
                    shingle_id_docs[next_shingle_id].add(doc_nr)
                    shingle_id[shingle] = next_shingle_id
                    doc_shingle_ids[doc_nr].add(shingle_id.get(shingle))
                    next_shingle_id += 1
        doc_shingle_ids[doc_nr] = sorted(doc_shingle_ids.get(doc_nr))


def Compare_Sets(d1, d2):
    list_a = doc_shingle_ids.get(d1)
    list_b = doc_shingle_ids.get(d2)
    nr_intersect_els = 0
    i_d1 = 0
    i_d2 = 0
    while i_d1 < (len(list_a) - 1) and i_d2 < (len(list_b) - 1):
        if list_a[i_d1] == list_b[i_d2]:
            nr_intersect_els += 1
            i_d1 += 1
        elif list_a[i_d1] < list_b[i_d2]:
            i_d1 += 1
        elif list_a[i_d1] > list_b[i_d2]:
            i_d2 += 1
        else:
            print("something is wrong in compare_sets method")
    return float(nr_intersect_els) / float(len(list_a) + len(list_b) - nr_intersect_els)


def Min_Hashing(nr_hashes):
    signature_matrix = np.full((nr_hashes, n_docs), 100000)
    for row_nr in shingle_id_docs:
        hash_list = Hash_Rows(row_nr, nr_hashes)
        for doc in shingle_id_docs.get(row_nr):
            for i in range(len(hash_list)):
                h_i = hash_list[i]
                if h_i < signature_matrix[i][doc]:
                    signature_matrix[i][doc] = h_i
    return signature_matrix


def Hash_Rows(row_nr, nr_hashes):
    c = len(shingle_id_docs)
    hash_list = []
    for i in range(nr_hashes):
        hash_list.append((list_a[i] * row_nr + list_b[i]) % c)
    return hash_list


def Compare_Signatures(d1, d2, signature_matrix):
    col1 = signature_matrix[:, d1]
    col2 = signature_matrix[:, d2]
    nr_similiar_signatures = 0

    for i in range(len(col1)):
        if col1[i] == col2[i]:
            nr_similiar_signatures += 1
    return float(nr_similiar_signatures) / float(len(col1))


def LSH(signature_matrix):
    multipliers = 10 ** np.arange(nr_rows)
    similiar_items_idx = []
    c = len(shingle_id_docs) * 10
    a = random.randint(1, c)
    b = random.randint(1, c)
    for band_i in range(nr_bands):
        bucket = []
        hashed_value_doc_id = defaultdict(set)
        band_mat_i = signature_matrix[band_i * nr_rows:band_i * nr_rows + nr_rows, :]
        for i in range(n_docs):
            col_i = band_mat_i[:, i]
            value_to_be_hashed = np.sum(col_i)
            hashed_value = (a*value_to_be_hashed+b) % c
            #bucket.append(hashed_value)
            hashed_value_doc_id[hashed_value].add(i)
        for bucket_nr in hashed_value_doc_id.keys():
            for doc_ind_x in range(0, len(hashed_value_doc_id[bucket_nr])):
                for doc_ind_y in range(doc_ind_x + 1, len(hashed_value_doc_id[bucket_nr])):
                    d1 = list(hashed_value_doc_id[bucket_nr])[doc_ind_x]
                    d2 = list(hashed_value_doc_id[bucket_nr])[doc_ind_y]
                    sim = Compare_Signatures(d1, d2, signature_matrix)
                    if sim > threshold:
                        print("the following documents are quite similiar")
                        print(d1, d2)
                        print(sim)
            
        '''
        for x in range(0, len(bucket)):
            for y in range(x+1, len(bucket)):
                if bucket[x] == bucket[y]:
                    d1 = list(hashed_value_doc_id[bucket[x]])[0]
                    d2 = list(hashed_value_doc_id.get(bucket[x]))[1]
                    sim = Compare_Signatures(d1, d2, signature_matrix)
                    if sim > threshold:
                        print("the following documents are quite similiar")
                        print(d1, d2)
                        print(sim )
                    print(d1, d2)
                    print(sim)

                for bucket_nr in hashed_value_doc_id.keys():
            for doc_ind_x in range(0, len(hashed_value_doc_id[bucket_nr])):
                for doc_ind_y in range(doc_ind_x + 1, len(hashed_value_doc_id[bucket_nr])):
                    d1 = list(hashed_value_doc_id[bucket_nr])[doc_ind_x]
                    d2 = list(hashed_value_doc_id[bucket_nr])[doc_ind_y]
                    sim = Compare_Signatures(d1, d2, signature_matrix)
                    if sim > threshold:
                        print("the following documents are quite similiar")
                        print(d1, d2)
                        print(sim)
                    
                    '''

def Valid_argument_check():
    if nr_bands * nr_rows == nr_hashes:
        return True
    else:
        return False


def Main():
    if Valid_argument_check():
        Store_File_Paths()
        Create_Shingles()
        signature_matrix = Min_Hashing(100)

        print(signature_matrix)
        print(Compare_Signatures(0, 1, signature_matrix))
        print(Compare_Sets(0, 1))
        LSH(signature_matrix)
        print(len(shingle_id.keys()))
    else:
        print("nr_bands * nr_rows != nr_hashes ")

Main()
