import numpy as np
import matplotlib.pyplot as plt

def cheb(n, x):
    if (n == 0): return float(1);  # first defenition
    if (n == 1): return float(x);  # second defenition
    return (2. * x * cheb(n - 1, x)) - cheb(n - 2, x) # third defenition


def find_coefs(n,t,y):
    t = rescale(t,-1,1)
    coefs = np.empty([n])
    for k in range(0, n):
        ratio = 2. / float(n + 1)
        sum = 0.
        for l in range(0, n + 1):
            tl = np.cos((float(l) + .5) * (np.pi / float(n + 1)))
            sum += np.interp(tl, t, y) * cheb(k, tl)
        coefs[k] = ratio * float(sum)
    #coefs[0] = coefs[0] / 2.  # todo: first coef is a factor 2 off. find out why
    return coefs


def get_y_hat(coefs,t):
    t = rescale(t,-1,1)
    yHat = np.empty([len(t)])
    for i,tx in zip(range(0,len(t)),t):
        sum = 0.
        for k in range(0, len(coefs)):
            sum += coefs[k] * cheb(k, tx)
        yHat[i] = sum
    return yHat

def rescale(x,min,max):
    return min + (((x-np.min(x)) * (max - min) ) / (np.max(x) - np.min(x)))


t = np.arange(0, 2* np.pi,0.1) #creates range from 0 to 2 * pi with a step of 0.5
y = np.sin(t)


t = np.array([
        1994.846154,
        1999.769231,
        2000.846154,
        2001.846154,
        2002.846154,
        2003.846154,
        2006.846154,
        2008.846154,
        2014.307692,
        2015.307692
    ])

y = np.array([
        -960,
        -986,
        -1024,
        -1146,
        -1132,
        -760,
        -1050,
        -1105,
        -909,
        -1071
    ])

#y = y - np.mean(y)



for i in range(1,20):
    coefs = find_coefs(i, t, y)
    print coefs[0]
    plt.plot(t, y)
    plt.plot(t,get_y_hat(coefs,t))
    plt.show()

