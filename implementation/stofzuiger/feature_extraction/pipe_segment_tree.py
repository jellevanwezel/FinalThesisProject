import unicodedata
from shapely import wkb
from sklearn.decomposition import PCA

from database.db import DB
import numpy as np

from feature_extraction.save_features import FeatureSaver


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
        features = []
        for area in self.roots_df.area.unique():
            area_pip_roots = self.roots_df[self.roots_df.area == area].pip_id.values
            print area
            area_segments_df = self.db.get_kb_pipe_segments(area_pip_roots)
            n_roots = len(area_segments_df.root.unique())
            for idx, root_id in zip(range(0, n_roots), area_segments_df.root.unique()):
                segment_df = area_segments_df[area_segments_df.root == root_id]

                # segment - tree

                acid = np.zeros([3])
                ground_water = np.zeros([5])
                stability = np.zeros([6])
                soil_type = np.zeros([7])

                for idx, row in segment_df.iterrows():

                    pipe_geom_string = row['geom']
                    if pipe_geom_string is None: continue
                    geom = wkb.loads(pipe_geom_string, hex=True)
                    pip_id = row['id']
                    #print "ROW: ", row['id']
                    #print self.intersect_pipe_with_area(geom)

                    # pipe
                    areas = self.intersect_pipe_with_area(geom)
                    for area_id, length in areas:
                        area_row = self.ground_areas_df[self.ground_areas_df['id'] == area_id]
                        a, g, st, so = self.names_to_nr(area_row)
                        acid[a] += length
                        ground_water[g] += length
                        stability[st] += length
                        soil_type[so] += length
                coating_percentage, sum_pce, total_length = self.coating(segment_df)
                acid = np.round(acid,decimals=3)
                ground_water = np.round(ground_water,decimals=3)
                stability = np.round(stability,decimals=3)
                soil_type = np.round(soil_type,decimals=3)
                coating_percentage = np.round(coating_percentage,decimals=3)
                features.append(np.concatenate(([area], [root_id], acid, ground_water, stability, soil_type, [coating_percentage])))
        return features

    def names_to_nr(self, row):
        a = {'Zuur':0, 'Zwakzuur':1, 'Water':2}[self.pd_serie_to_str(row['ph'])]
        g = {'Vrijdiep':0,'Water':1,'Zeerondiep':2,'Ondiep':3,'Diep':4}[self.pd_serie_to_str(row['gw_class'])]
        st = {'Stabiel':0, 'Redelijkstabiel':1, 'Instabiel':2, 'Water':3}[self.pd_serie_to_str(row['stability'])]
        so = {'Zandenleem':0, 'Water':1, 'Veenenzand':2, 'Veen':3, 'Kleienzand':4, 'Leem':5, 'Zand':6}[self.pd_serie_to_str(row['type'])]
        return a, g, st, so

    def pd_serie_to_str(self,pd_serie):
        pd_str = unicodedata.normalize('NFKD', pd_serie.to_string()).encode('ascii', 'ignore')
        return ''.join([i for i in pd_str if i.isalpha()])

    def coating(self,segment_df):
        bit_df = segment_df[segment_df.coating == 9]  # coating bitumen
        pce_df = segment_df[segment_df.coating == 10]  # coating pce
        bit_length = np.array(bit_df.length.values)  # get length of bitumen pipes
        pce_length = np.array(pce_df.length.values) # get length of pce pipes
        sum_bit = np.sum(bit_length)  # sum the length
        sum_pce = np.sum(pce_length)
        total_length = np.sum(sum_bit) + np.sum(sum_pce)  # total length of both types
        return sum_pce / total_length, sum_pce, total_length

    def intersect_pipe_with_area(self, pipe_geom):
        """
        gets the water level for the given pipe
        :param pipe_geom: LineString the pipe geom
        :return: areas this pipe is in
        :rtype : array
        """
        areas = []  # tuple of area_id and persentage length in that area
        for area_id, area_geom in self.ground_geoms.iteritems(): #  todo: narrow search space
            if not area_geom.intersects(pipe_geom): continue
            diff_geom = pipe_geom.intersection(area_geom)
            if diff_geom.length == pipe_geom.length: return [(area_id,1)]
            areas.append((area_id,diff_geom.length))
        return areas



fe = FeatureExtraction()
features = fe.extract()
fs = FeatureSaver()
fs.array_to_csv(features,'feature_test')
