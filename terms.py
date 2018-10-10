

class cTerms:

    def __init__(self):
        self.attribute = ''
        self.value = ''
        self.pheromone = None
        self.heuristic = None
        self.pheromone = None
        self.probability = None


    def get_heuristic(self, data):
        return

    def get_pheromone(self, data):
        return

    def get_probability(self, data):
        return


def get_terms(data):

    list_of_terms = []
    for a in data.attr_values:
        for v in data.attr_values[a]:
            term_obj = cTerms()
            term_obj.attribute = a
            term_obj.value = v
            list_of_terms.append(term_obj)

    return list_of_terms


def set_pheromone_init(list_of_terms):

    for term in list_of_terms:
        term.pheromone = 1/len(list_of_terms)

    return
