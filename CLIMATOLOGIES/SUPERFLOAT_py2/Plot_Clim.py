# script to create plot or subplot of climatology


import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from funzioni_CA import parsing_path
from funzioni_CA import new_directory
from commons.utils import addsep
from basins import V2 as OGS
from commons import season
from commons.layer import Layer
import glob
from funzioni_CA import new_directory
from utils import UNITS
import matplotlib.pylab as plt

OUTDIR     = addsep(args.outdir)
new_directory(OUTDIR + '/'  )

STAT='AVG'
STAT2='STD'
N_PLOTS=2
INDIR1 = 'CSV_V9C'
INDIR2 = 'CSV_PPCON'
   
#  create a layer list
PresDOWN = np.array([0,25,50,75,100,125,150,200,400,600,800,2000])
z=[]
i=0
for III in PresDOWN[:-1]:
    z.append( (III + PresDOWN[i+1])/2.)
    i+=1

z=np.array(z)
VARLIST  = ['DOXY', 'NITRATE', 'CHLA' , 'BBP700','POC' ]

SUBS     = OGS.Pred.basin_list[0:-1]
NCOL=5

for isub in SUBS:
   isub= isub.name
   for VARNAME in VARLIST:
       df  = pd.read_csv(INDIR1 + '/' +STAT + '_'+ VARNAME   + '_' + isub  + '.csv',index_col=0)
       st  = pd.read_csv(INDIR1 + '/' +STAT2 + '_'+ VARNAME  + '_' + isub  + '.csv',index_col=0)
       df.index , st.index  = z,z
       
       if N_PLOTS ==2:
          df1 = pd.read_csv(INDIR2 + '/' +STAT + '_'+ VARNAME   + '_' + isub  + '.csv',index_col=0)
          st1 = pd.read_csv(INDIR2 + '/' +STAT2 + '_'+ VARNAME  + '_' + isub  + '.csv',index_col=0)
          df1.index, st1.index = z,z
          fig,ax = plt.subplots(2,  NCOL,  sharey=True, sharex=True, figsize=[13,6])
       elif N_PLOTS <2:
           fig,ax = plt.subplots(NCOL,  sharey=True, sharex=True, figsize=[13,6])
       else:
           sys.exit('No yet implemented per more than 2 datasets')
         
       for kkk, ax in enumerate(ax.flatten()):
           if kkk <= NCOL -1:
              ax.plot      (df.iloc[:,kkk],z*-1, 'r',label='V9C')
              ax.errorbar  (df.iloc[:,kkk],z*-1, xerr =st.iloc[:,kkk] ,color='r', fmt='o', linewidth=1, capsize=1)
              ax.set_title (df.iloc[:,kkk].name , fontsize=12,fontweight="bold")
           else:
              ax.plot      (df1.iloc[:,kkk-NCOL],z*-1, 'dodgerblue',label='PPCON')
              ax.errorbar  (df1.iloc[:,kkk-NCOL],z*-1, xerr =st1.iloc[:,kkk-NCOL] ,color= 'dodgerblue', fmt='o', linewidth=1, capsize=1)
              ax.set_title (df1.iloc[:,kkk-NCOL].name , fontsize=12,fontweight="bold")
           ax.grid((True), linestyle=':', linewidth=0.5, color='k')
           if VARNAME =='DOXY':
              ax.set_xlim([170,250])
           if  VARNAME =='NITRATE':
              ax.set_xlim([0,8])
           if VARNAME =='CHLA':
               ax.set_ylim(-180 , 0)
               ax.set_xlim(0,0.8)
           #elif  VARNAME == 'BBP700':
           #   ax.set_xlim([0,0.002])
           if VARNAME == 'POC':
               ax.set_ylim(-310, 0)
               ax.set_xlim( 0, 60)

       lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
       lines_labels = lines_labels[4:6]
       lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
       fig.legend(lines, labels, loc='center right' , fontsize=14)
       del (lines_labels)
       fig.text(0.5, 0.04, VARNAME +' ' + UNITS(VARNAME) , ha='center')
       fig.text(0.04, 0.5, 'Depth (m)', va='center', rotation='vertical')
       fig.suptitle('Climatological Profile of '+ VARNAME + ' in ' +  isub , fontsize=14, color='k', style='italic')
       plt.subplots_adjust(left=0.1,hspace=0.25, wspace=0.3 ,bottom=0.15,  right=0.90)
       plt.savefig(OUTDIR+ 'Clim_' +VARNAME + '_' + isub + '.png' )
       plt.close()
     
