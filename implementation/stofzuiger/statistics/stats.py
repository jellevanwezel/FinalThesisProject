import numpy as np


class Stats(object):
    @staticmethod
    def mean_std(x):
        return np.mean(x), np.std(x)

    @staticmethod
    def autocorr(x):
        result = np.correlate(x, x, mode='full')
        return result[result.size / 2:]

    @staticmethod
    def normalize(arr):
        return (arr - np.min(arr)) / float((np.max(arr) - np.min(arr)))

    @staticmethod
    def rescale(x, min_val, max_val):
        return min_val + (((x - np.min(x)) * (max_val - min_val)) / float((np.max(x) - np.min(x))))
