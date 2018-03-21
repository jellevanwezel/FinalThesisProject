import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


class FeatureSaver():

    def __init__(self):
        self.area_feature = [
            ['area_name','mp_id'],
            ['Zuur', 'Zwakzuur', 'Water'],
            ['Vrijdiep', 'Water', 'Zeerondiep', 'Ondiep', 'Diep'],
            ['Stabiel', 'Redelijkstabiel', 'Instabiel', 'Water'],
            ['Zandenleem', 'Water', 'Veenenzand', 'Veen', 'Kleienzand', 'Leem', 'Zand'],
            ['pce_coating'],
            ['pipe_lenght']
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
