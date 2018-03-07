from database.db import DB
from database.kb_model import AreaModel
import numpy as np
from glvq import GlvqModel
import matplotlib.pyplot as plt

from interpolation.poly_cheb import PolyInterpolation


class LOOCV:

    def __init__(self,xval='date_float', yval='mep_uit'):
        self.xval = xval
        self.yval = yval
        self.area_model = AreaModel()
        self.polyInt = PolyInterpolation()

    def _log_progress(self, area_idx, nr_of_areas, mp_idx,nr_of_mps, omitted):
        area_name = self.area_model.get_area_name(area_idx)
        logString = area_name + ": " + str(area_idx + 1) + "/" + str(nr_of_areas) + ", mp: " + str(
            mp_idx + 1) + "/" + str(nr_of_mps)
        if omitted: logString = logString + " - omitted, has too little measurements"
        print logString

    def save_error_rates(self):
        nr_of_areas = self.area_model.get_number_of_areas()
        for area_idx in range(0,nr_of_areas):
            nr_of_mps = self.area_model.get_number_of_mps()
            for mp_idx in range(0,nr_of_mps):
                meas_df = self.area_model.get_mp_df(area_idx,mp_idx)
                meas_df = self.area_model.prepare_meas_df(meas_df)
                self._log_progress(area_idx, nr_of_areas, mp_idx,nr_of_mps,(meas_df==None))
                if meas_df == None: continue
                for loo_fold_idx in meas_df.shape[0]:
                    # create features
                    pass



                # polyInt.set_t(np.array(meas_df['x']))
                # polyInt.set_y(np.array(meas_df['y']))
                # testT = polyInt.t[meas_idx]
                # testY = polyInt.y[meas_idx]
                # polyInt.t = np.delete(polyInt.t, meas_idx)
                # polyInt.y = np.delete(polyInt.y, meas_idx)
                #
                #
                # glvq = GlvqModel()
                # glvq.fit(toy_data, toy_label)
                # pred = glvq.predict(toy_data)

    def create_features(self, meas_df, feature_size, nr_of_coefs, nr_of_bins):
        self.polyInt.set_t(np.array(meas_df['x']))
        self.polyInt.set_y(np.array(meas_df['y']))
        coefs = self.polyInt.find_coefs(nr_of_coefs)
        yHat = self.polyInt.get_y_hat(coefs)
        features = np.zeros([len(yHat) - feature_size,feature_size])
        labels = np.zeros([len(yHat) - (feature_size + 1)])
        for yHat_idx in range(0,len(yHat) - (feature_size + 1)):
            features[yHat_idx,:] = yHat[yHat_idx:yHat_idx+feature_size]
            labels[yHat_idx] = yHat[yHat_idx + feature_size]
        labels = np.round(labels)
        bin_size = int(np.floor(np.abs((np.min(labels) - np.max(labels)) / (nr_of_bins - 1))))
        bins = range(int(np.min(labels)), int(np.max(labels)), bin_size)
        binned_labels = np.digitize(labels,bins)
        return features, binned_labels, bins


am = AreaModel()
mp_df = am.get_mp_df(0,3)
mp_df = am.prepare_meas_df(mp_df)
loocv = LOOCV()
f, l, b = loocv.create_features(mp_df,5,10,20)

print l

print b

print np.unique(l)

#print str(np.min(l)) + " - " + str(np.max(l))
#print len(np.unique(l))