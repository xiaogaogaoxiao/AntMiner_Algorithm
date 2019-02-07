import math
import numpy as np


class Terms:

    def __init__(self, attr, value, dataset, min_case_per_rule):
        self.attribute = attr
        self.value = value
        self.covered_cases = []
        self.__available = True
        self.__entropy = None
        self.__logK = math.log2(len(dataset.class_values))
        self.__constructor(dataset, min_case_per_rule)

    def __constructor(self, dataset, min_case_per_rule):

        # A POSTERIORI PROBABILITY: P(W|A=V)
        class_idx = dataset.col_index[dataset.class_attr]
        attr_idx = dataset.col_index[self.attribute]
        data = dataset.data
        rows = list(np.where(data[:, attr_idx] == self.value)[0])  # row indexes for <self.attr=self.value> (covered)
        term_freq = len(rows)
        class_freq = {}.fromkeys(dataset.class_values, 0)
        for r in rows:
            class_freq[data[r, class_idx]] += 1

        # ENTROPY = -[ P(W|A=V) * log2(P(W|A=V)) ]
        if term_freq > 0:
            entropy = 0
            for w in class_freq:
                prob_posteriori = class_freq[w]/term_freq
                if prob_posteriori != 0:
                    entropy -= prob_posteriori * math.log2(prob_posteriori)
            self.__entropy = entropy
        else:
            print('term.__constructor: Term value doesnt appear in current dataset')
            self.__available = False

        # COVERED CASES
        self.covered_cases = rows
        if term_freq < min_case_per_rule:
            self.__available = False

        return

    def get_heuristic(self):
        return self.__logK - self.__entropy

    def available(self):
        return self.__available
