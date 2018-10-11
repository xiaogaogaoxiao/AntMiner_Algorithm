from terms import *


def ant_miner(dataset, no_of_ants, min_case_per_rule, max_uncovered_cases, no_rules_converg):

    TrainingSet = dataset
    DiscoveredRuleList = []

    while len(TrainingSet.data) > max_uncovered_cases:

        list_of_terms = get_terms(dataset.attr_values)
        ant_index = 0
        converg_test_index = 0

        set_pheromone_init(list_of_terms)

        set_heuristic_values(list_of_terms, dataset)

        while True:

            ant_index += 1

            RuleConstruction()
            RulePrune()
            PheromoneUpdating()

            CheckConverg()

            if ant_index >= no_of_ants or converg_test_index >= no_rules_converg:
                break

        R_best = ChoosesBestRule()
        DiscoveredRuleList.append(R_best)
        covered_cases = get_CoveredCases
        TrainingSet = TrainingSet - covered_cases

    return DiscoveredRuleList


def get_terms(dict_attr_values):

    list_of_terms = []
    for a in dict_attr_values:
        for v in dict_attr_values[a]:
            term_obj = cTerms()
            term_obj.attribute = a
            term_obj.value = v
            list_of_terms.append(term_obj)

    return list_of_terms


def set_pheromone_init(list_of_terms):

    for term in list_of_terms:
        term.pheromone = 1/len(list_of_terms)

    return


def set_heuristic_values(list_of_terms, dataset):

    terms_logK_entropy = []
    for term in list_of_terms:
        term.set_entropy(dataset)
        terms_logK_entropy.append(term.logK_entropy)

    for term in list_of_terms:
        term.set_heuristic(len(dataset.class_values), sum(terms_logK_entropy))

    return
