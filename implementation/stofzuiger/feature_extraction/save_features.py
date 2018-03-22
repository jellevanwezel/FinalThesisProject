import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


class FeatureSaver(object):

    def __init__(self):
        self.area_feature = [
            ['area_name','measure_point_id'],
            ['acid_Zuur', 'acid_Zwakzuur', 'acid_Water'],
            ['ground_water_Vrijdiep', 'ground_water_Water', 'ground_water_Zeerondiep', 'ground_water_Ondiep', 'ground_water_Diep'],
            ['stability_Stabiel', 'stability_Redelijkstabiel', 'stability_Instabiel', 'stability_Water'],
            ['ground_type_Zandenleem', 'ground_type_Water', 'ground_type_Veenenzand', 'ground_type_Veen', 'ground_type_Kleienzand', 'ground_type_Leem', 'ground_type_Zand'],
            ['pce_coating_percentage'],
            ['total_pipe_lenght']
        ]

    def array_to_csv(self, feature_array, file_name):
        with open(file_name + '.csv', 'a') as csv_file:
            csv_file.write(self.area_features_to_string() + '\n')  # write the header
            for val in feature_array:
                csv_file.write(','.join(val) + '\n')  # write the values to csv

    def area_features_to_string(self):
        out_arr = []
        for val in self.area_feature:
            out_arr.append(",".join(val))
        return ",".join(out_arr)
