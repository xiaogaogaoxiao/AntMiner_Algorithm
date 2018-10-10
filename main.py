import pandas as pd
from data import cDataset
from ant_miner import *

def main():

    # INPUT: USER-DEFINED PARAMETERS:
    NO_OF_ANTS = 30
    MIN_CASE_PER_RULE = 2
    MAX_UNCOVERED_CASES = 3
    NO_RULES_CONVERG = 5

    # INPUT: DATASET AND CLASS ATTRIBUTE NAME
    data = pd.read_csv('datasets/data_SSDP.csv', delimiter=';')
    class_attr = 'Label'

    # Object: DATASET
    data_SSDP = cDataset(data, class_attr)

    ant_miner(data_SSDP, NO_OF_ANTS, MIN_CASE_PER_RULE, MAX_UNCOVERED_CASES, NO_RULES_CONVERG)

if __name__ == '__main__':
    main()