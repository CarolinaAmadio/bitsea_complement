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
from commons.utils import addsep

INDIR        = addsep(args.inputdir)
VARNAME      = args.varname


LIST_FILE=[]
ICOUNT=0
FLE_LIST=glob.glob(INDIR+'/**/*nc')
LIST_PRINT_ITERATIONS=np.arange(0,len(FLE_LIST),500 )
print(str(len(FLE_LIST )))
nr_iteration=0

for FILE in FLE_LIST:
   nc = Dataset(FILE)
   VARLIST = nc.variables.keys()
   if  nr_iteration in LIST_PRINT_ITERATIONS: print('iteration nr: ' + str( nr_iteration  ))
   nr_iteration+=1
   if VARNAME in VARLIST:
      CHL= nc.variables[VARNAME][:]
      if (CHL < 0).any(axis=0):
         LIST_FILE.append(FILE)
         print('first negative value of '+ VARNAME  +' found at iteration: \n')
         print( ICOUNT)
         sys.exit("Negative value of "+ VARNAME +" was found")
         ICOUNT+=1
         nc.close()
print('oooooooooooooooooooooooooooooo')
print('List of the modified files: ')
print(LIST_FILE)
print('oooooooooooooooooooooooooooooo')
