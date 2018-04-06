import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os


class SaveStaticFeatures(object):
    # the feature names grouped
    area_feature_header = [
        ['area_name', 'measure_point_id'],
        ['acid_Zuur', 'acid_Zwakzuur', 'acid_Water'],
        ['ground_water_Vrijdiep', 'ground_water_Water', 'ground_water_Zeerondiep', 'ground_water_Ondiep',
         'ground_water_Diep'],
        ['stability_Stabiel', 'stability_Redelijkstabiel', 'stability_Instabiel', 'stability_Water'],
        ['ground_type_Zandenleem', 'ground_type_Water', 'ground_type_Veenenzand', 'ground_type_Veen',
         'ground_type_Kleienzand', 'ground_type_Leem', 'ground_type_Zand'],
        ['pce_coating_percentage'],
        ['total_pipe_lenght']
    ]

    @staticmethod
    def array_to_csv(feature_array, file_name):  # todo: to json
        """
        Saves the static features to a csv file
        :param feature_array: the list with the static features
        :param file_name: the desired filename
        :return:
        """
        filepath = os.path.dirname(os.path.abspath(__file__))
        name_path = filepath + '/data/' + file_name + '.csv'
        write_mode = 'r+' if os.path.exists(name_path) else 'w'
        with open(name_path, write_mode) as csv_file:
            csv_file.seek(0)
            csv_file.write(SaveStaticFeatures.area_features_header_to_string() + '\n')  # write the header
            for val in feature_array:
                csv_file.write(','.join(val) + '\n')  # write the values to csv
            csv_file.truncate()

    @staticmethod
    def area_features_header_to_string():
        """
        Creates the header string for the csv
        :return: the header string
        :rtype: str
        """
        out_arr = []
        for val in SaveStaticFeatures.area_feature_header:
            out_arr.append(",".join(val))
        return ",".join(out_arr)
