from functions import *


def ant_miner(dataset, no_of_ants, min_case_per_rule, max_uncovered_cases, no_rules_converg):

    training_dataset = copy.deepcopy(dataset)
    discovered_rule_list = []

    dataset_stagnation_test = 0
    no_of_remaining_cases = len(training_dataset.data)

    f = open("tic-tac-toe_log-results.txt", "a+")
    f.write('\n\n=============== EXTERNAL LOOP: Uncovered Cases ===============')
    f.close()
    idx_e = 0
    while no_of_remaining_cases > max_uncovered_cases:
        idx_e += 1
        f = open("tic-tac-toe_log-results.txt", "a+")
        f.write('\n\n===== EXTERNAL LOOP: Iteration ' + repr(idx_e))
        f.close()

        last_no_of_remaining_cases = no_of_remaining_cases

        if no_of_remaining_cases == last_no_of_remaining_cases:
            dataset_stagnation_test += 1

        if dataset_stagnation_test == no_rules_converg:
            f = open("tic-tac-toe_log-results.txt", "a+")
            f.write('\n\n=============== END External Loop: dataset stagnation: ===============')
            f.write('\n   - no_of_remaining_cases = ' + repr(no_of_remaining_cases))
            f.write('\n   - dataset_stagnation_test = ' + repr(dataset_stagnation_test))
            f.close()
            break

        ant_index = 0
        converg_test_index = 1
        list_of_current_rules = []
        list_of_current_rules_quality = []

        list_of_terms = get_terms(training_dataset.attr_values)
        list_of_terms = set_pheromone_init(list_of_terms)
        list_of_terms = set_heuristic_values(list_of_terms, training_dataset)

        f = open("tic-tac-toe_log-results.txt", "a+")
        f.write('\n\n---------- INTERNAL LOOP: no_of_ants || no_rules_converg ----------')
        f.close()
        idx_i = 0
        while True:
            idx_i += 1
            f = open("tic-tac-toe_log-results.txt", "a+")
            f.write('\n\n----- INTERNAL LOOP: Iteration ' + repr(idx_i))
            f.close()

            if ant_index == no_of_ants:
                f = open("tic-tac-toe_log-results.txt", "a+")
                f.write('\n\n---------- END Internal Loop: exceeded no_of_ants ----------')
                f.write('\n  - ant_index = ' + repr(ant_index))
                f.write('\n  - Total of while iterations: ' + repr(idx_i))
                f.close()
                break
            elif converg_test_index == no_rules_converg:
                f = open("tic-tac-toe_log-results.txt", "a+")
                f.write('\n\n---------- END Internal Loop: rule converged ----------')
                f.write('\n  - converg_test_index = ' + repr(converg_test_index))
                f.write('\n  - Total of while iterations: ' + repr(idx_i))
                f.close()
                break

            f = open("tic-tac-toe_log-results.txt", "a+")
            f.write('\n\n--->   Rule Construction   <---')
            f.close()
            current_rule = rule_construction(list_of_terms, min_case_per_rule, training_dataset)

            if current_rule is None:
                f = open("tic-tac-toe_log-results.txt", "a+")
                f.write('\n!!! Empty Rule Constructed !!!')
                f.close()
                # print('Empty rule')
                ant_index += 1
                converg_test_index += 1
                continue

            current_rule.set_quality(training_dataset)

            current_rule_pruned = rule_pruning(current_rule, min_case_per_rule, training_dataset)

            f = open("tic-tac-toe_log-results.txt", "a+")
            f.write('\n\n--->   INTERNAL LOOP RESULTS: (Iteration ' + repr(idx_i) + ')   <---')
            f.write('\n>Rule Constructed:')
            f.close()
            current_rule.print_txt("tic-tac-toe_log-results.txt", 'Class')
            f = open("tic-tac-toe_log-results.txt", "a+")
            f.write('\n-Quality: ' + repr(current_rule.quality))
            f.write('\n>Rule Pruned:')
            f.close()
            current_rule_pruned.print_txt("tic-tac-toe_log-results.txt", 'Class')
            f = open("tic-tac-toe_log-results.txt", "a+")
            f.write('\n-Quality: ' + repr(current_rule_pruned.quality))
            f.close()

            if len(list_of_current_rules) >= 1:
                last_list_rule = list_of_current_rules[-1]
                f = open("tic-tac-toe_log-results.txt", "a+")
                f.write('\n>Last rule of current_rule_list:')
                f.close()
                last_list_rule.print_txt("tic-tac-toe_log-results.txt", 'Class')
                f = open("tic-tac-toe_log-results.txt", "a+")
                f.write('\n-Quality: ' + repr(last_list_rule.quality))
                f.close()

            converg_test_index = check_convergence(current_rule_pruned, list_of_current_rules, converg_test_index)

            if converg_test_index == 1:
                list_of_current_rules.append(current_rule_pruned)
                list_of_current_rules_quality.append(current_rule_pruned.quality)
                f = open("tic-tac-toe_log-results.txt", "a+")
                f.write('\n\n!! Pruned Constructed Rule did not converged')
                f.write('\n!! Pruned Rule added to current_rule_list')
                f.close()

            list_of_terms = pheromone_updating(list_of_terms, current_rule_pruned)

            ant_index += 1

        if not list_of_current_rules_quality:
            f = open("tic-tac-toe_log-results.txt", "a+")
            f.write('\n\n!!! Internal Loop added no rule quality to list_of_current_rules_quality')
            f.close()
            continue

        best_rule_idx = list_of_current_rules_quality.index(max(list_of_current_rules_quality))
        best_rule = copy.deepcopy(list_of_current_rules[best_rule_idx])
        discovered_rule_list.append(best_rule)

        covered_cases = np.array(best_rule.covered_cases)
        training_dataset.data = np.delete(training_dataset.data, covered_cases, axis=0)
        training_dataset.data_updating()
        no_of_remaining_cases = len(training_dataset.data)

        f = open("tic-tac-toe_log-results.txt", "a+")
        f.write('\n\n===>   EXTERNAL LOOP RESULTS: (Iteration ' + repr(idx_e) + ')   <===')
        f.write('\n>Number of generated rules on internal loop: ' + repr(len(list_of_current_rules)))
        f.write('\n>Generated rules-quality list: ' + repr(list_of_current_rules_quality))
        f.write('\n>Best rule index: ' + repr(best_rule_idx))
        f.write('\n>Best rule:')
        f.close()
        best_rule.print_txt("tic-tac-toe_log-results.txt", 'Class')
        f = open("tic-tac-toe_log-results.txt", "a+")
        f.write('\n\n>Number of rules on external loop (discovered_rule_list length): ' + repr(len(discovered_rule_list)))
        f.write('\n>Best Rule number of covered cases: ' + repr(len(covered_cases)))
        f.write('\n>Last_no_of_remaining_cases: ' + repr(last_no_of_remaining_cases))
        f.write('\n>No_of_remaining_cases: ' + repr(no_of_remaining_cases))
        f.close()

    f = open("tic-tac-toe_log-results.txt", "a+")
    f.write('\n\n=============== END External Loop: (Ant-Miner Algorithm) ===============')
    f.write('\n   - no_of_remaining_cases = ' + repr(no_of_remaining_cases))
    f.write('\n   - max_uncovered_cases = ' + repr(max_uncovered_cases))
    f.close()

    # generating rule for remaining cases
    rule_for_remaining_cases = get_remaining_cases_rule(training_dataset)
    discovered_rule_list.append(rule_for_remaining_cases)

    return discovered_rule_list, training_dataset, no_of_remaining_cases

