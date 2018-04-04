import json
import os


class SaveSlidingWindow(object):
    @staticmethod
    def features_to_json(features, labels_points, labels_gradients, area_name, mp_id, file_name):
        filepath = os.path.dirname(os.path.abspath(__file__))
        data = {
            'features': features.tolist(),
            'labels': labels_points.tolist(),
            'label_gradients': labels_gradients.tolist()
        }

        filename = filepath + '/data/sliding_window/' + file_name + '.json'
        write_mode = 'r+' if os.path.exists(filename) else 'w'
        with open(filename, write_mode) as json_file:
            try:
                sw_dict = json.load(json_file)
            except:
                sw_dict = dict()
            if sw_dict.get(area_name) is not None:
                sw_dict[area_name][mp_id] = data  # area exists add mp
            else:
                sw_dict[area_name] = {mp_id: data}  # area_does not exist, create it
            json_file.seek(0)
            json.dump(sw_dict, json_file, indent=4)
            json_file.truncate()
