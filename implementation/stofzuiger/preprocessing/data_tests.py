import pandas as pd
import numpy as np


def labels_20_to_6():
    df = pd.read_csv(filepath_or_buffer='data_20.csv')
    df.loc[df.binned_points > 9, 'binned_points'] = 9
    df.loc[df.binned_points < 3, 'binned_points'] = 3
    print np.min(df.binned_points), np.max(df.binned_points)
    df.loc[:, 'binned_points'] = df.loc[:, 'binned_points'] - 3
    _, counts = np.unique(df.binned_points, return_counts=True)
    print counts
    print np.min(df.binned_points), np.max(df.binned_points)
    df.to_csv(path_or_buf='data_20_to_6.csv', index=False)


def labels_10_to_4():
    df = pd.read_csv(filepath_or_buffer='data_10.csv')
    df.loc[df.binned_points > 5, 'binned_points'] = 5
    df.loc[df.binned_points < 1, 'binned_points'] = 1
    print np.min(df.binned_points), np.max(df.binned_points)
    df.loc[:, 'binned_points'] = df.loc[:, 'binned_points'] - 1
    _, counts = np.unique(df.binned_points, return_counts=True)
    print counts
    print np.min(df.binned_points), np.max(df.binned_points)
    df.to_csv(path_or_buf='data_10_to_4.csv', index=False)


def grads_10():
    df = pd.read_csv(filepath_or_buffer='data_10.csv')
    # df.loc[df.binned_points > 5, 'binned_points'] = 5
    # df.loc[df.binned_points < 1, 'binned_points'] = 1
    print np.min(df.binned_gradients), np.max(df.binned_gradients)
    # df.loc[:, 'binned_gradients'] = df.loc[:, 'binned_gradients'] - 1
    _, counts = np.unique(df.binned_gradients, return_counts=True)
    print counts
    print np.min(df.binned_gradients), np.max(df.binned_gradients)
    # df.to_csv(path_or_buf='data_10_to_4.csv', index=False)

def grads_20():
    df = pd.read_csv(filepath_or_buffer='data_grad.csv')
    df.loc[df.binned_gradients > 11, 'binned_gradients'] = 11
    df.loc[df.binned_gradients < 4, 'binned_gradients'] = 4
    print np.min(df.binned_gradients), np.max(df.binned_gradients)
    df.loc[:, 'binned_gradients'] = df.loc[:, 'binned_gradients'] - 4
    _, counts = np.unique(df.binned_gradients, return_counts=True)
    print counts
    print np.min(df.binned_gradients), np.max(df.binned_gradients)
    df.to_csv(path_or_buf='data_grad_20.csv', index=False)

def bins_40():
    df = pd.read_csv(filepath_or_buffer='data.csv')
    df.loc[df.binned_points > 16, 'binned_points'] = 16
    df.loc[df.binned_points < 7, 'binned_points'] = 7
    # print np.min(df.binned_gradients), np.max(df.binned_gradients)
    df.loc[:, 'binned_points'] = df.loc[:, 'binned_points'] - 7
    _, counts = np.unique(df.binned_points, return_counts=True)
    print counts
    print np.min(df.binned_points), np.max(df.binned_points)
    df.to_csv(path_or_buf='data_40_to_10.csv', index=False)

def reshape_dataset(df, cut_left, cut_right):
    n_bins = len(np.unique(df.binned_points))
    df.loc[df.binned_points > cut_left, 'binned_points'] = cut_left
    df.loc[df.binned_points > n_bins - cut_right, 'binned_points'] = n_bins - cut_right
    df.loc[:, 'binned_points'] = df.loc[:, 'binned_points'] - cut_left
    return df


bins_40()