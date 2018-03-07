from database.db import DB
from interpolation.poly_func_class import PolyInterpolation
from statistics import stats
import numpy as np


class LOOCV:

    def __init__(self,xval='date_float', yval='mep_uit'):
        self.xval = xval
        self.yval = yval
        self.rootNumber = 0
        self.stof = DB()
        self.roots_df = self.stof.get_kb_roots()
        root_id = self.get_root_id(self.rootNumber)
        self.area_df = self.stof.get_kb_oodi_dd(root_id)

    def get_area_name(self,index):
        root = self.roots_df.iloc[index]
        return root['area_name']

    def get_mp_ids(self):
        return self.area_df.measurepoint_id.unique()

    def get_root_id(self,index):
        root = self.roots_df.iloc[index]
        return root['id']

    def save_errors(self):
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
                print area_name + ": " + str(rootIdx + 1) + "/" + str(self.roots_df.shape[0]) + ", mp: " + str(
                    mpointIdx + 1) + "/" + str(mpLen)
                meas_df = self.area_df[self.area_df.measurepoint_id == mpid]
                meas_df = meas_df[[self.xval, self.yval]]
                meas_df = meas_df.dropna()
                meas_df.columns = ['x', 'y']
                if (meas_df.shape[0] <= 2):
                    print area_name + ": " + str(rootIdx + 1) + "/" + str(self.roots_df.shape[0]) + ", mp: " + str(
                    mpointIdx + 1) + "/" + str(mpLen) + " - ommited, has to little measurements"
                    continue
                (m, s) = stats.mean_std(meas_df['y'])
                meas_df = meas_df[meas_df.y < m + 2 * s]
                meas_df = meas_df[meas_df.y > m - 2 * s]
                if (meas_df.shape[0] <= 2):
                    print area_name + ": " + str(rootIdx + 1) + "/" + str(self.roots_df.shape[0]) + ", mp: " + str(
                    mpointIdx + 1) + "/" + str(mpLen) + " - ommited, has to little measurements"
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
                        yHat = polyInt.get_y_hat(coefs, precision=2)
                        yFit = np.interp(testT, np.arange(-1.0, 1. + p, p), yHat)
                        e[mpointIdx, n] += np.abs(testY - yFit)
                    measIdx += 1
                e[mpointIdx, :] = e[mpointIdx, :] / float(meas_df.shape[0])
            np.savetxt('./results/' + area_name + '.csv', e, delimiter=',')