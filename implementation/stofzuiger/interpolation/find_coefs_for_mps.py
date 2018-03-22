from database.db import DB
from database.kb_model import AreaModel
from interpolation.poly_cheb import PolyInterpolation
from statistics import stats
import numpy as np


class CoefsFinder(object):

    def __init__(self,xval='date_float', yval='mep_uit'):
        self.xval = xval
        self.yval = yval
        self.poly = PolyInterpolation()
        self.area_model = AreaModel()

    def find_coefs(self,N):
        nr_of_areas = self.area_model.get_number_of_areas()
        for area_idx in range(0,nr_of_areas):
            nr_of_mps = self.area_model.get_number_of_mps(area_idx)
            mp_coefs = np.zeros([nr_of_mps,N + 1])
            mp_coefs[:] = np.nan
            area_name = self.area_model.get_area_name(area_idx)
            for mp_idx in range(0,nr_of_mps):
                meas_df = self.area_model.get_mp_df(area_idx,mp_idx)
                meas_df = self.area_model.prepare_meas_df(meas_df,xval=self.xval,yval=self.yval);
                self._log_progress(area_idx, nr_of_areas, mp_idx,nr_of_mps, (meas_df is None))
                if meas_df is None: continue
                self.poly.set_t(np.array(meas_df['x']))
                self.poly.set_y(np.array(meas_df['y']))
                mp_coefs[mp_idx,:] = self.poly.find_coefs(N)
            np.savetxt('coefs/' + area_name + '2.csv', mp_coefs, delimiter=',')

    def _log_progress(self, area_idx, nr_of_areas, mp_idx,nr_of_mps, omitted):
        area_name = self.area_model.get_area_name(area_idx)
        logString = area_name + ": " + str(area_idx + 1) + "/" + str(nr_of_areas) + ", mp: " + str(
            mp_idx + 1) + "/" + str(nr_of_mps)
        if omitted: logString = logString + " - omitted, has too little measurements"
        print logString

cf = CoefsFinder()
cf.find_coefs(11)
