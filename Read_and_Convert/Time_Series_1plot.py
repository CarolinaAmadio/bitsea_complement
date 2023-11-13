#export ONLINE_REPO=/g100_scratch/userexternal/camadio0/Multivariate_Assimilation_2017_2018/ONLINE/

import numpy as np
import pandas as pd
from commons.time_interval import TimeInterval
from commons.Timelist import TimeList
import basins.OGS as OGS
from instruments import superfloat
from instruments import superfloat as bio_float
from instruments.var_conversions import FLOATVARS
from commons.utils import addsep
from datetime import timedelta
from datetime import datetime
from commons import timerequestors
import numpy as np
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
import funzioni_CA

DATE_start  = '20130101'
DATE_end    = '20230401'

#varmod='O2o'
#varmod='N3n'
#varmod     ='P_l'
varmod='POC'
if varmod == 'O2o':
   VARNAME='DOXY'
elif varmod =='P_l':
   VARNAME='CHLA'
elif varmod == 'N3n':
   VARNAME='NITRATE'
elif varmod == 'POC':
   VARNAME='BBP700'

endstr  = '/'
funzioni_CA.parsing_path(OUTDIR ,endstr)
TSS= DATE_start+'_'+DATE_end+'_'+varmod+'_'  # string used in savefig and savecsv
funzioni_CA.new_directory(OUTDIR)

df= pd.DataFrame(index=np.arange(0,len(Profilelist)), columns=['ID','time','lat','lon','name','Type','qc'])
from instruments.var_conversions import FLOATVARS
for iii in range(0,len(Profilelist)):
    df.ID[iii]   = Profilelist[iii].ID()
    df.time[iii] = Profilelist[iii].time
    df.lat[iii]  = Profilelist[iii].lat
    df.lon[iii]  = Profilelist[iii].lon
    df.name[iii] = Profilelist[iii].name()
    TYPE_TMP     = Profilelist[iii]._my_float.origin(VARNAME)
    TYPE_TMP     = TYPE_TMP.status_var
    df.Type[iii] = TYPE_TMP
    p=Profilelist[iii]
    Pres, Profile, Qc = p.read(FLOATVARS[varmod])
    df.qc[iii]        = (np.unique(Qc))

df['time'] =  pd.to_datetime(df['time'], infer_datetime_format=True)
df['date']=df.time.dt.date
df['n_profiles_per_day']=1
df.date =pd.to_datetime(df.date)
df['month'] = df.date.dt.month
df['year'] = df.date.dt.year
df = df.sort_values(by='date',ascending=True)
df.index=np.arange(0,len(df))

if SAVE_CSV:
   df.to_csv(OUTDIR+TSS+'_'+VARNAME+'.csv' )
else:
   print('file data not saved')

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
from matplotlib import cm as color_map
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap

