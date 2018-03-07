from database.kb_model import AreaModel
from interpolation.poly_cheb import PolyInterpolation
import numpy as np


class LOOCV:

    def __init__(self,xval='date_float', yval='mep_uit'):
        self.xval = xval
        self.yval = yval
        self.area_model = AreaModel()

    def _log_progress(self, area_idx, nr_of_areas, mp_idx,nr_of_mps, omitted):
        area_name = self.area_model.get_area_name(area_idx)
        logString = area_name + ": " + str(area_idx + 1) + "/" + str(nr_of_areas) + ", mp: " + str(
            mp_idx + 1) + "/" + str(nr_of_mps)
        if omitted: logString = logString + " - omitted, has too little measurements"
        print logString

    def save_errors(self, max_n,precision=2):
        polyInt = PolyInterpolation(precision=precision)
        nr_of_areas = self.area_model.get_number_of_areas()
        for area_idx in range(0, nr_of_areas):
            area_name = self.area_model.get_area_name(area_idx)
            nr_of_mps = self.area_model.get_number_of_mps(area_idx)
            e = np.zeros([nr_of_mps, max_n])
            for mp_idx in range(0,nr_of_mps):
                meas_df = self.area_model.get_mp_df(area_idx,mp_idx)
                meas_df = self.area_model.prepare_meas_df(meas_df)
                self._log_progress(area_idx, nr_of_areas, mp_idx,nr_of_mps, (meas_df is None))
                if meas_df is None: continue
                for meas_idx in range(0,meas_df.shape[0]):
                    polyInt.set_t(np.array(meas_df['x']))
                    polyInt.set_y(np.array(meas_df['y']))
                    testT = polyInt.t[meas_idx]
                    testY = polyInt.y[meas_idx]
                    polyInt.t = np.delete(polyInt.t, meas_idx)
                    polyInt.y = np.delete(polyInt.y, meas_idx)
                    for n in range(0, max_n):
                        coefs = polyInt.find_coefs(n)
                        tHat = polyInt.get_t_hat(precision=precision)
                        yHat = polyInt.get_y_hat(coefs, precision=precision)
                        yFit = np.interp(testT, tHat, yHat)
                        e[mp_idx, n] += np.abs(testY - yFit)
                e[mp_idx, :] = e[mp_idx, :] / float(meas_df.shape[0])
            np.savetxt('./results/' + area_name + '2.csv', e, delimiter=',')