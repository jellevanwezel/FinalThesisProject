from shapely import wkb
import matplotlib.pyplot as plt
from database.db import DB

db = DB()
roots_df = db.get_kb_pipe_segments_roots()
for area in roots_df.area.unique():
    area_pip_roots = roots_df[roots_df.area == area].pip_id.values
    print area
    area_segments_df = db.get_kb_pipe_segments(area_pip_roots)
    n_roots = len(area_segments_df.root.unique())
    for idx, root_id in zip(range(0,n_roots),area_segments_df.root.unique()):
        segment_df = area_segments_df[area_segments_df.root == root_id]
        for idx, row in segment_df.iterrows():
            pipe_geom_string = row['geom']
            if pipe_geom_string is None: continue
            geom = wkb.loads(pipe_geom_string,hex=True)
            x, y = zip(*geom.coords[:])
            plt.plot(x,y)
        plt.show()