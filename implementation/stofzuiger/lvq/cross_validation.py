from database.db import DB


class LOOCV:

    def __init__(self,xval='date_float', yval='mep_uit'):
        self.xval = xval
        self.yval = yval
        self.rootNumber = 0
        self.stof = DB()
        self.roots_df = self.stof.get_kb_roots()
        root_id = self.get_root_id(self.rootNumber)
        self.area_df = self.stof.get_kb_oodi_dd(root_id)

    def get_area_name(self,index):
        root = self.roots_df.iloc[index]
        return root['area_name']

    def get_mp_ids(self):
        return self.area_df.measurepoint_id.unique()

    def get_root_id(self,index):
        root = self.roots_df.iloc[index]
        return root['id']

    