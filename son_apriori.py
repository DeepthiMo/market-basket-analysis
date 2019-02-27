#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from collections import defaultdict
from efficient_apriori import apriori

""" update these parameters to modify input data file and minimum support """
DATA_FILE = 'retail_25k-50Lines.dat'  #specify full path to input data file
MIN_SUPPORT = 0.00016 #min support=freq of itemset/total no. of transactions


def read_chunks(file=DATA_FILE, chunk_size=100):
    """ Breaks a file into smaller chunks to be processed sequentially. """
    with open(DATA_FILE, 'r') as data_file:
        while True:
            data = data_file.readlines(chunk_size)
            if not data:
                break
            yield data


def get_itemsets_for_chunk(chunk, min_support=MIN_SUPPORT):
    """ Reads a chunk and creates a list of frozensets. """
    chunk_data = [line.strip(" \n") for line in chunk]
    transactions = [frozenset(ls.split(' ')) for ls in chunk_data]

    itemsets, rules = apriori(transactions,
                              min_support = MIN_SUPPORT,
                              min_confidence = 1,
                              max_length = 15,
                              verbosity = 0
                             )
    return itemsets


def parse_chunks():
    """ Parses all chunks and creates a list of itemsets across all chunks
        in the source file. """
    itemsets_list = []
    for i, chunk in enumerate(read_chunks()):
        itemsets = get_itemsets_for_chunk(chunk)

        # remove itemsets with less than three items
        itemsets.pop(1, None)
        itemsets.pop(2, None)

        itemsets_list.append(itemsets)
        print('Completed chunk', i)
    return itemsets_list


def dictsum(*dicts):
    """ Calculates the elementwise sum for each element in a set of dictionaries. """
    summed_dicts = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            summed_dicts[k] += v
    return dict(summed_dicts)


def calc_final_itemsets(itemsets_list):
    """ Loop over item sets and compute running total of frequencies,
        filtering out item sets occurring less than four times. """
    full_set, filtered_set = {}, {}

    for chunk in itemsets_list:
        for outer_key, outer_data in chunk.items():
            full_set = dictsum(full_set, outer_data)
        filtered_set = {}
        for key, value in full_set.items():
            if value >= 4:
                filtered_set[key] = value
    return filtered_set


def format_results(finalset):
    """ Format final results per specification. """
    output_itemsets = ""

    for key, value in finalset.items():
        itemset_size = len(key)
        output_str = ""
        if itemset_size >= 3:
            sigma = value
            output_str = "<" + "item set size " + "(" + str(itemset_size) + ")" + ">, " + \
                         "<" + "co-occuring freq=" + str(sigma) + ">, "

            for index, item in enumerate(key):
                if index < itemset_size - 1:
                    output_str += "<" + item + ">,"

                #Adding end of line to last item
                elif index == itemset_size - 1:
                    output_str += "<" + item + ">\n"
            output_itemsets += output_str

    return output_itemsets


def save_results(output_itemsets):
    """ Write formatted final results to a output file. """
    with open("output.txt", "w") as file:
        file.write(output_itemsets)
    return 1


def main():
    """ Main entry point for the code. """
    itemsets_list = parse_chunks()
    filtered_results = calc_final_itemsets(itemsets_list)
    formatted_results = format_results(filtered_results)
    save_results(formatted_results)


if __name__ == "__main__":
    main()
