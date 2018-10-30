from functions import *


def ant_miner(dataset, no_of_ants, min_case_per_rule, max_uncovered_cases, no_rules_converg):

    training_dataset = copy.deepcopy(dataset)
    discovered_rule_list = []

    dataset_stagnation_test = 0
    no_of_remaining_cases = len(training_dataset.data)

    while no_of_remaining_cases > max_uncovered_cases:

        if dataset_stagnation_test == no_rules_converg:
            print('Dataset length stagnation')
            break

        last_no_of_remaining_cases = no_of_remaining_cases
        ant_index = 0
        converg_test_index = 1
        list_of_current_rules = []
        list_of_current_rules_quality = []

        list_of_terms = get_terms(training_dataset.attr_values)
        list_of_terms = set_pheromone_init(list_of_terms)
        list_of_terms = set_heuristic_values(list_of_terms, training_dataset)

        while True:

            if ant_index == no_of_ants:
                print('Rule iteration: exceeded no_of_ants')
                break
            elif converg_test_index == no_rules_converg:
                print('Rule iteration: rule converged')
                break

            current_rule = rule_construction(list_of_terms, min_case_per_rule, training_dataset)

            if current_rule is None:
                print('Empty rule')
                ant_index += 1
                converg_test_index += 1
                continue

            current_rule.set_quality(training_dataset)

            current_rule_pruned = rule_pruning(current_rule, min_case_per_rule, training_dataset)

            converg_test_index = check_convergence(current_rule_pruned, list_of_current_rules, converg_test_index)

            if converg_test_index == 1:
                list_of_current_rules.append(current_rule_pruned)
                list_of_current_rules_quality.append(current_rule_pruned.quality)

            list_of_terms = pheromone_updating(list_of_terms, current_rule_pruned)

            ant_index += 1

        if not list_of_current_rules_quality:
            continue

        best_rule_idx = list_of_current_rules_quality.index(max(list_of_current_rules_quality))
        best_rule = copy.deepcopy(list_of_current_rules[best_rule_idx])
        discovered_rule_list.append(best_rule)

        covered_cases = np.array(best_rule.covered_cases)
        training_dataset.data = np.delete(training_dataset.data, covered_cases, axis=0)
        training_dataset.data_updating()
        no_of_remaining_cases = len(training_dataset.data)

        if no_of_remaining_cases == last_no_of_remaining_cases:
            dataset_stagnation_test += 1

    return discovered_rule_list, training_dataset

