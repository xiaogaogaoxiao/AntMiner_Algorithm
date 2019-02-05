import collections
import math
import numpy as np


class cTerms:

    def __init__(self):
        self.attribute = ''
        self.value = ''
        self.pheromone = None
        self.heuristic = None
        self.entropy = None
        self.logK_entropy = None
        self.probability = None
        self.term_idx = None

    def set_entropy(self, dataset):

        # # A PRIORI PROBABILITY: P(W)
        # prob_apriori = {}
        # class_freq = dict(collections.Counter(dataset.data[:, dataset.col_index[dataset.class_attr]]))
        # for w in dataset.class_values:
        #     prob_apriori[w] = class_freq[w]/qtd_values
        #
        # # EVIDANCE: P(A=V)
        # freq = dict(collections.Counter(dataset.data[:, dataset.col_index[self.attribute]]))
        # prob_evidance = freq[self.value]/qtd_values
        #
        # # LIKELIHOOD: P(A=V|W)
        # prob_likelihood = {}
        # for w in dataset.class_values:
        #     value_freq = 0
        #     for line in range(qtd_values):
        #         if dataset.data[line, dataset.col_index[dataset.class_attr]] == w:
        #             if dataset.data[line, dataset.col_index[self.attribute]] == self.value:
        #                 value_freq += 1
        #     prob_likelihood[w] = value_freq/class_freq[w]

        # A POSTERIORI PROBABILITY: P(W|A=V)
        class_idx = dataset.col_index[dataset.class_attr]
        attr_idx = dataset.col_index[self.attribute]
        data = dataset.data
        # rows = data.index[data[self.attribute] == self.value].tolist()
        rows = list(np.where(data[:, attr_idx] == self.value)[0])
        value_freq = len(rows)

        prob_posteriori = {}.fromkeys(dataset.class_values, 0)
        for r in rows:
            prob_posteriori[data[r, class_idx]] += 1

        # ENTROPY
        if value_freq > 0:
            entropy = 0
            for w in prob_posteriori:
                w_freq = prob_posteriori[w]
                if w_freq != 0:
                    entropy -= w_freq * math.log2(w_freq)
            self.entropy = entropy
        else:
            print('Heuristic calc error: Term value doesnt appear in current dataset')

        self.logK_entropy = math.log2(len(dataset.class_values)) - self.entropy

        return

    def set_heuristic(self, k, denominator):

        if float(denominator) == 0.0:   # CHECK THE OCCURRENCE OF THIS CONDITION <<<<<<<<
            denominator = 0.0000001

        log_k = math.log2(k)
        fnc_heuristic = (log_k - self.entropy) / denominator
        self.heuristic = fnc_heuristic

        return

    def set_pheromone(self, data):
        return

    def set_probability(self, denominator):

        if denominator == 0.0:
            self.probability = 0
        else:
            self.probability = (self.heuristic * self.pheromone) / denominator

        return

