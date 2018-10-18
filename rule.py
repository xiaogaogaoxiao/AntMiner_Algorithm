import collections
import numpy as np


class cRule:

    def __init__(self, dataset):
        self.antecedent = {}
        self.consequent = None
        self.added_terms = []
        self.covered_cases = []
        self.no_covered_cases = None
        self.quality = None

        self.set_covered_cases_init(dataset)

    def set_covered_cases_init(self, dataset):
        self.covered_cases = list(range(len(dataset.data)))

        return

    def set_consequent(self, dataset):

        covered_cases = []
        for case in self.covered_cases:
            covered_cases.append(dataset.data[case])

        covered_cases = np.array(covered_cases)
        class_freq = dict(collections.Counter(covered_cases[:, dataset.col_index[dataset.class_attr]]))

        max_freq = 0
        class_chosen = None
        for w in class_freq:                # other way: class_chosen <= max(class_freq[])
            if class_freq[w] > max_freq:
                class_chosen = w
                max_freq = class_freq[w]

        self.consequent = class_chosen

        return

    def set_quality(self, dataset):

        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for row_idx in range(len(dataset.data)):

            if row_idx in self.covered_cases:       # positive cases
                if dataset.data[row_idx, dataset.col_index[dataset.class_attr]] == self.consequent:
                    tp += 1
                else:
                    fp += 1

            else:                                   # negative cases
                if dataset.data[row_idx, dataset.col_index[dataset.class_attr]] == self.consequent:
                    fn += 1
                else:
                    tn += 1

        quality = (tp / (tp + fn)) * (tn / (fp + tn))

        self.quality = quality

        return

