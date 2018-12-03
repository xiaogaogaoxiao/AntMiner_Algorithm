import numpy as np
import pandas as pd


def data_analysis(data):

    _data_exploration(data)
    data = _missing_values(data)
    print('\nAfter treating missing values\n')
    _data_exploration(data)
    data = _del_id(data)

    return data


def _data_exploration(data):

    no_of_attributes = len(data.iloc[0])
    for attr in range(no_of_attributes):
        print('Attribute: ', attr)
        print(np.unique(np.array(data.iloc[:, attr])))

    return


def _missing_values(data):

    missing = "?"
    missing_value = "missing"
    data = data.replace(to_replace=missing, value=missing_value)

    return data


def _del_id(data):

    label = 'id'
    if label in list(data.columns.values):
        data = data.drop(columns=label)

    return data
