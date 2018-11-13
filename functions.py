import copy
import collections
import numpy as np
from terms import cTerms
from rule import cRule


def get_terms(dict_attr_values):

    list_of_terms = []
    idx = 0
    for a in dict_attr_values:
        for v in dict_attr_values[a]:
            term_obj = cTerms()
            term_obj.attribute = a
            term_obj.value = v
            term_obj.term_idx = idx
            list_of_terms.append(term_obj)
            idx += 1

    return list_of_terms


def set_pheromone_init(list_of_terms):

    for term in list_of_terms:
        term.pheromone = 1/len(list_of_terms)

    return list_of_terms


def set_heuristic_values(list_of_terms, dataset):

    terms_logK_entropy = []
    for term in list_of_terms:
        term.set_entropy(dataset)
        terms_logK_entropy.append(term.logK_entropy)

    for term in list_of_terms:
        term.set_heuristic(len(dataset.class_values), sum(terms_logK_entropy))

    return list_of_terms


def set_probability_values(list_of_terms):

    denominator = 0

    for term in list_of_terms:
        den = term.heuristic * term.pheromone
        denominator = denominator + den

    for term in list_of_terms:
        term.set_probability(denominator)

    return list_of_terms


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
            break

    return term_chosen, index


def set_rule_covered_cases(current_rule, dataset):

    last_added_term_attr = current_rule.added_terms[-1].attribute

    cases = []
    attr_idx = dataset.col_index[last_added_term_attr]
    for case in current_rule.covered_cases:
        if dataset.data[case, attr_idx] == current_rule.added_terms[-1].value:
            cases.append(case)

    # current_rule.covered_cases = cases[:]
    # current_rule.no_covered_cases = len(cases)

    return cases[:], len(cases)


def set_pruned_rule_covered_cases(pruned_rule, dataset):

    covered_cases = pruned_rule.covered_cases[:]

    for attr in pruned_rule.antecedent:
        cases = []
        attr_idx = dataset.col_index[attr]

        for case in covered_cases:

            if dataset.data[case, attr_idx] == pruned_rule.antecedent[attr]:
                cases.append(case)

        covered_cases = cases[:]

    return covered_cases[:], len(covered_cases)


def list_terms_updating(list_of_terms, attribute):

    new_list = []
    for term in list_of_terms:
        if term.attribute != attribute:
            new_list.append(term)
            # list_of_terms.pop(term)

    return new_list


def rule_construction(list_of_terms, min_case_per_rule, dataset):

    constructed_rule = cRule(dataset)
    flag_empty_rule = 1
    current_list_of_terms = copy.deepcopy(list_of_terms)

    # Antecedent construction
    while True:

        previous_constructed_rule = copy.deepcopy(constructed_rule)

        if not current_list_of_terms:
            break

        current_list_of_terms = set_probability_values(current_list_of_terms)

        term_2b_added, term_2b_added_index = sort_term(current_list_of_terms)

        if term_2b_added is None:
            break

        constructed_rule.antecedent[term_2b_added.attribute] = term_2b_added.value
        constructed_rule.added_terms.append(term_2b_added)

        constructed_rule.covered_cases, constructed_rule.no_covered_cases = \
            set_rule_covered_cases(constructed_rule, dataset)

        if constructed_rule.no_covered_cases < min_case_per_rule:
            constructed_rule = copy.deepcopy(previous_constructed_rule)
            break

        current_list_of_terms = list_terms_updating(current_list_of_terms, term_2b_added.attribute)

    if not constructed_rule.antecedent:
        return None

    # Consequent selection
    constructed_rule.set_consequent(dataset)

    return constructed_rule


def rule_pruning(new_rule, min_case_per_rule, dataset):

    while True:

        if len(new_rule.antecedent) <= 1:
            break

        list_quality = []
        list_pruned_rules = []
        term_drop_idx = 0

        for term_drop in new_rule.antecedent:

            pruned_rule = cRule(dataset)
            pruned_rule.antecedent = new_rule.antecedent.copy()
            pruned_rule.added_terms = new_rule.added_terms[:]

            del pruned_rule.antecedent[term_drop]
            del pruned_rule.added_terms[term_drop_idx]

            pruned_rule.covered_cases, pruned_rule.no_covered_cases = \
                set_pruned_rule_covered_cases(pruned_rule, dataset)
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

        if best_rule_quality < new_rule.quality:
            break

        new_rule = copy.deepcopy(list_pruned_rules[best_rule_quality_idx])

    return new_rule


def pheromone_updating(list_of_terms, pruned_rule):

    # Getting used terms
    used_terms_idx = []
    for term in pruned_rule.added_terms:
        used_terms_idx.append(term.term_idx)

    # Increasing used terms pheromone
    denominator = 0
    for term in list_of_terms:
        if term.term_idx in used_terms_idx:
            term.pheromone += term.pheromone * pruned_rule.quality
        denominator += term.pheromone

    # Decreasing not used terms: normalization
    for term in list_of_terms:
        term.pheromone = term.pheromone / denominator

    return list_of_terms


def check_convergence(current_rule, list_of_rules, converg_test_index):

    idx = 1

    if len(list_of_rules) == 0:
        return idx

    previous_rule = copy.deepcopy(list_of_rules[-1])

    current_rule_terms = []
    for term in current_rule.added_terms:
        current_rule_terms.append(term.term_idx)

    previous_rule_terms = []
    for term in previous_rule.added_terms:
        previous_rule_terms.append(term.term_idx)

    if len(current_rule_terms) == len(previous_rule_terms):
        for current_term_i, previous_term_j in zip(current_rule_terms, previous_rule_terms):
            if current_term_i != previous_term_j:
                return idx

        idx = converg_test_index + 1

    return idx


def get_remaining_cases_rule(dataset):

    classes = dataset.data[:, dataset.col_index[dataset.class_attr]]
    class_freq = dict(collections.Counter(classes))

    max_freq = 0
    class_chosen = None
    for w in class_freq:                        # other way: class_chosen <= max(class_freq[])
        if class_freq[w] > max_freq:
            class_chosen = w
            max_freq = class_freq[w]

    rule = cRule(dataset)
    rule.covered_cases = []
    rule.consequent = class_chosen

    return rule


def classification_task(dataset, list_of_rules):

    predicted_classes = []
    chosen_class = None
    all_cases = len(dataset.data)
    compatibility = 1

    rules = copy.deepcopy(list_of_rules[:-1])
    remaining_cases_rule = copy.deepcopy(list_of_rules[-1])

    for case in range(all_cases):   # for each new case

        for rule in rules:          # sequential rule compatibility test

            antecedent = rule.antecedent
            for attr in antecedent:
                if antecedent[attr] != dataset.data[case, dataset.col_index[attr]]:
                    compatibility = 0

            if compatibility == 1:
                chosen_class = rule.consequent
                break

        if chosen_class is None:
            chosen_class = remaining_cases_rule.consequent

        predicted_classes.append(chosen_class)
        chosen_class = None

    return predicted_classes






















