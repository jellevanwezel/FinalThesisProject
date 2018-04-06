from collections import OrderedDict
import numpy as np


class FeatureLabels(object):
    acid = ('acid', ['Zuur', 'Zwakzuur', 'Water'])
    ground_water = ('ground_water', ['Vrijdiep', 'Water', 'Zeerondiep', 'Ondiep', 'Diep'])
    stability = ('stability', ['Stabiel', 'Redelijkstabiel', 'Instabiel', 'Water'])
    ground_type = ('ground_type', ['Zandenleem', 'Water', 'Veenenzand', 'Veen', 'Kleienzand', 'Leem', 'Zand'])
    pipe = ('pipe', ['coating', 'length'])
    groups = ['acid', 'ground_water', 'stability', 'ground_type']


class FeatureMap(object):
    def __init__(self, feature_labels=[]):
        self._fm = OrderedDict()
        for fl in feature_labels:
            self.add_group(*fl)

    def add_group(self, group_name, labels):
        """
        Add a feature group the the map
        :param group_name: name for this group
        :param labels: labels in this group
        :return:
        """
        self._fm[group_name] = OrderedDict()
        for label in labels: self._fm[group_name][label] = 0.0

    def set_feature(self, group, label, val):
        """
        Sets a feature value for the given group and label
        :param group: group name
        :param label: label name
        :param val: the value to be set
        :return:
        """
        self._fm[group][label] = val

    def get_feature(self, group, label):
        """
        Gets a feature from a group and label
        :param group: group name
        :param label: label name
        :return: the requsted value
        """
        return self._fm[group][label]

    def get_feature_list(self):
        """
        Converts the feature map to a list
        :return: numpy.array, list
        """
        features = list()
        labels = list()
        for gl, group in self._fm.items():
            for fl, val in group.items():
                features = features + [val]
                labels = labels + [fl]
        return np.array(features), labels
