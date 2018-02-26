import numpy as np


def mean_std(x):
    return (np.mean(x), np.std(x))

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size/2:]