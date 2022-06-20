New Zealand 1:50k coastline data from Land Information New Zealand Data Service https://data.linz.govt.nz/

Data is under Creative Commons Attribution 4.0 International license

To plot NZ coaslines from shape file
```
import geopandas
import matplotlib.pyplot as plt

coast_shape_fpath = 'nz-coastlines-and-islands-polygons-topo-150k.shp'
nz = geopandas.read_file(coast_shape_fpath)

fig, ax = plt.subplots(1,1)
fig.set_size_inches(10,10)
fig.set_facecolor('white')

nz.boundary.plot(ax=ax[0],color='k')

plt.show()
```