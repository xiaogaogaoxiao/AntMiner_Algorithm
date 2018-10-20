from functions import *


def ant_miner(dataset, no_of_ants, min_case_per_rule, max_uncovered_cases, no_rules_converg):

    TrainingSet = dataset
    DiscoveredRuleList = []

    while len(TrainingSet.data) > max_uncovered_cases:

        list_of_terms = get_terms(TrainingSet.attr_values)

        ant_index = 0
        converg_test_index = 0

        list_of_terms = set_pheromone_init(list_of_terms)
        list_of_terms = set_heuristic_values(list_of_terms, TrainingSet)

        list_of_current_rules = []

        while True:

            current_rule = rule_construction(list_of_terms, min_case_per_rule, TrainingSet)
            current_rule.set_quality(TrainingSet)

            current_rule_pruned = rule_pruning(current_rule, min_case_per_rule, TrainingSet)

            list_of_current_rules.append(current_rule_pruned)

            list_of_terms = pheromone_updating(list_of_terms, current_rule_pruned)

            converg_test_index = check_convergence(list_of_current_rules, converg_test_index)

            ant_index += 1

            if ant_index >= no_of_ants:
                break
            elif converg_test_index >= no_rules_converg:
                break


        # R_best = ChoosesBestRule()
        # DiscoveredRuleList.append(R_best)
        # covered_cases = get_CoveredCases
        # TrainingSet = TrainingSet - covered_cases

    return DiscoveredRuleList



