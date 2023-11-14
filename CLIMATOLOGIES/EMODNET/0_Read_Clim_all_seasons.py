# eXTRACTION OF 16 climatological values 
# per 1 var
# per a season list 

from commons.layer import Layer
import basins.V2 as basV2
#from basins import V2 as OGS
from static.climatology import get_climatology
from commons.time_interval import TimeInterval
from commons.Timelist import TimeList
import numpy as np
from commons.mask import Mask
from commons.submask import SubMask
import matplotlib.pyplot as pl
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from funzioni_CA import parsing_path
from funzioni_CA import new_directory
import pandas as pd

PresDOWN=np.array([550,650])
OUTDIR= 'FIGURES_and_CSV/'
parsing_path(OUTDIR,'/')  
new_directory(OUTDIR)
LayerList=[ Layer(PresDOWN[k], PresDOWN[k+1])  for k in range(len(PresDOWN)-1)]
SUBLIST = basV2.P.basin_list
CLIMLIST=['Year','winter','spring','summer','autumn']
clim_code=[-1,0,1,2,3]

for CLIM in clim_code:
    CLIMCODE=CLIMLIST[clim_code.index(CLIM)]
    print('.... Extracting Climatology and st_dev for .... ' + CLIMCODE)
    O2o_clim, O2o_std = get_climatology('O2o', SUBLIST, LayerList,basin_expand=True,climseason=CLIM)
    df_clim = pd.DataFrame(index=SUBLIST, columns=LayerList)
    df_std  = pd.DataFrame(index=SUBLIST, columns=LayerList)
    for iii in range(0,len(LayerList)):
       df_clim.iloc[:,iii] = O2o_clim[:,iii]
       df_std.iloc[:,iii] = O2o_std[:,iii]

    LAYERS=str(PresDOWN).replace(' ','_').replace('[','').replace(']','')
    df_clim.to_csv(OUTDIR+'Climatologia_'+str(CLIMCODE)+'_'+LAYERS+'.csv')
    df_std.to_csv(OUTDIR+'ST_deviation_'+str(CLIMCODE)+'_'+LAYERS+'.csv')
