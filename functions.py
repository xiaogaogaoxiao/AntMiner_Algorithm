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


def sort_term(list_of_terms, c_log_file):

    f = open(c_log_file, "a+")
    f.write('\n\n> TERM SORT:')
    f.close()

    term_chosen = None
    index = None

    terms_prob_sum = 0
    for term in list_of_terms:
        terms_prob_sum = terms_prob_sum + term.probability

    if terms_prob_sum == 0:
        return term_chosen, index

    number_sort = np.random.rand()
    f = open(c_log_file, "a+")
    f.write('\n- Sorted random number: ' + repr(number_sort))
    f.close()

    f = open(c_log_file, "a+")
    f.write('\n\nSorting...:')
    f.close()
    probabilities_sort = 0
    for term_idx, term in enumerate(list_of_terms):

        prob_norm = term.probability/terms_prob_sum
        probabilities_sort = probabilities_sort + prob_norm

        f = open(c_log_file, "a+")
        f.write('\n-Term ' + repr(term_idx) + ': Term_prob=' + repr(prob_norm) + ' Accum_Prob=' + repr(probabilities_sort))
        f.close()

        if number_sort <= probabilities_sort:
            term_chosen = term
            index = list_of_terms.index(term)
            break

    f = open(c_log_file, "a+")
    f.write('\n\n-> Term Sorted: Term ' + repr(index))
    f.close()

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


def rule_construction(list_of_terms, min_case_per_rule, dataset, idx_e, idx_i):
    c_log_file = "rule-construction-fnc_log-results.txt"

    constructed_rule = cRule(dataset)
    current_list_of_terms = copy.deepcopy(list_of_terms)

    # Antecedent construction
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
    while True:
        idx += 1
        f = open(c_log_file, "a+")
        f.write('\n\n>>>>>>>>>>>>>>> ITERATION ' + repr(idx))
        f.close()

        previous_constructed_rule = copy.deepcopy(constructed_rule)

        f = open(c_log_file, "a+")
        f.write('\n\n==> SEQUENTIAL CONSTRUCTION:')
        f.write('\n> List_of_terms size: ' + repr(len(current_list_of_terms)))
        f.close()

        if not current_list_of_terms:
            f = open(c_log_file, "a+")
            f.write('\n\n=============== END CONSTRUCTION')
            f.write('\n> Condition: empty terms list')
            f.write('\n   - current_list_of_terms size = ' + repr(len(current_list_of_terms)))
            f.write('\n   - iteration number = ' + repr(idx))
            f.close()
            break

        current_list_of_terms = set_probability_values(current_list_of_terms)

        term_2b_added, term_2b_added_index = sort_term(current_list_of_terms, c_log_file)

        if term_2b_added is None:
            f = open(c_log_file, "a+")
            f.write('\n\n>>>>> END Construction')
            f.write('\n!! Alternative Condition: empty term_2b_added')
            f.close()
            break
        f = open(c_log_file, "a+")
        f.write('\n\n> TERM TO BE ADDED: Attribute=' + repr(term_2b_added.attribute) + ' Value=' + repr(term_2b_added.value))
        f.close()

        constructed_rule.antecedent[term_2b_added.attribute] = term_2b_added.value
        constructed_rule.added_terms.append(term_2b_added)

        constructed_rule.covered_cases, constructed_rule.no_covered_cases = \
            set_rule_covered_cases(constructed_rule, dataset)

        f = open(c_log_file, "a+")
        f.write('\n\n==> CONSTRUCTION ITERATION ' + repr(idx) + ' RESULTS:')
        f.write('\n- Constructed Rule:')
        f.close()
        constructed_rule.print_txt(c_log_file, 'Class')
        f = open(c_log_file, "a+")
        f.write('\n- Previous Rule:')
        f.close()
        previous_constructed_rule.print_txt(c_log_file, 'Class')

        if constructed_rule.no_covered_cases < min_case_per_rule:
            f = open(c_log_file, "a+")
            f.write('\n\n=============== END CONSTRUCTION')
            f.write('\n> Condition: constructed_rule.no_covered_cases < min_case_per_rule')
            f.write('\n\n> Last constructed rule: (condition = true)')
            f.close()
            constructed_rule.print_txt(c_log_file, 'Class')
            f = open(c_log_file, "a+")
            f.write('\n-no_covered_cases: ' + repr(constructed_rule.no_covered_cases))
            f.close()

            constructed_rule = copy.deepcopy(previous_constructed_rule)

            f = open(c_log_file, "a+")
            f.write('\n\n> Previous constructed rule:')
            f.close()
            constructed_rule.print_txt(c_log_file, 'Class')
            f = open(c_log_file, "a+")
            f.write('\n-no_covered_cases: ' + repr(constructed_rule.no_covered_cases))
            f.close()
            break

        current_list_of_terms = list_terms_updating(current_list_of_terms, term_2b_added.attribute)

    if not constructed_rule.antecedent:
        f = open(c_log_file, "a+")
        f.write('\n\n>>>>> WARNING')
        f.write('\n!! No rule antecedent constructed')
        f.write('\n  - Number of iterations: ' + repr(idx))
        f.close()
        return None

    # Consequent selection
    constructed_rule.set_consequent(dataset)
    f = open(c_log_file, "a+")
    f.write('\n\n>>> FINAL RULE ')
    f.close()
    constructed_rule.print_txt(c_log_file, 'Class')
    f = open(c_log_file, "a+")
    f.write('\n-no_covered_cases: ' + repr(constructed_rule.no_covered_cases))
    f.write('\n\n> Number of iterations: ' + repr(idx))
    f.close()
    return constructed_rule


