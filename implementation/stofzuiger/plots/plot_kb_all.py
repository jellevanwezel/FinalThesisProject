from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.pyplot import figure, plot, show,scatter,clf,title
from database.db import DB
import numpy as np
from sklearn import linear_model
import scipy

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

def fit_sin(tt, yy):
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])
    def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

def mean_var(x):
    return (np.mean(x),np.std(x))

def show_plot(root_id,area_name):
    clf()
    mdf = stof.get_kb_measurements(root_id)
    mdf['date'] = mdf['date'].apply(lambda x: float(x.to_pydatetime().year) + float(x.to_pydatetime().month) / 13)
    #mdf['date'] = mdf['date'].apply(lambda x: x - np.min(mdf['date']))
    (avg,std) = mean_var(mdf['value'])
    mdf = mdf[mdf.value < avg + 2 * std]
    mdf = mdf[mdf.value > avg - 2 * std]
    pred = regression(mdf[['date']], mdf['value'])
    #pred_sin = fit_sin(mdf['date'], mdf['value'])
    scatter(mdf['date'], mdf['value'])
    #plot([np.min(mdf['date']),np.max(mdf['date'])],[avg,avg],'g--')
    #x = np.linspace(np.min(mdf['date']),np.max(mdf['date']),100)
    #plot(x,pred_sin['fitfunc'](x))
    #plot([np.min(mdf['date']), np.max(mdf['date'])], [avg - 2 * std, avg - 2 * std],'r:')
    #plot([np.min(mdf['date']), np.max(mdf['date'])], [avg + 2 * std, avg + 2 * std],'r:')
    plot(mdf['date'],pred)
    title(area_name + " - measurements")
    show()

NavigationToolbar2.forward = next_button
NavigationToolbar2.back = back_button

mdf = stof.get_kb_measurements(get_root_id(rootNumber))
show_plot(get_root_id(rootNumber),get_area_name(rootNumber))
show()