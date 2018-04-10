import json
import numpy as np

from interpolation.poly_cheb import PolyInterpolation


class SlidingWindow(object):
    def __init__(self, window_size=10, nr_of_coefs=10, nr_of_samples=25, omit_first_coef=True, file_path=None):
        self.nr_of_samples = nr_of_samples
        self.omit_first_coef = omit_first_coef
        self.window_size = window_size
        self.nr_of_coefs = nr_of_coefs
        self.file_path = file_path
        self.polyInt = PolyInterpolation()
        if file_path is not None:
            self.sw_dict = self.load_from_file()

    def create_features_labels(self, meas_df, area_name, mp_id):
        """
        Creates a features and labels for this measure point
        It interpolates the measure point data and applies a sliding window
        :param meas_df: measurement DataFrame
        :param area_name: name of the area the measurepoint is in
        :param mp_id: measure point id
        :return: the features and its corresponding labels
        :rtype: numpy.array, numpy.array, numpy.array
        """
        if self.file_path is not None: return self.from_file(area_name, mp_id)
        x, y_hat, coefs = self.interpolate(meas_df)
        features = np.zeros([len(y_hat) - (self.window_size + 1), self.window_size])
        labels = np.zeros([len(y_hat) - (self.window_size + 1)])
        labels_gradients = np.zeros([len(y_hat) - (self.window_size + 1)])
        for idx in range(0, len(y_hat) - (self.window_size + 1)):
            features[idx, :] = y_hat[idx:idx + self.window_size]  # todo: check if this is correct, index
            labels[idx] = y_hat[idx + self.window_size]
            gradient = self.gradient_at_idx(x, y_hat, idx + self.window_size)
            labels_gradients[idx] = gradient
        return features, labels, labels_gradients

    def gradient_at_idx(self, x, y, idx):
        """
        Gets the gradient between idx and idx + 1
        :param x: list with x values
        :param y:  list with y values
        :param idx: the index at which the gradient needs to be calculated
        :return: the gradient
        :rtype: float
        """
        dy = y[idx] - y[idx + 1]
        dx = x[idx] - x[idx + 1]
        return float(dy) / float(dx)  # todo: error is high because data is lost, check.

    def interpolate(self, meas_df):
        """
        Interpolates the measurements to give approximated but consistent measurements
        :param meas_df: the measurement DataFrame
        :return: the x values, the approximated y values and the found coefficients
        :rtype: numpy.array, numpy.array, numpy.array
        """
        t = np.array(meas_df['x'])
        y = np.array(meas_df['y'])
        self.polyInt.set_t_y(t, y)
        coefs = self.polyInt.find_coefs(self.nr_of_coefs)
        first_coef = coefs[0]
        if self.omit_first_coef:
            coefs[0] = 0
        x = np.arange(-1, 1, (2. / self.nr_of_samples))  # -1 and 1 because the chebs method
        y_hat = self.polyInt.get_y_hat_for_range(coefs, x)
        self.polyInt.save_chebs_to_file()  # save chebs to file for future use
        coefs[0] = first_coef
        return x, y_hat, coefs

    def from_file(self, area_name, mp_id):
        """
        Loads the features and labels from a file, all further params and calculations are ignored.
        :param area_name: name of the area
        :param mp_id: id of the measurement point
        :return: the features and its corresponding labels
        :rtype: numpy.array, numpy.array, numpy.array
        """
        area_dict = self.sw_dict.get(area_name)
        if area_dict is None:
            raise ValueError('Area not in file')
        mp_dict = area_dict.get(str(mp_id))
        if mp_dict is None:
            raise ValueError('Measurments not in file')
        features = np.array(mp_dict.get('features'))
        labels = mp_dict.get('labels')
        labels_gradients = mp_dict.get('label_gradients')
        return features, labels, labels_gradients

    def load_from_file(self):
        """
        loads the json file to a dictionary
        :return:
        """
        with open(self.file_path) as data_file:
            return json.load(data_file)

    def serialize_file_name(self):
        name_parts = list()
        name_parts.append(self.nr_of_samples)
        name_parts.append(int(self.omit_first_coef))
        name_parts.append(self.window_size)
        name_parts.append(self.nr_of_coefs)
        return '_'.join(map(str, name_parts))
