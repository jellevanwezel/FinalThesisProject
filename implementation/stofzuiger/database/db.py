import psycopg2 as pg
import pandas as pd
import os
import json
import numpy as np
from shapely.geometry import LineString
from shapely import wkb
import matplotlib.pyplot as plt


class DB:
    script_dir = os.path.dirname(__file__)

    def __init__(self):
        self.load_config()
        self.connect()

    def load_config(self):
        conf = json.load(open(os.path.join(self.script_dir, 'config.json')))
        self.username = conf['username']
        self.password = conf['password']
        self.dbname = conf['dbname']
        self.host = conf['host']

    def connect(self):
        try:
            self.connection = pg.connect(dbname=self.dbname, user=self.username, password=self.password, host=self.host)
        except pg.DatabaseError as e:
            print("\nAn OperationalError occurred. Error number {0}: {1}.".format(e.args[0], e.args[1]))

    def getQuery(self, file_name):
        """
        Opens the query file and returns it
        :param file_name: file name in ./queries
        :return: The sql file
        :rtype string:
        """
        fd = open(os.path.join(self.script_dir, 'queries', file_name + '.sql'), 'r')
        sqlFile = fd.read()
        fd.close()
        return sqlFile

    def do_query(self, query, params=None):
        """
        Excecutes the query and returns a DataFrame
        :param query: The query that should be excecuted
        :param params: The variables that should be inserted
        :return:The query result
        :rtype pandas.DataFrame:
        """
        df = pd.DataFrame()  # type: pd.DataFrame
        for chunk in pd.read_sql(query, params=params, con=self.connection, chunksize=5000):
            df = df.append(chunk)
        return df

    def get_kb_roots(self):
        """
        Gets the roots of the kb areas
        :return: The kb root measurepoint id's
        :rtype pandas.DataFrame:
        """
        query = self.getQuery('kb_roots')
        return self.do_query(query)

    def get_kb_measurements(self, root_id):
        """
        Gets all the measurements from a tree with given root
        :param root_id: int with the start node of the tree
        :return: A dataframe with the measurments of this tree
        :rtype pandas.DataFrame:
        """
        query = self.getQuery('kb_measurements')
        return self.do_query(query, {"root_id": root_id})

    def get_kb_differences(self, root_id):
        """
        Gets all the measurements from a tree with given root
        :param root_id: int with the start node of the tree
        :return: A dataframe with the measurments of this tree
        :rtype pandas.DataFrame:
        """
        query = self.getQuery('kb_differences')
        return self.do_query(query, {"root_id": root_id})

    def get_kb_distances(self,root_id):
        """
        Gets all the measurements from a tree with given root
        :param root_id: int with the start node of the tree
        :return: A dataframe with the measurments of this tree
        :rtype pandas.DataFrame:
        """
        query = self.getQuery('kb_distances')
        return self.do_query(query, {"root_id": root_id})

    def get_kb_flens(self,root_id):
        """
        Gets all the measurements from a tree with given root
        :param root_id: int with the start node of the tree
        :return: A dataframe with the measurments of this tree
        :rtype pandas.DataFrame:
        """
        query = self.getQuery('kb_flens')
        return self.do_query(query, {"root_id": root_id})


    def get_kb_oodi_dd(self, root_id):
        """
        Gets all the measurements from a tree with given root
        :param root_id: int with the start node of the tree
        :return: A dataframe with the measurments of this tree
        :rtype pandas.DataFrame:
        """
        query = self.getQuery('kb_oodi_dd')
        return self.do_query(query, {"root_id": root_id})

    def get_kb_ground_areas(self):
        """
        Gets all the ground info
        :return: A dataframe with the ground infos
        :rtype pandas.DataFrame:
        """
        query = self.getQuery('kb_ground_areas')
        return self.do_query(query)

    def get_kb_pipe_segments(self, roots):
        roots_string = "("+",".join(str(root) for root in roots)+")"
        query = self.getQuery("kb_pipe_segments")
        return self.do_query( query.replace("%(root_ids)s",roots_string))

    def get_kb_pipe_segments_roots(self):
        query = self.getQuery('kb_pipe_roots')
        return self.do_query(query)

db = DB();

# roots_df = db.get_kb_pipe_segments_roots()
# for area in roots_df.area.unique():
#     area_pip_roots = roots_df[roots_df.area == area].pip_id.values
#     print area
#     area_segments_df = db.get_kb_pipe_segments(area_pip_roots)
#     n_roots = len(area_segments_df.root.unique())
#     area_dict = {"coating":np.zeros([n_roots]),"length": np.zeros([n_roots])}
#     for idx, root_id in zip(range(0,n_roots),area_segments_df.root.unique()):
#         segment_df = area_segments_df[area_segments_df.root == root_id]
#         bit_df = segment_df[segment_df.coating == 9]
#         pce_df = segment_df[segment_df.coating == 10]
#         bit_length = np.array(bit_df.length.values)
#         pce_length = np.array(pce_df.length.values)
#         sum_bit = np.sum(bit_length)
#         sum_pce = np.sum(pce_length)
#         total_length = np.sum(sum_bit) + np.sum(sum_pce)
#         area_dict['coating'][idx] = sum_pce
#         area_dict['length'][idx] = total_length
#     print "mps:", len(area_dict['coating']), ", total pce:", np.sum(area_dict["coating"]) / np.sum(area_dict["length"]), ", total length:" ,  np.sum(area_dict["length"])

# roots_df = db.get_kb_pipe_segments_roots()
# for area in roots_df.area.unique():
#     area_pip_roots = roots_df[roots_df.area == area].pip_id.values
#     print area
#     area_segments_df = db.get_kb_pipe_segments(area_pip_roots)
#     n_roots = len(area_segments_df.root.unique())
#     for idx, root_id in zip(range(0,n_roots),area_segments_df.root.unique()):
#         segment_df = area_segments_df[area_segments_df.root == root_id]
#         for idx, row in segment_df.iterrows():
#             pipe_geom_string = row['geom']
#             if pipe_geom_string is None: continue
#             geom = wkb.loads(pipe_geom_string,hex=True)
#             x, y = zip(*geom.coords[:])
#             plt.plot(x,y)
#     plt.show()