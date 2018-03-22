from pyproj import transform, Proj
from shapely import ops, wkb
from functools import partial

class Project(object):

    code_from = 'epsg:4326'  # world long lat code
    code_to = 'epsg:28991'  # Amersfort projection

    def transform(self,geom):
        p1 = Proj(init=Project.code_from)
        p2 = Proj(init=Project.code_to)
        project = partial(transform, p1,p2)
        return ops.transform(project, geom)

    def load_and_project(self,geom_string):
        geom = wkb.loads(geom_string,hex=True)
        return self.transform(geom)