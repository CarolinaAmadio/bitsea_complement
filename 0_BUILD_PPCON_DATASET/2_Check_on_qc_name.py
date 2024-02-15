import argparse
def argument():
    parser = argparse.ArgumentParser(description = 
    """
    If the QC_VARNAME variable exists, it renames it.

    output: 2 FILE CSV  (INIT - END) 
    to save the metada of the modified files

    Note: The two loops before and after renaming the NetCDF file fill a list when we have e.g. QC_NITRATE
    and not NITRATE_QC (incorrect).
    ==> This implies that if I launch the same script twice, the second time
    I will print 2 empty dataframes because I have already acted and modified the dataset.
    ==> if i llaunch the script once the end repost must be empty
    """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(   '--inputdir','-i',
                                type = str,
                                required = True)
    parser.add_argument(   '--var','-v',
                                type = str,
                                required = True)
    return parser.parse_args()
args = argument()

import glob
from netCDF4 import Dataset
from commons.utils import addsep
import pandas as pd
import sys
import numpy as np

INDIR     = addsep(args.inputdir)
VAR_NAME  = args.var 
NAME=INDIR.split('/')[-2]

print('Dataset corrected name and variable:')
print(NAME + '_' + VAR_NAME)


# 1: Loop per check number of file with QC_VAR (instead VAR_QC)
LIST_NC  = glob.glob(INDIR + '/**/*nc')
LISTA_PPCON=[]
LIST_PRINT_ITERATIONS=np.arange(0,len(LIST_NC ),500 )
nr_iteration=0
for FILE in LIST_NC:
    nc = Dataset(FILE)
    if 'QC_'+VAR_NAME in nc.variables.keys():
       LISTA_PPCON.append(FILE)
    nc.close()   
    nr_iteration+=1
    if  nr_iteration in LIST_PRINT_ITERATIONS: print('iteration nr: ' + str( nr_iteration  ))
df=pd.DataFrame(LISTA_PPCON)
#print( LISTA_PPCON) 
if df.empty:
    sys.exit('no QC_VARIABLE to correct')
else:
    df.columns=['QC_'+VAR_NAME]
    df.to_csv(NAME + '_report_init.csv')


# 2: Loop to rename var 
for FILE in LIST_NC:
    nc=Dataset(FILE ,'r+')
    if 'QC_'+VAR_NAME in nc.variables.keys():
       nc.renameVariable('QC_'+VAR_NAME, VAR_NAME+'_QC')
    nc.close()

# 2: Loop per check number of file with QC_VAR (instead VAR_QC)
LISTA_PPCON=[]
for FILE in LIST_NC:
    nc = Dataset(FILE) 
    if 'QC_'+VAR_NAME in nc.variables.keys():
       LISTA_PPCON.append(FILE)

import pandas as pd
df1=pd.DataFrame(LISTA_PPCON)
if df1.empty:
    print('DataFrame at the end is empty for: \n')
    print( VAR_NAME)
else:
    df1.columns=['QC_'+VAR_NAME]
    df1.to_csv(NAME + '_report_end.csv')
