from terms_manager import TermsManager
from functions import *


def ant_miner(dataset, no_of_ants, min_case_per_rule, max_uncovered_cases, no_rules_converg, fold):
    log_file = "log_main.txt"
    i_log_file = "log_colony-loop.txt"
    f = open(log_file, "a+")
    f.write('\n\n\n==================== EXTERNAL LOOP ==========================================================================')
    f.write('\n> Stopping condition: number of uncovered cases')
    f.write('\n> Initialise pheromones > create t rule > choose best rule > add to the list > remove rule covered cases')
    f.write('\n============================================================================================================')
    f.write('\n FOLD OF CROSS VALIDATION: ' + repr(fold))
    f.close()

    training_dataset = copy.deepcopy(dataset)
    discovered_rule_list = []

    dataset_stagnation_test = 0
    no_of_remaining_cases = len(training_dataset.data)

    idx_e = 0
    while no_of_remaining_cases > max_uncovered_cases:
        idx_e += 1
        array_log_file = "log_dataset_external-Loop_fold-" + str(fold) + "iteration-" + str(idx_e) + ".txt"
        f = open(log_file, "a+")
        f.write('\n\n>>>>>>>>>>>>>>> ITERATION ' + repr(idx_e))
        f.write('\n> current dataset in ' + repr(array_log_file) + 'file')
        f.close()
        np.savetxt(array_log_file, training_dataset.data, fmt='%5s')

        previous_rule = Rule(training_dataset)
        best_rule = copy.deepcopy(previous_rule)

        ant_index = 0
        converg_test_index = 1

        terms_mgr = TermsManager(training_dataset, min_case_per_rule)

        # DATASET STAGNATION >> REVIEW NECESSITY
        last_no_of_remaining_cases = no_of_remaining_cases
        if no_of_remaining_cases == last_no_of_remaining_cases:
            dataset_stagnation_test += 1
        if dataset_stagnation_test == no_rules_converg:
            f = open(log_file, "a+")
            f.write('\n\n==================== END EXTERNAL LOOP')
            f.write('\n!! Alternative Condition: dataset stagnation')
            f.write('\n   - no_of_remaining_cases = ' + repr(no_of_remaining_cases))
            f.write('\n   - dataset_stagnation_test = ' + repr(dataset_stagnation_test))
            f.close()
            break

        f = open(log_file, "a+")
        f.write('\n> Number of terms: ' + repr(terms_mgr.size()))
        f.write('\n\n=> Internal Loop procedure: colony-loop_log-results.txt file <=\n')
        f.close()

        f = open(i_log_file, "a+")
        f.write('\n\n\n=================== INTERNAL LOOP ==========================================================================')
        f.write('\n> Stopping condition: no_of_ants || no_rules_converg')
        f.write('\n> Incremental rule construction > rule pruning > pheromone updating > convergence test')
        f.write('\n============================================================================================================')
        f.write('\n EXTERNAL LOOP ITERATION ' + repr(idx_e))
        f.close()

        idx_i = 0
        while True:
            idx_i += 1
            f = open(i_log_file, "a+")
            f.write('\n\n>>>>>>>>>>>>>>> ITERATION ' + repr(idx_i))
            f.close()

            if ant_index >= no_of_ants or converg_test_index >= no_rules_converg:
                f = open(i_log_file, "a+")
                f.write('\n\n==================== END Internal Loop')
                f.write('\n  - no_of_ants = ' + repr(no_of_ants))
                f.write('\n  - ant_index = ' + repr(ant_index))
                f.write('\n  - no_rules_converg = ' + repr(no_rules_converg))
                f.write('\n  - converg_test_index = ' + repr(converg_test_index))
                f.write('\n  - Number of iterations: ' + repr(idx_i))
                f.close()
                break

            # RULE CONSTRUCTION
            f = open(i_log_file, "a+")
            f.write('\n\n=> Rule Construction Function: rule-construction-fnc_log-results.txt file <=')
            f.close()

            current_rule = Rule(training_dataset)
            current_rule.construct(terms_mgr, min_case_per_rule, idx_e, idx_i)

            f = open(i_log_file, "a+")
            f.write('\n\n> Rule Constructed:')
            f.close()
            current_rule.print_txt(i_log_file, 'Class')
            f = open(i_log_file, "a+")
            f.write('\n-Quality: ' + repr(current_rule.quality))
            f.close()

            # RULE PRUNING
            f = open(i_log_file, "a+")
            f.write('\n\n=> Rule Pruning Function: rule-pruning-fnc_log-results.txt file <=')
            f.close()

            current_rule.prune(terms_mgr, idx_e, idx_i)

            f = open(i_log_file, "a+")
            f.write('\n\n> Rule Pruned:')
            f.close()
            current_rule.print_txt(i_log_file, 'Class')
            f = open(i_log_file, "a+")
            f.write('\n-Quality: ' + repr(current_rule.quality))
            f.close()

            f = open(i_log_file, "a+")
            f.write('\n\n> Best rule:')
            f.close()
            best_rule.print_txt(i_log_file, 'Class')
            f = open(i_log_file, "a+")
            f.write('\n-Quality: ' + repr(best_rule.quality))
            f.close()

            if current_rule.equals(previous_rule):
                converg_test_index += 1
                f = open(i_log_file, "a+")
                f.write('\n\n!!! Constructed Rule converged')
                f.close()
            else:
                converg_test_index = 1
                if current_rule.quality > best_rule.quality:
                    best_rule = copy.deepcopy(current_rule)
                    f = open(i_log_file, "a+")
                    f.write('\n\n!!! NEW BEST RULE')
                    f.close()

            terms_mgr.pheromone_updating(current_rule.antecedent, current_rule.quality)
            previous_rule = copy.deepcopy(current_rule)
            ant_index += 1

        discovered_rule_list.append(best_rule)

        # covered_cases = np.array(best_rule.covered_cases)
        # training_dataset.data = np.delete(training_dataset.data, covered_cases, axis=0)
        training_dataset.data_updating(best_rule.covered_cases)
        no_of_remaining_cases = len(training_dataset.data)

        # just for log register
        f = open(log_file, "a+")
        f.write('\n>> Internal Loop Results:')
        f.write('\n>Best rule:')
        f.close()
        best_rule.print_txt(log_file, 'Class')
        f = open(log_file, "a+")
        f.write('\n- number of covered cases: ' + repr(len(best_rule.covered_cases)))
        f.write('\n\n>> External Loop Information:')
        f.write('\n>Number of rules on discovered_rule_list: ' + repr(len(discovered_rule_list)))
        f.write('\n>Last_no_of_remaining_cases: ' + repr(last_no_of_remaining_cases))
        f.write('\n>No_of_remaining_cases: ' + repr(no_of_remaining_cases))
        f.close()
    # END OF WHILE (AVAILABLE_CASES > MAX_UNCOVERED_CASES)

    # just for log register
    f = open(log_file, "a+")
    f.write('\n\n==================== END EXTERNAL LOOP: end of Ant-Miner Algorithm')
    f.write('\n> Stopping Condition: number of remaining cases')
    f.write('\n   - no_of_remaining_cases = ' + repr(no_of_remaining_cases))
    f.write('\n   - max_uncovered_cases = ' + repr(max_uncovered_cases))
    f.close()

    # generating rule for remaining cases
    rule = Rule(training_dataset)
    rule.general_rule()
    # rule_for_remaining_cases = get_remaining_cases_rule(training_dataset)
    discovered_rule_list.append(rule)

    return discovered_rule_list, training_dataset, no_of_remaining_cases

