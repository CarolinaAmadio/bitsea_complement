from basins.region import Region, Rectangle
import basins.V2 as basV2
import pandas as pd
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
#from basins_CA import ARGO_cross_Med_basins
import numpy as np
from basins_CA import plot_map_subbasins
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.patches as mpatches
import matplotlib.patheffects as PathEffects
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.colors as colors
from matplotlib import cm as color_map
import matplotlib as mpl
from funzioni_CA import parsing_path
from funzioni_CA import new_directory
from funzioni_CA import plot_Medsea2
from utils import cmp_for_maps

INPUTDIR = 'FIGURES_and_CSV/'
NAMEFILE = 'EMODNET_climatology.csv'
endstr='/'
parsing_path(INPUTDIR,endstr)
new_directory(INPUTDIR)
SIZE=20 # font of number in map

# importo climatologie
df_clim = pd.read_csv(INPUTDIR + NAMEFILE  , index_col=0)
#df_clim =  df_clim.iloc[0:-2,:]
print('........')
print('manually removed med and atl in Climatologie file emodnet')
print('........')
#chiamo funzione pee subasin med
name_basins, basin_borders = plot_map_subbasins()
df_clim.index=name_basins

# create map
cmap,colors= cmp_for_maps(name_basins)
colors =colors[::-1]

fig, ax = plt.subplots(figsize=(15,10))
map = Basemap(
     llcrnrlon  =  -6, #  np.round(df.LON.min()-2,0), # Longitude lower right corner
     llcrnrlat  =  30, # np.round(df.LAT.min()-2,0), # Latitude lower right corner
     urcrnrlon  =  40, # np.round(df.LON.max()+2,0), # Longitude upper right corner
     urcrnrlat  =  46, # np.round(df.LAT.max()+2,0), # Latitude upper right corner
     resolution =   'i', # Crude resolution
     projection = 'cyl', # Transverse Mercator projection
     )

map.drawcoastlines()
map.drawmapboundary(fill_color='lightcyan')
map.fillcontinents(color='white' ,lake_color='lightcyan')
map.drawparallels(np.arange(20,48,10.), labels=[1,0,0,0] ,dashes=[2,2], fontsize=20)
map.drawmeridians(np.arange(0,40,10.), labels=[0,0,0,1],dashes=[2,2], fontsize=20)

for III in range(0,len(name_basins)):
    print(III)
    print(name_basins[III])
    lat_corners= np.array(basin_borders[III])[:,1]
    lon_corners= np.array(basin_borders[III])[:,0]
    poly_corners = np.zeros((len(lat_corners), 2), np.float64)
    poly_corners[:,0] = lon_corners
    poly_corners[:,1] = lat_corners
    patches = []
    patches.append(Polygon(poly_corners))
    ax.add_collection(PatchCollection(patches, facecolor=colors[III] , edgecolor='k', linewidths=0.5))

    if np.isnan(np.round(df_clim.iloc[III,0]) ):
       VALSTR = str(np.round(df_clim.iloc[III,0]))
    else:
       VALSTR =str(int(np.round(df_clim.iloc[III,0])))
    if III ==0:
      plt.annotate( VALSTR , xy=(lon_corners.mean(), lat_corners.mean()+0.5 ) , color='w', size=SIZE, weight='bold' )
    elif III in [1]:
      plt.annotate( VALSTR , xy=(lon_corners.mean()+0., lat_corners.mean()+2.8 ) , color='w', size=SIZE, weight='bold' )
    elif III in [2]:
      plt.annotate( VALSTR , xy=(lon_corners.mean()-0.6, lat_corners.mean()+2.8 ) , color='w', size=SIZE, weight='bold' )
    elif III in [3]:
      plt.annotate( VALSTR , xy=(lon_corners.mean()+1, lat_corners.mean()-1 ) , color='w', size=SIZE, weight='bold' )
    elif III in [4]:
      plt.annotate( VALSTR , xy=(lon_corners.mean()-1, lat_corners.mean()-1.5 ) , color='w', size=SIZE, weight='bold' )
    elif III in [5]:
      plt.annotate( VALSTR , xy=(lon_corners.mean()-2, lat_corners.mean()+0.5 ) , color='k', size=SIZE, weight='bold' )
    elif III in [6]:
      plt.annotate( VALSTR , xy=(14. , lat_corners.mean()-2 ) , color='k', size=SIZE, weight='bold' )
    elif III in [7,13]:
      plt.annotate( VALSTR , xy=( lon_corners.mean()+0.1, lat_corners.mean()  )  , color='k', size=SIZE, weight='bold'  )
    elif III in [8]:
      plt.annotate( VALSTR , xy=( lon_corners.mean()-0.8, lat_corners.mean()+1 ) , color='k', size=SIZE, weight='bold') # , bbox={'facecolor': 'w', 'alpha': 0.8, 'pad': 3}  )
    elif III in [9]:
      plt.annotate( VALSTR , xy=( lon_corners.mean()+.5, lat_corners.mean()+1 ) , color='k', size=SIZE, weight='bold')#
    elif III in [10]:
      plt.annotate( VALSTR , xy=( lon_corners.mean()-0.7, lat_corners.mean()+2 ) , color='k', size=SIZE, weight='bold') #,bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 10}  )
    elif III in [11]:
      plt.annotate( VALSTR , xy=( lon_corners.mean()+0.1, lat_corners.mean() ) , color='k', size=SIZE, weight='bold' )
    else:
      plt.annotate( VALSTR , xy=( lon_corners.mean()-0.8, lat_corners.mean()+1 ) , color='k', size=SIZE, weight='bold')

# bbox={'facecolor': 'g', 'alpha': 0.5, 'pad': 10} )
#plt.subplots_adjust(left=0.1,top = 0.98,bottom=0.05,  right=0.99)
#plt.title('EMODnet Climatology 600m O2o (EMODNET) ', fontsize=20)
#plt.savefig(INPUTDIR+'/emodnet_Climatologie_600'+'m.png')
