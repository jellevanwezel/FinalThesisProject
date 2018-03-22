from collections import OrderedDict
import numpy as np

class FeatureLabels(object):
    acid = ('acid',['Zuur', 'Zwakzuur', 'Water'])
    ground_water = ('ground_water', ['Vrijdiep', 'Water', 'Zeerondiep', 'Ondiep', 'Diep'])
    stability = ('stability', ['Stabiel', 'Redelijkstabiel', 'Instabiel', 'Water'])
    ground_type = ('ground_type',['Zandenleem', 'Water', 'Veenenzand', 'Veen', 'Kleienzand', 'Leem', 'Zand'])
    pipe = ('pipe', ['coating','length'])

class FeatureMap(object):

    def __init__(self,feature_labels = []):
        self._fm = OrderedDict()
        for fl in feature_labels:
            self.add_group(*fl)

    def add_group(self,group_name,labels):
        self._fm[group_name] = OrderedDict()
        for label in labels: self._fm[group_name][label] = 0.0

    def set_feature(self,group,label,val):
        self._fm[group][label] = val

    def get_feature(self,group,label):
        return self._fm[group][label]

    def get_feature_list(self):
        features = list()
        labels = list()
        for gl,group in self._fm.items():
            for fl, val in group.items():
                features = features + [val]
                labels = labels + [fl]
        return np.array(features), labels

