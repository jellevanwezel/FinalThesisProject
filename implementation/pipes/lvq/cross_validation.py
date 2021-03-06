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
        self.conf_matrix = np.zeros((n_bins, n_bins))

    def split(self, df):
        """
        Creates splits from the given DataFrame grouped by the measurement point
        :param df: The dataFrame with the features and labels
        :return: list of dictionaries with the splits
        :rtype: list
        """
        data_splits = []
        for _ in range(self.n_folds):
            data_splits.append({
                'train_data': pd.DataFrame(),
                'train_labels': pd.DataFrame(),
                'test_data': pd.DataFrame(),
                'test_labels': pd.DataFrame(),
            })
        kfold = KFold(n_splits=self.n_folds, shuffle=False)
        for mp_id in tqdm(df.iloc[:, 1].unique(), desc='Folding'):
            meas_df = df[df.iloc[:, 1] == mp_id]
            for fold_idx, (train_idx, test_idx) in zip(range(self.n_folds), kfold.split(meas_df)):
                tr_data = data_splits[fold_idx]['train_data'].append(meas_df.iloc[train_idx, 2:-4], ignore_index=True)
                data_splits[fold_idx]['train_data'] = tr_data
                tr_lab = data_splits[fold_idx]['train_labels'].append(meas_df.iloc[train_idx, -4:], ignore_index=True)
                data_splits[fold_idx]['train_labels'] = tr_lab
                te_data = data_splits[fold_idx]['test_data'].append(meas_df.iloc[test_idx, 2:-4], ignore_index=True)
                data_splits[fold_idx]['test_data'] = te_data
                te_lab = data_splits[fold_idx]['test_labels'].append(meas_df.iloc[test_idx, -4:], ignore_index=True)
                data_splits[fold_idx]['test_labels'] = te_lab
        return data_splits

    def predict_lvq(self, train_data, train_labels, test_data, test_labels, lvq_model):
        """
        Trains a lvq model on the train data and tests on the test data.
        :param train_data:
        :param train_labels:
        :param test_data:
        :param test_labels:
        :param lvq_model:
        :return: The confusion matrix
        """
        lvq_model.fit(train_data, train_labels)
        pred_labels = lvq_model.predict(test_data)
        for p_idx, t_idx in zip(pred_labels, test_labels):
            self.conf_matrix[p_idx, t_idx] += 1

    def cross_validate(self, data_df, gradient=False):
        """
        Cross validates the lvq model with the given dataset.
        :param data_df:
        :param gradient: wether or not the gradient should be used as label
        :return: the confusion matrix
        :rtype: numpy.array
        """
        label_idx = 3 if gradient else 2  # todo: magic number fix, use column name
        data_splits = self.split(data_df)
        for fold_dict in tqdm(data_splits, desc='Validating'):
            train_data = fold_dict['train_data']
            test_data = fold_dict['test_data']
            train_labels = fold_dict['train_labels'].iloc[:, label_idx]
            test_labels = fold_dict['test_labels'].iloc[:, label_idx]
            self.predict_lvq(train_data, train_labels, test_data, test_labels, self.lvq_model)
        return np.round(self.conf_matrix / self.n_folds, 1)

    def print_conv_matrix(self):
        """
        Prints the confusion matrix
        """
        labels = map(str, range(self.n_bins))
        spacing = len(str(np.max(self.conf_matrix.astype(int))))
        space_str = '%0' + str(spacing) + 's'
        top_spaces = ''.join([' '] * spacing)
        print '  ' + top_spaces + top_spaces.join(labels)
        for row_label, row in zip(labels, self.conf_matrix):
            print '%s |%s|' % (row_label, ' '.join(space_str % int(np.ceil(i)) for i in row))



