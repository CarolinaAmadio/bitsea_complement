# to run after Conv_Profilelist_to_csv.py in Read_and_Convert directory
import pandas as pd
from commons.mask import Mask
import numpy as np
import sys
from matchup_CA import NEAREST_AT_CA_IDX_LATLON
from netCDF4 import Dataset
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
import funzioni_CA
from utils import rewriteCYCLE as FC
import glob
from utils import UNITS
import warnings
warnings.filterwarnings('ignore')

maskfile     =  '/g100_work/OGS_devC/Benchmark/SETUP/PREPROC/MASK/meshmask.nc'
SAT_INP      =  '/gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/ONLINE_V9C/SAT/CHL/DT/DAILY/CHECKED_24/'
INDIR        =  '/g100_scratch/userexternal/camadio0/PPCON/SUPERFLOAT/'
DEPTH        = 5 #layer 0-5m
VARNAME='CHLA'
satvar='CHL'

UNIT = UNITS(VARNAME)

# load metadata file about floats
df           = pd.read_csv('20190101_20191231_P_l__'+ VARNAME +'.csv', index_col=0)
df_metadata  = df[df.Type!='Reconstructed']
df_metadata.index= np.arange(0,len(df_metadata))
WMO_LIST     = list(df_metadata.WMO.drop_duplicates())

# using mask for matchup
TheMask = Mask(maskfile)
nav_lat = TheMask.ylevels[:,0]
nav_lon = TheMask.xlevels[0,:]

# matchup
lon_serv, lat_serv , ilonp, ilatp =    NEAREST_AT_CA_IDX_LATLON(df_metadata, nav_lat,nav_lon, 'lon','lat')

# fill datadrame with lat lon idx of matchup
df_metadata['MODEL_LAT']          = lat_serv
df_metadata['MODEL_LAT_idx']      = ilatp
df_metadata['MODEL_LON']          = lon_serv
df_metadata['MODEL_LON_idx']      = ilonp

# fill dataframe with SAT value at surface
df_metadata['SAT_DATA'] = np.nan
for III in range(0,len(df_metadata)):

   tmp  = df_metadata.iloc[III,:]
   date = tmp.time[0:10].replace('-','')
   FILE = glob.glob(SAT_INP + date+'*nc')
   if len(FILE) >1:
      sys.exit('errore')

   nc = Dataset(FILE[0])
   var= nc.variables[satvar ][0,tmp.MODEL_LAT_idx,tmp.MODEL_LON_idx]
   df_metadata['SAT_DATA'].iloc[III] = var

# fill dataframe with insitu at rurface
# fill dataframe with Reconstrcuters at surface
df_metadata['REC_DATA'] = np.nan
df_metadata['INSITU_DATA'] = np.nan
for III in range(0,len(df_metadata)):
    tmp  = df_metadata.iloc[III,:]
    FILE1= glob.glob( INDIR + str(tmp.WMO) + '/*' + FC(tmp.CYCLE)+ '.nc' )
    if len(FILE1) >1:
       sys.exit('errore')
    nc1     = Dataset(FILE1[0])
    VARLIST = nc1.variables.keys()
    varfl   , zfl  = nc1.variables[VARNAME][:] , nc1.variables['PRES_'+VARNAME][:]
    varfl   = np.nanmean(varfl[zfl<=DEPTH])
    df_metadata['INSITU_DATA'].iloc[III] = varfl

    if 'CHLA_PPCON' in VARLIST:
        varrec , zrec= nc1.variables['CHLA_PPCON'][:] , nc1.variables['PRES_CHLA_PPCON'][:]
        varrec = np.nanmean(varrec[zrec<=DEPTH])
        df_metadata['REC_DATA'].iloc[III] = varrec

    else:
        if 'DOXY' in VARLIST:
            df_metadata['REC_DATA'].iloc[III] = -9999
        else:
            df_metadata['REC_DATA'].iloc[III] = int(9999)

df1 = df_metadata[df_metadata.REC_DATA !=-9999]
df1 = df1[df1.REC_DATA < 9999]
df1 = (df1.dropna(subset=['SAT_DATA']))
df2 = df1[['WMO','Basin','SAT_DATA','REC_DATA', 'INSITU_DATA' ]]
df2.index=np.arange(0,df2.shape[0])

df2['INSITU_bias']           = df2['INSITU_DATA'].sub(df2['SAT_DATA'], axis = 0)
df2['reconstructed_bias'] = df2['REC_DATA'].sub(df2['SAT_DATA'], axis = 0)

ncol= [ 'INSITU_bias'  ,'reconstructed_bias']
df3 = pd.DataFrame(index=np.arange(0 , len(df2.WMO.drop_duplicates() ) ) , columns= ncol)

for iii ,  WMO in enumerate (df2.WMO.drop_duplicates()):
    SERV=df2[df2.WMO==WMO]
    df3.INSITU_bias.iloc[iii]        = SERV.mean().INSITU_bias
    df3.reconstructed_bias.iloc[iii] = SERV.mean().reconstructed_bias

df3.index=df2.WMO.drop_duplicates()

import matplotlib.pyplot as plt
fig,ax = plt.subplots(figsize=(14,5))
df3.plot(kind='bar', ax=ax,stacked=False, color=['red','dodgerblue','deepskyblue', 'silver'],  title='bias (data-SATELLITE) CHLA')
plt.axhline(y=0., color='k', linestyle='-')

plt.xticks( rotation='vertical', fontsize=16)
plt.yticks( fontsize=16)
ax.grid((True), linestyle=':', linewidth=0.5, color='k')
plt.subplots_adjust(left=0.1,top=0.93,bottom=0.23 )
plt.savefig('Floats_sat_Bias.png')
from commons_ import col_to_dt

font = {'family': 'serif',
        'color':  'k',
        'alpha':  0.7,
        'weight': 'normal',
        'size': 16,
        }


fontx=  {
        'rotation': 'vertical',
        'family'  : 'serif',
        'color'   :  'k',
        'alpha'   :  0.7,
        'weight'  : 'normal',
        'size'    : 16,
         }

#   time series per floats
for WMO in df1.WMO:
    SERV=df1[df1.WMO==WMO]
    SERV =col_to_dt(SERV,'date')
    SERV.index=SERV.date
    SERV = SERV[['SAT_DATA','REC_DATA', 'INSITU_DATA' ]]
    fig,ax = plt.subplots(figsize=(14,5))
    SERV.plot(kind='line', ax=ax, color=['darkgray', 'dodgerblue','red' ,'deepskyblue', 'silver'])

    plt.title( str(WMO) + ' timeseries CHLA 2019' , rotation='horizontal', fontdict=font   )
    plt.xticks( ** fontx)
    plt.yticks( **font)

    plt.xlabel('Date', rotation='horizontal' ,  fontdict=font)
    plt.ylabel( VARNAME + ' ' + UNIT, fontdict=font)
    ax.grid((True), linestyle=':', linewidth=0.5, color='k')
    plt.subplots_adjust(left=0.1,top=0.90,bottom=0.27 )
    plt.savefig( str(WMO) +'_' + VARNAME  + '_float_sat_rec.png')
    plt.close()

  
