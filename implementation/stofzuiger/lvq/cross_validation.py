from database.db import DB
from database.kb_model import AreaModel


class LOOCV:

    def __init__(self,xval='date_float', yval='mep_uit'):
        self.xval = xval
        self.yval = yval
        self.area_model = AreaModel()


    def