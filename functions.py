import numpy as np
from terms import cTerms
from rule import cRule


def get_terms(dict_attr_values):

    list_of_terms = []
    for a in dict_attr_values:
        for v in dict_attr_values[a]:
            term_obj = cTerms()
            term_obj.attribute = a
            term_obj.value = v
            list_of_terms.append(term_obj)

    return list_of_terms


def set_pheromone_init(list_of_terms):

    for term in list_of_terms:
        term.pheromone = 1/len(list_of_terms)

    return


def set_heuristic_values(list_of_terms, dataset):

    terms_logK_entropy = []
    for term in list_of_terms:
        term.set_entropy(dataset)
        terms_logK_entropy.append(term.logK_entropy)

    for term in list_of_terms:
        term.set_heuristic(len(dataset.class_values), sum(terms_logK_entropy))

    return


def set_probability_values(list_of_terms):

    denominator = 0
    for term in list_of_terms:
        den = term.heuristic * term.pheromone
        denominator = denominator + den

    for term in list_of_terms:
        term.set_probability(denominator)

    return


def sort_term(list_of_terms):

    term_chosen = None
    index = None

    terms_prob_sum = 0
    for term in list_of_terms:
        terms_prob_sum = terms_prob_sum + term.probability
    if terms_prob_sum == 0:
        return term_chosen, index

    number_sort = np.random.rand()

    probabilities_sort = 0
    for term in list_of_terms:

        prob_norm = term.probability/terms_prob_sum
        probabilities_sort = probabilities_sort + prob_norm

        if number_sort <= probabilities_sort:
            term_chosen = term
            index = list_of_terms.index(term)
            return term_chosen, index

    return term_chosen, index


def set_rule_coveredcases(current_rule, dataset):

    covered_cases = current_rule.covered_cases[:]
    last_added_term_attr = current_rule.added_terms[-1].attribute

    cases = []
    attr_idx = dataset.col_index[last_added_term_attr]
    for case in covered_cases:
        if dataset.data[case, attr_idx] == current_rule.added_terms[-1].value:
            cases.append(case)
    covered_cases = cases[:]

    current_rule.covered_cases = covered_cases[:]
    current_rule.no_covered_cases = len(covered_cases)

    return


def list_terms_updating(list_of_terms, attribute):

    new_list = []
    for term in list_of_terms:
        if term.attribute != attribute:
            new_list.append(term)
            # list_of_terms.pop(term)

    return new_list


