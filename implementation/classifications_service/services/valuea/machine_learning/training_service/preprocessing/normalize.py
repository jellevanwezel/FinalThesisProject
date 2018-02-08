from sklearn import preprocessing


def normalize(data, normalize_over_features=False):
    if normalize_over_features:
        return preprocessing.normalize(data, 'max', 0)
    else:
        return preprocessing.normalize(data, 'max')
