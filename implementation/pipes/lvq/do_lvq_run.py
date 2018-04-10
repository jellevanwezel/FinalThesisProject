import glvq
import numpy as np

from feature_extraction.sliding_window import SlidingWindow
from feature_extraction.static_features import StaticFeatures
from lvq.predictor import Predictor
from preprocessing.dataset import Dataset

sw_file = '../feature_extraction/data/sliding_window/50_0_10_10.json'
sw = SlidingWindow(file_path=sw_file)
# Gets the sliding window data from the measurements
# Can be generated from the database or extracted from a file
#
#
sf_file = '../feature_extraction/data/static_features.csv'
sf = StaticFeatures(file_path=sf_file)
# Gets the static features by the measure points
# Can be generated from the database or extracted from a file


ds = Dataset()
df, mid_points = ds.generate_dataset(sw, sf, n_label_bins=20)
# Concatenates the static data and the sliding window and bins the labels


# df = ds.rescale_labels(df, 5, 11)
# mid_points = np.array(mid_points)[4:]
# optional, removes barely used labels
# Still needs to be optimized

mpdata = df.loc[df.measure_point_id == 767]
df = df[df.measure_point_id != 767]
#  take 1 measure point for testing and remove it from the dataset

x = df.iloc[:, 2:-4]
# the data to train lvq on,
# column 1 = area id
# column 2 = measure point id
# column -4 and -3 are the actual labels [real_point, gradient]
# column -2 and -1 are the binned labels [real_point, gradient]

y = df.binned_points
# set y as the labels to train on (only use the real_point, gradient performs worse.)

model = glvq.GlvqModel(prototypes_per_class=1)
# the lvq model, Lgmlvq performs best, way better than everything else

model.fit(x, y)
# train the lvq model (Lgmlvq takes a long time)

window = np.array(mpdata.iloc[0, 2:12])
# take a window from the test data

static_features = np.array(mpdata.iloc[0, 12:-4])
# take the static features by this window

real_bins = np.array(mpdata.iloc[0:10, -2])
real_labels = np.array(mpdata.iloc[0:10, -4])
real_binned_labels = np.array(mpdata.iloc[0:10, -2])
# take the real data for comparison

predictor = Predictor(model, mid_points)
pred_labels, pred_bins = predictor.predict_n_steps(window, static_features, 10)
# predict n steps from the initial window

print 'window     ', ','.join(map(str, (map(int, window))))
print 'real_labels', ','.join(map(str, (map(int, real_labels))))
print 'pred_labels', ','.join(map(str, (map(int, pred_labels))))
print 'real_bins  ', ','.join(map(str, (map(int, real_bins))))
print 'pred_bins  ', ','.join(map(str, (map(int, pred_bins))))

# prints the results, should be spaced better for comparing.
