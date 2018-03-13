import numpy as np


def mean_std(x):
    return (np.mean(x), np.std(x))

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size/2:]

def normalize(arr):
    return (arr - np.min(arr)) / float((np.max(arr) - np.min(arr)))