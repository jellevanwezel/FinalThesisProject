import numpy as np
from database.kb_model import AreaModel
from interpolation.poly_cheb import PolyInterpolation
import matplotlib.pyplot as plt


class SlidingWindow(object):

    def __init__(self,feature_size=10,nr_of_coefs=10,nr_of_bins=6,nr_of_samples=50, omit_first_coef=True):
        self.nr_of_samples = nr_of_samples
        self.omit_first_coef = omit_first_coef
        self.feature_size=feature_size
        self.nr_of_coefs=nr_of_coefs
        self.nr_of_bins=nr_of_bins
        self.area_model = AreaModel()
        self.polyInt = PolyInterpolation()

    # todo: refactor
    def create_features_labels(self, meas_df):
        t = np.array(meas_df['x'])
        y = np.array(meas_df['y'])
        self.polyInt.set_t_y(t,y)
        coefs = self.polyInt.find_coefs(self.nr_of_coefs)
        if self.omit_first_coef:coefs[0] = 0
        x = np.arange(-1,1,(2./self.nr_of_samples)) # todo: fix magic numbers and range here is weird
        yHat = self.polyInt.get_y_hat_for_range(coefs,x)
        self.polyInt.save_chebs_to_file()  # save chebs to file for future use
        features = np.zeros([len(yHat) - (self.feature_size + 1),self.feature_size])
        labels = np.zeros([len(yHat) - (self.feature_size + 1)])
        labels_gradients = np.zeros([len(yHat) - (self.feature_size + 1)])
        for yHat_idx in range(0,len(yHat) - (self.feature_size + 1)):
            features[yHat_idx,:] = yHat[yHat_idx:yHat_idx+self.feature_size]
            labels[yHat_idx] = yHat[yHat_idx + self.feature_size]
            xy_idx = yHat_idx + (self.feature_size - 1)
            dy = yHat[xy_idx] - yHat[xy_idx + 1]
            dx = x[xy_idx] - x[xy_idx + 1]
            labels_gradients[yHat_idx] = float(dy) / float(dx) # dy/dx todo:  error-rates are high, fix
        return features, labels, labels_gradients

    def bin_labels(self, labels, nr_of_bins):
        labels = np.round(labels)
        bin_size = np.abs(np.min(labels) - np.max(labels)) / float(nr_of_bins)
        bins = np.arange(int(np.min(labels)) + bin_size, int(np.max(labels)), bin_size)
        binned_labels = np.digitize(labels,bins)
        return binned_labels, bins