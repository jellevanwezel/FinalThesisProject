from matplotlib.pyplot import figure, plot, show,scatter
from database.db import db

stof = db()
stof.connect()
df = stof.get_kb_roots()
firstRoot = df.iloc[2]
mdf = stof.get_kb_measurements(firstRoot['id'])
plot(mdf['date'], mdf['value'])
show() # Depending on whether you use IPython or interactive mode, etc.