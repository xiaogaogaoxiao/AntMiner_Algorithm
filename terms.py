import collections
import math


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

        qtd_values = len(dataset.data)

        # A PRIORI PROBABILITY: P(W)
        prob_apriori = {}
        class_freq = dict(collections.Counter(dataset.data[:, dataset.col_index[dataset.class_attr]]))
        for w in dataset.class_values:
            prob_apriori[w] = class_freq[w]/qtd_values

        # EVIDANCE: P(A=V)
        freq = dict(collections.Counter(dataset.data[:, dataset.col_index[self.attribute]]))
        prob_evidance = freq[self.value]/qtd_values

        # LIKELIHOOD: P(A=V|W)
        prob_likelihood = {}
        for w in dataset.class_values:
            value_freq = 0
            for line in range(qtd_values):
                if dataset.data[line, dataset.col_index[dataset.class_attr]] == w:
                    if dataset.data[line, dataset.col_index[self.attribute]] == self.value:
                        value_freq += 1
            prob_likelihood[w] = value_freq/class_freq[w]

        # A POSTERIORI PROBABILITY: P(W|A=V)
        prob_posteriori = {}
        for w in dataset.class_values:
            prob_posteriori[w] = (prob_likelihood[w] * prob_apriori[w]) / prob_evidance

        # ENTROPY
        w_entropy = []
        for w in dataset.class_values:
            if prob_posteriori[w] == 0:
                entropy = 0
            else:
                entropy = (-1) * prob_posteriori[w] * math.log2(prob_posteriori[w])
            w_entropy.append(entropy)
        self.entropy = sum(w_entropy)
        self.logK_entropy = math.log2(len(dataset.class_values)) - self.entropy

        return

    def set_heuristic(self, k, denominator):

        if float(denominator) == 0.0:
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

