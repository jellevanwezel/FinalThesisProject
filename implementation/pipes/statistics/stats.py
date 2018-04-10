import numpy as np


class Stats(object):
    @staticmethod
    def mean_std(x):
        """Calculates the mean for given array x"""
        return np.mean(x), np.std(x)

    @staticmethod
    def autocorr(x):
        """calculates the auto correlation for the given array x"""
        result = np.correlate(x, x, mode='full')
        return result[result.size / 2:]

    @staticmethod
    def normalize(arr):
        """normalizes the given array (rescale between 1 and 0)"""
        return (arr - np.min(arr)) / float((np.max(arr) - np.min(arr)))

    @staticmethod
    def rescale(x, min_val, max_val):
        """rescales the array between min_val and max_val"""
        return min_val + (((x - np.min(x)) * (max_val - min_val)) / float((np.max(x) - np.min(x))))
