import copy
from terms import Terms


class TermsManager:

    def __init__(self, dataset, min_case_per_rule):
        self.__terms_dict = {}
        self.__terms_availability = {}
        self.__pheromone_table = {}
        self.__heuristic_table = {}
        self.__no_of_terms = 0

        # build object
        self.__constructor(dataset, min_case_per_rule)

    def __constructor(self, dataset, min_case_per_rule):

        attr_values = dataset.attr_values
        attrs = list(attr_values.keys())
        heuristic_accum = 0

        # TABLES: { Attr : {} }
        self.__pheromone_table = {}.fromkeys(attrs, {})
        self.__heuristic_table = {}.fromkeys(attrs, {})

        # TERMS: constructing __terms_dict and __terms_availability
        self.__terms_dict = {}.fromkeys(attrs, [])
        self.__terms_availability = {}.fromkeys(attrs)
        for attr in attrs:
            list_of_terms = []
            for value in attr_values[attr]:
                term_obj = Terms(attr, value, dataset, min_case_per_rule)
                if term_obj.available():
                    list_of_terms.append(term_obj)
                    self.__no_of_terms += 1
                    heuristic_accum += term_obj.get_heuristic()
            self.__terms_dict[attr] = copy.deepcopy(list_of_terms)
            self.__terms_availability[attr] = True

        # Constructing __pheromone_table: { Attr : { Value : Pheromone } }
        initial_pheromone = 1 / self.__no_of_terms
        for attr in attrs:
            values = dataset.attr_values[attr]
            self.__pheromone_table[attr] = {}.fromkeys(values, initial_pheromone)
            self.__heuristic_table[attr] = {}.fromkeys(values)

        # Constructing __heuristic_table: { Attr : { Value : Heuristic } }
        if heuristic_accum == 0: print('!!! Heuristic normalization denominator equal Zero')  # CHECK NECESSITY
        for attr in attrs:
            attr_terms = self.__terms_dict[attr]
            for term in attr_terms:
                self.__heuristic_table[term.attribute][term.value] = (term.get_heuristic() / heuristic_accum)

        return

    def size(self):
        return self.__no_of_terms