def rule_pruning(new_rule, min_case_per_rule, dataset, idx_e, idx_i):
    p_log_file = "rule-pruning-fnc_log-results.txt"

    f = open(p_log_file, "a+")
    f.write('\n\n\n================== RULE PRUNING LOOP =========================================================================')
    f.write('\n> Stopping condition: pruned rule quality be less than best quality so far or if pruned rule antecedent has just one term')
    f.write('\n> Receives constructed rule > drops each term on antecedent, sequentially from first to last > each term dropped consists on another rule > new pruned rule is the one of higher quality ')
    f.write('\n> IF no new rules have higher quality than the new pruned rule, or if new pruned rule has oly one term in the antecedent > returns pruned rule')
    f.write('\n==============================================================================================================')
    f.write('\n EXTERNAL LOOP ITERATION ' + repr(idx_e))
    f.write('\n INTERNAL LOOP ITERATION ' + repr(idx_i))
    f.write('\n\n> RULE TO BE PRUNED :')
    f.close()
    new_rule.print_txt(p_log_file, 'Class')
    f = open(p_log_file, "a+")
    f.write('\n-Number of covered cases: ' + repr(new_rule.no_covered_cases))
    f.write('\n-Quality: ' + repr(new_rule.quality))
    f.close()

    idx = 0
    while True:
        idx += 1

        f = open(p_log_file, "a+")
        f.write('\n\n>>>>>>>>>>>>>>> ITERATION ' + repr(idx))
        f.close()

        if len(new_rule.antecedent) <= 1:
            f = open(p_log_file, "a+")
            f.write('\n\n================== END PRUNING FUNCTION LOOP')
            f.write('\n> Condition: pruned rule antecedent = 1')
            f.write('\n  - Number of iterations: ' + repr(idx))
            f.close()
            break

        list_quality = []
        list_pruned_rules = []

        f = open(p_log_file, "a+")
        f.write('\n\n==> CURRENT RULE :')
        f.close()
        new_rule.print_txt(p_log_file, 'Class')

        f = open(p_log_file, "a+")
        f.write('\n\n==> TERMS DROPPING PROCEDURE:')
        f.close()
        for term_idx, term_drop in enumerate(new_rule.antecedent):

            f = open(p_log_file, "a+")
            f.write('\n\n>>> TERM ' + repr(term_idx))
            f.write('\n\n> Term_2b_dropped: Attribute=' + repr(term_drop) + ' Value=' + repr(new_rule.antecedent[term_drop]))
            f.close()

            pruned_rule = cRule(dataset)
            pruned_rule.antecedent = new_rule.antecedent.copy()
            pruned_rule.added_terms = new_rule.added_terms[:]

            del pruned_rule.antecedent[term_drop]
            del pruned_rule.added_terms[term_idx]

            pruned_rule.covered_cases, pruned_rule.no_covered_cases = \
                set_pruned_rule_covered_cases(pruned_rule, dataset)
            pruned_rule.set_consequent(dataset)

            if pruned_rule.no_covered_cases < min_case_per_rule:
                pruned_rule.quality = 0
                list_pruned_rules.append(pruned_rule)
                list_quality.append(pruned_rule.quality)

                f = open(p_log_file, "a+")
                f.write('\n> Pruned Rule:')
                f.close()
                pruned_rule.print_txt(p_log_file, 'Class')
                f = open(p_log_file, "a+")
                f.write('\n-Number of covered cases: ' + repr(pruned_rule.no_covered_cases))
                f.write('\n-Quality: ' + repr(pruned_rule.quality))
                f.close()
                continue

            pruned_rule.set_quality(dataset)
            list_pruned_rules.append(pruned_rule)
            list_quality.append(pruned_rule.quality)

            f = open(p_log_file, "a+")
            f.write('\n> Pruned Rule:')
            f.close()
            pruned_rule.print_txt(p_log_file, 'Class')
            f = open(p_log_file, "a+")
            f.write('\n-Number of covered cases: ' + repr(pruned_rule.no_covered_cases))
            f.write('\n-Quality: ' + repr(pruned_rule.quality))
            f.close()

        best_rule_quality = max(list_quality)
        best_rule_quality_idx = list_quality.index(max(list_quality))

        f = open(p_log_file, "a+")
        f.write('\n\n==> BEST PRUNED RULE:')
        f.write('\n> Created at >>> TERM ' + repr(best_rule_quality_idx))
        f.close()

        if best_rule_quality < new_rule.quality:
            f = open(p_log_file, "a+")
            f.write('\n\n================== END PRUNING FUNCTION LOOP')
            f.write('\n> Condition: best quality of new pruned rules < current rule quality')
            f.write('\n  - Number of iterations: ' + repr(idx))
            f.write('\n\n> Final Pruned Rule:')
            f.close()
            new_rule.print_txt(p_log_file, 'Class')
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






















