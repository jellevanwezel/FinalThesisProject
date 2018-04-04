from database.area_model import AreaModel
from database.db import DB

db = DB()
model = AreaModel()

roots_df = db.get_kb_pipe_segments_roots()
area_pip_roots = roots_df[roots_df.area == 'Almelo Tusveld'].pip_id.values
area_segments_df = db.get_kb_pipe_segments(area_pip_roots)

print roots_df[roots_df['area'] == 'Denekamp 2']

print area_segments_df