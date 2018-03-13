import json

import numpy as np
import matplotlib.pyplot as plt
import os

from statistics import stats


class PolyInterpolation:

    def __init__(self,precision=6):
        self.precision = precision
        self.chebs = dict()
        self.data_path = os.path.dirname(os.path.realpath(__file__)) + "/data/"
        self.chebs_file_name = 'chebs.json'
        self.load_chebs_from_file()


    def set_t(self,t):
        self.t = stats.normalize(t) * 2 - 1  # rescale between -1 and 1

    def set_y(self,y):
        self.y = y

    def set_t_y(self,t,y):
        t = stats.normalize(t) * 2 - 1
        self.y = y
        self.t, self.y = zip(*sorted(zip(t, y))) #sort on x

    def cheb(self,n, x):
        if (n == 0): return 1.;  # first defenition
        if (n == 1): return float(x);  # second defenition
        if self.chebs.get(n) != None:  # if the n is stored, find the x
            nCheb = self.chebs.get(n)
            if nCheb.get(round(x, self.precision)) != None:  # if the x is stored, return the x
                return nCheb.get(round(x, self.precision))
            nCheb[round(x, self.precision)] = 2. * x * self.cheb(n - 1, x) - self.cheb(n - 2, x)  # x not stored, create it
        else:
            self.chebs[n] = {
                round(x, self.precision): 2. * x * self.cheb(n - 1, x) - self.cheb(n - 2,x)
                }  # n not stored create it, with this value for x
            nCheb = self.chebs.get(n)
        return nCheb.get(round(x, self.precision))  # return the created value of for n,x

    def find_coefs(self,n):
        coefs = np.empty([n+1])
        for k in range(0, n+1):
            ratio = 2. / float(n + 1)
            sum = 0.
            for l in range(0, n+1):
                tl = np.cos((float(l) + .5) * (np.pi / float(n + 1)))
                sum += np.interp(tl, self.t, self.y) * self.cheb(k, tl)
            coefs[k] = ratio * float(sum)
        coefs[0] = coefs[0] / 2. # todo: first coef is a factor 2 off. find out why
        return coefs

    def get_y_hat(self,coefs,precision=3):
        p = float(10. ** -precision)
        yHat = np.empty([2 * (10 ** precision) + 1])
        i = 0
        for tx in np.arange(-1.0, 1. + p, p):
            sum = 0.
            for k in range(0, len(coefs)):
                sum += coefs[k] * self.cheb(k, tx)
            yHat[i] = sum
            i += 1
        return yHat

    def get_y_hat_for_range(self,coefs,np_range):
        # todo: say it should be always scaled between -1 and 1, or just do the rescale
        yHat = np.empty([len(np_range)])
        for idx,tx in enumerate(np_range):
            sum = 0.
            for k in range(0, len(coefs)):
                sum += coefs[k] * self.cheb(k, tx)
            yHat[idx] = sum
            idx += 1
        return yHat

    def plot_y_hat(self,coefs,precision=3):
        p = float(10. ** -precision)
        yHat = self.get_y_hat(coefs,precision)
        plt.plot(np.arange(-1.0, 1. + p,p), yHat)
        plt.plot(self.t, self.y)
        plt.show()

    def get_t_hat(self,precision=3):
        p = float(10. ** -precision)
        return np.arange(-1.0, 1.0 + p,p)

    def r_squared(self,coefs,precision=3):
        i = 0
        yHat = self.get_y_hat(coefs,precision)
        p = float(10. ** -precision)
        y = np.empty([2 * (10 ** precision) + 1])
        for tx in np.arange(-1.0, 1. + p, p):
            y[i] = np.interp(tx, self.t, self.y)
            i += 1
        return 1 - (np.sum(np.power((y-yHat),2)) / np.sum(np.power(y-np.mean(y),2)))

    def avg_dist_reg(self, coefs, precision=3):
        yHat = self.get_y_hat(coefs,precision)
        p = float(10. ** -precision)
        y = np.empty([2 * (10 ** precision) + 1])
        tx_range = np.arange(-1.0, 1. + p, p)
        for i, tx in zip(range(0,len(tx_range)),tx_range):
            y[i] = np.interp(tx, self.t, self.y)
        #return np.sqrt(np.sum(np.power((y-yHat),2))) / (2 * (10 ** precision) + 1) + (l * len(coefs))
        return np.sum(np.abs(y - yHat))

    def load_chebs_from_file(self):
        file_name = self.data_path + self.chebs_file_name
        try:
            with open(file_name, 'r') as file_chebs:
                chebs = json.load(file_chebs)
        except:
            chebs = dict()
        return chebs

    def save_chebs_to_file(self):
        file_name = self.data_path + self.chebs_file_name
        saved_chebs = self.load_chebs_from_file()
        merged = self.merge_two_dicts(self.chebs,saved_chebs)
        with open(file_name, 'w') as outfile:
            json.dump(merged, outfile)

    def merge_two_dicts(self, d1, d2):
        merged = d1.copy()  # start with x's keys and values
        merged.update(d2)  # modifies z with y's keys and values & returns None
        return merged