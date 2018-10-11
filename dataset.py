import pandas as pd
import numpy as np


class cDataset:

    def __init__(self, data, class_attr):
        self.class_attr = class_attr
        self.class_values = []
        self.attr_values = {}
        self.col_index = {}
        self.col_values = {}
        self.data = np.array(data)

        self.set_data(data)

    def set_data(self, data):
        attr = list(data.columns.values)

        self.attr_values = dict.fromkeys(attr)
        for name in attr:
            self.attr_values[name] = list(pd.unique(data[name]))

        self.class_values = self.attr_values[self.class_attr]
        del self.attr_values[self.class_attr]

        self.col_values = dict.fromkeys(attr)
        for name in attr:
            self.col_values[name] = list(data[name])

        self.col_index = dict.fromkeys(attr)
        for idx in range(len(attr)):
            self.col_index[attr[idx]] = idx
