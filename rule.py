import collections
import numpy as np


class Rule:

    def __init__(self, dataset):
        self.antecedent = {}
        self.consequent = None
        self.covered_cases = list(range(len(dataset.data)))
        self.no_covered_cases = len(dataset.data)
        self.quality = 0

    def construct(self, terms, min_case_per_rule, idx_e, idx_i):
        c_log_file = "log_rule-construct.txt"
        f = open(c_log_file, "a+")
        f.write('\n\n\n=============== RULE CONSTRUCTION LOOP ======================================================================')
        f.write('\n> Stopping condition: rule cover less than minimum cases or there is no more attributes to be added')
        f.write('\n> Sequential construction: Sort a term to be added to rule > check number of covered cases ')
        f.write('\n> IF Stopping condition: set rule consequent')
        f.write('\n=============================================================================================================')
        f.write('\n EXTERNAL LOOP ITERATION ' + repr(idx_e))
        f.write('\n INTERNAL LOOP ITERATION ' + repr(idx_i))
        f.close()
        idx = 0

        # ANTECEDENT CONSTRUCTION
        while True:
            idx += 1
            f = open(c_log_file, "a+")
            f.write('\n\n>>>>>>>>>>>>>>> ITERATION ' + repr(idx))
            f.close()
            f = open(c_log_file, "a+")
            f.write('\n> List_of_terms size: ' + repr(len(terms.size())))
            f.write('\n\n==> CURRENT RULE:')
            f.close()
            self.print_txt(c_log_file, 'Class')

            if terms.size() == 0:
                f = open(c_log_file, "a+")
                f.write('\n\n=============== END CONSTRUCTION')
                f.write('\n> Condition: empty terms list')
                f.write('\n   - current_list_of_terms size = ' + repr(len(terms.size())))
                f.write('\n   - iteration number = ' + repr(idx))
                f.close()
                break

            sorted_term = terms.sort_term()
            covered_cases = list(set(sorted_term.covered_cases) & set(self.covered_cases))
            f = open(c_log_file, "a+")
            f.write('\n\n==> TERM TO BE ADDED: Attribute='+repr(sorted_term.attribute)+' Value='+repr(sorted_term.value))
            f.write('\n- Current rule covered cases: ' + repr(self.covered_cases))
            f.write('\n- Sorted term covered cases: ' + repr(sorted_term.covered_cases))
            f.write('\n- Intersection covered cases: ' + repr(covered_cases))
            f.write('\n- Number of intersection covered cases: ' + repr(len(covered_cases)))
            f.close()

            if len(covered_cases) >= min_case_per_rule:
                self.antecedent[sorted_term.attribute] = sorted_term.value
                self.covered_cases = covered_cases
                self.no_covered_cases = len(self.covered_cases)

                f = open(c_log_file, "a+")
                f.write('\n\n==> NEW CONSTRUCTED RULE:')
                f.close()
                self.print_txt(c_log_file, 'Class')
            else:
                f = open(c_log_file, "a+")
                f.write('\n\n=============== END CONSTRUCTION')
                f.write('\n> Condition: new rule doesnt cover minimum cases')
                f.write('\n   - current_list_of_terms size = ' + repr(len(list_of_terms.size())))
                f.write('\n   - iteration number = ' + repr(idx))
                f.close()
                break

            terms.update()

        # CONSEQUENT SELECTION

        # SET QUALITY

        return

    def set_covered_cases(self, dataset):

        previous_covered_cases = list(self.covered_cases)

        last_term = self.added_terms[-1]
        last_term_attr_idx = dataset.col_index[last_term.attribute]
        last_term_value = last_term.value
        last_term_cases = list(np.where(dataset.data[:, last_term_attr_idx] == last_term_value)[0])

        new_covered_cases = list(set(previous_covered_cases).intersection(last_term_cases))

        self.covered_cases = new_covered_cases
        self.no_covered_cases = len(new_covered_cases)

        return

    def set_pruned_covered_cases(self, dataset):

        attr_cases = []
        for attr in self.antecedent:
            attr_idx = dataset.col_index[attr]
            attr_cases.append(list(np.where(dataset.data[:, attr_idx] == self.antecedent[attr])[0]))

        new_covered_cases = list(set(self.covered_cases).intersection(*attr_cases))

        self.covered_cases = new_covered_cases
        self.no_covered_cases = len(new_covered_cases)

        return

    def gen_pruned_rule(self, rule, attr_drop, term_idx, dataset, min_case_per_rule, idx_e, idx_i):
        self.antecedent = rule.antecedent.copy()
        self.added_terms = rule.added_terms[:]
        del self.antecedent[attr_drop]
        del self.added_terms[term_idx]
        self.set_pruned_covered_cases(dataset)
        self.set_consequent(dataset)

        if self.no_covered_cases < min_case_per_rule:  # POSSIBLE TO HAPPEN?
            self.quality = 0
        self.set_quality(dataset, idx_e, idx_i, p=True)

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
        col_class = dataset.col_index[dataset.class_attr]

        for row_idx in range(len(dataset.data)):
            # positive cases (TP|FP): covered by the rule
            if row_idx in self.covered_cases:
                if dataset.data[row_idx, col_class] == self.consequent:
                    tp += 1
                else:  # covered but doesnt have the class predicted
                    fp += 1
            # negative cases (TN|FN): not covered by the rule
            else:
                if dataset.data[row_idx, col_class] == self.consequent:
                    fn += 1
                else:  # not covered and doesnt have the class predicted
                    tn += 1

        den1 = (tp + fn)
        den2 = (fp + tn)
        if den1 == 0:
            self.quality = 0
        elif den2 == 0:
            self.quality = 1
        else:
            self.quality = (tp / den1) * (tn / den2)

        # just for log register
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

    def equals(self, prev_rule):

        attr_this = self.antecedent.keys()
        attr_prev = prev_rule.antecedent.keys()

        if self.consequent == prev_rule.consequent:
            if len(set(attr_this) ^ set(attr_prev)) == 0:   # both have same keys
                for attr in attr_this:
                    if self.antecedent[attr] != prev_rule.antecedent[attr]:
                        return False
            else:
                return False
        else:
            return False

        return True

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
