from collections import Counter

import glvq
import pandas as pd
from sklearn.model_selection import KFold
import numpy as np
from tqdm import tqdm


class CrossValidateLvq(object):
    def __init__(self, n_bins, n_folds, lvq_model):
        self.n_bins = n_bins
        self.n_folds = n_folds
        self.lvq_model = lvq_model
        self.conv_matrix = np.zeros((n_bins, n_bins))

    def split(self, df):
        data_splits = list()
        kfold = KFold(n_splits=self.n_folds, shuffle=False)
        for fold_idx, (train_idx, test_idx) in zip(range(splits), kfold.split(df)):
            fold_dict = dict()
            fold_dict['train_data'] = df.iloc[train_idx, 2:-4]
            fold_dict['train_labels'] = df.iloc[train_idx, -4:]
            fold_dict['test_data'] = df.iloc[test_idx, 2:-4]
            fold_dict['test_labels'] = df.iloc[test_idx, -4:]
            data_splits.append(fold_dict)
        return data_splits

    def predict_lvq(self, train_data, train_labels, test_data, test_labels, lvq_model):
        lvq_model.fit(train_data, train_labels)
        pred_labels = lvq_model.predict(test_data)
        for p_idx, t_idx in zip(pred_labels, test_labels):
            self.conv_matrix[p_idx, t_idx] += 1

    def cross_validate(self, data_df, gradient=False):
        label_idx = 3 if gradient else 2  # todo: magic number fix
        data_splits = self.split(data_df)
        for fold_dict in tqdm(data_splits):
            train_data = fold_dict['train_data']
            test_data = fold_dict['test_data']
            train_labels = fold_dict['train_labels'].iloc[:, label_idx]
            test_labels = fold_dict['test_labels'].iloc[:, label_idx]
            self.predict_lvq(train_data, train_labels, test_data, test_labels, self.lvq_model)
        return np.round(self.conv_matrix / self.n_folds, 1)


splits = 2
df = pd.read_csv(filepath_or_buffer='../preprocessing/data.csv')
cv_lvq = CrossValidateLvq(10, 5, glvq.LgmlvqModel())
error_matrix = cv_lvq.cross_validate(df)
labels = map(str, range(10))
print
print '     ' + '   '.join(labels)
for row_label, row in zip(labels, error_matrix):
    print '%s |%s|' % (row_label, ' '.join('%03s' % int(np.ceil(i)) for i in row))
