from shapely import wkb
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from database.db import DB
from feature_extraction.projections import Project


def rescale(x,min,max):
    return min + (((x-np.min(x)) * (max - min) ) / float((np.max(x) - np.min(x))))

db = DB()
roots_df = db.get_kb_pipe_segments_roots()
proj = Project()
for area in roots_df.area.unique():
    area_pip_roots = roots_df[roots_df.area == area].pip_id.values
    print area
    area_segments_df = db.get_kb_pipe_segments(area_pip_roots)
    colors = cm.rainbow(np.linspace(0, 1, len(area_segments_df.root.unique())))
    n_roots = len(area_segments_df.root.unique())
    for segment_idx, root_id in zip(range(0,n_roots),area_segments_df.root.unique()):
        segment_df = area_segments_df[area_segments_df.root == root_id]
        for idx, row in segment_df.iterrows():
            pipe_geom_string = row['geom']
            if pipe_geom_string is None: continue
            geom = proj.load_and_project(pipe_geom_string)
            x, y = zip(*geom.coords[:])
            plt.plot(x,y,c=colors[segment_idx],linewidth=2)
    plt.xticks([])
    plt.yticks([])
    plt.title(area)
    plt.show()
