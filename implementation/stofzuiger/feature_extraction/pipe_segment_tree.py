from shapely import wkb
from database.db import DB
import numpy as np

class FeatureExtraction:

    def __init__(self):
        self.db = DB()
        self.roots_df = self.db.get_kb_pipe_segments_roots()
        self.ground_areas_df = self.db.get_kb_ground_areas()
        self.create_area_geoms()

    def create_area_geoms(self):
        self.ground_geoms = dict()
        for idx, row in self.ground_areas_df.iterrows():
            geom_string = row['geom']
            self.ground_geoms[row['id']] = wkb.loads(geom_string, hex=True)

    def extract(self):
        for area in self.roots_df.area.unique():
            area_pip_roots = self.roots_df[self.roots_df.area == area].pip_id.values
            print area
            area_segments_df = self.db.get_kb_pipe_segments(area_pip_roots)
            n_roots = len(area_segments_df.root.unique())
            for idx, root_id in zip(range(0, n_roots), area_segments_df.root.unique()):
                segment_df = area_segments_df[area_segments_df.root == root_id]

                # segment - tree

                for idx, row in segment_df.iterrows():
                    pipe_geom_string = row['geom']
                    if pipe_geom_string is None: continue
                    geom = wkb.loads(pipe_geom_string, hex=True)
                    print "ROW: ", row['id']
                    self.water_level(geom)

                    # pipe

    def coating(self,segment_df):
        bit_df = segment_df[segment_df.coating == 9]  # coating bitumen
        pce_df = segment_df[segment_df.coating == 10]  # coating pce
        bit_length = np.array(bit_df.length.values)  # get length of bitumen pipes
        pce_length = np.array(pce_df.length.values) # get length of pce pipes
        sum_bit = np.sum(bit_length)  # sum the length
        sum_pce = np.sum(pce_length)
        total_length = np.sum(sum_bit) + np.sum(sum_pce)  # total length of both types
        return sum_pce/total_length, sum_pce, total_length

    def water_level(self, pipe_geom):
        """
        gets the water level for the given pipe
        :param pipe_geom: LineString the pipe geom
        :return: The most prominent water level
        :rtype pandas.DataFrame:
        """

        areas = []
        for area_id, area_geom in self.ground_geoms.iteritems():
            if area_geom.intersects(pipe_geom):
                areas.append((area_id,area_geom))
        if len(areas) > 1:
            print "Is in multiple areas"
            lenghts = []
            ids = []
            for (id,area) in areas:
                diff_geom = pipe_geom.intersection(area)
                lenghts.append(diff_geom.length)
                ids.append(id)
            print zip(ids, np.array(lenghts) / pipe_geom.length), np.sum(np.array(lenghts)), pipe_geom.length


fe = FeatureExtraction()
fe.extract()