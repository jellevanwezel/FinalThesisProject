from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.pyplot import figure, plot, show,scatter,clf,title
from database.db import DB
import numpy as np
from sklearn import linear_model

rootNumber = 0

stof = DB()
roots_df = stof.get_kb_roots()

forward = NavigationToolbar2.forward
previous = NavigationToolbar2.back

def next_button(self, *args, **kwargs):
    global rootNumber
    if rootNumber != roots_df.shape[0] - 1:
        rootNumber = rootNumber + 1
    show_plot(get_root_id(rootNumber), get_area_name(rootNumber))
    forward(self, *args, **kwargs)

def back_button(self, *args, **kwargs):
    global rootNumber
    if rootNumber != 0:
        rootNumber = rootNumber - 1
    show_plot(get_root_id(rootNumber), get_area_name(rootNumber))
    previous(self, *args, **kwargs)

def get_root_id(index):
    global roots_df
    root = roots_df.iloc[index]
    return root['id']

def get_area_name(index):
    global roots_df
    root = roots_df.iloc[index]
    return root['area_name']

def regression(x,y):
    reg = linear_model.LinearRegression()
    reg.fit(x, y)
    return reg.predict(x)

def mean_var(x):
    return (np.mean(x),np.std(x))

def show_plot(root_id,area_name):
    clf()
    mdf = stof.get_kb_distances(root_id)
    scatter(mdf['distance'], mdf['value'])
    pred = regression(mdf[['distance']], mdf['value'])
    plot(mdf['distance'],pred)
    title(area_name)
    show()

NavigationToolbar2.forward = next_button
NavigationToolbar2.back = back_button

mdf = stof.get_kb_measurements(get_root_id(rootNumber))
show_plot(get_root_id(rootNumber),get_area_name(rootNumber))
show()