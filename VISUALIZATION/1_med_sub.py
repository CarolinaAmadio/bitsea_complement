import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.patheffects as PathEffects
import matplotlib.colors as colors
from matplotlib import cm as color_map
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from basins.region import Region, Rectangle
import basins.V2 as basV2
def plot_map_subbasins():
      """ input : none
        output: list_name --> subbasins code and subbabis limits of the area
      """
      list_name=['alb','swm1','swm2','nwm','tyr1','tyr2','adr1','adr2','aeg','ion1','ion2','ion3','lev1','lev2','lev3','lev4']
      matrix_borders=(basV2.alb.borders,basV2.swm1.borders,basV2.swm2.borders,basV2.nwm.borders, basV2.tyr1.borders, basV2.tyr2.borders,  basV2.adr1.borders, basV2.adr2.borders, basV2.aeg.borders, basV2.ion1.borders, basV2.ion2.borders, basV2.ion3.borders ,basV2.lev1.borders, basV2.lev2.borders, basV2.lev3.borders, basV2.lev4.borders)
      return(list_name, matrix_borders)


def cmp_for_maps(n_of_plots , color_map_name = 'jet'):
  """
  return a colormap with  n_of_plots n_colors(input is a list)

  """
  number_of_plots = len(n_of_plots)
  color_map_name = color_map_name
  my_map = color_map.get_cmap(color_map_name)
  colors = my_map(np.linspace(0, 1, number_of_plots, endpoint=True))
  colors = np.flipud(colors)
  cmap = mpl.cm.ScalarMappable( cmap=color_map_name)
  cmap.set_array([])
  return(cmap,colors)

name_basins, basin_borders = plot_map_subbasins()
cmap,colors= cmp_for_maps(name_basins)
colors = colors[::-1]


PLOT_POSITION=False # serve per plottare anche i floats oltre alla mappa i floats hanno un formato csv
NAMEVAR = 'N3n'
fig, ax = plt.subplots(figsize=(16, 8))
df = pd.read_csv('Float_assimilated.csv',index_col=0)
map = Basemap(
     llcrnrlon  =  -10, #  np.round(df.LON.min()-2,0), # Longitude lower right corner
     llcrnrlat  =  30, # np.round(df.LAT.min()-2,0), # Latitude lower right corner
     urcrnrlon  =  40, # np.round(df.LON.max()+2,0), # Longitude upper right corner
     urcrnrlat  =  48, # np.round(df.LAT.max()+2,0), # Latitude upper right corner
     resolution =   'i', # Crude resolution
     projection = 'merc', # Transverse Mercator projection
     #lat_0      =   np.round(lat.mean(),0), # Central latitude
     #lon_0      =   np.round(lon.mean(),0)   # Central longitude
)
map.drawcoastlines()
map.drawmapboundary(fill_color='aliceblue')
map.fillcontinents(color='khaki' ,lake_color='lightcyan')
map.drawparallels(np.arange(20,48,10.), labels=[1,0,0,0] ,dashes=[2,2])
map.drawmeridians(np.arange(0,40,10.), labels=[0,0,0,1],dashes=[2,2])

for III in range(0,len(name_basins)):
    lat_corners= np.array(basin_borders[III])[:,1]
    lon_corners= np.array(basin_borders[III])[:,0]
    poly_corners = np.zeros((len(lat_corners), 2), np.float64)
    poly_corners[:,0] = lon_corners
    poly_corners[:,1] = lat_corners
    x, y = map( poly_corners[:,0], poly_corners[:,1] )
    xy = zip(x,y)
    poly = Polygon( list(xy), facecolor=colors[III])
    plt.gca().add_patch(poly)

map.fillcontinents(color='khaki' ,lake_color='lightcyan')

ax.annotate(text = "Alb",xy  = (map(-3.5,  35.8) ), 'w', fontsize=16)
ax.annotate(text = "Swm1",xy = (map(1.5,   37.5) ), fontsize=16)
ax.annotate(text = "Nwm",xy  = (map(2,     40.5) ), fontsize=16)
ax.annotate(text = "Swm2",xy = (map(5.1,   37.1) ), fontsize=16)
ax.annotate(text = "Tyr1",xy = (map(10,    41.7) ), fontsize=16)
ax.annotate(text = "Tyr2",xy = (map(10.8,  38.3) ), fontsize=16)
ax.annotate(text = "Adr1",xy = (map(14.3,  43)   ), fontsize=16)
ax.annotate(text = "Adr2",xy = (map(18.,   40.5) ), fontsize=16)
ax.annotate(text = "Aeg",xy = (map(25,     37)   ), fontsize=16)
ax.annotate(text = "Ion1",xy = (map(12,    34.5) ), fontsize=16)
ax.annotate(text = "Ion2",xy = (map(18.5,  34.)  ), fontsize=16)
ax.annotate(text = "Ion3",xy = (map(18.5,  38)   ), fontsize=16)
ax.annotate(text = "Lev1",xy = (map(23,    33)   ), fontsize=16)
ax.annotate(text = "Lev2",xy = (map(31,    31.8) ), fontsize=16)
ax.annotate(text = "Lev3",xy = (map(30.,   35)   ), fontsize=16)
ax.annotate(text = "Lev4",xy = (map(33.5,  34.1) ), fontsize=16)

# se hai dei float puoi plottartli
if PLOT_POSITION ==True:
   colLON = NAMEVAR+'_LON'
   colLAT = NAMEVAR+'_LAT'
   lon = np.array(df[colLON].dropna())
   lat = np.array(df[colLAT].dropna())
   x, y = map(lon, lat)  # transform coordinates
   for i in np.arange(0,len(x)):
       plt.scatter(x[i], y[i], marker = 'o', color = 'Grey', edgecolors='k',  s=10, zorder=4)
       plt.gca()
plt.title( 'Flat Positions for '  + NAMEVAR + '(tot profiles='+str(len(lon))+')')
plt.savefig(NAMEVAR+'_Mappa.png')
