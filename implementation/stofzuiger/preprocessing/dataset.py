from pandas import DataFrame

from database.area_model import AreaModel
import numpy as np
from tqdm import tqdm
import pandas as pd

from feature_extraction.feature_map import FeatureLabels
from feature_extraction.sliding_window import SlidingWindow
from feature_extraction.static_features import StaticFeatures


class Dataset(object):
    def __init__(self):
        self.area_model = AreaModel()

    def generate_dataset(self, sliding_window, static_features, n_label_bins):

        id_names = ['area_id', 'measure_point_id']
        sw_names = self.get_sliding_window_names(sliding_window.feature_size)
        static_names = self.get_static_names()
        label_names = ['point_label', 'gradient_label']
        c_names = id_names + sw_names + static_names + label_names
        df = DataFrame(columns=c_names)

        print '--- Extracting Static Features ---\n'
        sf = static_features.extract_static_features()
        sf_dict = static_features.extract_static_features_to_dict(sf)

        print '--- Extracting Sliding Window ---\n'
        nr_of_areas = self.area_model.get_number_of_areas()
        for area_idx in tqdm(range(0, nr_of_areas)):
            area_name = self.area_model.get_area_name(area_idx)
            # print area_name, str(area_idx + 1) + '/' + str(self.area_model.get_number_of_areas())
            for mp_idx, mp_id in enumerate(self.area_model.get_mp_ids(area_idx)):
                meas_df = self.area_model.get_mp_df(area_idx, mp_idx)
                meas_df = self.area_model.prepare_meas_df(meas_df)
                if meas_df is None: continue
                if sf_dict.get((area_name, mp_id)) is None: continue
                sf_row = sf_dict[(area_name, mp_id)]
                if self.file_path is not None:
                    sw_features, labels, label_gradients = sliding_window.create_features_labels(meas_df)
                else:
                    sw_features, labels, label_gradients = sliding_window.from_file(area_name, mp_idx)
                for window_idx in range(0, len(sw_features)):
                    labels_grouped = [labels[window_idx], label_gradients[window_idx]]
                    f_row = [area_name, mp_id] + sw_features[window_idx].tolist() + sf_row + labels_grouped
                    row_dict = dict(zip(c_names, f_row))
                    df = df.append(row_dict, ignore_index=True)

        binned_points = self.bin_labels(np.array(df.iloc[:, -2]), n_label_bins)
        binned_gradients = self.bin_labels(np.array(df.iloc[:, -1]), n_label_bins)
        df['binned_points'] = pd.Series(binned_points, index=df.index)
        df['binned_gradients'] = pd.Series(binned_gradients, index=df.index)

        return df

    # todo: sliding window should return this
    def get_sliding_window_names(self, sw_size):
        names = []
        for i in range(0, sw_size):
            names.append('sw_' + str(i))
        return names

    # todo: static features should return this
    def get_static_names(self):
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
        labels = np.round(labels)
        bin_size = np.abs(np.min(labels) - np.max(labels)) / float(nr_of_bins)
        bins = np.arange(int(np.min(labels)) + bin_size, int(np.max(labels)), bin_size)
        binned_labels = np.digitize(labels, bins)
        return binned_labels, bins


sw = SlidingWindow()
sf_file = '../feature_extraction/data/static_features.csv'
sf = StaticFeatures(file_path=sf_file)
ds = Dataset()
df = ds.generate_dataset(sw, sf, 10)
df.to_csv(path_or_buf='./data.csv')
