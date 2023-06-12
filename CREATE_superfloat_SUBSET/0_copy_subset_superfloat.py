from netCDF4 import Dataset
import numpy as np
#import sys
#sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
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
from os import environ

print('programma per copiare un dataset in scratch per un intervallo di tempo specifico fare export del dataset desiderato')
# export PYTHONPATH='/g100/home/userexternal/camadio0/bit.sea_py3/'

DATE_start   =  '20170101'
DATE_end     =  '20190101'
endstr       =  '/'
INDIR        = '/g100_work/OGS_devC/V9C/RUNS_SETUP/PREPROC/DA/SUPERFLOAT/'
OUTDIR       = '/g100_scratch/userexternal/camadio0/VALIDAZIONE_RUN_CMEMS_scripts/VALIDAZIONE_FLOAT/SUPERFLOAT_VALIDATION_O2/'

if "ONLINE_REPO" in environ:
    pass
else:
    sys.exit('import ONLINE_REPO')
if "PYTHONPATH" in environ:
    pass
else:
    sys.exit('export PYTHONPATH')

# Info to copy dataset
TI_3         =  timerequestors.TimeInterval(starttime=DATE_start, endtime=DATE_end, dateformat='%Y%m%d')
Profilelist  =  bio_float.FloatSelector('DOXY'  ,TI_3, OGS.med)

#parsing_path(INDIR, endstr)
#parsing_path(OUTDIR, endstr)
#new_directory(OUTDIR)

import shutil
from utils import rewriteCYCLE

for p in Profilelist:
    WMO           = p.name()
    NR_PROFILE__  = p.profile_nr()
    NR_PROFILE    = rewriteCYCLE(NR_PROFILE__)
    FILE          = glob.glob(INDIR + WMO + endstr + '*'+ WMO+ '_'+NR_PROFILE+'.nc')
    if len(FILE) !=1 :
        sys.exit('check parsing of netcdf filename')
    print(OUTDIR + WMO + endstr)
    new_directory(OUTDIR + WMO + endstr)
    shutil.copy(FILE[0], OUTDIR + WMO + endstr )
    
shutil.copy('0_Subset_superfloat.py', OUTDIR)
