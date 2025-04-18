"""
This script compares vertical oxygen climatologies from BGC-Argo floats and EMODnet in each Mediterranean sub-basin (excluding Atlantic).
It loads yearly averaged mean and standard deviation NetCDF files, plots vertical profiles for each basin, and saves the figures.
The script also creates necessary directories and copies itself to the output folder for reproducibility.

da risistemare con quello del bitsea
"""

import numpy as np
from bitsea.commons.layer import Layer
from bitsea.basins import V2 as OGS
import netCDF4 as NC

from bitsea.static.climatology import get_climatology
import matplotlib.pylab as plt
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from funzioni_CA import parsing_path
from funzioni_CA import new_directory
from bitsea.commons.mask import Mask

TheMask=Mask.from_file("/g100_work/OGS_devC/camadio/Neccton_hindcast1999_2022/wrkdir/MASKS/meshmask.nc")
z_lev= TheMask.zlevels

PresDOWN = np.array([0,25,50,75,100,125,150,200,400,600,800,1000,1500,2000,2500,3000,4000,5000])
LayerList = [ Layer(PresDOWN[k], PresDOWN[k+1])  for k in range(len(PresDOWN)-1) ]
LayerDepth = [ .5*(ll.bottom+ll.top) for ll in LayerList ]

z_interp=np.arange(0,200,10)
z_interp = np.append(z_interp , np.arange(200, 600, 40))
z_interp = np.append(z_interp , np.arange(600,1001, 50))

LayerFloatDepth = [.5*(z_interp[il]+z_interp[il+1]) for il in range(len(z_interp)-1)]

SUBLIST = []
for sub in OGS.Pred.basin_list:
    if 'atl' in sub.name: continue
    SUBLIST.append(sub)

O2o_emodnet = get_climatology('O2o',SUBLIST, LayerList, basin_expand=True, QC=True)

#OUTDIR= '/g100/home/userexternal/camadio0/float_preproc/CLIMATOLOGIE/FLOAT_CLIMATOLOGIES/new_clim_SF_V8C_2012_2021_swm2/'
INCLIMAfloat = 'CLIMAfloat/'
OUTDIR='/g100/home/userexternal/camadio0/CLIMATOLOGIE/FLOAT_CLIMATOLOGIES/new_clim_FLOAT_V12C_2012_2025/'

parsing_path(OUTDIR,'/')
new_directory(OUTDIR)
parsing_path(OUTDIR+INCLIMAfloat,'/')
new_directory(OUTDIR+ INCLIMAfloat)

# create parsing
fileo2oclima_float = OUTDIR+'yr_Avg_O2o.nc'  ##INCLIMAfloat + 'yr_Avg_O2o.nc'
fileo2ostd_float =   OUTDIR+ 'yr_Std_O2o.nc' # INCLIMAfloat + 'yr_Std_O2o.nc'

O2o_float = list(range(2))
dset = NC.Dataset(fileo2oclima_float)
O2o_float[0] = np.array(dset.variables['O2o'])
dset.close()

dset = NC.Dataset(fileo2ostd_float)
O2o_float[1] = np.array(dset.variables['O2o'])
dset.close()


plt.close('all')

for isub,sub in enumerate(SUBLIST):
    print(sub)
    fig,axs = plt.subplots(2,1,sharex=True,figsize=[7,15])
    for ii in range(2):
        plt.sca(axs[ii])
        plt.plot(O2o_float[0][isub,:],z_lev,'g-',label='Float')
        plt.plot(O2o_float[0][isub,:]+O2o_float[1][isub,:],z_lev,'g:')
        plt.plot(O2o_float[0][isub,:]-O2o_float[1][isub,:],z_lev,'g:')

        plt.plot(O2o_emodnet[0][isub,:],LayerDepth,'ro',label='Insitu')
        plt.plot(O2o_emodnet[0][isub,:]+O2o_emodnet[1][isub,:],LayerDepth,'r-.')
        plt.plot(O2o_emodnet[0][isub,:]-O2o_emodnet[1][isub,:],LayerDepth,'r-.')
        plt.grid()

    plt.sca(axs[0])
    plt.ylim(200,0)
    plt.title(sub.name)
    plt.legend()
    plt.sca(axs[1])
    plt.ylim(2000,200)
    plt.xlabel('mmol O2/m^3')

    plt.savefig(OUTDIR+ INCLIMAfloat +sub.name + 'O2oclima_float_emodnet.png')

#plt.show(block=False)


import shutil 
shutil.copy('compare_clima.py'  , OUTDIR + INCLIMAfloat )

