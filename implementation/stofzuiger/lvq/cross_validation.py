import sys

from database.db import DB
from database.kb_model import AreaModel
import numpy as np
from glvq import GlvqModel
import matplotlib.pyplot as plt

from interpolation.poly_cheb import PolyInterpolation


class LOOCV:

    def __init__(self,xval='date_float', yval='mep_uit',feature_size=5,nr_of_coefs=10,nr_of_bins=20 ):
        self.xval = xval
        self.yval = yval
        self.feature_size=feature_size
        self.nr_of_coefs=nr_of_coefs
        self.nr_of_bins=nr_of_bins
        self.area_model = AreaModel()
        self.polyInt = PolyInterpolation()

    def _log_progress(self, area_idx, nr_of_areas, mp_idx,nr_of_mps, omitted):
        area_name = self.area_model.get_area_name(area_idx)
        logString = area_name + ": " + str(area_idx + 1) + "/" + str(nr_of_areas) + ", mp: " + str(
            mp_idx + 1) + "/" + str(nr_of_mps)
        if omitted: logString = logString + " - omitted, has too little measurements"
        print logString

    def cross_validate_per_mp(self):
        nr_of_areas = self.area_model.get_number_of_areas()
        for area_idx in range(0,nr_of_areas):
            nr_of_mps = self.area_model.get_number_of_mps(area_idx)
            for mp_idx in range(0,nr_of_mps):
                meas_df = self.area_model.get_mp_df(area_idx,mp_idx)
                meas_df = self.area_model.prepare_meas_df(meas_df)
                self._log_progress(area_idx, nr_of_areas, mp_idx,nr_of_mps,(meas_df is None))
                if meas_df is None: continue
                features, binned_labels, bins = self.create_features(
                    meas_df, self.feature_size, self.nr_of_coefs, self.nr_of_bins
                )
                errors = 0;
                nr_of_folds = features.shape[0]
                for fold_idx in range(0,nr_of_folds):
                    sys.stdout.write('\r' + "mp progress " + str(int((fold_idx + 1) / float(nr_of_folds) * 100)) + "%")
                    test_data = features[fold_idx, :]
                    test_label = binned_labels[fold_idx]
                    train_data = np.delete(features,fold_idx,0)
                    train_label = np.delete(binned_labels,fold_idx)
                    glvq_model = GlvqModel()
                    glvq_model.fit(train_data,train_label)
                    pred_label = glvq_model.predict([test_data])
                    if pred_label[0] != test_label: errors += 1
                print
                print str(errors) + "/" + str(nr_of_folds) + ", " + str(float(errors)/float(nr_of_folds))


    def create_features(self, meas_df, feature_size, nr_of_coefs, nr_of_bins):
        self.polyInt.set_t(np.array(meas_df['x']))
        self.polyInt.set_y(np.array(meas_df['y']))
        coefs = self.polyInt.find_coefs(nr_of_coefs)
        yHat = self.polyInt.get_y_hat(coefs)
        features = np.zeros([len(yHat) - (feature_size + 1),feature_size])
        labels = np.zeros([len(yHat) - (feature_size + 1)])
        for yHat_idx in range(0,len(yHat) - (feature_size + 1)):
            features[yHat_idx,:] = yHat[yHat_idx:yHat_idx+feature_size]
            labels[yHat_idx] = yHat[yHat_idx + feature_size]
        labels = np.round(labels)
        bin_size = int(np.floor(np.abs((np.min(labels) - np.max(labels)) / (nr_of_bins - 1))))
        bins = range(int(np.min(labels)), int(np.max(labels)), bin_size)
        binned_labels = np.digitize(labels,bins)
        return features, binned_labels, bins

loocv = LOOCV()
loocv.cross_validate_per_mp()