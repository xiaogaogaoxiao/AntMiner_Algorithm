import pandas as pd


class cDataset:

    def __init__(self, data, class_attr):
        self.class_attr = class_attr
        self.class_values = {}
        self.data = data
        self.attr_values = {}

        self.set_data()

    def set_data(self):
        attr = list(self.data.columns.values)
        self.attr_values = dict.fromkeys(attr)

        for name in attr:
            self.attr_values[name] = list(pd.unique(self.data[name]))
        self.class_values = {self.class_attr: self.attr_values[self.class_attr]}
        del self.attr_values[self.class_attr]