import sys
from collections import defaultdict, Counter, OrderedDict
from pprint import pprint

import time

import sklearn
from sklearn.model_selection import KFold

from database.kb_model import AreaModel
import numpy as np
import glvq

from feature_extraction.sliding_window import SlidingWindow
from interpolation.poly_cheb import PolyInterpolation

import matplotlib.pyplot as plt

from statistics import stats


class LOOCV:

    def __init__(self,xval='date_float', yval='mep_uit',feature_size=5,nr_of_coefs=10,nr_of_bins=10,
                 nr_of_samples=30,gradients=False, nr_of_folds=2, lvq_model=glvq.GlvqModel,):
        self.xval = xval
        self.yval = yval
        self.nr_of_folds = nr_of_folds
        self.gradients = gradients
        self.nr_of_samples = nr_of_samples
        self.feature_size=feature_size
        self.nr_of_coefs=nr_of_coefs
        self.nr_of_bins=nr_of_bins
        self.area_model = AreaModel()
        self.polyInt = PolyInterpolation()
        self.feature_ext = SlidingWindow(feature_size,nr_of_coefs,nr_of_bins,nr_of_samples)
        self.lvq_model = lvq_model
        print " --- Config --- "
        for key,val in self.__dict__.items(): print str(key) + ": " + str(val)
        print

    def _log_progress(self, area_idx, nr_of_areas, mp_idx,nr_of_mps, omitted):
        area_name = self.area_model.get_area_name(area_idx)
        logString = area_name + ": " + str(area_idx + 1) + "/" + str(nr_of_areas) + ", mp: " + str(
            mp_idx + 1) + "/" + str(nr_of_mps)
        if omitted: logString = logString + " - omitted, has too little measurements"
        print logString

    def cross_validate_per_mp(self):
        nr_of_areas = self.area_model.get_number_of_areas()
        plt.figure()
        for area_idx in range(0,nr_of_areas):
            nr_of_mps = self.area_model.get_number_of_mps(area_idx)
            for mp_idx in range(2,nr_of_mps):
                meas_df = self.area_model.get_mp_df(area_idx,mp_idx)
                meas_df = self.area_model.prepare_meas_df(meas_df)
                self._log_progress(area_idx, nr_of_areas, mp_idx,nr_of_mps,(meas_df is None))
                if meas_df is None: continue
                print meas_df
                features, labels, labels_gradients = self.feature_ext.create_features_labels(meas_df)
                if self.gradients:labels = labels_gradients
                binned_labels, bins = self.feature_ext.bin_labels(labels,self.nr_of_bins)
                #self.n_fold(self.nr_of_folds, features, binned_labels, self.nr_of_bins)

    def cross_validate_per_area(self):
        nr_of_areas = self.area_model.get_number_of_areas()



        for area_idx in range(0,nr_of_areas):
            print self.area_model.get_area_name(area_idx) + " " + str(area_idx + 1) + "/" + str(nr_of_areas)
            nr_of_mps = self.area_model.get_number_of_mps(area_idx)
            area_features = np.array([]).reshape(0,self.feature_size)
            area_labels = np.array([])
            for mp_idx in range(0,nr_of_mps):
                meas_df = self.area_model.get_mp_df(area_idx,mp_idx)
                meas_df = self.area_model.prepare_meas_df(meas_df)
                if meas_df is None: continue
                features, labels, labels_gradients = self.feature_ext.create_features_labels(meas_df)
                if self.gradients:labels = labels_gradients

                #concatinate the extracted features with the sliding window features

                area_features = np.concatenate((area_features,features),axis=0)
                area_labels = np.concatenate((area_labels,labels),axis=0)
            if len(area_features) == 0:
                print "Skipped, no datapoints"
                continue
            binned_labels, bins = self.feature_ext.bin_labels(area_labels, self.nr_of_bins)
            nr_of_folds = area_features.shape[0]
            self.n_fold(nr_of_folds, area_features, binned_labels)

    def cross_validate_all(self):
        nr_of_areas = self.area_model.get_number_of_areas()
        all_features = np.array([]).reshape(0, self.feature_size)
        all_labels = np.array([])

        mp_features = np.genfromtxt('../feature_extraction/feature_test.csv', dtype=None, delimiter=',', skip_header=0)
        mp_features = mp_features[1:,:]

        for area_idx in range(0,nr_of_areas):
            nr_of_mps = self.area_model.get_number_of_mps(area_idx)
            for mp_idx in range(0,nr_of_mps):
                meas_df = self.area_model.get_mp_df(area_idx,mp_idx)
                meas_id = meas_df.measurepoint_id.values[0]
                meas_df = self.area_model.prepare_meas_df(meas_df)
                if meas_df is None: continue
                static_features = np.where(np.array(mp_features[:, 1]) == meas_id)
                features, labels, labels_gradients = self.feature_ext.create_features_labels(meas_df)
                features = np.concatenate((features, np.tile(static_features,(features.shape[0],1))),axis=1)
                if self.gradients:labels = labels_gradients
                all_features = np.concatenate((all_features,features),axis=0)
                all_labels = np.concatenate((all_labels,labels),axis=0)
        binned_labels, bins = self.feature_ext.bin_labels(all_labels, self.nr_of_bins)
        self.n_fold(self.nr_of_folds, all_features, binned_labels,log_pregress=True)

    def _log_n_fold_progress(self,fold,nr_of_folds, start_time):
        unit = "s"
        time_elapsed = int(time.time() - start_time)
        if time_elapsed > 60 : unit = "m"; time_elapsed = int(time_elapsed/60)
        if time_elapsed > 60 : unit = "h"; time_elapsed = np.round(time_elapsed/60.,1)
        sys.stdout.write('\rFold: ' + str(fold + 1) + "/" + str(nr_of_folds) + " in: " + str(time_elapsed) + unit)

    def _log_n_fold_errors(self,errors):
        print " --- Errors ---"
        for key, val in OrderedDict(sorted(errors.items())).items():
            print "[" + str(key) + ": " + str(val) + "]",
        else:
            print
        print "error-rate: " + str(round(1 - (errors[0] / float(errors['total_validations'])), 4))

    def _predict_lvq(self,train_data,train_labels,test_data,test_labels):
        lvq_model = self.lvq_model()
        lvq_model.fit(train_data, train_labels)
        pred_labels = lvq_model.predict(test_data)
        return test_labels - pred_labels


    def n_fold(self,nr_of_folds,features,labels,log_pregress=False,log_errors=True):
        kfold =  KFold(n_splits=nr_of_folds, shuffle=True)
        error_dict = Counter({}) #Counter dict, values start at 0 and can be added.
        if log_pregress:
            print " --- Progress --- "
            start_time = time.time()
        for fold_idx, (train_idx, test_idx) in zip(range(nr_of_folds),kfold.split(features)):
            if log_pregress: self._log_n_fold_progress(fold_idx,nr_of_folds,start_time)
            test_data, test_labels, train_data, train_labels = self.get_fold(test_idx,train_idx,features,labels)
            error_dists = self._predict_lvq(train_data,train_labels,test_data,test_labels)
            values, counts = np.unique(error_dists, return_counts=True)
            error_dict += Counter(dict(zip(values,counts)))
            error_dict['total_validations'] += len(test_idx)
        if log_pregress: print; print
        if log_errors: self._log_n_fold_errors(error_dict)

    def get_fold(self,test_fold,train_fold,data,labels):
        test_data = data[test_fold, :]
        test_label = labels[test_fold]
        train_data = data[train_fold, :]
        train_label = labels[train_fold]
        return test_data,test_label,train_data,train_label

loocv = LOOCV(lvq_model=glvq.GmlvqModel)
loocv.cross_validate_all()