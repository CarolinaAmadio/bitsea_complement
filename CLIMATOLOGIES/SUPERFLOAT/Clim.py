# script that create a file of clim and stdev per vars per a list of layer 
# input: VARLIST/VARNAME , daterange , layerlist , outdir
# save a csv file as:  OUTDIR +'AVG_'   + varmod + '_' + sub.name + '.csv'
# save a csv file as:  OUTDIR +'STD_'   + varmod + '_' + sub.name + '.csv'  

import argparse
def argument():
    parser = argparse.ArgumentParser(description =
    """
    """
    , formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(   '--outdir','-o',
                                type = str,
                                required = True)

    return parser.parse_args()
args = argument()

import numpy as np
import pandas
from commons import timerequestors
from commons import season
from basins import V2 as OGS
import warnings
warnings.filterwarnings('ignore')
from instruments import superfloat
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from commons.layer import Layer
import pandas as pd
from instruments import check
from commons.utils import addsep

OUTDIR     = addsep(args.outdir)

VARLIST  = ['DOXY', 'NITRATE', 'CHLA' , 'BBP700' , 'POC']
SUBS     = OGS.Pred.basin_list[:-1] # no Atlantic

from funzioni_CA import new_directory
new_directory(OUTDIR)

# create a layer list
PresDOWN = np.array([0,25,50,75,100,125,150,200,400,600,800,2000])
LayerList = [ Layer(PresDOWN[k], PresDOWN[k+1])  for k in range(len(PresDOWN)-1) ]
nLayers=len(LayerList)

# create a season list
serv= season.season()
SERV_LIST=serv.SEASON_LIST_NAME
SERV_LIST.append('yearly')

# for all variable in list
for VARNAME in VARLIST:
    if VARNAME ==  'POC':
       VARNAME =   'BBP700'
       varmod  =   'POC'
    else:
       varmod  = VARNAME
    for isub,sub in enumerate(SUBS):
        print(sub)
        df  = pd.DataFrame(index=np.arange(0,nLayers), columns=SERV_LIST  )
        dfst= pd.DataFrame(index=np.arange(0,nLayers), columns=SERV_LIST  )
        for iseas, seas in enumerate (SERV_LIST ):
           print(seas)
           if iseas <=3: #
              req = timerequestors.Clim_season(iseas,serv) #  <--- da 0 a 3 do not use it for yearly clim.
           else:
              req =timerequestors.TimeInterval(starttime='19500101', endtime='21000101',dateformat='%Y%m%d')
           Profilelist=superfloat.FloatSelector(VARNAME , req, sub)
           # loop over profiles
           if len(Profilelist) > 0:
              LIST=[ list() for i in range(nLayers) ]
              # loop over layers in a profile
              for p in Profilelist:
                  if varmod  == VARNAME:
                     Pres,Profile, Qc =  p.read(VARNAME)
                  else:
                     Pres,Profile, Qc =  p.read(VARNAME,varmod)
                  if VARNAME == 'NITRATE':
                     flag3_array = (Profile > 3)  & (Pres <=15)
                     flag3 = flag3_array.sum() > 0
                     if flag3:
                        pass
                     else:
                        PRES, PROFILE, QC = Pres,Profile, Qc
                  else:
                      PRES, PROFILE, QC = Pres,Profile, Qc
                  for ilayer, layer in enumerate(LayerList):
                     ii=(PRES>layer.top) & (PRES<=layer.bottom)
                     LIST[ilayer].append(PROFILE[ii])
                    
              # compute mean and stdev
              LIST_mean=[]
              LIST_std =[]
              for L in LIST:
                  A=np.nanmean(np.hstack(L))
                  LIST_mean.append(A)
                  B=np.std(np.hstack(L))
                  LIST_std.append(B)
                
              df[seas]  = LIST_mean
              dfst[seas]= LIST_std
             
        df.to_csv(OUTDIR +'AVG_'   + varmod + '_' + sub.name + '.csv')
        dfst.to_csv(OUTDIR +'STD_' + varmod + '_' + sub.name + '.csv')
      
import shutil
shutil.copy( 'Clim.py', OUTDIR)
  
