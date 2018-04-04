import json

import numpy as np
from __builtin__ import file

from interpolation.poly_cheb import PolyInterpolation


class SlidingWindow(object):
    def __init__(self, feature_size=10, nr_of_coefs=10, nr_of_samples=50, omit_first_coef=True, file_path=None):
        self.nr_of_samples = nr_of_samples
        self.omit_first_coef = omit_first_coef
        self.feature_size = feature_size
        self.nr_of_coefs = nr_of_coefs
        self.file_path = file_path
        self.polyInt = PolyInterpolation()

    def create_features_labels(self, meas_df, mp_id, area_name):
        if self.file_path is not None: return self.from_file(mp_id, area_name)
        x, y_hat, coefs = self.interpolate(meas_df)
        features = np.zeros([len(y_hat) - (self.feature_size + 1), self.feature_size])
        labels = np.zeros([len(y_hat) - (self.feature_size + 1)])
        labels_gradients = np.zeros([len(y_hat) - (self.feature_size + 1)])
        # length of y_hat - feature size and one for the label
        for idx in range(0, len(y_hat) - (self.feature_size + 1)):
            features[idx, :] = y_hat[idx:idx + self.feature_size]
            labels[idx] = y_hat[idx + self.feature_size]
            gradient = self.gradient_at_idx(x, y_hat, idx)
            labels_gradients[idx] = gradient
        return features, labels, labels_gradients

    def gradient_at_idx(self, x, y, idx):
        xy_idx = idx + (self.feature_size - 1)
        dy = y[xy_idx] - y[xy_idx + 1]
        dx = x[xy_idx] - x[xy_idx + 1]
        return float(dy) / float(dx)  # todo:  error-rates are high, might be an error here FIX

    def interpolate(self, meas_df):
        t = np.array(meas_df['x'])
        y = np.array(meas_df['y'])
        self.polyInt.set_t_y(t, y)
        coefs = self.polyInt.find_coefs(self.nr_of_coefs)
        if self.omit_first_coef: coefs[0] = 0
        x = np.arange(-1, 1, (2. / self.nr_of_samples))  # -1 and 1 because the chebs method
        y_hat = self.polyInt.get_y_hat_for_range(coefs, x)
        self.polyInt.save_chebs_to_file()  # save chebs to file for future use
        return x, y_hat, coefs

    def from_file(self, area_name, mp_id):
        with open(self.file_path) as data_file:
            sw_dict = json.load(data_file)
        area_dict = sw_dict.get(area_name)
        mp_dict = area_dict.get(mp_id)
        features = mp_dict.get('features')
        labels = mp_dict.get('labels')
        labels_gradients = mp_dict.get('labels_gradients')
        return features, labels, labels_gradients

    def serialize_file_name(self):
        name_parts = list()
        name_parts.append(self.nr_of_samples)
        name_parts.append(int(self.omit_first_coef))
        name_parts.append(self.feature_size)
        name_parts.append(self.nr_of_coefs)
        return '_'.join(map(str, name_parts))
