import numpy as np


def train(data_labels, params):
    data = data_labels['data']
    k = params['k']
    max_iter = params['max_iter']

    random_indexes = np.arange(data.shape[0])
    np.random.shuffle(random_indexes)

    cluster_idexes = random_indexes[:k]
    clusters = data[cluster_idexes, :]

    clusterLabels = np.ones(data.shape[0])

    for i in range(0, max_iter):
        for row_idx in range(0, data.shape[0]):
            data_point = data[row_idx, :]
            dara_point_rep = np.tile(data_point, (clusters.shape[0], 1))
            distances = np.sqrt(np.sum((np.square(dara_point_rep - clusters)), axis=1))  # euclidean dist
            clusterLabels[row_idx] = np.argmin(distances)
        for cluster_idx in range(0, k):
            clusters[cluster_idx, :] = np.mean(data[np.where(clusterLabels == cluster_idx)], axis=0)
    return clusters
