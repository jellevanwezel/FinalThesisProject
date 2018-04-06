from pandas import DataFrame

from database.area_model import AreaModel
import numpy as np
from tqdm import tqdm
import pandas as pd
import logging as log

from feature_extraction.feature_map import FeatureLabels
from feature_extraction.sliding_window import SlidingWindow
from feature_extraction.static_features import StaticFeatures


class Dataset(object):
    def __init__(self):
        self.area_model = AreaModel()

    def generate_dataset(self, sliding_window, static_features, n_label_bins=10):
        """
        Concatinates the sliding window and the static features and bins the labels.
        :param sliding_window: Sliding window object
        :param static_features: Static features object
        :param n_label_bins: number of bins to be used
        :return: the Dataset as a DataFrame
        :rtype: pandas.DataFrame
        """
        id_names = ['area_id', 'measure_point_id']
        sw_names = self.get_sliding_window_names(sliding_window.feature_size)
        static_names = self.get_static_names()
        label_names = ['point_label', 'gradient_label']
        c_names = id_names + sw_names + static_names + label_names
        data_dict = dict()
        for c_name in c_names:
            data_dict[c_name] = []

        log.info('Extracting Static Features')

        sf = static_features.extract_static_features()
        sf_dict = static_features.extract_static_features_to_dict(sf)

        log.info('Extracting Sliding Window')

        nr_of_areas = self.area_model.get_number_of_areas()
        for area_idx in tqdm(range(0, nr_of_areas), desc='Areas'):
            area_name = self.area_model.get_area_name(area_idx)
            # print area_name, str(area_idx + 1) + '/' + str(self.area_model.get_number_of_areas())
            for mp_idx, mp_id in enumerate(self.area_model.get_mp_ids(area_idx)):
                meas_df = None
                if sliding_window.file_path is None:
                    meas_df = self.area_model.get_mp_df(area_idx, mp_idx)
                    meas_df = self.area_model.prepare_meas_df(meas_df)
                    if meas_df is None: continue
                if sf_dict.get((area_name, mp_id)) is None: continue
                sf_row = sf_dict[(area_name, mp_id)]
                try:
                    sw_features, labels, label_gradients = sliding_window.create_features_labels(meas_df, area_name,
                                                                                                 mp_id)
                except:
                    continue  # todo: log error
                for window_idx in range(0, len(sw_features)):
                    labels_grouped = [labels[window_idx], label_gradients[window_idx]]
                    f_row = [area_name, mp_id] + sw_features[window_idx].tolist() + sf_row + labels_grouped
                    for c_name, val in zip(c_names, f_row):
                        data_dict[c_name].append(val)
                        # row_dict = dict(zip(c_names, f_row))
                        # df = df.append(row_dict, ignore_index=True)

        binned_points, _ = self.bin_labels(data_dict['point_label'], n_label_bins)
        binned_gradients, _ = self.bin_labels(data_dict['gradient_label'], n_label_bins)
        data_dict['binned_points'] = binned_points
        data_dict['binned_gradients'] = binned_gradients
        df = pd.DataFrame.from_dict(data_dict)
        df = df.reindex(c_names + ['binned_points', 'binned_gradients'], axis=1)
        return df

    # todo: sliding window should return this
    def get_sliding_window_names(self, sw_size):
        """Generates the column names for the sliding window"""
        names = []
        for i in range(0, sw_size):
            names.append('sw_' + str(i))
        return names

    # todo: static features should return this
    def get_static_names(self):
        """Generates the column names for the static features"""
        names = []
        groups = [FeatureLabels.acid,
                  FeatureLabels.ground_water,
                  FeatureLabels.stability,
                  FeatureLabels.ground_type,
                  FeatureLabels.pipe]
        for group in groups:
            group_name = group[0]
            for label in group[1]:
                names.append(group_name + '_' + label)
        return names

    def bin_labels(self, labels, nr_of_bins):
        """Bins the labels to the given nr_of_bins"""
        labels = np.round(labels)
        bin_size = np.abs(np.min(labels) - np.max(labels)) / float(nr_of_bins)
        bins = np.arange(int(np.min(labels)) + bin_size, int(np.max(labels)), bin_size)
        binned_labels = np.digitize(labels, bins)
        return binned_labels, bins


sw_file = '../feature_extraction/data/sliding_window/20_1_10_10.json'
sw = SlidingWindow(file_path=sw_file)
sf_file = '../feature_extraction/data/static_features.csv'
sf = StaticFeatures(file_path=sf_file)
ds = Dataset()
df = ds.generate_dataset(sw, sf, n_label_bins=20)
df.to_csv(path_or_buf='./data.csv', index=False)
