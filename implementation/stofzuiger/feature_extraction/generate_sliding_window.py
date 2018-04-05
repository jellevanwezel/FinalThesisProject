from tqdm import tqdm
from database.area_model import AreaModel
from feature_extraction.save_sliding_window import SaveSlidingWindow
from feature_extraction.sliding_window import SlidingWindow

sw = SlidingWindow(nr_of_samples=20)  # insert config here :)

area_model = AreaModel()
file_name = sw.serialize_file_name()

nr_of_areas = area_model.get_number_of_areas()
for area_idx in tqdm(range(0, nr_of_areas), desc='Sliding Window'):
    area_name = area_model.get_area_name(area_idx)
    for mp_idx, mp_id in enumerate(area_model.get_mp_ids(area_idx)):
        meas_df = area_model.get_mp_df(area_idx, mp_idx)
        meas_df = area_model.prepare_meas_df(meas_df)
        if meas_df is None: continue
        sw_features, labels, label_gradients = sw.create_features_labels(meas_df, area_name, mp_id)
        SaveSlidingWindow.features_to_json(sw_features, labels, label_gradients, area_name, mp_id, file_name)
