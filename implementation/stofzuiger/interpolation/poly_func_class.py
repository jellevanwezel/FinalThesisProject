import numpy as np
import matplotlib.pyplot as plt

class PolyInterpolation:

    def __init__(self,precision=6):
        self.precision = precision
        self.chebs = dict()

    def set_t(self,t):
        self.t = (t - np.min(t)) / (np.max(t) - np.min(t)) * 2 - 1  # rescale between -1 and 1

    def set_y(self,y):
        self.y = y

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
            sum = 0.;
            for l in range(0, n+1):
                tl = np.cos((float(l) + .5) * (np.pi / float(n + 1)))
                sum += np.interp(tl, self.t, self.y) * self.cheb(k, tl)
            coefs[k] = ratio * float(sum)
        coefs[0] = coefs[0] / 2. # todo: first coef is a factor 2 off. find out why
        return coefs

    def get_y_hat(self,coefs,precision=3):
        p = float(10. ** -precision)
        yHat = np.empty([2 * (10 ** precision) + 1])
        i = 0;
        for tx in np.arange(-1.0, 1. + p, p):
            sum = 0.
            for k in range(0, len(coefs)):
                sum += coefs[k] * self.cheb(k, tx)
            yHat[i] = sum
            i += 1
        return yHat

    def plot_y_hat(self,coefs,precision=3):
        p = float(10. ** -precision)
        yHat = self.get_y_hat(coefs,precision)
        plt.plot(np.arange(-1.0, 1. + p,p), yHat)
        plt.plot(self.t, self.y)
        plt.show()

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
        i = 0
        yHat = self.get_y_hat(coefs,precision)
        p = float(10. ** -precision)
        y = np.empty([2 * (10 ** precision) + 1])
        for tx in np.arange(-1.0, 1. + p, p):
            y[i] = np.interp(tx, self.t, self.y)
            i += 1
        #return np.sqrt(np.sum(np.power((y-yHat),2))) / (2 * (10 ** precision) + 1) + (l * len(coefs))
        return np.sum(np.abs(y - yHat))

# t = np.array([7.307692,8.923077,9.923077,10.923077,11.923077,13,14,15,16,16.923077,18,19,21,22,23.384615,24.384615,25.461538,28.461538])
# y = np.array([-994,-1004,-988,-1072,-928,-572,-1164,-1226,-740,-1080,-1130,-1040,-1080,-1050,-1025,-1080,-960,-1050])
# polyInt = PolyInterpolation(t,y)
# coefs = polyInt.find_coefs(n=25)
# print polyInt.r_squared(coefs)
# polyInt.plot_y_hat(coefs)


# polyInt = PolyInterpolation(t,y)
# rs = np.empty([51])
# for n in range(0,51):
#     coefs = polyInt.find_coefs(n)
#     rs[n] = polyInt.avg_dist_reg(coefs,0.1)
#     print "n:" + str(n) + " dist:" + str(rs[n])
# plt.plot(range(0,51),rs)
# plt.show()