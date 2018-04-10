import numpy as np


class Predictor(object):
    def __init__(self, lvq_model, mid_points):
        self.lvq_model = lvq_model
        self.mid_points = mid_points

    def predict_n_steps(self, window, static_features, n_steps, ):
        result = list()
        predicted_bins = list()
        for i in range(n_steps):
            data = np.concatenate((window, static_features))
            label = self.lvq_model.predict(np.array([data]))
            mpl = self.mid_points[label[0]]
            result.append(mpl)
            predicted_bins.append(label[0])
            window = np.concatenate((window[1:], np.array([mpl])))
        return result, predicted_bins
