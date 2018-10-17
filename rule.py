
class cRule:

    def __init__(self, dataset):
        self.antecedent = {}
        self.consequent = None
        self.added_terms = []
        self.covered_cases = []
        self.no_covered_cases = None
        self.quality = None

        self.set_covered_cases(dataset)

    def set_covered_cases(self, dataset):
        self.covered_cases = list(range(len(dataset.data)))

        return

