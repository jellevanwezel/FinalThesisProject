from pyproj import transform, Proj
from shapely import ops, wkb
from functools import partial


class Projections(object):
    code_from = 'epsg:4326'  # world long lat code
    code_to = 'epsg:28991'  # Amersfort projection

    @staticmethod
    def transform(geom):
        """
        Projects the geom object from epsg:4326 to epsg:28991
        :param geom: the geom object
        :return: the transformed geom object
        :rtype: shapely.geom
        """
        p1 = Proj(init=Projections.code_from)
        p2 = Proj(init=Projections.code_to)
        project = partial(transform, p1, p2)
        return ops.transform(project, geom)

    @staticmethod
    def load_and_project(geom_string):
        """
        Loads the object from hex string and projects it
        :param geom_string: the geom hex string
        :return: the transformed geom object
        :rtype: shapely.geom
        """
        geom = wkb.loads(geom_string, hex=True)
        return Projections.transform(geom)
