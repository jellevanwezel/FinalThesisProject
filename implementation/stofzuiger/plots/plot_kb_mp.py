from matplotlib.backend_bases import NavigationToolbar2
from database.db import DB
import numpy as np
import matplotlib.pyplot as plt
import statistics.regression as reg
import statistics.stats as stats

class KB_plotter(object):

    def __init__(self,xval='date_float'):
        self.xval = xval
        self.rootNumber = 0
        self.mpNumber = 0
        self.stof = DB()
        self.roots_df = self.stof.get_kb_roots()
        root_id = self.get_root_id(self.rootNumber)
        self.area_df = self.stof.get_kb_oodi_dd(root_id)
        self.meas_df = self.area_df[self.area_df.measurepoint_id == self.get_mp_ids()[0]]
        NavigationToolbar2.forward = self.next_button_area
        NavigationToolbar2.back = self.back_button_area
        NavigationToolbar2.forward_mp = self.next_button_mp
        NavigationToolbar2.back_mp = self.back_button_mp
        NavigationToolbar2.toolitems = NavigationToolbar2.toolitems + (
            ('Back mp', 'Back to  previous mp', 'back', 'back_mp'),
            ('Forward mp', 'Forward to next mp', 'forward', 'forward_mp')
        )

    def next_button_area(self, *args, **kwargs):
        if self.rootNumber != self.roots_df.shape[0] - 1:
            self.rootNumber = self.rootNumber + 1
            root_id = self.get_root_id(self.rootNumber)
            self.area_df = self.stof.get_kb_oodi_dd(root_id)
            self.meas_df = self.area_df[self.area_df.measurepoint_id == self.get_mp_ids()[0]]
            self.mpNumber = 0
        self.show_plot()

    def back_button_area(self, *args, **kwargs):
        if self.rootNumber != 0:
            self.rootNumber = self.rootNumber - 1
            root_id = self.get_root_id(self.rootNumber)
            self.area_df = self.stof.get_kb_oodi_dd(root_id)
            self.meas_df = self.area_df[self.area_df.measurepoint_id == self.get_mp_ids()[0]]
            self.mpNumber = 0
        self.show_plot()


    def next_button_mp(self, *args, **kwargs):
        if self.mpNumber != self.get_mp_ids().shape[0] - 1:
            self.mpNumber = self.mpNumber + 1
            mpid = self.get_mp_ids()[self.mpNumber]
            self.meas_df = self.area_df[self.area_df.measurepoint_id == mpid]
        self.show_plot()

    def back_button_mp(self, *args, **kwargs):
        if self.mpNumber != 0:
            self.mpNumber = self.mpNumber - 1
            mpid = self.get_mp_ids()[self.mpNumber]
            self.meas_df = self.area_df[self.area_df.measurepoint_id == mpid]
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
        print self.meas_df['date_float'] - np.min(self.meas_df['date_float'])
        print self.meas_df['mep_uit']
        area_name = self.get_area_name(self.rootNumber)
        mp_name = str(self.get_mp_ids()[self.mpNumber])
        plt.suptitle(area_name + " - " + mp_name)
        self.sub_plot(221, "MEP-aan",self.meas_df[[self.xval,'mep_aan']],True,True,False,True)
        self.sub_plot(222, "MEP-uit", self.meas_df[[self.xval,'mep_uit']],True,True,False,True)
        self.sub_plot(223, "Diff", self.meas_df[[self.xval,'difference']],True,True,False,True)
        self.sub_plot(224, "I-Flens", self.meas_df[[self.xval,'iflens']],True,True,False,True)
        plt.show()

    def sub_plot(self,loc, name, mdf,mean=False,std=False,sin=False,lin=False):
        mdf.columns = ['x', 'y']
        if(mdf['y'].isnull().all()):
            return
        (m,s) = stats.mean_std(mdf['y'])
        mdf = mdf[mdf.y < m + 2 * s]
        mdf = mdf[mdf.y > m - 2 * s]
        (m, s) = stats.mean_std(mdf['y'])
        plt.subplot(loc)
        plt.title(name)
        plt.scatter(mdf['x'],mdf['y'])
        if mean: plt.plot([np.min(mdf['x']),np.max(mdf['x'])],[m,m],'g--')
        if std:
            plt.plot([np.min(mdf['x']),np.max(mdf['x'])],[m + s,m + s],'r:')
            plt.plot([np.min(mdf['x']), np.max(mdf['x'])], [m - s, m - s],'r:')

        if sin:
            ls = np.linspace(np.min(mdf['x']), np.max(mdf['x']), 100)
            sin_pred = reg.fit_sin(mdf['x'], mdf['y'])
            plt.plot(ls,sin_pred['fitfunc'](ls))
        if lin:
            try:
                pred = reg.fit_lin(mdf[['x']], mdf['y'])
                plt.plot(mdf['x'], pred)
            except:
                return




plotter = KB_plotter()
plotter.show_plot()