from functions import *


def ant_miner(dataset, no_of_ants, min_case_per_rule, max_uncovered_cases, no_rules_converg):

    TrainingSet = dataset
    DiscoveredRuleList = []

    while len(TrainingSet.data) > max_uncovered_cases:

        list_of_terms = get_terms(dataset.attr_values)
        ant_index = 0
        converg_test_index = 0

        set_pheromone_init(list_of_terms)

        set_heuristic_values(list_of_terms, dataset)

        while True:

            ant_index += 1

            current_rule_list = []
            current_rule = cRule(TrainingSet)

            rule_construction(current_rule, list_of_terms, min_case_per_rule, dataset)

            # RulePrune()

            current_rule_list.append(current_rule)

            # PheromoneUpdating()

            # CheckConverg()

            if ant_index >= no_of_ants:
                break
            elif converg_test_index >= no_rules_converg:
                break

        # R_best = ChoosesBestRule()
        # DiscoveredRuleList.append(R_best)
        # covered_cases = get_CoveredCases
        # TrainingSet = TrainingSet - covered_cases

    return DiscoveredRuleList


def rule_construction(current_rule, list_of_terms, min_case_per_rule, dataset):

    # Antecedent construction
    while True:

        if not list_of_terms:
            break               # verify this line

        set_probability_values(list_of_terms)

        term_2b_added, term_2b_added_index = sort_term(list_of_terms)

        if term_2b_added == None:
            break

        current_rule.antecedent[term_2b_added.attribute] = term_2b_added.value
        current_rule.added_terms.append(term_2b_added)

        set_rule_coveredcases(current_rule, dataset)

        if current_rule.no_covered_cases < min_case_per_rule:
            current_rule.antecedent.popitem()
            break

        list_of_terms = list_terms_updating(list_of_terms, term_2b_added.attribute)

    # Consequent selection
    teste = []
    teste.append(1)

    return

