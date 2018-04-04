import json

import numpy as np
import matplotlib.pyplot as plt
import os

from statistics.stats import Stats


class PolyInterpolation(object):
    def __init__(self, precision=6):
        self.precision = precision
        self.chebs = dict()
        self.data_path = os.path.dirname(os.path.realpath(__file__)) + "/data/"
        self.chebs_file_name = 'chebs.json'
        self.load_chebs_from_file()
        self.t = np.array([])
        self.y = np.array([])

    def set_t(self, t):
        self.t = Stats.rescale(t, -1, 1)

    def set_y(self, y):
        self.y = y

    def set_t_y(self, t, y):
        t = Stats.rescale(t, -1, 1)
        self.y = y
        self.t, self.y = zip(*sorted(zip(t, y)))  # sort on x

    def cheb(self, n, x):
        if n == 0: return 1.  # first defenition
        if n == 1: return float(x)  # second defenition
        if not (self.chebs.get(n) is None):  # if the n is stored, find the x
            n_cheb = self.chebs.get(n)
            if not (n_cheb.get(round(x, self.precision)) is None):  # if the x is stored, return the x
                return n_cheb.get(round(x, self.precision))
            n_cheb[round(x, self.precision)] = 2. * x * self.cheb(n - 1, x) - self.cheb(n - 2,
                                                                                        x)  # x not stored, create it
        else:
            self.chebs[n] = {
                round(x, self.precision): 2. * x * self.cheb(n - 1, x) - self.cheb(n - 2, x)
            }  # n not stored create it, with this value for x
            n_cheb = self.chebs.get(n)
        return n_cheb.get(round(x, self.precision))  # return the created value of for n,x

    def find_coefs(self, n):
        coefs = np.empty([n + 1])
        for k in range(0, n + 1):
            ratio = 2.0 / float(n + 1)
            cheb_sum = 0.0
            for l in range(0, n + 1):
                tl = np.cos((float(l) + 0.5) * (np.pi / float(n + 1)))
                cheb_sum += np.interp(tl, self.t, self.y) * self.cheb(k, tl)
            coefs[k] = ratio * float(cheb_sum)
        coefs[0] /= 2.0  # as writen in the paper devide first coef by 2
        return coefs

    def get_y_hat(self, coefs, precision=3):
        p = float(10. ** -precision)
        y_hat = np.empty([2 * (10 ** precision) + 1])
        i = 0
        for tx in np.arange(-1.0, 1. + p, p):
            cheb_sum = 0.
            for k in range(0, len(coefs)):
                cheb_sum += coefs[k] * self.cheb(k, tx)
            y_hat[i] = cheb_sum
            i += 1
        return y_hat

    def get_y_hat_for_range(self, coefs, np_range):
        # todo: say it should be always scaled between -1 and 1, or just do the rescale
        y_hat = np.empty([len(np_range)])
        for idx, tx in enumerate(np_range):
            cheb_sum = 0.
            for k in range(0, len(coefs)):
                cheb_sum += coefs[k] * self.cheb(k, tx)
            y_hat[idx] = cheb_sum
            idx += 1
        return y_hat

    def plot_y_hat(self, coefs, precision=3):
        p = float(10. ** -precision)
        y_hat = self.get_y_hat(coefs, precision)
        plt.plot(np.arange(-1.0, 1. + p, p), y_hat)
        plt.plot(self.t, self.y)
        plt.show()

    def get_t_hat(self, precision=3):
        p = float(10. ** -precision)
        return np.arange(-1.0, 1.0 + p, p)

    def r_squared(self, coefs, precision=3):
        i = 0
        y_hat = self.get_y_hat(coefs, precision)
        p = float(10. ** -precision)
        y = np.empty([2 * (10 ** precision) + 1])
        for tx in np.arange(-1.0, 1. + p, p):
            y[i] = np.interp(tx, self.t, self.y)
            i += 1
        return 1 - (np.sum(np.power((y - y_hat), 2)) / np.sum(np.power(y - np.mean(y), 2)))

    def avg_dist_reg(self, coefs, precision=3):
        y_hat = self.get_y_hat(coefs, precision)
        p = float(10. ** -precision)
        y = np.empty([2 * (10 ** precision) + 1])
        tx_range = np.arange(-1.0, 1. + p, p)
        for i, tx in zip(range(0, len(tx_range)), tx_range):
            y[i] = np.interp(tx, self.t, self.y)
        return np.sum(np.abs(y - y_hat))

    def load_chebs_from_file(self):
        file_name = self.data_path + self.chebs_file_name
        try:
            with open(file_name, 'r') as file_chebs:
                chebs = json.load(file_chebs)
        except IOError:
            print "File:", file_name, "not found! Using empty dictionary."
            chebs = dict()
        return chebs

    def save_chebs_to_file(self):
        file_name = self.data_path + self.chebs_file_name
        saved_chebs = self.load_chebs_from_file()
        merged = self.merge_two_dicts(self.chebs, saved_chebs)
        with open(file_name, 'w') as outfile:
            json.dump(merged, outfile)

    def merge_two_dicts(self, d1, d2):
        merged = d1.copy()
        merged.update(d2)
        return merged
