from database.db import DB
from statistics import stats


class model:

    def __init__(self):
        self.stof = DB()
        self.roots_df = self.stof.get_kb_roots()

    def get_area_id(self, area_idx):
        root = self.roots_df.iloc[area_idx]
        return root['id']

    def get_area_df(self,area_idx):
        area_id = self.get_area_id(area_idx)
        return self.stof.get_kb_oodi_dd(area_id)

    def get_mp_df(self,area_idx,mp_idx):
        area_df = self.get_area_df(area_idx)
        return self.area_df[area_df.measurepoint_id == self.get_mp_ids()[mp_idx]]

    def get_mp_ids(self,areaIdx):
        return self.get_area_df(areaIdx).measurepoint_id.unique()

    def get_area_name(self,area_idx):
        root = self.roots_df.iloc[area_idx]
        return root['area_name']

    def get_number_of_mps(self,area_idx):
        return self.get_mp_ids(area_idx).shape[0]

    def get_number_of_areas(self):
        return self.roots_df.shape[0]

    def prepare_meas_df(self,meas_df, xval='date_float', yval='mep_uit'):
        meas_df = meas_df[[xval, yval]]
        meas_df = meas_df.dropna()
        meas_df.columns = ['x', 'y']
        if (meas_df.shape[0] <= 2):
            return None
        (m, s) = stats.mean_std(meas_df['y'])
        meas_df = meas_df[meas_df.y < m + 2 * s]
        meas_df = meas_df[meas_df.y > m - 2 * s]
        if (meas_df.shape[0] <= 2):
            return None
        return meas_df

