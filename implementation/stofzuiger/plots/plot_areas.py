from shapely import wkb
import matplotlib.pyplot as plt
import numpy as np
from database.db import DB

def getRGBfromI(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

def rescale(x,min,max):
    return min + (((x-np.min(x)) * (max - min) ) / float((np.max(x) - np.min(x))))

db = DB()
roots_df = db.get_kb_pipe_segments_roots()
for area in roots_df.area.unique():
    area_pip_roots = roots_df[roots_df.area == area].pip_id.values
    print area
    area_segments_df = db.get_kb_pipe_segments(area_pip_roots)
    max_id = np.max(area_segments_df.root)
    min_id = np.min(area_segments_df.root)
    print max_id,min_id
    n_roots = len(area_segments_df.root.unique())
    for idx, root_id in zip(range(0,n_roots),area_segments_df.root.unique()):
        segment_df = area_segments_df[area_segments_df.root == root_id]
        for idx, row in segment_df.iterrows():
            pipe_geom_string = row['geom']
            if pipe_geom_string is None: continue
            geom = wkb.loads(pipe_geom_string,hex=True)
            x, y = zip(*geom.coords[:])
            plt.plot(x,y,color=tuple(c / 255. for c in getRGBfromI(int(rescale(root_id,min_id,max_id)))),linewidth=2)
    plt.show()
