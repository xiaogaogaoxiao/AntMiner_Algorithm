

class cTerms:

    def __init__(self):
        self.attribute = ''
        self.value = ''
        self.heuristic = None
        self.pheromone = None
        self.probability = None

    def get_heuristic(self, data):
        return

    def get_pheromone(self, data):
        return

    def get_probability(self, data):
        return


def get_terms(dataset):

    list_of_terms = []
    for a in dataset.attr_values:
        for v in dataset.attr_values[a]:
            term_obj = cTerms()
            term_obj.attribute = a
            term_obj.value = v
            list_of_terms.append(term_obj)

    return list_of_terms
