from netCDF4 import Dataset
import numpy as np
import sys
#sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
import glob
from bitsea.commons.time_interval import TimeInterval
from bitsea.commons.Timelist import TimeList
from bitsea.commons import timerequestors
import bitsea.basins.OGS as OGS
from bitsea.instruments import superfloat as bio_float
from bitsea.instruments import superfloat
from os import environ

import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Executed usually after float download. it creates a subset of the input dataset
    to limit the analysis to a specific time range
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(   '--inputdir','-i',
                                type = str,
                                required = True,
                                help ='/g100_scratch/userexternal/camadio0/PPCON/SUPERFLOAT_PPCon_202312'
                                )
    parser.add_argument(   '--outdir','-o',
                                type = str,
                                required = True,
                                help ='new name of dir e.g. SUPERFLOAT_PPCon_202312_yr2019/ '
                                )
    parser.add_argument(   '--datestart','-s',
                                type = str,
                                required = True,
                                )
    parser.add_argument(   '--dateend','-e',
                                type = str,
                                required = True,
                                )

    return parser.parse_args()

args = argument()
from bitsea.commons.utils import addsep

print ('__________________________________________________________')
print('Program to copy a subset of a dataset for a specific time interval')
print ('__________________________________________________________\n')

if "ONLINE_REPO" in environ:
    pass
else:
    sys.exit('import ONLINE_REPO')

if "PYTHONPATH" in environ:
    pass
else:
    sys.exit('export PYTHONPATH')

# Info to copy dataset
INDIR        = addsep(args.inputdir)
OUTDIR       = addsep(args.outdir)
DATE_start   = args.datestart
DATE_end     = args.dateend

endstr       =  '/'
TI_3         =  timerequestors.TimeInterval(starttime=DATE_start, endtime=DATE_end, dateformat='%Y%m%d')
Profilelist  =  bio_float.FloatSelector(None  ,TI_3, OGS.med)

print ('__________________________________________________________\n')
import os # Check whether the OUTDIR exists if not creates it
isExist = os.path.exists(OUTDIR)
if not isExist:
   os.makedirs(OUTDIR)
   print("The new directory is created!" + OUTDIR)
print ('__________________________________________________________\n')

#
print ('__________________________________________________________')
print ('Program create a dataset with\n' +
        'WMO :    ' + str(len(superfloat.get_wmo_list(Profilelist) )) + 'and\n'   +
        'Profiles nr : '+   str(len(Profilelist))    +
        '\n INPUT DIRECTORY : ' + INDIR + '\n'
        ' SAVED IN :' +  OUTDIR)
print ('__________________________________________________________')


import shutil
def rewriteCYCLE(NR_PROFILE__):
      # se non funziona controlla import
      if NR_PROFILE__ >= 100:
         NR_PROFILE = str(NR_PROFILE__)
      elif 10 <=  NR_PROFILE__  <= 99:
         NR_PROFILE = str(0) + str(NR_PROFILE__)
      else:
         NR_PROFILE = '00' + str(NR_PROFILE__)
      return(NR_PROFILE)

for p in Profilelist:
    WMO           = p.name()
    NR_PROFILE__  = p._my_float.cycle 
    NR_PROFILE    = rewriteCYCLE(NR_PROFILE__)
    FILE          = glob.glob(INDIR + WMO + endstr + '*'+ WMO+ '_'+NR_PROFILE+'.nc')
    if len(FILE) !=1 :
        FILE = [next(f for f in FILE if f.split('/')[-1].startswith('SD'))]
        if len(FILE) !=1 :
            sys.exit('check parsing of netcdf filename')
    print(OUTDIR + WMO + endstr)     
    isExist = os.path.exists(OUTDIR + WMO + endstr)
    if not isExist:
       os.makedirs(OUTDIR + WMO + endstr)
    shutil.copy(FILE[0], OUTDIR + WMO + endstr )

print(OUTDIR + WMO + endstr)
shutil.copy('0_copy_subset_superfloat.py', OUTDIR)

#Float_Index = glob.glob(INDIR  + '*.txt' )
#for III in Float_Index: shutil.copy(III,  OUTDIR )
