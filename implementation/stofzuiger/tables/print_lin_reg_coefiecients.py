from matplotlib.backend_bases import NavigationToolbar2
from sklearn import linear_model

from database.db import DB
import numpy as np
import matplotlib.pyplot as plt
import statistics.regression as reg
import statistics.stats as stats

class KB_coef_printer:

    def __init__(self,xval='date_float'):
        self.xval = xval
        self.rootNumber = 0
        self.mpNumber = 0
        self.stof = DB()
        self.roots_df = self.stof.get_kb_roots()
        root_id = self.get_root_id(self.rootNumber)
        self.area_df = self.stof.get_kb_oodi_dd(root_id)
        self.meas_df = self.area_df[self.area_df.measurepoint_id == self.get_mp_ids()[0]]


    def get_root_id(self,index):
        root = self.roots_df.iloc[index]
        return root['id']

    def get_mp_ids(self):
        return self.area_df.measurepoint_id.unique()

    def get_area_name(self,index):
        root = self.roots_df.iloc[index]
        return root['area_name']

    def print_coefs(self):
        plt.clf()
        area_name = self.get_area_name(self.rootNumber)
        mp_name = str(self.get_mp_ids()[self.mpNumber])
        plt.suptitle(area_name + " - " + mp_name)
        self.sub_plot(221, "MEP-aan",self.meas_df[[self.xval,'mep_aan']],True,True,False,True)
        self.sub_plot(222, "MEP-uit", self.meas_df[[self.xval,'mep_uit']],True,True,False,True)
        self.sub_plot(223, "Diff", self.meas_df[[self.xval,'difference']],True,True,False,True)
        self.sub_plot(224, "I-Flens", self.meas_df[[self.xval,'iflens']],True,True,False,True)
        plt.show()


    def get_coefs(self,mdf):
        mdf.columns = ['x', 'y']
        reg = linear_model.LinearRegression()
        reg.fit(mdf['x'], mdf['y'])
        return reg.coef_



plotter = KB_plotter()
plotter.show_plot()