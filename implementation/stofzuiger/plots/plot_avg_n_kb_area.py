from matplotlib.backend_bases import NavigationToolbar2
from database.db import DB
import numpy as np
import matplotlib.pyplot as plt

from interpolation.poly_func_class import PolyInterpolation
from statistics import stats


class KB_plotter_avg_n:

    def __init__(self,xval='date_float'):
        self.xval = xval
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
        plt.clf()

    def back_button_area(self, *args, **kwargs):
        if self.rootNumber != 0:
            self.rootNumber = self.rootNumber - 1
            root_id = self.get_root_id(self.rootNumber)
            self.area_df = self.stof.get_kb_oodi_dd(root_id)
        plt.clf()

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

    def show_plot(self):
        plt.clf()
        area_name = self.get_area_name(self.rootNumber)
        max_n = 10
        mpLen = len(self.get_mp_ids())
        e = np.zeros([mpLen,max_n])
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
            t = meas_df['x']
            y = meas_df['y']
            polyInt = PolyInterpolation(t, y)
            for n in range(0,max_n):
                coefs = polyInt.find_coefs(n)
                dist = polyInt.avg_dist_reg(coefs, 10000)
                e[idx,n] = dist
            e[idx,:]  = (e[idx,:] - np.min(e[idx,:])) / (np.max(e[idx,:]) - np.min(e[idx,:]))
            #plt.plot(range(0, max_n), e[idx,:])
        plt.plot(range(0, max_n), np.mean(e,axis=0))
        plt.title(area_name)
        plt.show()




plotter = KB_plotter_avg_n()
plotter.show_plot()