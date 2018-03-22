import numpy as np
from pyproj import Proj, transform
from shapely import wkb, ops
import shapely
from functools import partial

from shapely.geometry import LineString

p1 = {'x':6.84165399, 'y': 52.28074897}
p2 = {'x':6.84165026, 'y': 52.28075176}

epsg_a = 'epsg:28991'
epsg_nl = 'epsg:23095'
epsg_w84 = 'epsg:4326'

proj_w84 = Proj(init=epsg_w84)
proj_nl = Proj(init=epsg_nl)
proj_a = Proj(init=epsg_a)

geom_str = '0102000020E610000009000000B2A5D4' \
           '9D13A41A400EF0841FE52F4A40DABF7D' \
           '4C14A41A40D6D4691EE52F4A401B0550' \
           'CA21A41A4056503A8DE32F4A40385AD6' \
           '61E3A41A402344B4D1E22F4A40E366F0' \
           '3001A51A4006E095ACE22F4A40353641' \
           '8CA3A61A40A23AA574E32F4A4038B4F6' \
           'A1F5A61A405B44ECC5E32F4A403DD522' \
           'AF8FA71A40F1CB7509E42F4A40334606' \
           '7602A81A4008629C46E42F4A40'
geom = wkb.loads(geom_str,hex=True)
project = partial(transform,proj_w84,proj_a)
geom2 = ops.transform(project, geom)
print geom2.length

xy_tuple_list = []
for point in geom.coords:
    xy_tuple = transform(proj_w84, proj_a,*point)
    xy_tuple_list.append(xy_tuple)

pipe_t  = LineString(xy_tuple_list)

print np.round(pipe_t.length,2)


xy_tuple_list = []
for point in geom.coords:
    xy_tuple = transform(proj_w84, proj_nl, *point)
    xy_tuple_list.append(xy_tuple)

pipe_t  = LineString(xy_tuple_list)

print pipe_t.length


p1_x_nl, p1_y_nl =  transform(proj_w84, proj_nl,p1['x'],p1['y'])
p2_x_nl, p2_y_nl =  transform(proj_w84, proj_nl,p2['x'],p2['y'])
p1_x_a, p1_y_a =  transform(proj_w84, proj_a, p1['x'], p1['y'])
p2_x_a, p2_y_a =  transform(proj_w84, proj_a, p2['x'], p2['y'])

print 'length nl:', np.abs(p1_x_nl - p2_x_nl) + np.abs(p1_y_nl - p2_y_nl)
print 'length am:', np.abs(p1_x_a - p2_x_a) + np.abs(p1_y_a - p2_y_a)
print 'length w84:', np.abs(p1['x'] - p2['x']) + np.abs(p1['y'] - p2['y'])




