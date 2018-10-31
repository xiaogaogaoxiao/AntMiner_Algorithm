import pandas as pd
from dataset import cDataset
from k_fold_crossvalidation import k_fold
from ant_miner import *


def main():

    # INPUT: USER-DEFINED PARAMETERS:
    no_of_ants = 3000
    min_cases_per_rule = 10
    max_uncovered_cases = 10
    no_rules_converg = 10

    # INPUT: DATASET AND CLASS ATTRIBUTE NAME
    header = list(pd.read_csv('datasets/tic-tac-toe_header.txt', delimiter=','))
    data = pd.read_csv('datasets/tic-tac-toe_data.txt', delimiter=',', header=None, names=header, index_col=False)
    class_attr = 'Class'

    # K-FOLD CROSS-VALIDATION SETTINGS
    k = 10
    training_folders, test_folders = k_fold(data, class_attr, k)

    # GLOBAL VARIABLES
    predictive_accuracy = []


    # K ITERATIONS OF ANT-MINER ALGORITHM AND CLASSIFICATION TASK BASED ON GENERATED RULES:

    for fold in range(k):

        print('\nFOLD: ', fold)

        # CONSTRUCTING DATASET FOR K ITERATION OF K-FOLD CROSS VALIDATION
        kfold_test_cases = test_folders[fold]
        kfold_training_cases = training_folders[fold]
        training_data = data.drop(kfold_test_cases, axis=0).copy()
        test_data = data.drop(kfold_training_cases, axis=0).copy()

        # Objects: TRAINING AND TEST DATASETS
        training_dataset = cDataset(training_data, class_attr)
        test_dataset = cDataset(test_data, class_attr)

        # ANT-MINER ALGORITHM: list of rules generator
        discovered_rule_list, final_training_set, no_of_remaining_cases = \
            ant_miner(training_dataset, no_of_ants, min_cases_per_rule, max_uncovered_cases, no_rules_converg)

        print('\nRULES:\n')
        for rule in discovered_rule_list:
            rule.print(class_attr)

        # CLASSIFICATION OF NEW CASES
        test_dataset_real_classes = test_dataset.get_real_classes()
        test_dataset_classification_classes = classification_task(test_dataset, discovered_rule_list)

        # PREDICTIVE ACCURACY CALCULATION
        accuracy = get_predictive_accuracy(test_dataset_real_classes, test_dataset_classification_classes)
        predictive_accuracy.append(accuracy)

    return


if __name__ == '__main__':
    main()
