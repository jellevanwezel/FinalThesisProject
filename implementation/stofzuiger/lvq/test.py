from collections import Counter

import glvq
import pandas as pd
from sklearn.model_selection import KFold
import numpy as np
from tqdm import tqdm


def split(n_splits, df):
    data_splits = list()
    kfold = KFold(n_splits=n_splits, shuffle=False)
    for fold_idx, (train_idx, test_idx) in zip(range(splits), kfold.split(df)):
        fold_dict = dict()
        fold_dict['train_data'] = df.iloc[train_idx, 2:-2]
        fold_dict['train_labels'] = df.iloc[train_idx, -2:]
        fold_dict['test_data'] = df.iloc[test_idx, 2:-2]
        fold_dict['test_labels'] = df.iloc[test_idx, -2:]
        data_splits.append(fold_dict)
    return data_splits


def predict_lvq(train_data, train_labels, test_data, test_labels, lvq_model):
    lvq_model.fit(train_data, train_labels)
    pred_labels = lvq_model.predict(test_data)
    return test_labels - pred_labels


def cross_validator(data_splits, lvq_model=glvq.GlvqModel(), gradient=False):
    error_dict = Counter({})
    for fold_dict in tqdm(data_splits):
        train_data = fold_dict['train_data']
        test_data = fold_dict['test_data']
        train_labels = fold_dict['train_labels'].iloc[:, int(gradient)]  # label on column 0 is point 1 is gradient
        test_labels = fold_dict['test_labels'].iloc[:, int(gradient)]
        error_dists = predict_lvq(train_data, train_labels, test_data, test_labels, lvq_model)
        values, counts = np.unique(error_dists, return_counts=True)
        error_dict += Counter(dict(zip(values, counts)))
        error_dict['total_validations'] += test_data.shape[0]
    return error_dict


splits = 2
df = pd.read_csv(filepath_or_buffer='../preprocessing/data.csv')
data_splits = split(splits, df)
errors = cross_validator(data_splits)
print errors
