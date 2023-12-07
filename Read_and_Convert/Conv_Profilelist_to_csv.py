#export ONLINE_REPO=/g100_work/OGS_devC/V9C/RUNS_SETUP/PREPROC/DA/
# EX NAME: Time_Series_1plot.py
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

df['time'] =  pd.to_datetime(df['time'], infer_datetime_format=True)
df['date']=df.time.dt.date
df['n_profiles_per_day']=1
df.date =pd.to_datetime(df.date)
df['month'] = df.date.dt.month
df['year'] = df.date.dt.year
df = df.sort_values(by='date',ascending=True)
df.index=np.arange(0,len(df))

#
df[df=='D'].count()
df[df=='A'].count()

# PLOTLINE
import matplotlib.dates as mdates

# BARPOLT staked
df4 =df.groupby(by=['year','month']).sum()
df4.reset_index(inplace=True)
df4['DATE_'] = pd.to_datetime(df4[['year', 'month']].assign(DAY=1))
list_VM = df.groupby(by=['year','month'], as_index=False).agg({'Type':list})
if np.array_equal(list_VM.index.values, df4.index.values):
   df4['type'] = list_VM['Type']
ad =pd.DataFrame(index=np.arange(0,len(df4)), columns=(['A','D']))
from collections import Counter
for iii in range(0,len(df4)):
    tmp = df4.iloc[iii,:]
    ll = dict(Counter(tmp.type))
    if 'A' in ll:
        ad.A[iii] = ll["A"]
    if 'D'in ll:
        ad.D[iii] = ll['D']

if PLT_STACKED:
   fig,ax = plt.subplots(figsize=(14,5))
   ad.index = df4['DATE_'].dt.strftime('%Y-%m')
   ad.plot(kind='bar', ax=ax,stacked=True, color=['dodgerblue','r'],  title='total of assimilation per day')
   x = np.arange(0, len(ad) , 3)
   labels = ad.index[::3]
   plt.xticks(x, labels, rotation='vertical')
   ax.grid((True), linestyle=':', linewidth=0.5, color='k')
   ax.set_title('Monthly-Time serie ARGO '+varmod+'_MODE ( start date: '+DATE_start+' end date: '+ DATE_end +')', fontsize=16,fontweight="bold")
# center text
   ax.set_ylabel('N. Profiles')
   txt= 'Tot n. of profiles: '+np.str(len(Profilelist))
   plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
   plt.subplots_adjust(left=0.1,top=0.93,bottom=0.23 )
   plt.savefig(OUTDIR+TSS+'float_stackedbarplot.png')
   plt.close()

if PLT_BAR:
   fig,ax = plt.subplots(figsize=(14,5))
   tot = ad.sum(axis=1)
   tot.plot(kind='bar', color='dodgerblue')
   x = np.arange(0, len(tot) , 3)
   labels = tot.index[::3]
   plt.xticks(x, labels, rotation='vertical')
   ax.grid((True), linestyle=':', linewidth=0.5, color='k')
   #ax.set_title('Monthly-Time serie ARGO '+varmod+' ( start date: '+DATE_start+' end date: '+ DATE_end +')', fontsize=16,fontweight="bold")
   txt= 'Tot n. of profiles: '+np.str(len(Profilelist))
   plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
   plt.subplots_adjust(left=0.1,top=0.93,bottom=0.23 )
   plt.savefig(OUTDIR+TSS+'float_barplot.png' )
   plt.close()

if PLT_BAR:
   fig,ax = plt.subplots(figsize=(14,5))
   tot = ad.sum(axis=1)
   tot.plot(kind='area', color='silver', alpha=0.8)
   tot.index.name =''
   x = np.arange(0, len(tot) , 3)
   labels = tot.index[::3]
   plt.xticks(x, labels, rotation='vertical')
   ax.grid((True), linestyle=':', linewidth=0.5, color='k')
   ax.tick_params(axis='both', which='major', labelsize=16)
   plt.subplots_adjust(left=0.1,top=0.95,bottom=0.25, right=0.98 )
   plt.savefig(OUTDIR+TSS+'float_areaplot.png')
   plt.close()

import shutil
#shutil.copy('Time_Series_1plot.py', OUTDIR)





