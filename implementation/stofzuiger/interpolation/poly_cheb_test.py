import numpy as np
import matplotlib.pyplot as plt


# chebyshev
def cheb(n, x):
    if (n == 0): return float(1)  # T0(x)
    if (n == 1): return float(x)  # T1(x)
    return (2.0 * x * cheb(n - 1, x)) - cheb(n - 2.0, x)  # Tn(x)


# calculates the n coefficients for the given t and y values
def find_coefs(n, t, y):
    t = rescale(t, -1, 1)
    coefs = np.empty([n])
    for k in range(0, n):
        # loop over array [0,1,2,...,n-1]
        ratio = 2.0 / float(n + 1)
        # 2/(n+1)
        sum = 0.0
        for l in range(0, n + 1):
            # loop over array [0,1,2,...,n]
            tl = np.cos((float(l) + 0.5) * (np.pi / float(n + 1)))
            # t_l = cos( (l+(1/2)) * pi/(n+1) )
            sum += np.interp(tl, t, y) * cheb(k, tl)
            # sum of f_i(t_l) * T_k(t_l)
        coefs[k] = ratio * float(sum)
        # sum * 2/(n+1)
    return coefs


# calculates the y approximation on the given t values and coefficients
def get_y_hat(coefs, t):
    t = rescale(t, -1, 1)
    # rescale t between -1 and 1
    yHat = np.empty([len(t)])
    # create empty array for the approximated values
    for idx, tx in zip(range(0, len(t)), t):
        # loop over all values in t as tx and the index of tx
        sum = 0.0
        for k in range(0, len(coefs)):
            # loop over all the coefficients
            sum += coefs[k] * cheb(k, tx)
            # c_i,k * g_k(tx)
        yHat[idx] = sum
        # f_i(tx)
    return yHat


# rescales the array x between min and max
def rescale(x, min, max):
    return min + (((x - np.min(x)) * (max - min)) / float((np.max(x) - np.min(x))))


# plots the data
def plot_data(location, n_coefs, title, t, y, half_first_coef=False):
    plt.subplot(location)
    plt.plot(t, y, label='data')
    for c in n_coefs:
        coefs = find_coefs(c, t, y)
        if half_first_coef: coefs[0] /= 2.0
        plt.plot(t, get_y_hat(coefs, t), label=(str(c) + ' coefficients'))
    plt.title(title)
    plt.legend(loc='upper right')
    plt.xlim(np.min(t), np.max(t))


# sin data between 0 and 2 pi
t = np.arange(0, 2 * np.pi, 0.1)  # creates range from 0 to 2 * pi with a step of 0.1
y = np.sin(t)
plot_data(221, [1, 16], 'Sine wave', t, y)

# real data
# t: Years and months as floats
# y: measurements (micro voltages)
t = np.array([
    1994.846154, 1999.769231, 2000.846154, 2001.846154, 2002.846154,
    2003.846154, 2006.846154, 2008.846154, 2014.307692, 2015.307692
])
y = np.array([
    -960, -986, -1024, -1146, -1132,
    -760, -1050, -1105, -909, -1071
])
plot_data(222, [1, 16], 'Real data', t, y)
plot_data(223, [1, 16], 'Real data - First Coef divided by 2', t, y, half_first_coef=True)
plot_data(224, [1, 16], 'Real data - Mean substracted', t, (y - np.mean(y)))

plt.show()
