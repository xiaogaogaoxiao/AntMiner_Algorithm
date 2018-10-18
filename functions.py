import numpy as np
import copy
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


def set_rule_covered_cases(current_rule, dataset):

    last_added_term_attr = current_rule.added_terms[-1].attribute

    cases = []
    attr_idx = dataset.col_index[last_added_term_attr]
    for case in current_rule.covered_cases:
        if dataset.data[case, attr_idx] == current_rule.added_terms[-1].value:
            cases.append(case)

    current_rule.covered_cases = cases[:]
    current_rule.no_covered_cases = len(cases)

    return


def set_pruned_rule_covered_cases(pruned_rule, dataset):

    covered_cases = pruned_rule.covered_cases[:]

    for attr in pruned_rule.antecedent:
        cases = []
        attr_idx = dataset.col_index[attr]

        for case in covered_cases:

            if dataset.data[case, attr_idx] == pruned_rule.antecedent[attr]:
                cases.append(case)

        covered_cases = cases[:]

    pruned_rule.covered_cases = covered_cases[:]
    pruned_rule.no_covered_cases = len(covered_cases)

    return


def list_terms_updating(list_of_terms, attribute):

    new_list = []
    for term in list_of_terms:
        if term.attribute != attribute:
            new_list.append(term)
            # list_of_terms.pop(term)

    return new_list


def rule_construction(current_rule, list_of_terms, min_case_per_rule, dataset):

    previous_rule = copy.deepcopy(current_rule)

    # Antecedent construction
    while True:

        if not list_of_terms:
            break

        set_probability_values(list_of_terms)

        term_2b_added, term_2b_added_index = sort_term(list_of_terms)

        if term_2b_added is None:
            break

        current_rule.antecedent[term_2b_added.attribute] = term_2b_added.value
        current_rule.added_terms.append(term_2b_added)

        set_rule_covered_cases(current_rule, dataset)

        if current_rule.no_covered_cases < min_case_per_rule:
            current_rule = copy.deepcopy(previous_rule)
            break

        previous_rule = copy.deepcopy(current_rule)
        list_of_terms = list_terms_updating(list_of_terms, term_2b_added.attribute)

    # Consequent selection
    current_rule.set_consequent(dataset)

    return


def rule_pruning(current_rule, min_case_per_rule, dataset):

    while True:

        list_quality = []
        list_pruned_rules = []
        term_drop_idx = 0

        for term_drop in current_rule.antecedent:

            pruned_rule = cRule(dataset)
            pruned_rule.antecedent = current_rule.antecedent.copy()     # PAY ATTENTION TO DEBUG HERE
            pruned_rule.added_terms = current_rule.added_terms[:]

            del pruned_rule.antecedent[term_drop]
            del pruned_rule.added_terms[term_drop_idx]

            set_pruned_rule_covered_cases(pruned_rule, dataset)         # DEBUG THIS NEW FUNCTION
            pruned_rule.set_consequent(dataset)

            if pruned_rule.no_covered_cases < min_case_per_rule:
                pruned_rule.quality = 0
                list_pruned_rules.append(pruned_rule)
                list_quality.append(pruned_rule.quality)
                term_drop_idx += 1
                continue

            pruned_rule.set_quality(dataset)
            list_pruned_rules.append(pruned_rule)
            list_quality.append(pruned_rule.quality)

            term_drop_idx += 1

        best_rule_quality = max(list_quality)
        best_rule_quality_idx = list_quality.index(max(list_quality))

        if best_rule_quality < current_rule.quality:
            break

        current_rule = copy.deepcopy(list_pruned_rules[best_rule_quality_idx])

        if len(current_rule.antecedent) == 1:
            break

    return
