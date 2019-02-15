from sklearn.model_selection import StratifiedKFold, KFold


def k_fold(data, class_attr, n_splits=10, stratified=False):

    training_folders = dict.fromkeys(range(n_splits))
    test_folders = dict.fromkeys(range(n_splits))
    idx = 0

    if stratified:
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True)
        for train, test in skf.split(data, data[class_attr]):
            training_folders[idx] = list(train)
            test_folders[idx] = list(test)
            idx += 1

    elif not stratified:
        kf = KFold(n_splits=n_splits, shuffle=True)
        for train, test in kf.split(data):
            training_folders[idx] = list(train)
            test_folders[idx] = list(test)
            idx += 1

    return training_folders, test_folders

