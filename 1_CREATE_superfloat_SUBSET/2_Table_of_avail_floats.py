from netCDF4 import Dataset
import numpy as np
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
import funzioni_CA
from funzioni_CA import new_directory
from funzioni_CA import parsing_path
import glob
from commons.time_interval import TimeInterval
from commons.Timelist import TimeList
from commons import timerequestors
import basins.OGS as OGS
from instruments import superfloat as bio_float
from instruments import superfloat
from instruments.var_conversions import FLOATVARS
from os import environ
import pandas as pd

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
                                default='OUTPUT_csv',
                                help ='name of dir if you want to sava data csv'
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
from commons.utils import addsep

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

TSS= DATE_start+'_'+DATE_end+'_'

VARLIST = ['Tot','Chla','N3n','O2o']
ITEM    = ['WMO','Nr_profiles'] 

COLUMN_LIST = []
for iii in ITEM:
    for lll in VARLIST:
        col_name = iii +'_' + lll  
        COLUMN_LIST.append(col_name)

df = pd.DataFrame(index= np.arange(0,1), columns=COLUMN_LIST)

for VAR in VARLIST:
    #print(VAR)
    if VAR == 'Tot':
       Profilelist            =  bio_float.FloatSelector(None ,TI_3, OGS.med)
       df['WMO_Tot']          =  len(superfloat.get_wmo_list(Profilelist)) 
       df['Nr_profiles_Tot']  =  len(Profilelist)
    else:
       Profilelist            =  bio_float.FloatSelector( FLOATVARS[VAR] ,TI_3, OGS.med) 
       df['WMO_'+VAR]         =  len(superfloat.get_wmo_list(Profilelist))
       df['Nr_profiles_'+VAR] =  len(Profilelist)

print(df)
import shutil
df.to_csv(OUTDIR + TSS+'Table_of_avail_floats.csv' )
shutil.copy('2_Table_of_avail_floats.py', OUTDIR)
