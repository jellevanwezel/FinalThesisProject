import numpy as np
from interpolation.cheb_store import ChebStore
from statistics.stats import Stats


class ChebInterpolation(object):
    file_name = 'chebs.json'

    def __init__(self):
        self.cheb_store = ChebStore(ChebInterpolation.file_name)

    def cheb(self, n, x):
        """Recursive Chebishev function (See paper)"""
        if n == 0:
            return 1.  # first defenition
        if n == 1:
            return float(x)  # second defenition
        if self.cheb_store.has_cheb(n, x):
            return self.cheb_store.get_cheb(n, x)
        cheb = 2. * x * self.cheb(n - 1, x) - self.cheb(n - 2, x)
        self.cheb_store.add_cheb(n, x, cheb)
        return cheb

    def find_coefs(self, n, t, y):
        """Gets the coefs for this time series"""
        t, y = ChebInterpolation.prepare_t_y(t, y)
        coefs = np.empty([n + 1])
        for k in range(0, n + 1):
            cheb_sum = 0.0
            for l in range(0, n + 1):
                tl = np.cos((float(l) + 0.5) * (np.pi / float(n + 1)))
                cheb_sum += np.interp(tl, t, y) * self.cheb(k, np.round(tl, 3))
            coefs[k] = 2.0 / (n + 1.0) * float(cheb_sum)
        coefs[0] /= 2.0  # as writen in the paper devide first coef by 2
        return coefs

    def get_y_hat_range(self, coefs, t=np.arange(-1, 1.1, 0.1)):
        """Gets the approximated functions for an range x"""
        t_original = t
        if np.min(t) < -1 or np.max(t) > 1:
            t = Stats.rescale(t, -1, 1)
        y_hat = []
        for time_step in enumerate(t):
            y_hat.append(self.get_y_hat(coefs, time_step))
        return np.array(y_hat), t_original

    def get_y_hat(self, coefs, t):
        """Calculates a singe aproximated value of y"""
        cheb_sum = 0.0
        for k in range(0, len(coefs)):
            cheb_sum += coefs[k] * self.cheb(k, np.round(t, 3))
        return cheb_sum

    @staticmethod
    def prepare_t_y(self, t, y):
        """Sorts and rescales t"""
        return zip(*sorted(zip(Stats.rescale(t, -1, 1), y)))
