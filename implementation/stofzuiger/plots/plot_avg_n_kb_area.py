from matplotlib.backend_bases import NavigationToolbar2
from database.db import DB
import numpy as np
import matplotlib.pyplot as plt

from interpolation.poly_cheb import PolyInterpolation
from statistics import stats


class KB_plotter_avg_n(object):

    def __init__(self,xval='date_float', yval='mep_uit'):
        self.xval = xval
        self.yval = yval
        self.rootNumber = 0
        self.stof = DB()
        self.roots_df = self.stof.get_kb_roots()
        root_id = self.get_root_id(self.rootNumber)
        self.area_df = self.stof.get_kb_oodi_dd(root_id)
        NavigationToolbar2.forward = self.next_button_area
        NavigationToolbar2.back = self.back_button_area
        NavigationToolbar2.home = self.home_button

    def next_button_area(self, *args, **kwargs):
        if self.rootNumber != self.roots_df.shape[0] - 1:
            self.rootNumber = self.rootNumber + 1
            root_id = self.get_root_id(self.rootNumber)
            self.area_df = self.stof.get_kb_oodi_dd(root_id)
        #plt.clf()

    def back_button_area(self, *args, **kwargs):
        if self.rootNumber != 0:
            self.rootNumber = self.rootNumber - 1
            root_id = self.get_root_id(self.rootNumber)
            self.area_df = self.stof.get_kb_oodi_dd(root_id)
        #plt.clf()

    def home_button(self, *args, **kwargs):
        self.show_plot()

    def get_root_id(self,index):
        root = self.roots_df.iloc[index]
        return root['id']

    def get_mp_ids(self):
        return self.area_df.measurepoint_id.unique()

    def get_area_name(self,index):
        root = self.roots_df.iloc[index]
        return root['area_name']

    def save_errors(self):
        for rootIdx in range(0,self.roots_df.shape[0]):
            print "area: " + str(rootIdx) + "/" + str(self.roots_df.shape[0])
            rootId = self.get_root_id(rootIdx)
            self.area_df = self.stof.get_kb_oodi_dd(rootId)
            area_name = self.get_area_name(rootIdx)
            max_n = 50
            mpLen = len(self.get_mp_ids())
            e = np.zeros([mpLen, max_n])
            polyInt = PolyInterpolation(precision=2)
            for idx, mpid in enumerate(self.get_mp_ids()):
                meas_df = self.area_df[self.area_df.measurepoint_id == mpid]
                meas_df = meas_df[[self.xval, 'mep_uit']]
                meas_df = meas_df.dropna()
                meas_df.columns = ['x', 'y']
                if (meas_df.shape[0] <= 1):
                    continue
                (m, s) = stats.mean_std(meas_df['y'])
                meas_df = meas_df[meas_df.y < m + 2 * s]
                meas_df = meas_df[meas_df.y > m - 2 * s]
                polyInt.set_t(meas_df['x'])
                polyInt.set_y(meas_df['y'])
                for n in range(0, max_n):
                    coefs = polyInt.find_coefs(n)
                    e[idx, n] = polyInt.avg_dist_reg(coefs[0:n], precision=2)
                #e[idx, :] = (e[idx, :] - np.min(e[idx, :])) / (np.max(e[idx, :]) - np.min(e[idx, :]))
            np.savetxt(area_name + '.csv', e, delimiter=',')

    def save_errors_LOOCV(self):
        polyInt = PolyInterpolation(precision=2)
        for rootIdx in range(20, self.roots_df.shape[0]):
            print
            rootId = self.get_root_id(rootIdx)
            self.area_df = self.stof.get_kb_oodi_dd(rootId)
            area_name = self.get_area_name(rootIdx)
            max_n = 50
            mpLen = len(self.get_mp_ids())
            e = np.zeros([mpLen, max_n])
            for mpointIdx, mpid in enumerate(self.get_mp_ids()):
                meas_df = self.area_df[self.area_df.measurepoint_id == mpid]
                meas_df = meas_df[[self.xval, self.yval]]
                meas_df = meas_df.dropna()
                meas_df.columns = ['x', 'y']
                if (meas_df.shape[0] <= 2):
                    print area_name + ": " + str(rootIdx + 1) + "/" + str(self.roots_df.shape[0]) + ", mp: " + str(
                    mpointIdx + 1) + "/" + str(mpLen) + " - ommited, has too little measurements"
                    continue
                (m, s) = stats.mean_std(meas_df['y'])
                meas_df = meas_df[meas_df.y < m + 2 * s]
                meas_df = meas_df[meas_df.y > m - 2 * s]
                if (meas_df.shape[0] <= 2):
                    print area_name + ": " + str(rootIdx + 1) + "/" + str(self.roots_df.shape[0]) + ", mp: " + str(
                    mpointIdx + 1) + "/" + str(mpLen) + " - ommited, has too little measurements"
                    continue
                print area_name + ": " + str(rootIdx + 1) + "/" + str(self.roots_df.shape[0]) + ", mp: " + str(
                    mpointIdx + 1) + "/" + str(mpLen)
                measIdx = 0
                for test_row in meas_df.iterrows():
                    polyInt.set_t(np.array(meas_df['x']))
                    polyInt.set_y(np.array(meas_df['y']))
                    testT = polyInt.t[measIdx]
                    testY = np.array(polyInt.y)[measIdx]
                    polyInt.t = np.delete(polyInt.t, measIdx)
                    polyInt.y = np.delete(polyInt.y, measIdx)
                    for n in range(0, max_n):
                        coefs = polyInt.find_coefs(n)
                        p = float(10. ** -2)
                        yHat = polyInt.get_y_hat(coefs,precision=2)
                        yFit = np.interp(testT,np.arange(-1.0, 1. + p, p), yHat)
                        e[mpointIdx, n] += np.abs(testY - yFit)
                    measIdx += 1
                e[mpointIdx, :] = e[mpointIdx, :] / float(meas_df.shape[0])
            np.savetxt(area_name + '.csv', e, delimiter=',')


    def show_plot(self):
        #plt.clf()
        area_name = self.get_area_name(self.rootNumber)
        max_n = 25
        mpLen = len(self.get_mp_ids())
        e = np.zeros([mpLen,max_n])
        polyInt = PolyInterpolation(precision=2)
        for idx, mpid in enumerate(self.get_mp_ids()):
            print str(idx) + "/" + str(mpLen)
            meas_df = self.area_df[self.area_df.measurepoint_id == mpid]
            meas_df = meas_df[[self.xval, 'mep_uit']]
            meas_df = meas_df.dropna()
            meas_df.columns = ['x', 'y']
            if(meas_df.shape[0] <= 1):
                continue
            (m,s) = stats.mean_std(meas_df['y'])
            meas_df = meas_df[meas_df.y < m + 2 * s]
            meas_df = meas_df[meas_df.y > m - 2 * s]
            polyInt.set_t(meas_df['x'])
            polyInt.set_y(meas_df['y'])

            coefs = polyInt.find_coefs(max_n)
            for n in range(0,max_n):
                e[idx, n] = polyInt.avg_dist_reg(coefs[0:n],precision=2)
            e[idx,:]  = (e[idx,:] - np.min(e[idx,:])) / (np.max(e[idx,:]) - np.min(e[idx,:]))
            #plt.plot(range(0, max_n), e[idx,:])
        plt.plot(range(0, max_n), np.mean(e,axis=0))
        plt.title(area_name)
        plt.show()




plotter = KB_plotter_avg_n()
plotter.save_errors_LOOCV()