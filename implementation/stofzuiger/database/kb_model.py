from database.db import DB
from statistics import stats


class AreaModel(object):

    def __init__(self,save_areas=True):
        self.save_areas = save_areas
        self.stof = DB()
        self.roots_df = self.stof.get_kb_roots()
        self.areas = dict()

    def get_area_id(self, area_idx):
        root = self.roots_df.iloc[area_idx]
        return root['id']

    def get_area_df(self,area_idx):
        area_id = self.get_area_id(area_idx)
        if not self.save_areas: return self.stof.get_kb_oodi_dd(area_id)
        if area_id in self.areas:
            return self.areas[area_id]
        self.areas[area_id] = self.stof.get_kb_oodi_dd(area_id)
        return self.areas[area_id]

    def get_mp_df(self,area_idx,mp_idx):
        area_df = self.get_area_df(area_idx)
        return area_df[area_df.measurepoint_id == self.get_mp_ids(area_idx)[mp_idx]]

    def get_mp_ids(self,areaIdx):
        return self.get_area_df(areaIdx).measurepoint_id.unique()

    def get_area_name(self,area_idx):
        root = self.roots_df.iloc[area_idx]
        return root['area_name']

    def get_number_of_measurments(self,area_idx,mp_idx):
        return self.get_mp_df(area_idx,mp_idx).shape[0]

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


# model = AreaModel(save_areas=True)
# for area_idx in range(0,model.get_number_of_areas()):
#    if area_idx != 0: print
#    print model.get_area_name(area_idx) + " has " + str(model.get_number_of_mps(area_idx)) + " mps"
#    for mp_idx in range(0,model.get_number_of_mps(area_idx)):
#        print "mp " + str(mp_idx) + " has " + str(model.get_number_of_measurments(area_idx,mp_idx)) + " measurements"

