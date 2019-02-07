import copy
import numpy as np
from term import Term


class TermsManager:

    def __init__(self, dataset, min_case_per_rule):
        self.__terms_dict = {}
        self.__terms_availability = {}
        self.__pheromone_table = {}
        self.__heuristic_table = {}
        self.__no_of_terms = 0

        # build object
        self.__constructor(dataset, min_case_per_rule)

    def __constructor(self, dataset, min_case_per_rule):

        attr_values = dataset.attr_values
        attrs = list(attr_values.keys())
        heuristic_accum = 0

        # TABLES: { Attr : {} }
        self.__pheromone_table = {}.fromkeys(attrs, {})
        self.__heuristic_table = {}.fromkeys(attrs, {})

        # TERMS: constructing __terms_dict and __terms_availability
        self.__terms_dict = {}.fromkeys(attrs, [])
        self.__terms_availability = {}.fromkeys(attrs)
        for attr in attrs:
            list_of_terms = []
            for value in attr_values[attr]:
                term_obj = Term(attr, value, dataset, min_case_per_rule)
                if term_obj.available():
                    list_of_terms.append(term_obj)
                    self.__no_of_terms += 1
                    heuristic_accum += term_obj.get_heuristic()
            self.__terms_dict[attr] = copy.deepcopy(list_of_terms)
            self.__terms_availability[attr] = True

        # Constructing __pheromone_table: { Attr : { Value : Pheromone } }
        initial_pheromone = 1 / self.__no_of_terms
        for attr in attrs:
            values = attr_values[attr]
            self.__pheromone_table[attr] = {}.fromkeys(values, initial_pheromone)
            self.__heuristic_table[attr] = {}.fromkeys(values)

        # Constructing __heuristic_table: { Attr : { Value : Heuristic } }
        if heuristic_accum == 0: print('!!! Heuristic normalization denominator equal Zero')  # CHECK NECESSITY
        for attr in attrs:
            attr_terms = self.__terms_dict[attr]
            for term in attr_terms:
                self.__heuristic_table[term.attribute][term.value] = (term.get_heuristic() / heuristic_accum)

        return

    def __get_prob_accum(self):

        accum = 0
        for attr in self.__terms_availability:
            if self.__terms_availability[attr]:
                for value in self.__heuristic_table[attr]:
                    accum += self.__heuristic_table[attr][value] * self.__pheromone_table[attr][value]

        return accum

    def size(self):
        return self.__no_of_terms

    def available(self):
        for attr in self.__terms_availability:
            if self.__terms_availability[attr]:
                return True

        return False

    def sort_term(self):
        c_log_file = "log_rule-construct.txt"
        f = open(c_log_file, "a+")
        f.write('\n\n> TERM SORT:')
        f.close()

        attribute = None
        value = None
        cases = []

        prob_normalization = self.__get_prob_accum()
        number_sort = np.random.rand()

        f = open(c_log_file, "a+")
        f.write('\n- Sorted random number: ' + repr(number_sort))
        f.write('\n\nSorting...:')
        f.close()

        term_idx = 0
        prob_accum = 0
        for attr in self.__terms_availability:
            if self.__terms_availability[attr]:
                for term in self.__terms_dict[attr]:
                    val = term.value
                    prob = (self.__heuristic_table[attr][val] * self.__heuristic_table[attr][val]) / prob_normalization
                    prob_accum += prob

                    term_idx += 1
                    f = open(c_log_file, "a+")
                    f.write('\n-Term '+repr(term_idx)+': Term_prob='+repr(prob)+' Accum_Prob=' + repr(prob_accum))
                    f.close()

                    if number_sort <= prob_accum:
                        attribute = attr
                        value = val
                        cases = term.covered_cases
                        break

        f = open(c_log_file, "a+")
        f.write('\n\n-> Term Sorted: Term ' + repr(term_idx))
        f.close()

        return attribute, value, cases

    def update_availability(self, attr):
        self.__terms_availability[attr] = False
        return

    def pheromone_updating(self):

        # update self.__probability_table
        # reset self.__terms_availability

        return
