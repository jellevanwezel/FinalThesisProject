from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.pyplot import figure, plot, show,scatter,clf
from database.db import DB
import numpy as np
import pandas as pd

rootNumber = 0

stof = DB()
roots_df = stof.get_kb_roots()

forward = NavigationToolbar2.forward
previous = NavigationToolbar2.back

def next_button(self, *args, **kwargs):
    global rootNumber
    if rootNumber != roots_df.shape[0] - 1:
        rootNumber = rootNumber + 1
    show_plot(get_root_id(rootNumber))
    forward(self, *args, **kwargs)

def back_button(self, *args, **kwargs):
    global rootNumber
    if rootNumber != 0:
        rootNumber = rootNumber - 1
    show_plot(get_root_id(rootNumber))
    previous(self, *args, **kwargs)

def get_root_id(index):
    global roots_df
    root = roots_df.iloc[index]
    return root['id']

def show_plot(root_id):
    clf()
    mdf = stof.get_kb_measurements(root_id)
    print mdf['date'].shape
    print mdf['value'].shape
    print mdf['groundval'].shape
    mdf['date'] = mdf['date'].apply(lambda x: float(x.to_pydatetime().year) + float(x.to_pydatetime().month) / 13)
    scatter(mdf['date'], mdf['value'] - mdf['groundval'])
    show()

NavigationToolbar2.forward = next_button
NavigationToolbar2.back = back_button

mdf = stof.get_kb_measurements(get_root_id(rootNumber))
mdf['date'] = mdf['date'].apply(lambda x: float(x.to_pydatetime().year) + float(x.to_pydatetime().month)/13)
scatter(mdf['date'],mdf['value']- mdf['groundval'])
show()