from database.db import DB
from interpolation.poly_func_class import PolyInterpolation
from statistics import stats
import numpy as np


class CoefsFinder:

    def __init__(self,xval='date_float', yval='mep_uit'):
        self.xval = xval
        self.yval = yval
        self.rootNumber = 0
        self.mpNumber = 0
        self.stof = DB()
        self.poly = PolyInterpolation()
        self.roots_df = self.stof.get_kb_roots()

    def get_root_id(self,index):
        root = self.roots_df.iloc[index]
        return root['id']

    def get_mp_ids(self,area_df):
        return area_df.measurepoint_id.unique()

    def get_area_name(self,index):
        root = self.roots_df.iloc[index]
        return root['area_name']

    def prepare_meas_df(self,meas_df):
        meas_df = meas_df[[self.xval, self.yval]]
        meas_df = meas_df.dropna()
        meas_df.columns = ['x', 'y']
        if (meas_df.shape[0] <= 2):
            return None
        (m, s) = stats.mean_std(meas_df['y'])
        meas_df = meas_df[meas_df.y < m + 2 * s]
        meas_df = meas_df[meas_df.y > m - 2 * s]
        if (meas_df.shape[0] <= 2):
            return None
        return meas_df

    def find_coefs(self,N):
        nr_of_areas = self.stof.get_kb_roots().shape[0]
        for area_idx in range(0,nr_of_areas):
            root_id = self.get_root_id(area_idx)
            area_df = self.stof.get_kb_oodi_dd(root_id)
            nr_of_mps = self.get_mp_ids(area_df).shape[0]
            mp_coefs = np.zeros([nr_of_mps,N + 1])
            mp_coefs[:] = np.nan
            area_name = self.get_area_name(area_idx)
            for mpoint_idx, mp_id in enumerate(self.get_mp_ids(area_df)):
                meas_df = area_df[area_df.measurepoint_id == mp_id]
                meas_df = self.prepare_meas_df(meas_df);
                if meas_df is None:
                    print area_name + ": " + str(area_idx + 1) + "/" + str(nr_of_areas) + ", mp: " + str(
                        mpoint_idx + 1) + "/" + str(nr_of_mps) + " - ommited, has too little measurements"
                    continue
                print area_name + ": " + str(area_idx + 1) + "/" + str(nr_of_areas) + ", mp: " + str(
                    mpoint_idx + 1) + "/" + str(nr_of_mps)
                self.poly.set_t(np.array(meas_df['x']))
                self.poly.set_y(np.array(meas_df['y']))
                mp_coefs[mpoint_idx,:] = self.poly.find_coefs(N)
            np.savetxt('coefs/' + area_name + '.csv', mp_coefs, delimiter=',')


cf = CoefsFinder()
cf.find_coefs(11)
