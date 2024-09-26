import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(   '--inputdir','-i',
                                type = str,
                                required = True,
                                )
    parser.add_argument(   '--varname','-vv',
                                type = str,
                                required = True,
                                )
    return parser.parse_args()

args = argument()
from commons.utils import addsep
import glob
from netCDF4 import Dataset
import pandas as pd
import sys
import numpy as np

INDIR        = addsep(args.inputdir)
VARNAME      = args.varname

print('Input dataset: '  +  INDIR)

value = input("Do you want to overwrite the input dataset?  \n y/n or Y/N:  ")
if value == 'y' or value == 'Y': 
   pass
else:
   sys.exit('Error Not valid choice') 

ICOUNT=0
FLE_LIST=glob.glob(INDIR+'/**/*nc')
LIST_PRINT_ITERATIONS=np.arange(0,len(FLE_LIST),500 )
print(str(len(FLE_LIST )))
nr_iteration=0
for FILE in FLE_LIST:
   nc = Dataset(FILE, 'r+' )
   VARLIST = nc.variables.keys()
   if  nr_iteration in LIST_PRINT_ITERATIONS: print('iteration nr: ' + str( nr_iteration  ))
   nr_iteration+=1
   if VARNAME in VARLIST:
      CHL= nc.variables[VARNAME][:]
      if (CHL < 0).any(axis=0):
         print('neg val corrected') 
         ii=CHL<=0
         CHL[ii] = 0.005
         nc[VARNAME][:] =CHL
         ICOUNT+=1
         nc.close()
