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
        self.stof = DB()
        self.roots_df = self.stof.get_kb_roots()
        NavigationToolbar2.forward = self.next_button
        NavigationToolbar2.back = self.back_button

    def next_button(self, *args, **kwargs):
        if self.rootNumber != self.roots_df.shape[0] - 1:
            self.rootNumber = self.rootNumber + 1
        self.show_plot()

    def back_button(self, *args, **kwargs):
        if self.rootNumber != 0:
            self.rootNumber = self.rootNumber - 1
        self.show_plot()

    def get_root_id(self,index):
        root = self.roots_df.iloc[index]
        return root['id']

    def get_area_name(self,index):
        root = self.roots_df.iloc[index]
        return root['area_name']

    def show_plot(self):
        plt.clf()
        root_id = self.get_root_id(self.rootNumber)
        area_name = self.get_area_name(self.rootNumber)
        mdf = self.stof.get_kb_oodi_dd(root_id)
        print mdf
        plt.suptitle(area_name)
        self.sub_plot(221, "MEP-aan",mdf[[self.xval,'mep_aan']],True,True,True,True)
        self.sub_plot(222, "MEP-uit", mdf[[self.xval,'mep_uit']],True,True,True,True)
        self.sub_plot(223, "Diff", mdf[[self.xval,'difference']],True,True,True,True)
        self.sub_plot(224, "I-Flens", mdf[[self.xval,'iflens']],True,True,False,True)
        plt.show()

    def sub_plot(self,loc, name, mdf,mean=False,std=False,sin=False,lin=False):
        mdf.columns = ['x', 'y']
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
        if lin: plt.plot(mdf['x'], reg.fit_lin(mdf[['x']], mdf['y']))


