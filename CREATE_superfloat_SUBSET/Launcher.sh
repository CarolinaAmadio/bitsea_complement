#!/bin/bash
#SBATCH --job-name=copy_ppcon
#SBATCH -N1
#SBATCH --ntasks-per-node=16
#SBATCH --time=00:20:00
#SBATCH --mem=300gb
#SBATCH --account=OGS23_PRACE_IT
#SBATCH --partition=g100_usr_prod


module load autoload
module load intelmpi/oneapi-2021--binary
module load intelmpi/oneapi-2021--binary netcdf/4.7.4--oneapi--2021.2.0-ifort ncview
LIBDIR=/g100_work/OGS23_PRACE_IT/COPERNICUS/V10C/HOST/g100
export    HDF5_DIR=$LIBDIR
export NETCDF4_DIR=$LIBDIR
export    GEOS_DIR=$LIBDIR
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$LIBDIR

cd $SLURM_SUBMIT_DIR

. ../profile.inc

source /g100_work/OGS23_PRACE_IT/COPERNICUS/py_env_3.9.18_new/bin/activate
export ONLINE_REPO=/g100/home/userexternal/camadio0/CLIMATOLOGIE/FLOAT_CLIMATOLOGIES/new_clim_FLOAT_V12C_2012_2025/
export PYTHONPATH=$PYTHONPATH:/g100/home/userexternal/camadio0/CLIMATOLOGIE/FLOAT_CLIMATOLOGIES/new_clim_FLOAT_V12C_2012_2025/bit.sea/src/

# Input arguments to be passed n the script
DATE_start='20120101'
DATE_end='20240101'
INDIR='/g100/home/userexternal/camadio0/CLIMATOLOGIE/FLOAT_CLIMATOLOGIES/new_clim_FLOAT_V12C_2012_2025/SUPERFLOAT'

OUTDIR=/g100/home/userexternal/camadio0/CLIMATOLOGIE/FLOAT_CLIMATOLOGIES/new_clim_FLOAT_V12C_2012_2025/bitsea_complement/CREATE_superfloat_SUBSET/SUPERFLOAT_2012_2024/
mkdir -p $OUTDIR

#  make a copy of the dataset es V9C_GB into my scratch for the date range datastart to dataend
#my_prex "python 0_copy_subset_superfloat.py -i $INDIR -o $OUTDIR -s $DATE_start -e $DATE_end"


# create float index
cp 1_dump_index.py $OUTDIR
cd $OUTDIR
my_prex "python 1_dump_index.py -i $OUTDIR -o $OUTDIR/Float_Index.txt -t superfloat"

exit 0
python 2_Table_of_avail_floats.py -i $INDIR -o $OUTDIR -s $DATE_start -e $DATE_end

exit 0

# gurado quanti float ci sono per vars e creo una tabella 
# as in https://docs.google.com/presentation/d/1BAUIWEUpthU3b0uCtYCbQ3qSrr2ZHpPxVWET94d8cpY/edit#slide=id.gffe6e32a58_0_0
python 2_Table_of_avail_floats.py


# in 'SUPERFLOAT_CANYON' in scratch ci sono due dataset:
# 1. SUPERFLOAT_CANYON_20220721_SMOOTHED_bl
# 2. SUPERFLOAT_CANYON_20220721_SMOOTH_CALIBR
# I floats con var NITRATE E NITRATE_QC = -9999 vengono copiati nel dataset di output
# e.g. INPUTDIR  = BASEDIR + 'SUPERFLOAT_CANYON/SUPERFLOAT_CANYON_20220721_SMOOTHED_bl/'
#      OUTDIR    = BASEDIR + 'SUPERFLOAT_2017_2019_V9C/'

# e.g. INPUTDIR  = BASEDIR + 'SUPERFLOAT_CANYON/SUPERFLOAT_CANYON_20220721_SMOOTH_CALIBR/'
#      OUTDIR    = BASEDIR + 'SUPERFLOAT_2017_2019_V9C_QUALCOSA/' 

# prima faccio il check se sono vere le condizioni sopra
python 3_dump_pseudo_obs.py

# RICREO IL  float index
python 1_dump_index.py -i $OUTDIR -o ${OUTDIR}/Float_Index.txt -t superfloat

# vedo se ho fatto bene il copia incolla della pseudovar in var con qc -9999
python 4_check_pseudo_dump.py

export ONLINE_REPO='/g100_scratch/userexternal/camadio0/SUPERFLOAT_2017_2019_V9C/'
python 2_Table_of_avail_floats.py

# rinomino il Dataset di output
mv /g100_scratch/userexternal/camadio0/SUPERFLOAT_2017_2019_V9C/ /g100_scratch/userexternal/camadio0/SUPERFLOAT_2017_2019_V9C_SMOOTHED_bl/
