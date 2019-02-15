import copy
import numpy as np
from terms_manager import TermsManager
from rule import Rule


class AntMiner:

    def __init__(self, dataset, no_of_ants, min_case_per_rule, max_uncovered_cases, no_rules_converg, fold):
        self.dataset = dataset
        self.no_of_ants = no_of_ants
        self.min_case_per_rule = min_case_per_rule
        self.max_uncovered_cases = max_uncovered_cases
        self.no_rules_converg = no_rules_converg
        self.discovered_rule_list = []
        self.fold = fold

    def fit(self):
        log_file = "log_main.txt"
        i_log_file = "log_colony-loop.txt"
        f = open(log_file, "a+")
        f.write('\n\n\n==================== EXTERNAL LOOP ==========================================================================')
        f.write('\n> Stopping condition: number of uncovered cases')
        f.write('\n> Initialise pheromones > create t rule > choose best rule > add to the list > remove rule covered cases')
        f.write('\n============================================================================================================')
        f.write('\n FOLD OF CROSS VALIDATION: ' + repr(self.fold))
        f.close()

        no_of_remaining_cases = len(self.dataset.data)

        idx_e = 0
        while no_of_remaining_cases > self.max_uncovered_cases:
            idx_e += 1
            array_log_file = "log_dataset_external-Loop_fold-" + str(self.fold) + "iteration-" + str(idx_e) + ".txt"
            f = open(log_file, "a+")
            f.write('\n\n>>>>>>>>>>>>>>> ITERATION ' + repr(idx_e))
            f.write('\n> current dataset in ' + repr(array_log_file) + 'file')
            f.close()
            np.savetxt(array_log_file, self.dataset.data, fmt='%5s')

            previous_rule = Rule(self.dataset)
            best_rule = copy.deepcopy(previous_rule)

            ant_index = 0
            converg_test_index = 1

            terms_mgr = TermsManager(self.dataset, self.min_case_per_rule)
            if not terms_mgr.available():
                array_log_file = "log_NO-TERMS_fold" + str(self.fold) + "_iteration-" + str(idx_e) + ".txt"
                f = open(log_file, "a+")
                f.write('\n\n==================== END EXTERNAL LOOP')
                f.write('\n!! Alternative Condition: there are no terms in current dataset that covers enough cases')
                f.write('\n   - no_of_remaining_cases = ' + repr(no_of_remaining_cases))
                f.write('\n\n=>> dataset in ' + repr(array_log_file) + 'file')
                f.close()
                np.savetxt(array_log_file, self.dataset.data, fmt='%5s')
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

                if ant_index >= self.no_of_ants or converg_test_index >= self.no_rules_converg:
                    f = open(i_log_file, "a+")
                    f.write('\n\n==================== END Internal Loop')
                    f.write('\n  - no_of_ants = ' + repr(self.no_of_ants))
                    f.write('\n  - ant_index = ' + repr(ant_index))
                    f.write('\n  - no_rules_converg = ' + repr(self.no_rules_converg))
                    f.write('\n  - converg_test_index = ' + repr(converg_test_index))
                    f.write('\n  - Number of iterations: ' + repr(idx_i))
                    f.close()
                    break

                # RULE CONSTRUCTION
                f = open(i_log_file, "a+")
                f.write('\n\n=> Rule Construction Function: rule-construction-fnc_log-results.txt file <=')
                f.close()

                current_rule = Rule(self.dataset)
                current_rule.construct(terms_mgr, self.min_case_per_rule, idx_e, idx_i)

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

            self.discovered_rule_list.append(best_rule)
            self.dataset.data_updating(best_rule.covered_cases)
            no_of_remaining_cases = len(self.dataset.data)

            # just for log register
            f = open(log_file, "a+")
            f.write('\n>> Internal Loop Results:')
            f.write('\n>Best rule:')
            f.close()
            best_rule.print_txt(log_file, 'Class')
            f = open(log_file, "a+")
            f.write('\n- number of covered cases: ' + repr(len(best_rule.covered_cases)))
            f.write('\n\n>> External Loop Information:')
            f.write('\n>Number of rules on discovered_rule_list: ' + repr(len(self.discovered_rule_list)))
            f.write('\n>No_of_remaining_cases: ' + repr(no_of_remaining_cases))
            f.close()
        # END OF WHILE (AVAILABLE_CASES > MAX_UNCOVERED_CASES)

        # just for log register
        f = open(log_file, "a+")
        f.write('\n\n==================== END EXTERNAL LOOP: end of Ant-Miner Algorithm')
        f.write('\n> Stopping Condition: number of remaining cases')
        f.write('\n   - no_of_remaining_cases = ' + repr(no_of_remaining_cases))
        f.write('\n   - max_uncovered_cases = ' + repr(self.max_uncovered_cases))
        f.close()

        # just for log register
        ac_log_file = "log_accuracy-measure.txt"
        f = open(ac_log_file, "a+")
        f.write('\n\n=> DISCOVERED RULE LIST:')
        f.close()
        for r in self.discovered_rule_list:
            r.print_txt(ac_log_file, 'Class')

        # generating rule for remaining cases
        if no_of_remaining_cases > 0:
            rule = Rule(self.dataset)
            rule.general_rule()

            f = open(ac_log_file, "a+")
            f.write('\n\n=> GENERAL RULE: from remaining uncovered cases')
            f.close()
            rule.print_txt(ac_log_file, 'Class')

            self.discovered_rule_list.append(rule)

            f = open(ac_log_file, "a+")
            f.write('\n\n=> FINAL LIST OF DISCOVERED RULES:')
            f.close()
            for r in self.discovered_rule_list:
                r.print_txt(ac_log_file, 'Class')

        else:
            f = open(ac_log_file, "a+")
            f.write('\n\n!!! No general rule created: there are no remaining uncovered cases')
            f.close()

        return

    def predict(self, test_dataset):

        predicted_classes = []
        all_cases = len(test_dataset.data)

        rules = copy.deepcopy(self.discovered_rule_list[:-1])
        remaining_cases_rule = copy.deepcopy(self.discovered_rule_list[-1])

        for case in range(all_cases):  # for each new case
            chosen_class = None
            compatibility = True

            for rule in rules:  # sequential rule compatibility test

                for attr, value in rule.antecedent.items():
                    if value != test_dataset.data[case, test_dataset.col_index[attr]]:
                        compatibility = False
                        break

                if compatibility:
                    chosen_class = rule.consequent
                    break

            if chosen_class is None:
                chosen_class = remaining_cases_rule.consequent

            if chosen_class is None:
                print("Error: no class chosen")

            predicted_classes.append(chosen_class)

        return predicted_classes
