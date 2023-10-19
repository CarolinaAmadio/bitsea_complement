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
