import pandas as pd
import glvq
import numpy as np

from feature_extraction.sliding_window import SlidingWindow
from feature_extraction.static_features import StaticFeatures
from lvq.cross_validation import CrossValidateLvq
from preprocessing.dataset import Dataset

splits = 5

sw_file = '../feature_extraction/data/sliding_window/50_0_10_10.json'
sw = SlidingWindow(file_path=sw_file)
#  sw = SlidingWindow()
sf_file = '../feature_extraction/data/static_features.csv'
sf = StaticFeatures(file_path=sf_file)

ds = Dataset()
df, mid_points = ds.generate_dataset(sw, sf, n_label_bins=20)
df = ds.rescale_labels(df, 5, 11)

n_bins = len(np.unique(df.binned_points))
largest_label = np.unique(df.binned_points)[-1]
n_bins = n_bins if largest_label == n_bins - 1 else largest_label + 1

model = glvq.LgmlvqModel(prototypes_per_class=1)
cv_lvq = CrossValidateLvq(n_bins, splits, model)
cv_lvq.cross_validate(df, gradient=False)

print
cv_lvq.print_conv_matrix()
tp = np.sum(cv_lvq.conf_matrix.diagonal())
tot = np.sum(np.sum(cv_lvq.conf_matrix))
print
print tp / float(tot)