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

    def set_quality(self, dataset, idx_e, idx_i, p):

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

        den1 = (tp + fn)
        den2 = (fp + tn)

        if den1 == 0:
            self.quality = 0
        elif den2 == 0:
            self.quality = 1
        else:
            self.quality = (tp / den1) * (tn / den2)

        if self.quality == 1 or 0:
            q_log_file = "log_rule-quality-analisys.txt"
            f = open(q_log_file, "a+")
            f.write('\n\n\n==============================================================================================================')
            f.write('\n=============== RULE QUALITY ANALISYS ========================================================================')
            f.write('\n==============================================================================================================')
            f.write('\n\n=> Code reference:')
            f.write('\n- idx_e: ' + repr(idx_e))
            f.write('\n- idx_i: ' + repr(idx_i))
            f.write('\n- pruning: ' + repr(p))
            f.write('\n\n=> Quality calculation info:')
            f.write('\n- Quality: ' + repr(self.quality))
            f.write('\n- TP: ' + repr(tp))
            f.write('\n- FP: ' + repr(fp))
            f.write('\n- FN: ' + repr(fn))
            f.write('\n- TN: ' + repr(tn) + '\n')
            f.close()
            self.print_txt(q_log_file, 'Class')

            array_log_file = "log_rule-quality-analisys_array-e" + str(idx_e) + "i" + str(idx_i) + "p" + str(p) + ".txt"
            f = open(q_log_file, "a+")
            f.write('\n- covered cases: ' + repr(self.covered_cases))
            f.write('\n- number of covered cases: ' + repr(self.no_covered_cases))
            f.write('\n\n>> DATASET USED FOR CALCULATION: ' + repr(array_log_file) + ' file <=')
            f.close()
            np.savetxt(array_log_file, dataset.data, fmt='%5s')

        return

    def print(self, class_attr):

        print("IF { ", end="")

        antecedent_attrs = list(self.antecedent.keys())
        qtd_of_terms = len(antecedent_attrs)

        for t in range(0, qtd_of_terms):
            print(antecedent_attrs[t] + " = " + str(self.antecedent[antecedent_attrs[t]]), end="")

            if t < qtd_of_terms - 1:
                print(" AND ", end="")

        print(" } THAN { " + class_attr + " = " + str(self.consequent) + " }")

        return

    def print_txt(self, file, class_attr):

        antecedent_attrs = list(self.antecedent.keys())
        qtd_of_terms = len(antecedent_attrs)

        f = open(file, "a+")
        f.write('\n*RULE:   IF { ')
        for t in range(0, qtd_of_terms):
            f.write(repr(antecedent_attrs[t]) + ' = ' + repr(self.antecedent[antecedent_attrs[t]]))
            if t < qtd_of_terms - 1:
                f.write(' AND ')

        f.write(' } THAN { ' + repr(class_attr) + ' = ' + repr(self.consequent) + ' }')
        f.close()

        return
