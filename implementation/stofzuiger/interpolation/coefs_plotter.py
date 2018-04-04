from matplotlib.backend_bases import NavigationToolbar2
from database.db import DB
import numpy as np
import matplotlib.pyplot as plt

from interpolation.poly_cheb import PolyInterpolation
from statistics import stats


# todo: Refactor this to use the Model

class CoefsPlotter(object):
    def __init__(self, xval='date_float', yval='mep_uit'):
        self.xval = xval
        self.yval = yval
        self.rootNumber = 0
        self.mpNumber = 0
        self.stof = DB()
        self.roots_df = self.stof.get_kb_roots()
        root_id = self.get_root_id(self.rootNumber)
        self.area_df = self.stof.get_kb_oodi_dd(root_id)
        self.polyInt = PolyInterpolation(precision=3)
        self.area_df = self.stof.get_kb_oodi_dd(root_id)
        self.meas_df = self.area_df[self.area_df.measurepoint_id == self.get_mp_ids()[0]]
        self.meas_df = self.prepare_meas_df(self.meas_df)
        NavigationToolbar2.forward = self.next_button_area
        NavigationToolbar2.back = self.back_button_area
        NavigationToolbar2.forward_mp = self.next_button_mp
        NavigationToolbar2.back_mp = self.back_button_mp
        NavigationToolbar2.toolitems = NavigationToolbar2.toolitems + (
            ('Back mp', 'Back to  previous mp', 'back', 'back_mp'),
            ('Forward mp', 'Forward to next mp', 'forward', 'forward_mp')
        )
        plt.figure()
        plt.show()

    def next_button_area(self, *args, **kwargs):
        if self.rootNumber != self.roots_df.shape[0] - 1:
            self.rootNumber = self.rootNumber + 1
            root_id = self.get_root_id(self.rootNumber)
            self.area_df = self.stof.get_kb_oodi_dd(root_id)
            self.meas_df = self.area_df[self.area_df.measurepoint_id == self.get_mp_ids()[0]]
            self.meas_df = self.prepare_meas_df(self.meas_df)
            self.mpNumber = 0
        self.show_plot()

    def back_button_area(self, *args, **kwargs):
        if self.rootNumber != 0:
            self.rootNumber = self.rootNumber - 1
            root_id = self.get_root_id(self.rootNumber)
            self.area_df = self.stof.get_kb_oodi_dd(root_id)
            self.meas_df = self.area_df[self.area_df.measurepoint_id == self.get_mp_ids()[0]]
            self.meas_df = self.prepare_meas_df(self.meas_df)
            self.mpNumber = 0
        self.show_plot()

    def next_button_mp(self, *args, **kwargs):
        if self.mpNumber != self.get_mp_ids().shape[0] - 1:
            self.mpNumber = self.mpNumber + 1
            mpid = self.get_mp_ids()[self.mpNumber]
            self.meas_df = self.area_df[self.area_df.measurepoint_id == mpid]
            self.meas_df = self.prepare_meas_df(self.meas_df)
        self.show_plot()

    def back_button_mp(self, *args, **kwargs):
        if self.mpNumber != 0:
            self.mpNumber = self.mpNumber - 1
            mpid = self.get_mp_ids()[self.mpNumber]
            self.meas_df = self.area_df[self.area_df.measurepoint_id == mpid]
            self.meas_df = self.prepare_meas_df(self.meas_df)
        self.show_plot()

    def get_root_id(self, index):
        root = self.roots_df.iloc[index]
        return root['id']

    def get_mp_ids(self):
        return self.area_df.measurepoint_id.unique()

    def get_area_name(self, index):
        root = self.roots_df.iloc[index]
        return root['area_name']

    def get_number_of_mps(self):
        return self.get_mp_ids().shape[0]

    def get_number_of_areas(self):
        return self.roots_df.shape[0]

    def prepare_meas_df(self, meas_df):
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

    def show_plot(self):
        plt.clf()
        if self.meas_df is None:
            print 'Not enough points'
            return
        area_name = self.get_area_name(self.rootNumber)
        self.polyInt.set_t(np.array(self.meas_df['x']))
        self.polyInt.set_y(np.array(self.meas_df['y']))
        coefs = self.polyInt.find_coefs(10)
        yHat = self.polyInt.get_y_hat_for_range(coefs, np.arange(-1, 1, 0.04))
        tHat = np.arange(-1, 1, 0.04)
        t = self.polyInt.t
        y = self.polyInt.y
        t_sorted, y_sorted = zip(*sorted(zip(t, y), key=lambda x: x[0]))
        plt.plot(t_sorted, y_sorted)
        plt.plot(tHat, yHat)
        area_title = area_name + ": " + str(self.rootNumber + 1) + "/" + str(self.get_number_of_areas())
        mp_title = "mp: " + str(self.mpNumber + 1) + "/" + str(self.get_number_of_mps())
        plt.title(area_title + " " + mp_title)
        plt.draw()


plotter = CoefsPlotter()
plotter.show_plot()
