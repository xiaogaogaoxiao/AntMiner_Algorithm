import pandas as pd
from dataset import cDataset
from ant_miner import *


def main():

    # INPUT: USER-DEFINED PARAMETERS:
    NO_OF_ANTS = 3000
    MIN_CASE_PER_RULE = 10
    MAX_UNCOVERED_CASES = 10
    NO_RULES_CONVERG = 10

    # INPUT: DATASET AND CLASS ATTRIBUTE NAME
    header = list(pd.read_csv('datasets/tic-tac-toe_header.txt', delimiter=','))
    data = pd.read_csv('datasets/tic-tac-toe_data.txt', delimiter=',', header=None, names=header, index_col=0)
    class_attr = 'Class'

    # Object: DATASET
    dataset_SSDP = cDataset(data, class_attr)

    DiscoveredRuleList, TrainingSet = ant_miner(dataset_SSDP, NO_OF_ANTS,
                                                MIN_CASE_PER_RULE, MAX_UNCOVERED_CASES, NO_RULES_CONVERG)

    for rule in DiscoveredRuleList:
        rule.print(class_attr)


if __name__ == '__main__':
    main()
