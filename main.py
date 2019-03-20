import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

from dataset import Dataset
from ant_miner import AntMiner
from k_fold_crossvalidation import k_fold
from data_preprocessing import data_analysis


def main():

    # INPUT: USER-DEFINED PARAMETERS:
    no_of_ants = 3000
    min_cases_per_rule = 10
    max_uncovered_cases = 10
    no_rules_converg = 10

    # INPUT: DATASET AND CLASS ATTRIBUTE NAME
    log_file = "log_main.txt"
    ac_log_file = "log_accuracy-measure.txt"
    header = list(pd.read_csv('datasets/tic-tac-toe_header.txt', delimiter=','))
    data = pd.read_csv('datasets/tic-tac-toe_data.txt', delimiter=',', header=None, names=header, index_col=False)
    class_attr = 'Class'

    #data = data_analysis(data)

    # K-FOLD CROSS-VALIDATION SETTINGS
    k = 10
    training_folders, test_folders = k_fold(data, class_attr, n_splits=k, stratified=False)

    # GLOBAL VARIABLES
    predictive_accuracy = []
    no_of_discovered_rules = []

    # K ITERATIONS OF ANT-MINER ALGORITHM AND CLASSIFICATION TASK BASED ON GENERATED RULES:
    for fold in range(k):

        print('\nFOLD: ', fold)
        f = open(log_file, "a+")
        f.write('\n\n\n****************************************************************************************************')
        f.write('\n**************************************** FOLD: ' + repr(fold) + ' ***************************************************')
        f.write('\n****************************************************************************************************')
        f.close()

        # CONSTRUCTING DATASET FOR K ITERATION OF K-FOLD CROSS VALIDATION
        kfold_test_cases = test_folders[fold]
        kfold_training_cases = training_folders[fold]
        training_data = data.drop(kfold_test_cases, axis=0).copy()
        test_data = data.drop(kfold_training_cases, axis=0).copy()
        f = open(log_file, "a+")
        f.write('\n> TRAINING CASES: ' + repr(kfold_training_cases))
        f.write('\n> TEST CASES: ' + repr(kfold_test_cases))
        f.close()

        # Objects: TRAINING AND TEST DATASETS
        training_dataset = Dataset(training_data, class_attr)
        test_dataset = Dataset(test_data, class_attr)

        # Just for log registes
        f = open(ac_log_file, "a+")
        f.write('\n\n\n=============== PREDICTION ACCURACY ANALISYS =================================================================')
        f.write('\n\n=> FOLD: ' + repr(fold))
        f.close()

        # ANT-MINER ALGORITHM: list of rules generator
        f = open(log_file, "a+")
        f.write('\n\n>>>>>>>>>>>>>>>>>>>> ANT-MINER ALGORITHM\n')
        f.close()
        ant_miner = AntMiner(training_dataset, no_of_ants, min_cases_per_rule, max_uncovered_cases, no_rules_converg, fold)
        ant_miner.fit()

        print('\nRULES:\n')
        f = open(log_file, "a+")
        f.write('\n\n>>>>>>>>>>>>>>>>>>>> DISCOVERED MODEL (Ant-Miner Algorithm Results)')
        f.write('\n>> Discovered rule list:')
        f.close()
        for rule in ant_miner.discovered_rule_list:
            rule.print(class_attr)
            rule.print_txt(log_file, class_attr)
        no_of_discovered_rules.append(len(ant_miner.discovered_rule_list))

        # CLASSIFICATION OF NEW CASES
        test_dataset_real_classes = test_dataset.get_real_classes()
        test_dataset_predicted_classes = ant_miner.predict(test_dataset)
        f = open(ac_log_file, "a+")
        f.write('\n\n=> TARGETS:')
        f.write('\n- Real classes:      ' + repr(test_dataset_real_classes))
        f.write('\n- Predicted classes: ' + repr(test_dataset_predicted_classes))
        f.close()

        # PREDICTIVE ACCURACY CALCULATION
        accuracy = accuracy_score(test_dataset_real_classes, test_dataset_predicted_classes)
        predictive_accuracy.append(accuracy)
        f = open(log_file, "a+")
        f.write('\n\n>> Number of discovered rules: ' + repr(len(ant_miner.discovered_rule_list)))
        f.write('\n>> Predictive Accuracy: ' + repr(accuracy))
        f.close()

    # PREDICTIVE ACCURACY OF K-FOLDS
    predictive_accuracy_mean = np.mean(predictive_accuracy)
    predictive_accuracy_std = np.std(predictive_accuracy)
    no_of_discovered_rules_average = np.mean(no_of_discovered_rules)

    print('\nPREDICTIVE ACCURACIES:')
    print('\n', predictive_accuracy)
    print('\nPREDICTIVE ACCURACY MEAN', predictive_accuracy_mean)
    print('\nPREDICTIVE ACCURACY STD', predictive_accuracy_std)
    f = open(log_file, "a+")
    f.write('\n\n\n****************************************************************************************************')
    f.write('\n****************************** 10-FOLD CROSS VALIDATION INFO ******************************')
    f.write('\n****************************************************************************************************')
    f.write('\n> PREDICTIVE ACCURACIES: ' + repr(predictive_accuracy))
    f.write('\n> K-FOLD ACCURACY (mean +- std): ' + repr(predictive_accuracy_mean) +
            ' +- ' + repr(predictive_accuracy_std))
    f.write('\n> AVERAGE NUMBER OF DISCOVERED RULES: ' + repr(no_of_discovered_rules_average))
    f.close()

    return


if __name__ == '__main__':
    main()
