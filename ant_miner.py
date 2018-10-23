from functions import *


def ant_miner(dataset, no_of_ants, min_case_per_rule, max_uncovered_cases, no_rules_converg):

    TrainingSet = copy.deepcopy(dataset)
    discovered_rule_list = []

    while len(TrainingSet.data) > max_uncovered_cases:

        list_of_terms = get_terms(TrainingSet.attr_values)

        ant_index = 0
        converg_test_index = 0

        list_of_terms = set_pheromone_init(list_of_terms)
        list_of_terms = set_heuristic_values(list_of_terms, TrainingSet)

        list_of_current_rules = []
        list_of_current_rules_quality = []

        while True:

            current_rule = rule_construction(list_of_terms, min_case_per_rule, TrainingSet)

            if current_rule is None:
                continue

            current_rule.set_quality(TrainingSet)

            current_rule_pruned = rule_pruning(current_rule, min_case_per_rule, TrainingSet)

            converg_test_index = check_convergence(current_rule_pruned, list_of_current_rules, converg_test_index)

            if converg_test_index == 1:
                list_of_current_rules.append(current_rule_pruned)
                list_of_current_rules_quality.append(current_rule_pruned.quality)

            list_of_terms = pheromone_updating(list_of_terms, current_rule_pruned)

            ant_index += 1

            if ant_index >= no_of_ants:
                break
            elif converg_test_index >= no_rules_converg:
                break

        best_rule_idx = list_of_current_rules_quality.index(max(list_of_current_rules_quality))
        best_rule = copy.deepcopy(list_of_current_rules[best_rule_idx])
        discovered_rule_list.append(best_rule)

        covered_cases = np.array(best_rule.covered_cases)
        TrainingSet.data = np.delete(TrainingSet.data, covered_cases, axis=0)
        TrainingSet.data_updating()

    return discovered_rule_list, TrainingSet

