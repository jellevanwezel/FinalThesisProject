from database.db import DB
from statistics.stats import Stats


class AreaModel(object):
    def __init__(self, save_areas=True):
        self.save_areas = save_areas
        self.stof = DB()
        self.roots_df = self.stof.get_kb_roots()
        self.areas = dict()

    def get_area_id(self, area_idx):
        """
        Gets the id of an area by its index in the dataframe
        :param area_idx: integer of the index
        :return: the area id
        :rtype: int
        """
        root = self.roots_df.iloc[area_idx]
        return root['id']

    def get_area_df(self, area_idx):
        """
        Gets the area DataFrame by its index
        :param area_idx: index of the area
        :return: The area DataFrame
        :rtype: pandas.DataFrame
        """
        area_id = self.get_area_id(area_idx)
        if not self.save_areas: return self.stof.get_kb_oodi_dd(area_id)
        if area_id in self.areas:
            return self.areas[area_id]
        self.areas[area_id] = self.stof.get_kb_oodi_dd(area_id)
        return self.areas[area_id]

    def get_mp_df(self, area_idx, mp_idx):
        """
        Gets the measurepoint Dataframe by its index
        :param area_idx: index of the area
        :param mp_idx: index of the measure point
        :return: The measure point DataFrame
        :rtype: pandas.DataFrame
        """
        area_df = self.get_area_df(area_idx)
        return area_df[area_df.measurepoint_id == self.get_mp_ids(area_idx)[mp_idx]]

    def get_mp_ids(self, area_idx):
        """
        Get a list of measure point indexes for the given area
        :param area_idx: index of the area
        :return: A list with idexes of measurepoints
        :rtype: list
        """
        return self.get_area_df(area_idx).measurepoint_id.unique()

    def get_area_name(self, area_idx):
        """
        gets the name of an area by its index
        :param area_idx: index of the area
        :return: The name as a string of the area
        :rtype: str
        """
        root = self.roots_df.iloc[area_idx]
        return root['area_name']

    def get_number_of_measurments(self, area_idx, mp_idx):
        """
        Gets the number of measurements in the measure point
        :param area_idx: index of the area
        :param mp_idx: index of the measure point
        :return: number of measurments
        :rtype: int
        """
        return self.get_mp_df(area_idx, mp_idx).shape[0]

    def get_number_of_mps(self, area_idx):
        """
        Gets the number of measure points in the area
        :param area_idx: index of the area
        :return: number of measure points
        :rtype: int
        """
        return self.get_mp_ids(area_idx).shape[0]

    def get_number_of_areas(self):
        """
        Gets the number of areas in the database
        :return: number of areas
        :rtype: int
        """
        return self.roots_df.shape[0]

    def prepare_meas_df(self, meas_df, xval='date_float', yval='mep_uit'):
        """
        Prepares the measure point DataFrame by removing outliers and checking if it has more than 2 points
        :param meas_df: the measurement DataFrame
        :param xval: name of the x value
        :param yval: name of the y value
        :return: the measurement DataFrame of None if it has less than 2 datapoints
        :rtype: pandas.DataFrame, None
        """
        meas_df = meas_df[[xval, yval]]
        meas_df = meas_df.dropna()
        meas_df.columns = ['x', 'y']
        if meas_df.shape[0] <= 2:
            return None
        (m, s) = Stats.mean_std(meas_df['y'])
        meas_df = meas_df[meas_df.y < m + 2 * s]
        meas_df = meas_df[meas_df.y > m - 2 * s]
        if meas_df.shape[0] <= 2:
            return None
        return meas_df
