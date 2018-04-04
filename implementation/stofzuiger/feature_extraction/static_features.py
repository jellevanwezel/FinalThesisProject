import unicodedata

from tqdm import tqdm

from database.db import DB
import numpy as np

from feature_extraction.feature_map import FeatureMap, FeatureLabels
from feature_extraction.projections import Projections
from feature_extraction.save_static_features import SaveStaticFeatures


class StaticFeatures(object):
    def __init__(self, file_path=None):
        self.file_path = file_path
        if file_path is None:
            self.db = DB()
            self.roots_df = self.db.get_kb_pipe_segments_roots()
            self.ground_areas_df = self.db.get_kb_ground_areas()
            self.proj = Projections()
            self.create_area_geoms()

    # gets the areas from the db and creates the geom objects for intersection.
    # todo: takes long, maybe serialize and save
    def create_area_geoms(self):
        self.ground_geoms = dict()
        for idx, row in self.ground_areas_df.iterrows():
            geom_string = row['geom']
            self.ground_geoms[row['id']] = self.proj.load_and_project(geom_string)

    def create_feature_map(self):
        fm = FeatureMap([
            FeatureLabels.acid,
            FeatureLabels.ground_water,
            FeatureLabels.stability,
            FeatureLabels.ground_type,
            FeatureLabels.pipe
        ])
        return fm

    # todo: refactor to use area model
    # extracts the features for the pipes attached to a mp from the database, intersected with the areas
    def extract_static_features(self):
        if self.file_path is not None:
            return self._extract_static_features_from_file()
        features = []
        for area_name in tqdm(self.roots_df.area.unique()):
            area_segments_df = self.get_area_segments(area_name)
            for pipe_root_id in area_segments_df.root.unique():
                pipes_df = self.get_pipes_df(pipe_root_id, area_segments_df)
                if np.sum(pipes_df.length.values) == 0: continue
                fm = self.create_feature_map()
                for idx, pipe_row in pipes_df.iterrows():
                    pipe_geom = self.proj.load_and_project(pipe_row['geom'])
                    area_intersects = self.intersect_pipe_with_area(pipe_geom)
                    self.set_area_features(fm, area_intersects)
                self.set_pipe_features(fm, pipes_df)
                mp_id = self.get_segment_mp_id(pipe_root_id, area_segments_df)
                feature_row = np.concatenate(([area_name], [mp_id], fm.get_feature_list()[0]))
                features.append(feature_row)
        return features

    def extract_static_features_to_dict(self, features):
        f_dict = dict()
        for idx, row in enumerate(features):
            if self.file_path is not None: row = list(row)  # todo: dirty hack, fix
            f_dict[(row[0], row[1])] = row[2:]
        return f_dict

    def _extract_static_features_from_file(self):
        features = np.genfromtxt(self.file_path, delimiter=',', skip_header=1, dtype=None)
        return features

    def set_area_features(self, fm, area_intersects):
        for area_id, length in area_intersects:
            area_row = self.ground_areas_df[self.ground_areas_df['id'] == area_id]
            for group in FeatureLabels.groups:  # todo: define this list somewhere
                label = self.pd_serie_to_str(area_row[group])
                new_val = fm.get_feature(group, label) + length
                fm.set_feature(group, label, new_val)

    def set_pipe_features(self, fm, segment_df):
        group_name = FeatureLabels.pipe[0]
        coating_name = FeatureLabels.pipe[1][0]
        length_name = FeatureLabels.pipe[1][1]  # todo: refactor feature label names, unclear
        coating_val, _, _ = self.segment_coating(segment_df)
        length_val = self.segment_length(segment_df)
        fm.set_feature(group_name, coating_name, coating_val)
        fm.set_feature(group_name, length_name, length_val)

    def get_segment_mp_id(self, pipe_root_id, area_segments_df):
        root_df = area_segments_df[area_segments_df.id == pipe_root_id]
        mp_id = int(root_df.mp_id.iloc[0])
        return mp_id

    def get_area_segments(self, area_name):
        area_pip_roots = self.roots_df[self.roots_df.area == area_name].pip_id.values
        area_segments_df = self.db.get_kb_pipe_segments(area_pip_roots)
        return area_segments_df

    def get_pipes_df(self, pipe_root_id, area_segments_df):
        pipes_df = area_segments_df[area_segments_df.root == pipe_root_id]
        pipes_df = pipes_df[pipes_df.length != 0]  # drop pipes with length 0
        return pipes_df.dropna(subset=['length', 'geom', 'coating'])

    # filthy function to get the python string from a dataframe
    def pd_serie_to_str(self, pd_serie):
        pd_str = unicodedata.normalize('NFKD', pd_serie.to_string()).encode('ascii', 'ignore')
        return ''.join([i for i in pd_str if i.isalpha()])

    # Gets the coating from a pipe segment
    def segment_coating(self, segment_df):
        bit_df = segment_df[segment_df.coating == 9]  # coating bitumen
        pce_df = segment_df[segment_df.coating != 9]  # coating pce
        bit_length = np.array(bit_df.length.values)  # get length of bitumen pipes
        pce_length = np.array(pce_df.length.values)  # get length of pce pipesddd
        sum_bit = np.sum(bit_length)  # sum the length
        sum_pce = np.sum(pce_length)
        total_length = np.sum(sum_bit) + np.sum(sum_pce)  # total length of both types
        return sum_pce / total_length, sum_pce, total_length

    def segment_length(self, segment_df):
        return np.sum(np.array(segment_df.length.values))

    # finds the areas this pipe intersects with, should always return atleast 1 area
    def intersect_pipe_with_area(self, pipe_geom):
        """
        gets the water level for the given pipe
        :param pipe_geom: LineString the pipe geom
        :return: areas this pipe is in
        :rtype : array
        """
        areas = []  # tuple list of area_id and persentage length in that area
        for area_id, area_geom in self.ground_geoms.iteritems():  # todo: check if search space can be narrowed
            if not area_geom.intersects(pipe_geom): continue
            diff_geom = pipe_geom.intersection(area_geom)
            if diff_geom.length == pipe_geom.length: return [(area_id, np.round(pipe_geom.length, 2))]
            areas.append((area_id, np.round(diff_geom.length, 2)))
        return areas

# sf = StaticFeatures()
# features = sf.extract_static_features()
# fs = SaveStaticFeatures()
# fs.array_to_csv(features, 'static_features')